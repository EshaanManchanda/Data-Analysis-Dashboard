from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from data_preparation import load_data

app = Dash(__name__)

# Load data
patients = load_data()

# Process data
patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
patients['Year'] = patients['BIRTHDATE'].dt.year
patients['Age'] = (pd.to_datetime('today') - patients['BIRTHDATE']).dt.days / 365.25

# Group data for visualizations
yearly_counts = patients.groupby('Year').size().reset_index(name='Count')
gender_counts = patients['GENDER'].value_counts().reset_index(name='Count')
ethnicity_counts = patients['ETHNICITY'].value_counts().reset_index(name='Count')

# Create initial figures
birth_fig = px.line(yearly_counts, x='Year', y='Count', title='Number of Births Over Time')
gender_fig = px.pie(gender_counts, names='GENDER', values='Count', title='Gender Distribution')
ethnicity_fig = px.bar(ethnicity_counts, x='ETHNICITY', y='Count', title='Ethnicity Distribution')
age_fig = px.histogram(patients, x='Age', nbins=20, title='Age Distribution of Patients')

# Calculate metrics
average_age = patients['Age'].mean()
gender_distribution = patients['GENDER'].value_counts().to_dict()
ethnicity_distribution = patients['ETHNICITY'].value_counts().to_dict()
# Placeholder for average stay duration
average_stay_duration = 0  # Replace with actual calculation when data is available

app.layout = html.Div(style={'padding': '20px'}, children=[
    html.H1("Data Analysis Dashboard", style={'textAlign': 'center'}),
    html.H1("Hospital's Patient Overview", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select Year:", style={'font-weight': 'bold'}),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in sorted(patients['Year'].unique())],
            value=sorted(patients['Year'].unique())[-1],  # default to the latest year
            clearable=False
        ),
    ], style={'width': '50%', 'margin': 'auto', 'padding-bottom': '20px'}),
    
    html.Div([
        dcc.Graph(
            id='births-graph',
            figure=birth_fig
        ),
        dcc.Graph(
            id='gender-graph',
            figure=gender_fig
        ),
        dcc.Graph(
            id='ethnicity-graph',
            figure=ethnicity_fig
        ),
        dcc.Graph(
            id='age-graph',
            figure=age_fig
        ),
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-around'}),
    
    html.Div([
        html.H2(f'Average Age of Patients: {average_age:.2f} years'),
        html.H2(f'Average Stay Duration: {average_stay_duration} days'),  # Placeholder
        html.H2(f'Gender Distribution: {gender_distribution}'),
        html.H2(f'Ethnicity Distribution: {ethnicity_distribution}')
    ], style={'textAlign': 'center', 'padding-top': '20px'})
])

@app.callback(
    Output('births-graph', 'figure'),
    Input('year-dropdown', 'value')
)
def update_births_graph(selected_year):
    filtered_data = patients[patients['Year'] <= selected_year]
    yearly_counts = filtered_data.groupby('Year').size().reset_index(name='Count')
    fig = px.line(yearly_counts, x='Year', y='Count', title='Number of Births Over Time')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
