from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Initialize the data structure
columns = ['Patient Name', 'Diseases', 'Days Stayed', 'Doctor Name']
patients_df = pd.DataFrame(columns=columns)

def add_patient(patients_df, name, diseases, days_stayed, doctor):
    new_patient = pd.DataFrame([{
        'Patient Name': name,
        'Diseases': diseases,
        'Days Stayed': days_stayed,
        'Doctor Name': doctor
    }])
    patients_df = pd.concat([patients_df, new_patient], ignore_index=True)
    return patients_df

def calculate_bill(diseases, days_stayed):
    total_sum = sum(diseases.values()) * days_stayed
    return total_sum

def generate_bill(patients_df, patient_name):
    patient = patients_df[patients_df['Patient Name'] == patient_name].iloc[0]
    total_sum = calculate_bill(patient['Diseases'], patient['Days Stayed'])

    bill = f"""
    ----------- Hospital Bill -----------
    Patient Name: {patient['Patient Name']}
    Doctor: {patient['Doctor Name']}
    Days Stayed: {patient['Days Stayed']}
    Diseases:
    """
    for disease, price in patient['Diseases'].items():
        bill += f"    - {disease}: {price}\n"
    bill += f"Total Price: {total_sum}\n"
    bill += "-------------------------------------"

    return bill

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_patient', methods=['POST'])
def add_patient_route():
    global patients_df
    name = request.form['name']
    diseases = {}
    disease_names = request.form.getlist('disease_name')
    disease_prices = request.form.getlist('disease_price')
    for disease, price in zip(disease_names, disease_prices):
        diseases[disease] = float(price)
    days_stayed = int(request.form['days_stayed'])
    doctor = request.form['doctor']
    
    patients_df = add_patient(patients_df, name, diseases, days_stayed, doctor)
    return redirect(url_for('index'))

@app.route('/generate_bill', methods=['POST'])
def generate_bill_route():
    patient_name = request.form['patient_name']
    bill = generate_bill(patients_df, patient_name)
    return render_template('bill.html', bill=bill)

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))

    