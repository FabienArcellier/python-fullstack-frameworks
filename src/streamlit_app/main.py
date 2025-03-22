import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

def fetch_space_launches():
    """Fetch space launch data from Launch Library API."""
    url = "https://ll.thespacedevs.com/2.2.0/launch/previous/?limit=200&mode=detailed"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        st.error("Unable to retrieve launch data")
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
            'Mission': launch.get('mission', {}).get('name', 'Unknown'),
            'Status': launch['status']['name']
        })
    return pd.DataFrame(launch_data)

def create_launch_timeline(df):
    """Create a timeline of launches per month."""
    df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M')
    monthly_launches = df.groupby('Month').size().reset_index(name='Launches')
    monthly_launches['Month'] = monthly_launches['Month'].astype(str)
    return monthly_launches

def main():
    st.title("Space Missions Timeline")

    # Fetch and process launch data
    launches = fetch_space_launches()
    df = process_launch_data(launches)

    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Launcher filter
    selected_launchers = st.sidebar.multiselect(
        "Select Launchers", 
        df['Launcher'].unique()
    )
    
    # Launch Site filter
    selected_sites = st.sidebar.multiselect(
        "Select Launch Sites", 
        df['Launch Site'].unique()
    )

    # Status filter
    selected_statuses = st.sidebar.multiselect(
        "Select Launch Statuses", 
        df['Status'].unique()
    )

    # Apply filters
    filtered_df = df.copy()
    if selected_launchers:
        filtered_df = filtered_df[filtered_df['Launcher'].isin(selected_launchers)]
    if selected_sites:
        filtered_df = filtered_df[filtered_df['Launch Site'].isin(selected_sites)]
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['Status'].isin(selected_statuses)]

    # Display filtered launches
    st.subheader("Launch List")
    st.dataframe(filtered_df[['Name', 'Date', 'Launcher', 'Launch Site', 'Mission', 'Status']])

    # Create launch timeline
    monthly_launches = create_launch_timeline(filtered_df)
    
    # Plot timeline
    st.subheader("Number of Launches per Month")
    fig = px.bar(
        monthly_launches, 
        x='Month', 
        y='Launches', 
        title='Space Launch Chronology'
    )
    st.plotly_chart(fig)

    # Additional statistics
    st.subheader("Launch Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Launches", len(filtered_df))
    
    with col2:
        st.metric("Unique Launchers", filtered_df['Launcher'].nunique())
    
    with col3:
        st.metric("Unique Launch Sites", filtered_df['Launch Site'].nunique())

if __name__ == "__main__":
    main()
