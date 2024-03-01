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




        // app.js

        
    document.getElementById('add-patient-form').addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(event.target); // Collect form data

    fetch('/patient', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Could not add patient');
        }
        return response.json(); 
    })
    .then(data => {
        // Successfully added patient
        console.log('Patient added:', data);
        // Optionally clear the form or update the displayed patients list 
    })
    .catch(error => {
        console.error('Error adding patient:', error);
        // Display an error message to the user
    });

    document.getElementById('add-doctor-form').addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission
        
        const formData = new FormData(event.target); // Collect form data
        
        try {
            const response = await fetch('/doctor', {
                method: 'POST',
                body: formData
            });
    
            if (!response.ok) {
                throw new Error('Could not add doctor');
            }
    
            const data = await response.json(); 
            console.log('Doctor added:', data);
            // Optionally clear the form or update the displayed doctors list 
        } catch (error) {
            console.error('Error adding doctor:', error);
            // Display an error message to the user
        }
    });

});

document.getElementById('del_doc').addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData(event.target); // Collect form data

    fetch('/delete-doctor', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Could not add patient');
        }
        return response.json(); 
    })
    .then(data => {
        // Successfully added patient
        console.log('Patient added:', data);
        // Optionally clear the form or update the displayed patients list 
    })
    .catch(error => {
        console.error('Error adding patient:', error);
        // Display an error message to the user
    });

}); 
});


