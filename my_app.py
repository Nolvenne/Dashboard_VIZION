import streamlit as st  # Streamlit for the web application
import pandas as pd  # For data manipulation and analysis
import plotly.express as px  # For quick visualization, mainly for plotting
import plotly.graph_objects as go  # For more detailed plot customization (e.g., for creating advanced charts)
import numpy as np  # For numerical operations, often used with data processing
import streamlit.components.v1 as components  # For embedding custom HTML and JS, such as D3 visualizations
import json  # For working with JSON data



# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')

    # Convert columns to numeric, forcing non-numeric values to NaN
    year_columns = ['Total2016', 'Total2017', 'Total2018', 'Total2019', 'Total2020', 'Total2021']
    for col in year_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Optionally fill NaN values with 0 or handle as per your needs
    df = df.fillna(0)
    
    return df

df = load_data()

# App title
st.markdown("""
    <style>
        .title-box {
            background-color: #333333;  /* Darker gray background */
            color: #f4f4f4;  /* Lighter text color for contrast */
            padding: 30px;  /* Increased padding for better spacing */
            text-align: center;
            border-radius: 10px;
            font-size: 30px;  /* Increased font size for a bigger title */
            font-weight: bold;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 40px;  /* Increased margin at the bottom */
        }
    </style>
    <div class="title-box">
        VIZION: Global Solar Production Tracker
    </div>
""", unsafe_allow_html=True)


st.subheader("Dataset cover the 2016 to 2021")
# Sidebar for filtering by country or continent
st.sidebar.header("Filter Data")
continent_filter = st.sidebar.selectbox("Select Continent", ["All"] + df['Continent'].unique().tolist())

# Filter the data based on the selections
if continent_filter != "All":
    df = df[df['Continent'] == continent_filter]

#filter year
year_filter = st.sidebar.selectbox("Select Year for Chart", [ "2020", "2019", "2018", "2017", "2016"])


# Dropdown to select a year for Choropleth Map
#st.subheader("Solar Production by Country and Continent (Choropleth map)")

# Melt the DataFrame to include all years for animation
df_melt = df.melt(id_vars=['Country', 'Continent'], 
                  value_vars=['Total2016', 'Total2017', 'Total2018', 'Total2019', 'Total2020', 'Total2021'],
                  var_name='Year', value_name='SolarProduction')

# Filter the data for the selected year
data_selected_year = df_melt[df_melt['Year'] == f'Total{year_filter}'].dropna()

# Define a list of unique solar production values
unique_values = sorted(data_selected_year['SolarProduction'].unique())

# Generate a list of colors (one for each value)
colors = px.colors.qualitative.Set3  # You can also use other sets like 'Set2', 'Set3', etc.
color_map = {value: colors[i % len(colors)] for i, value in enumerate(unique_values)}
             
# Generate the animated Choropleth map with discrete colors
Cho_fig = px.choropleth(data_selected_year, 
                     locations='Country', 
                     locationmode='country names', 
                     color='SolarProduction',
                     hover_name='Country', 
                     color_discrete_map=color_map,  # Apply the discrete color map
                     title=f"Solar Production by Country in {year_filter}",
                     labels={'SolarProduction': 'Solar Production (in MW)'},
                     animation_frame='Year',  # Animation over the years
                     projection='natural earth'  # Set map projection
                    )

# Display the map in Streamlit
st.plotly_chart(Cho_fig, use_container_width=True)



# Line Plot: Solar production trend (Total from 2016 to 2021) for selected countries
df_line = df.melt(id_vars=["Country"], value_vars=["Total2016", "Total2017", "Total2018", "Total2019", "Total2020", "Total2021"], var_name="Year", value_name="Solar Production")
line_fig = px.line(df_line, x="Year", y="Solar Production", color="Country", title="Annual Solar Production Trend", labels={"Solar Production": "Solar Production (in MW)"})
#st.plotly_chart(line_fig)


# Bar Chart: Total solar production for a specific year ()
#st.subheader(f"Total Solar Production in {year_filter}")
df_bar = df[["Country", f"Total{year_filter}"]]
bar_fig = px.bar(df_bar, x="Country", y=f"Total{year_filter}", title=f"Solar Production in {year_filter}", labels={f"Total{year_filter}": "Solar Production (in MW)"})
#st.plotly_chart(bar_fig)



# Pie Chart: Share of solar production by continent for a specific year
#st.subheader(f"Share of Solar Production by Country in {year_filter}")
df_pie = df[[f"Country", f"Total{year_filter}"]]
pie_fig = px.pie(df_pie, names="Country", values=f"Total{year_filter}", title=f"Share of Solar Production by Country in {year_filter}")
#st.plotly_chart(pie_fig)


#st.subheader("Dynamic Bubble Chart - Country Data")
# Load the data from CSV
# Load the data
df = pd.read_csv('data.csv')

