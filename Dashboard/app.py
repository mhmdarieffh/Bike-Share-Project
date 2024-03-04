import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the dashboard
st.title('Bike Sharing Dashboard')

# Load the data
@st.cache_data
def load_data():
    data_path = 'days_data.csv'  # Update this path
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])  # Convert 'date' to datetime
    df['year_month'] = df['date'].dt.strftime('%Y-%m')  # Add 'year_month' for monthly trends
    return df

data = load_data()

# Sidebar for filters
st.sidebar.header('Filters')
year_option = st.sidebar.selectbox('Select Year:', options=data['year'].unique())
filtered_data = data[data['year'] == year_option]

# Main dashboard content
# Using columns for layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Casual Users", f"{filtered_data['casual'].sum():,.0f}")
with col2:
    st.metric("Total Registered Users", f"{filtered_data['registered'].sum():,.0f}")
with col3:
    st.metric("Total Rides", f"{filtered_data['total_count'].sum():,.0f}")

# Monthly Trend Analysis with Plotly
st.header('Monthly Trend Analysis')
monthly_data = filtered_data.groupby('year_month').agg({'casual': 'sum', 'registered': 'sum', 'total_count': 'sum'}).reset_index()
fig = px.line(monthly_data, x='year_month', y=['total_count', 'casual', 'registered'], labels={'value': 'Number of Users', 'year_month': 'Month'}, title='Monthly Usage Trend')
st.plotly_chart(fig, use_container_width=True)

# Weather Impact on Usage with Plotly
st.header('Weather Impact on Usage')
fig = px.box(filtered_data, x='weather', y='total_count', title='Impact of Weather on User Count')
st.plotly_chart(fig, use_container_width=True)

# Temperature vs User Activity with Plotly
st.header('Temperature vs User Activity')
fig = px.scatter(filtered_data, x='temp', y='total_count', color='season', title='Temperature vs Total User Count by Season', labels={'temp': 'Normalized Temperature', 'total_count': 'Total User Count'})
st.plotly_chart(fig, use_container_width=True)

# Year-over-Year Monthly Comparison
st.header('Year-over-Year Monthly Comparison')
# Pivot table to compare months across years
pivot_data = data.pivot_table(values='total_count', index='month', columns='year', aggfunc='sum')
fig = px.line(pivot_data, labels={'value': 'Total User Count', 'variable': 'Year'}, title='Monthly User Count Year-over-Year')
fig.update_xaxes(type='category')  # Treat the x-axis as category to maintain the month order
st.plotly_chart(fig, use_container_width=True)
