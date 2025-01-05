import streamlit as st
import pandas as pd
import plotly.express as px
from geopy.geocoders import Nominatim

# Load the dataset
def load_data():
    file_path = "database.csv"  # Adjust if necessary
    data = pd.read_csv(file_path)
    return data

data = load_data()

# Geocode latitude and longitude to states
def add_state_column(data):
    if 'State' in data.columns:
        return data

    geolocator = Nominatim(user_agent="earthquake_app")

    def get_state(lat, lon):
        try:
            location = geolocator.reverse((lat, lon), exactly_one=True)
            if location and 'address' in location.raw:
                return location.raw['address'].get('state', 'Unknown')
        except Exception as e:
            return 'Unknown'

    st.write("Adding 'State' column using reverse geocoding. This may take some time...")
    data['State'] = data.apply(lambda row: get_state(row['Latitude'], row['Longitude']), axis=1)
    return data

data = add_state_column(data)

# Preprocess data for visualization
def preprocess_data(data):
    state_counts = data['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Occurrences']
    return state_counts

state_data = preprocess_data(data)

# Streamlit app
st.title("Earthquake Likelihood by State")

st.write("### Earthquake Dataset Overview")
st.dataframe(data.head())

# Bar chart visualization
st.write("### Earthquake Occurrences by State")
fig = px.bar(state_data, x='State', y='Occurrences', 
             title='Earthquake Occurrences by State', 
             labels={'Occurrences': 'Number of Earthquakes'},
             color='Occurrences')

st.plotly_chart(fig)

# Add filters if needed
magnitude_filter = st.slider("Select minimum magnitude:", 0.0, data['Magnitude'].max(), 5.0)
filtered_data = data[data['Magnitude'] >= magnitude_filter]

filtered_state_data = filtered_data['State'].value_counts().reset_index()
filtered_state_data.columns = ['State', 'Occurrences']

st.write(f"### States with Earthquakes of Magnitude >= {magnitude_filter}")
fig_filtered = px.bar(filtered_state_data, x='State', y='Occurrences', 
                      title=f'States with Earthquakes (Magnitude >= {magnitude_filter})',
                      labels={'Occurrences': 'Number of Earthquakes'},
                      color='Occurrences')

st.plotly_chart(fig_filtered)

# Requirements
st.write("### Requirements")
st.code("""pip install streamlit pandas plotly geopy""")
