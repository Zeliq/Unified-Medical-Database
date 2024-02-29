import flask
from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
import os  # For environment variables
from dotenv import load_dotenv

load_dotenv()
print("Connecting to database:", os.environ.get('DB_NAME'))
db = mysql.connector.connect(
    host=os.environ.get('DB_HOST', '127.0.0.1'),  
    user=os.environ.get('DB_USER', 'root@localhost'),
    password=os.environ.get('DB_PASSWORD', 'zeliq2003'),
    database=os.environ.get('DB_NAME', 'DBMS_MINI_PROJECT')
)

app = flask.Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) 



# Patient Endpoints
# @app.route('/patients', methods=['GET'])
# def get_patients():
#     try:
#         cursor = db.cursor()
#         cursor.execute("SELECT * FROM patient")
#         patients = cursor.fetchall()
#         return jsonify(patients) 
#     except mysql.connector.Error as err:
#         return jsonify({'error': str(err)}), 500 

# @app.route('/patients', methods=['GET'])
# def get_patients():
#     try:
#         cursor = db.cursor()
#         cursor.execute("SELECT * FROM patient")
#         patients = cursor.fetchall()

#         # Pass data to the template
#         return render_template('patients.html', patients=patients)  
#     except mysql.connector.Error as err:
#         return jsonify({'error': str(err)}), 500 


# ... Existing endpoints ...

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'CORS test successful!'})


@app.route('/patient/<patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    try:
        cursor = db.cursor()

        # Fetch patient data
        cursor.execute("SELECT * FROM Patient WHERE Pid = %s", (patient_id,))
        patient = cursor.fetchone()

        if not patient:
            return jsonify({'message': 'Patient not found'}), 404

        # Convert patient tuple to dictionary
        patient_dict = dict(zip(cursor.column_names, patient))

        # Fetch associated medical records
        cursor.execute("""
            SELECT * FROM MedicalRecord
            WHERE Med_Id = %s
        """, (patient_id,))
        medical_records = cursor.fetchall()

        # Combine the data 
        result = {
            **patient_dict,  
            'medical_records': medical_records 
        }

        return jsonify(result) 

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

@app.route('/doctors')
def doctors():
    return render_template('doctors.html')

@app.route('/patient', methods=['POST'])
def add_patient():
    # (Add data validation here)
    try:
        data = request.get_json()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO patient (Pid, Pname, Pnum, Paddress, Dr_id) 
            VALUES (%s, %s, %s, %s, %s)""", 
            (data['Pid'], data['Pname'], data['Pnum'], data['Paddress'], data['dr_id'])
        )
        db.commit()
        return jsonify({'patient_id': cursor.lastrowid}), 201  
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 

# Doctor Endpoints
@app.route('/doctors', methods=['GET'])
def get_doctors():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM doctor")
        doctors = cursor.fetchall()
        return jsonify(doctors)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/doctor/<doctor_id>', methods=['GET'])
def get_doctor_by_id(doctor_id):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM doctor WHERE doctor_id = %s", (doctor_id,))
        doctor = cursor.fetchone()
        if doctor:
            return jsonify(doctor)
        else:
            return jsonify({'message': 'Doctor not found'}), 404  
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 

@app.route('/doctor', methods=['POST'])
def add_doctor():
    # (Add data validation here)
    try:
        data = request.get_json()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO doctor (first_name, last_name, hospital_id, specialty) 
            VALUES (%s, %s, %s, %s)""", 
            (data['first_name'], data['last_name'], data['hospital_id'], data['specialty'])
        )
        db.commit()
        return jsonify({'doctor_id': cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 

# ... (Add similar endpoints for hospitals and relatives)

# ... (Previous code for patient and doctor endpoints)

# Hospital Endpoints
@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM hospital")
        hospitals = cursor.fetchall()
        return jsonify(hospitals)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/hospital/<hospital_id>', methods=['GET'])
def get_hospital_by_id(hospital_id):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM hospital WHERE hospital_id = %s", (hospital_id,))
        hospital = cursor.fetchone()
        if hospital:
            return jsonify(hospital)
        else:
            return jsonify({'message': 'Hospital not found'}), 404  
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 

@app.route('/hospital', methods=['POST'])
def add_hospital():
    # (Add data validation here)
    try:
        data = request.get_json()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO hospital (hospital_name, location) 
            VALUES (%s, %s)""", 
            (data['hospital_name'], data['location'])
        )
        db.commit()
        return jsonify({'hospital_id': cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 

# Relative Endpoints
@app.route('/relatives', methods=['GET'])
def get_relatives():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM relative")
        relatives = cursor.fetchall()
        return jsonify(relatives)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

@app.route('/relative/<relative_id>', methods=['GET'])
def get_relative_by_id(relative_id):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM relative WHERE relative_id = %s", (relative_id,))
        relative = cursor.fetchone()
        if relative:
            return jsonify(relative)
        else:
            return jsonify({'message': 'Relative not found'}), 404  
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 

@app.route('/relative', methods=['POST'])
def add_relative():
    # (Add data validation here)
    try:
        data = request.get_json()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO relative (patient_id, first_name, last_name, relationship, contact_info) 
            VALUES (%s, %s, %s, %s, %s)""", 
            (data['patient_id'], data['first_name'], data['last_name'], data['relationship'], data['contact_info'])
        )
        db.commit()
        return jsonify({'relative_id': cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500 

# ... (Rest of the code) 
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
    

if __name__ == '__main__':
    app.run(debug=True) 
