let searchInput;
document.addEventListener('DOMContentLoaded', () => {
    // Fetch patients
    fetch('/patients')
        .then(response => response.json())
        .then(patients => {
            const patientsList = document.querySelector('table.patients tbody');
            if (patientsList) {
                patientsList.innerHTML = ''; // Clear existing rows

                patients.forEach(patient => {
                    const row = document.createElement('tr');

                    const idCell = document.createElement('td');
                    idCell.textContent = patient.Pid;
                    row.appendChild(idCell);

                    const nameCell = document.createElement('td');
                    nameCell.textContent = patient.Pname;
                    row.appendChild(nameCell);

                    const phCell = document.createElement('td');
                    phCell.textContent = patient.Pnum;
                    row.appendChild(phCell);

                    const addressCell = document.createElement('td');
                    addressCell.textContent = patient.Paddress;
                    row.appendChild(addressCell);

                    const drIdCell = document.createElement('td');
                    drIdCell.textContent = patient.Dr_id;
                    row.appendChild(drIdCell);

                    patientsList.appendChild(row);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching patients:', error);
            // ... (Display an error message)
        });

    // Fetch doctors
        fetch('/doctors')
        .then(response => response.json())
        .then(doctors => {
            const doctorsList = document.querySelector('table.doctors tbody');
            if (doctorsList) {
                doctorsList.innerHTML = ''; // Clear existing rows

                doctors.forEach(doctor => {
                    const row = document.createElement('tr');

                    const idCell = document.createElement('td');
                    idCell.textContent = doctor.Did;
                    row.appendChild(idCell);

                    const nameCell = document.createElement('td');
                    nameCell.textContent = doctor.Dname;
                    row.appendChild(nameCell);

                    // Phone Number 
                    const phoneCell = document.createElement('td'); 
                    phoneCell.textContent = doctor.Dnum; 
                    row.appendChild(phoneCell);

                    // Specialization 
                    const specializationCell = document.createElement('td'); 
                    specializationCell.textContent = doctor.DType; 
                    row.appendChild(specializationCell);

                    const hospIdCell = document.createElement('td');
                    hospIdCell.textContent = doctor.Hos_id;
                    row.appendChild(hospIdCell);

                    doctorsList.appendChild(row);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching doctors:', error);
            // ... (Display an error message)
        });

    // Fetch hospitals
    fetch('/hospitals')
        .then(response => response.json())
        .then(hospitals => {
            const hospitalsList = document.querySelector('table.hospitals tbody');
            if (hospitalsList) {
                hospitalsList.innerHTML = ''; // Clear existing rows

                hospitals.forEach(hospital => {
                    const row = document.createElement('tr');

                    const idCell = document.createElement('td');
                    idCell.textContent = hospital.Hid;
                    row.appendChild(idCell);

                    const nameCell = document.createElement('td');
                    nameCell.textContent = hospital.Hname;
                    row.appendChild(nameCell);

                    const phoneCell = document.createElement('td');
                    phoneCell.textContent = hospital.Hnum;
                    row.appendChild(phoneCell);

                    const addressCell = document.createElement('td');
                    addressCell.textContent = hospital.Haddress;
                    row.appendChild(addressCell);

                    hospitalsList.appendChild(row);
                });
            }
        })
        .catch(error => {
            console.error('Error fetching hospitals:', error);
            // ... (Display an error message)
        });

        window.searchPatient = () => {
            searchInput = document.getElementById('searchInput');
            const patientId = searchInput.value.trim();
    
            if (patientId === '') {
                // Display an error message or handle empty search
                return;
            }
    
            // Fetch patient details based on the entered patient ID
            fetch(`/search_patient/${patientId}`)
                .then(response => response.json())
                .then(patientDetails => {
                    // Handle the response (update the UI, display patient details, etc.)
                    console.log(patientDetails);
                })
                .catch(error => {
                    console.error('Error searching patient:', error);
                    // Handle the error (display an error message, etc.)
                });
        };

}); 