function searchPatient() {
    const patientId = document.getElementById('searchInput').value;

    fetch(`/search_patient/${patientId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch patient data');
            }
            return response.json();
        })
        .then(data => {
            const resultsContainer = document.createElement('div');
            resultsContainer.id = 'search-results';  // Add an ID for easy access

            if (data.message) {
                resultsContainer.innerHTML = `<p class="error">Error: ${data.message}</p>`;
            } else {
                resultsContainer.innerHTML = renderPatientDetails(data);
            }

            // Insert the results into the page
            const existingResults = document.getElementById('search-results');
            if (existingResults) {
                existingResults.replaceWith(resultsContainer);
            } else {
                document.body.appendChild(resultsContainer);
            }
        })
        .catch(error => {
            console.error('Error searching patient:', error);
            // Display a generic error message on the frontend
            const errorContainer = document.createElement('div');
            errorContainer.className = 'error-container';
            errorContainer.textContent = 'An error occurred while searching for the patient. Please try again later.';
            document.body.appendChild(errorContainer);
        });
}


// function renderPatientDetails(data) {
//     let html = '<h2>Search Results</h2>'; 

//     // Patient Details
//     html += `
//         <h3>Patient Details</h3>
//         <table>
//             <tr><th>ID</th><td>${data.patient.Pid}</td></tr>
//             <tr><th>Name</th><td>${data.patient.Pname}</td></tr>
//             <tr><th>Phone</th><td>${data.patient.Pnum}</td></tr>
//             <tr><th>Address</th><td>${data.patient.Paddress}</td></tr>
//         </table>
//     `;

//     // Medical Records
//     if (data.medical_records && data.medical_records.length > 0) {
//         html += `
//             <h3>Medical Records</h3>
//             <table>
//                 <tr>
//                     <th>ID</th>
//                     <th>Mode</th>
//                     <th>Allergies</th>
//                     <th>Condition</th>
//                     <th>History</th> 
//                 </tr>
//                 ${data.medical_records.map(record => `
//                     <tr>
//                         <td>${record.Mid}</td>
//                         <td>${record.MODE}</td>
//                         <td>${record.Mallergies}</td>
//                         <td>${record.Mcondition}</td>
//                         <td>${record.Mhistory}</td>
//                     </tr>
//                 `).join('')}
//             </table>
//         `;
//     } else {
//         html += '<p>No medical records found.</p>';
//     }

//     // Doctor
//     if (data.doctor) {
//         html += `
//             <h3>Doctor Details</h3>
//             <table>
//                 <tr>
//                     <th>ID</th>
//                     <th>Name</th>
//                     <th>Phone Number</th>
//                     <th>Specialization</th>
//                 </tr>
//                 <tr>
//                     <td>${data.doctor.Did}</td>
//                     <td>${data.doctor.Dname}</td>
//                     <td>${data.doctor.Dnum}</td>
//                     <td>${data.doctor.DType}</td>
//                 </tr>
//             </table>
//         `;
//     }

//     // Relatives
//     if (data.relatives && data.relatives.length > 0) {
//         html += `
//             <h3>Relatives</h3>
//             <table>
//                 <tr>
//                     <th>ID</th>
//                     <th>Name</th>
//                     <th>Phone Number</th>
//                     <th>Relation</th>
//                 </tr>
//                 ${data.relatives.map(relative => `
//                     <tr>
//                         <td>${relative.Rid}</td>
//                         <td>${relative.Rname}</td>
//                         <td>${relative.Rnum}</td>
//                         <td>${relative.RRelation}</td>
//                     </tr>
//                 `).join('')}
//             </table>
//         `;
//     } else {
//         html += '<p>No relatives found.</p>';
//     }

//     return html;
// }

function renderPatientDetails(data) {
    console.log('Data:', data); // Log the contents of the data object to the console

    let html = '<h2>Search Results</h2>';

    // Patient Details
    if (data.patient) {
        html += `
            <h3>Patient Details</h3>
            <table>
                <tr><th>ID</th><td>${data.patient.Pid}</td></tr>
                <tr><th>Name</th><td>${data.patient.Pname}</td></tr>
                <tr><th>Phone</th><td>${data.patient.Pnum}</td></tr>
                <tr><th>Address</th><td>${data.patient.PAddress}</td></tr>
            </table>

            <h3>Doctor Details</h3>
            <table>
                <tr><th>ID</th><td>${data.patient.Did}</td></tr>
                <tr><th>Name</th><td>${data.patient.Dname}</td></tr>
                <tr><th>Phone</th><td>${data.patient.Dnum}</td></tr>
            </table>

            <h3>Relatives Details</h3>
            <table>
                <tr><th>Name</th><td>${data.patient.Rname}</td></tr>
                <tr><th>Relation</th><td>${data.patient.RRelation}</td></tr>
                <tr><th>Phone</th><td>${data.patient.Rnum}</td></tr>
            </table>

            <h3>Medical Record</h3>
            <table>
                <tr><th>Medical ID</th><td>${data.patient.Mid}</td></tr>
                <tr><th>Medical History</th><td>${data.patient.Mhistory}</td></tr>
                <tr><th>Allergies</th><td>${data.patient.Mallergies}</td></tr>
                <tr><th>Medical Condition</th><td>${data.patient.Mcondition}</td></tr>
                <tr><th>Mode Of Consultation</th><td>${data.patient.MODE}</td></tr>
                <tr><th>Date Of Consultation</th><td>${data.patient.DoC}</td></tr>
            </table>
        `;
    }

    // Medical Records
    if (data.medical_records && data.medical_records.length > 0) {
        html += `
            <h3>Medical Records</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Mode</th>
                    <th>Allergies</th>
                    <th>Condition</th>
                    <th>History</th> 
                </tr>
                ${data.medical_records.map(record => `
                    <tr>
                        <td>${record.Mid}</td>
                        <td>${record.MODE}</td>
                        <td>${record.Mallergies}</td>
                        <td>${record.Mcondition}</td>
                        <td>${record.Mhistory}</td>
                    </tr>
                `).join('')}
            </table>
        `;
    } else {
        console.log('No medical records found.'); // Log if no medical records are found
    }

    // Doctor Details
    if (data.doctor) {
        html += `
            <h3>Doctor Details</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Phone Number</th>
                    <th>Specialization</th>
                </tr>
                <tr>
                    <td>${data.doctor.Did}</td>
                    <td>${data.doctor.Dname}</td>
                    <td>${data.doctor.Dnum}</td>
                    <td>${data.doctor.DType}</td>
                </tr>
            </table>
        `;
    } else {
        console.log('No doctor found.'); // Log if no doctor is found
    }

    // Relatives
    if (data.relatives && data.relatives.length > 0) {
        html += `
            <h3>Relatives</h3>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Phone Number</th>
                    <th>Relation</th>
                </tr>
                ${data.relatives.map(relative => `
                    <tr>
                        <td>${relative.Rid}</td>
                        <td>${relative.Rname}</td>
                        <td>${relative.Rnum}</td>
                        <td>${relative.RRelation}</td>
                    </tr>
                `).join('')}
            </table>
        `;
    } else {
        console.log('No relatives found.'); // Log if no relatives are found
    }

    return html;
}
