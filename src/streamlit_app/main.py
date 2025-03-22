import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

def fetch_space_launches():
    """Fetch space launch data from Launch Library API."""
    url = "https://ll.thespacedevs.com/2.2.0/launch/previous/?limit=40&mode=detailed"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        st.error("Impossible de récupérer les données de lancement")
        return []

def process_launch_data(launches):
    """Process launch data into a DataFrame."""
    launch_data = []
    for launch in launches:
        launch_data.append({
            'Name': launch['name'],
            'Date': launch['net'],
            'Launcher': launch['rocket']['configuration']['name'],
            'Launch Site': launch['pad']['location']['name'],
            'Mission': launch.get('mission', {}).get('name', 'Unknown')
        })
    return pd.DataFrame(launch_data)

def create_launch_timeline(df):
    """Create a timeline of launches per month."""
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_launches = df.groupby('Month').size().reset_index(name='Launches')
    monthly_launches['Month'] = monthly_launches['Month'].astype(str)
    return monthly_launches

def main():
    st.title("Chronologie des Missions Spatiales")

    # Fetch and process launch data
    launches = fetch_space_launches()
    df = process_launch_data(launches)

    # Sidebar filters
    st.sidebar.header("Filtres")
    
    # Launcher filter
    selected_launchers = st.sidebar.multiselect(
        "Sélectionner les Lanceurs", 
        df['Launcher'].unique()
    )
    
    # Launch Site filter
    selected_sites = st.sidebar.multiselect(
        "Sélectionner les Sites de Lancement", 
        df['Launch Site'].unique()
    )

    # Apply filters
    filtered_df = df.copy()
    if selected_launchers:
        filtered_df = filtered_df[filtered_df['Launcher'].isin(selected_launchers)]
    if selected_sites:
        filtered_df = filtered_df[filtered_df['Launch Site'].isin(selected_sites)]

    # Display filtered launches
    st.subheader("Liste des Lancements")
    st.dataframe(filtered_df[['Name', 'Date', 'Launcher', 'Launch Site', 'Mission']])

    # Create launch timeline
    monthly_launches = create_launch_timeline(filtered_df)
    
    # Plot timeline
    st.subheader("Nombre de Lancements par Mois")
    fig = px.bar(
        monthly_launches, 
        x='Month', 
        y='Launches', 
        title='Chronologie des Lancements Spatiaux'
    )
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
