from dash import Dash, html, dcc, Input, Output, callback
import requests
from dash_mantine_components import MultiSelect, MantineProvider
import plotly.express as px

def get_multiselect_list():
    url = "http://127.0.0.1:5000/Sector"
    _sectors = None
    try: 
        response = requests.get(url)
        if response.status_code == 200:
            _sectors= response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    multiselect_list=[]
    if _sectors:
        for s in _sectors:
            multiselect_list.append({"value": s, "label": s})
    return multiselect_list

app= Dash()
app.layout = MantineProvider(
    theme={"colorScheme": "dark", "primaryColor": "blue"},
    children= [html.H1("Sectors"),
              MultiSelect(
            label="Choose your options",
            placeholder="Select multiple sectors",
            data=get_multiselect_list(),  # Fetch the list of sectors
            value=[],  # Default selected values
            searchable=True,  # Enable search functionality
            clearable=True,  # Allow clearing the selection
            id='sector-multiselect',
        ), 
        dcc.Graph(id='pie-chart'),
        html.Button('Download', id='download-button', n_clicks=0),
        dcc.Download(id="dummy-output")
        ])

@callback(
    Output('pie-chart', 'figure'),
    Input('sector-multiselect', 'value'))
def update_figure(selected):
    data = {
    'labels': selected,
    'values': [ebitda_all_sectors[s] for s in selected]}

    # Create a pie chart using Plotly Express
    fig = px.pie(data, values='values', names='labels', title='EBITDA Distribution')

    fig.update_layout(transition_duration=500)

    return fig

# Callback to handle button click and make API call
@app.callback(
    Output('dummy-output', 'data'),
    Input('download-button', 'n_clicks')
)
def make_api_call(n_clicks):
    if n_clicks > 0:
        try:
            # Example API call (replace with your API endpoint)
            response = requests.get('http://127.0.0.1:5000/download', stream=True)
            # You can process the response here if needed
            if response.status_code == 200:
                return dcc.send_bytes(response.content, filename="constituents-financials_csv.csv")
            else:
                print(f"Error: {response.status_code}")  # Log error in console
        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # Log exception
    return None  # No output to display

def get_ebitda(sector:str):
    url = "http://127.0.0.1:5000/"
    try: 
        response = requests.get(url, params={"Sector": sector})
        if response.status_code == 200:
            return response.json()
        print("Cannot get ebitda, err")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    
def get_ebitda_all_sectors():
    url = "http://127.0.0.1:5000/Sector"
    try: 
        response = requests.get(url)
        if response.status_code == 200:
            _sectors= response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        _sectors = None
    ebitda_dict = {}
    if _sectors:
        for sector in _sectors:
            ebitda = sum(get_ebitda(sector))
            if ebitda:
                ebitda_dict[sector] = ebitda
    return ebitda_dict

if __name__ == '__main__':
    ebitda_all_sectors= get_ebitda_all_sectors()
    print(ebitda_all_sectors)
    app.run(debug=True)