import pandas as pd

def load_data():
    # Load the dataset
    patients = pd.read_csv('patients.csv')
    return patients