# Clean up any extra spaces in column names
df.columns = df.columns.str.strip()

# Sidebar for user input to select year and continent
#st.sidebar.header("Filter Options")

# Prepare Data based on the selected year and continent
data_selected_year = df[['Country', f'Total{year_filter}', 'Continent']].dropna()

if continent_filter != "All":
    data_selected_year = data_selected_year[data_selected_year['Continent'] == continent_filter]

# Create a Bubble Chart using Plotly Express
bubble_fig = px.scatter(data_selected_year,
                 x=f'Total{year_filter}',  # X-axis based on the selected year
                 y=f'Total{year_filter}',  # Y-axis based on the selected year
                 size=f'Total{year_filter}',  # Bubble size is determined by production value
                 color='Country',  # Bubble color determined by country
                 hover_name='Country',  # Display country on hover
                 size_max=100,  # Maximum bubble size
                 title=f"Solar Production by Country in {year_filter}",
                 template='plotly_dark')

# Display the bubble chart in Streamlit
#st.plotly_chart(fig, use_container_width=True)

line_fig.update_layout(showlegend=True)


col2, col3= st.columns(2)  # First row (3 columns)
with col2:
    st.plotly_chart(line_fig)
with col3:
    st.plotly_chart(pie_fig)


# Layout for the second row (2 columns)
col4, col5= st.columns(2) 
with col4:
    st.plotly_chart(bar_fig) # Second row (2 columns)
with col5:
    st.plotly_chart(bubble_fig)



# Load your dataset (replace with the path to your dataset)

# Load the data
df = pd.read_csv('data.csv')

# Clean up any extra spaces in column names
df.columns = df.columns.str.strip()

# Prepare the year filter with the correct column names
year_filt = ['Total2016', 'Total2017', 'Total2018', 'Total2019', 'Total2020', 'Total2021']

# Melt the DataFrame to prepare it for a stream graph
df_melt = df.melt(id_vars=['Country', 'Continent'], 
                  value_vars=year_filt,
                  var_name='Year', value_name='SolarProduction')

# Create Streamlit app
st.subheader("Solar Production by Country")

# Initialize the figure for Stream Graph
Stream_fig = go.Figure()

# Add traces for each country
for country in df_melt['Country'].unique():
    df_country = df_melt[df_melt['Country'] == country]
    Stream_fig.add_trace(go.Scatter(
        x=df_country['Year'], 
        y=df_country['SolarProduction'],
        stackgroup='one',  # Use 'one' to create a stacked stream graph
        name=country,
        hoverinfo='x+y+name',  # Display the country and values on hover
        line=dict(shape='linear'),
        mode='lines+markers',  # Adds dots to the line for better visibility
        marker=dict(size=8),  # Size of the markers (dots)
        fill='tonexty',  # Fill the area under the line
        fillcolor='rgba(255, 0, 0, 0.1)'  # Color fill under the curve
    ))

# Show the figure in Streamlit
st.plotly_chart(Stream_fig)




# Create a DataFrame

data= pd.read_csv('data.csv')
df = pd.DataFrame(data)


# Filter the data based on the selected year
df_tree = df[['Country', 'Continent', f'Total{year_filter}']]

# Create the TreeMap Figure
tree_map_fig = px.treemap(df_tree, 
                           path=["Continent", "Country"], 
                           values=f"Total{year_filter}", 
                           title=f"Share of Solar Production by Country in {year_filter}",
                           color=f"Country",  # Coloring based on the production in 2021
                           color_continuous_scale="Viridis")

# Create Play Button and Animation
frames = []

# Create frames for animation (transition between Continent -> Country)
for continent in df['Continent'].unique():
    filtered_df = df_tree[df_tree['Continent'] == continent]
    
    # Generate frame for each continent, path will be dynamic based on selection
    frame = go.Frame(
        data=[
            go.Treemap(
                labels=filtered_df['Country'],
                parents=[continent] * len(filtered_df),
                values=filtered_df[f"Total{year_filter}"],
                hoverinfo="label+value+percent entry"
            )
        ],
        name=continent
    )
    frames.append(frame)

# Adding frames to the tree map figure
tree_map_fig.frames = frames

# Update layout for Play and Pause buttons
tree_map_fig.update_layout(
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[
            dict(
                label="Play",
                method="animate",
                args=[None, dict(frame=dict(duration=2000, redraw=True), fromcurrent=True)]
            ),
            dict(
                label="Pause",
                method="relayout",
                args=[{"sliders": None}]
            )
        ]
    )],
    title=f"Solar Production by Country and Continent ({year_filter})"
)
# Display the TreeMap with the animation controls
st.plotly_chart(tree_map_fig, use_container_width=True)




# Read the HTML file content
with open("new.html", "r") as file:
    html_code = file.read()

# Display the HTML file in Streamlit
components.html(html_code, height=500)


