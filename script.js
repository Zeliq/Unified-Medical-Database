// Fetch Patient Data (Initial Display)
fetch('/patients')
    .then(response => response.json())
    .then(patients => {
        const patientsList = document.getElementById('patients-list');
        patients.forEach(patient => {
            const patientDiv = document.createElement('div');
            patientDiv.innerHTML = `
                <h3>${patient.first_name} ${patient.last_name}</h3> 
                <p>ID: ${patient.patient_id}</p>
                <p>Contact: ${patient.contact_info}</p> 
            `;
            patientsList.appendChild(patientDiv);
        });
    })
    .catch(error => console.error('Error fetching patients:', error));

// Search Functionality
const searchForm = document.getElementById('search-form');
const patientDetails = document.getElementById('patient-details');

searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const patientId = document.getElementById('patient-id').value;

    fetch(`/patient/${patientId}`)
        .then(response => response.json())
        .then(patient => {
            patientDetails.innerHTML = ''; // Clear previous data

            if (patient.message) {
                patientDetails.textContent = patient.message; 
            } else {
                patientDetails.innerHTML = `
                    <h3>${patient.first_name} ${patient.last_name}</h3> 
                    <p>ID: ${patient.patient_id}</p>
                    <p>Contact: ${patient.contact_info}</p> 

                    <h4>Medical Records:</h4>
                    <ul>
                        ${patient.medical_records.map(record => `
                            <li>Date: ${record.date} - Notes: ${record.notes}</li> 
                        `).join('')} 
                    </ul>
                `;
            }
        })
        .catch(error => console.error('Error fetching patient:', error));

        // ... (Your fetch code)

patients.forEach(patient => {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${patient.Pid}</td>
        <td>${patient.Pname}</td>
        <td>${patient.Paddress}</td>
        <td>${patient.Pnum}</td>
    `;
    patientsList.appendChild(row); 
});

});
