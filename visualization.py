import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def plot_admissions_over_time(patients):
    # Sample plot with Matplotlib
    plt.figure(figsize=(10, 6))
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
    patients['Year'] = patients['BIRTHDATE'].dt.year
    yearly_counts = patients.groupby('Year').size()
    plt.plot(yearly_counts.index, yearly_counts.values, marker='o')
    plt.title('Number of Births Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Births')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_interactive_admissions(patients):
    # Sample plot with Plotly
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
    patients['Year'] = patients['BIRTHDATE'].dt.year
    yearly_counts = patients.groupby('Year').size().reset_index(name='Count')
    fig = px.line(yearly_counts, x='Year', y='Count', title='Number of Births Over Time')
    fig.show()

# Example usage
if __name__ == "__main__":
    from data_preparation import load_data
    patients = load_data()
    plot_admissions_over_time(patients)
    plot_interactive_admissions(patients)
