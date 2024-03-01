from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

# Establish database connection
db = mysql.connector.connect(
    host=os.environ.get('DB_HOST', '127.0.0.1'),
    user=os.environ.get('DB_USER', 'root@localhost'),
    password=os.environ.get('DB_PASSWORD', 'zeliq2003'),
    database=os.environ.get('DB_NAME', 'DBMS_MINI_PROJECT')
)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


# Patient Endpoints

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'CORS test successful!'})


@app.route('/patient/<patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    try:
        with db.cursor(dictionary=True) as cursor:
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
        app.logger.error('An error occurred: %s', err)
        return jsonify({'error': str(err)}), 500


# @app.route('/patients', methods=['GET'])
# def get_patients():
#     try:
#         with db.cursor(dictionary=True) as cursor:
#             cursor.execute("SELECT * FROM patient")
#             patients = cursor.fetchall()
#             return jsonify(patients)
#     except mysql.connector.Error as err:
#         app.logger.error('An error occurred: %s', err)
#         return jsonify({'error': str(err)}), 500


@app.route('/')
def index():
    try:
        return render_template('index.html')
    except mysql.connector.Error as err:
        app.logger.error('An error occurred: %s', err)
        return jsonify({'error': str(err)}), 500

# @app.route('/patients')
# def patients():
#     return render_template('patients.html')



@app.route('/patients')
def patients():
    try:
        cursor = db.cursor(dictionary=True)  # Use dictionary cursor for easy access
        cursor.execute("SELECT * FROM patient")
        patients = cursor.fetchall()
        return render_template('patients.html', patients=patients)
    except mysql.connector.Error as err:
        app.logger.error('An error occurred: %s', err)
        return jsonify({'error': str(err)}), 500


# @app.route('/doctors')
# def doctors():
#     return render_template('doctors.html')

@app.route('/doctors')
def doctors():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Doctor")  # Make sure the table name is correct (Doctor instead of doctor)
        doctors = cursor.fetchall()
        return render_template('doctors.html', doctors=doctors)
    except mysql.connector.Error as err:
        app.logger.error('An error occurred: %s', err)
        return jsonify({'error': str(err)}), 500



@app.route('/hospitals')
def hospitals():
  try:
      cursor = db.cursor(dictionary=True)
      cursor.execute("SELECT * from Hospital")
      hospitals = cursor.fetchall()
      return render_template('hospitals.html', hospitals=hospitals)
  except mysql.connector.Error as err:
      app.logger.error('An error occurred: %s', err)
      return jsonify({'error': str(err)}), 500

# @app.route('/search_patient/<patient_id>')
# def search_patient(patient_id):
#     try:
#         with db.cursor(dictionary=True) as cursor:
#             # Fetch medical records
#             cursor.execute("""
#                 SELECT * FROM MedicalRecord
#                 WHERE Med_Id = %s
#             """, (patient_id,))
#             medical_records = cursor.fetchall()

#             # Fetch doctor details (assuming one doctor per patient)
#             if medical_records:
#                 Med_id = medical_records[0]['Mid']  # Get Mid from the first record
#                 cursor.execute("""
#                     SELECT Did FROM MakesRecord
#                     WHERE Mid = %s
#                 """, (Med_id,))
#                 doctor = cursor.fetchone()
#             else:
#                 doctor = None  

#             if doctor:
#                 # Corrected the query to fetch doctor details based on the doctor ID
#                 cursor.execute("""
#                     SELECT * FROM Doctor
#                     WHERE Did = %s   
#                 """, (doctor['Did'],))
#                 doc = cursor.fetchone()
#             else:
#                 doc = None

#             # Fetch patient details
#             cursor.execute("""
#                 SELECT * FROM Patient
#                 WHERE Pid = %s
#             """, (patient_id,))
#             patient = cursor.fetchone()

#             # Fetch relatives
#             cursor.execute("""
#                 SELECT r.* FROM Relatives r
#                 JOIN PatientRelative pr ON r.Rid = pr.Rid
#                 WHERE pr.Pid = %s
#             """, (patient_id,))
#             relatives = cursor.fetchall()

#             # Combine the results
#             result = {
#                 "patient": patient,
#                 "medical_records": medical_records,
#                 "doctor": doc,
#                 "relatives": relatives
#             }

#             return jsonify(result)

#     except mysql.connector.Error as err:
#         app.logger.error('An error occurred: %s', err)
#         return jsonify({'error': str(err)}), 500
    
@app.route('/search_patient/<int:patient_id>')
def search_patient(patient_id):
    try:
        with db.cursor(dictionary=True) as cursor:
            # Fetch patient details, medical records, doctor details, and relatives in a single query
            cursor.execute("""
                SELECT p.*, m.*, d.*, r.*
                FROM Patient p
                LEFT JOIN MedicalRecord m ON p.Pid = m.Med_Id
                LEFT JOIN MakesRecord mr ON m.Mid = mr.Mid
                LEFT JOIN Doctor d ON mr.Did = d.Did
                LEFT JOIN PatientRelative pr ON p.Pid = pr.Pid
                LEFT JOIN Relatives r ON pr.Rid = r.Rid
                WHERE p.Pid = %s
            """, (patient_id,))

            # Fetch all the rows
            rows = cursor.fetchall()

            if not rows:
                return jsonify({'message': 'Patient not found'}), 404

            # Group the results by their types
            result = {
                "patient": rows[0],  # Assuming patient details are unique
            }

            return jsonify(result)

    except mysql.connector.Error as err:
        app.logger.error('An error occurred: %s', err)
        return jsonify({'error': str(err)}), 500




# ...

# @app.route('/search_patient/<patient_id>')
# def search_patient(patient_id):
#     try:
#         with db.cursor(dictionary=True) as cursor:
#             # Fetch patient details, medical records, doctor details, and relatives in a single query
#             cursor.execute("""
#                 SELECT DISTINCT
#                     p.*, 
#                     m.*,
#                     d.*,
#                     r.*
#                 FROM Patient p
#                 JOIN MedicalRecord m ON p.Pid = m.Med_Id
#                 JOIN MakesRecord mr ON m.Mid = mr.Mid
#                 JOIN Doctor d ON mr.Did = d.Did
#                 JOIN PatientRelative pr ON p.Pid = pr.Pid
#                 JOIN Relatives r ON pr.Rid = r.Rid
#                 WHERE p.Pid = %s
#             """, (patient_id,))

#             # Fetch all the rows
#             rows = cursor.fetchall()

#             if not rows:
#                 return jsonify({'message': 'Patient not found'}), 404

#             # Group the results by their types
#             result = {
#                 "patient": rows[0],  # Assuming patient details are unique
#             }

#             # Render the patient details using the patient_details.html template
#             return render_template('patient_details.html', patient_details=result)

#     except mysql.connector.Error as err:
#         app.logger.error('An error occurred: %s', err)
#         return jsonify({'error': str(err)}), 500



# @app.route('/patient', methods=['POST'])
# def add_patient():
#     # (Add data validation here)
#     try:
#         data = request.get_json()
#         with db.cursor() as cursor:
#             cursor.execute("""
#                 INSERT INTO patient (Pid, Pname, Pnum, Paddress, Dr_id)
#                 VALUES (%s, %s, %s, %s, %s)""",
#                            (data['Pid'], data['Pname'], data['Pnum'], data['Paddress'], data['dr_id'])
#                            )
#             db.commit()
#             return jsonify({'patient_id': cursor.lastrowid}), 201

#     except mysql.connector.Error as err:
#         app.logger.error('An error occurred: %s', err)
#         return jsonify({'error': str(err)}), 500


@app.route('/patient', methods=['POST'])
def add_patient():
    data = request.form  # Access form data
    # (Add data validation here)
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO patient (Pid, Pname, Pnum, Paddress, Dr_id) 
                VALUES (%s, %s, %s, %s, %s)""",  
                (data['Pid'], data['Pname'], data['Pnum'], data['Paddress'], data['Dr_id']) 
            )
        db.commit()
        return jsonify({'patient_id': cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        app.logger.error('An error occurred: %s', err)
        return jsonify({'error': str(err)}), 500

# Add this route to render AddPatients.html
@app.route('/add-patient')
def add_patient_page():
    return render_template('AddPatient.html')

@app.route('/success')
def successful():
    return render_template('success.html')

@app.route('/doctor', methods=['POST'])
def add_doctor():
    data = request.form

    try:
        with db.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Doctor (Did, Dname, Dnum, DType, Hos_id)
                VALUES (%s, %s, %s, %s, %s)""",
                (data['Did'], data['Dname'], data['Dnum'], data['DType'], data['Hos_id'])
            )
            db.commit()
            # Redirect to a different page after adding the doctor
            return redirect(url_for('successful'))
    except mysql.connector.Error as err:
        app.logger.error('An error occurred: %s', err)
        return jsonify({'error': str(err)}), 500

@app.route('/add-doctor')
def add_doctor_page():
    return render_template('AddDoctor.html')
# ... (Other endpoints)

# ... (Rest of the code)


@app.route('/delete-doctor', methods=['POST'])
def delete_doctor():
    doctor_id = request.form.get('Did')  # Assuming you're passing the doctor_id via form data

    try:
        with db.cursor() as cursor:
            # Execute the DELETE query
            cursor.execute("DELETE FROM Doctor WHERE Did = %s", (doctor_id,))
            db.commit()
            
            # Check if any rows were affected
            if cursor.rowcount > 0:
                return redirect(url_for('successful')), 200
            else:
                return jsonify({'message': 'Doctor not found'}), 404
    except mysql.connector.Error as err:
        app.logger.error('An error occurred: %s', err)
        return jsonify({'error': str(err)}), 500

@app.route('/del-doc')
def del_doc():
    return render_template('Del_Doc.html')

if __name__ == '__main__':
    app.run(debug=True)
