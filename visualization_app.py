import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import pydeck as pdk

# Set page configuration
st.set_page_config(
    page_title="Commercial Real Estate Market Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the visual appeal
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-weight: 600;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .metric-container {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    .highlight {
        color: #3730A3;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("📊 Commercial Real Estate Interactive Analytics")
st.markdown("""
This dashboard provides an interactive exploration of commercial real estate trends across major US markets,
focusing on COVID-19 recovery patterns, office occupancy, and market dynamics.
""")

# Load data
@st.cache_data
def load_data():
    occupancy_df = pd.read_csv('Major Market Occupancy Data-revised.csv')
    availability_df = pd.read_csv('Price and Availability Data.csv')
    unemployment_df = pd.read_csv('Unemployment.csv')
    
    # Create period column for easier plotting
    occupancy_df['period'] = occupancy_df['year'].astype(str) + "-" + occupancy_df['quarter']
    
    # Add coordinates for map visualization
    market_coordinates = {
        'Manhattan': {'lat': 40.7831, 'lon': -73.9712},
        'San Francisco': {'lat': 37.7749, 'lon': -122.4194},
        'Los Angeles': {'lat': 34.0522, 'lon': -118.2437},
        'Chicago': {'lat': 41.8781, 'lon': -87.6298},
        'Boston': {'lat': 42.3601, 'lon': -71.0589},
        'Dallas/Ft Worth': {'lat': 32.7767, 'lon': -96.7970},
        'Houston': {'lat': 29.7604, 'lon': -95.3698},
        'Washington D.C.': {'lat': 38.9072, 'lon': -77.0369},
        'Philadelphia': {'lat': 39.9526, 'lon': -75.1652},
        'South Bay/San Jose': {'lat': 37.3382, 'lon': -121.8863},
        'Austin': {'lat': 30.2672, 'lon': -97.7431},
        'Seattle': {'lat': 47.6062, 'lon': -122.3321},
        'Atlanta': {'lat': 33.7490, 'lon': -84.3880},
        'Denver': {'lat': 39.7392, 'lon': -104.9903},
        'Miami': {'lat': 25.7617, 'lon': -80.1918},
        'Phoenix': {'lat': 33.4484, 'lon': -112.0740}
    }
    
    # Add coordinates to occupancy dataframe
    occupancy_map_df = occupancy_df.copy()
    occupancy_map_df['lat'] = occupancy_map_df['market'].map(lambda x: market_coordinates.get(x, {}).get('lat'))
    occupancy_map_df['lon'] = occupancy_map_df['market'].map(lambda x: market_coordinates.get(x, {}).get('lon'))
    
    return occupancy_df, availability_df, unemployment_df, occupancy_map_df

occupancy_df, availability_df, unemployment_df, occupancy_map_df = load_data()

# Creating the market recovery analysis
def create_recovery_analysis():
    # Compute pre-pandemic baseline (Q1 2020)
    baseline = occupancy_df[(occupancy_df['year'] == 2020) & (occupancy_df['quarter'] == 'Q1')].copy()
    baseline = baseline[['market', 'avg_occupancy_proportion']]
    baseline = baseline.rename(columns={'avg_occupancy_proportion': 'baseline_occupancy'})
    
    # Find pandemic low point for each market
    pandemic_low = occupancy_df.loc[occupancy_df.groupby('market')['avg_occupancy_proportion'].idxmin()]
    pandemic_low = pandemic_low[['market', 'year', 'quarter', 'avg_occupancy_proportion']]
    pandemic_low = pandemic_low.rename(columns={'avg_occupancy_proportion': 'pandemic_low'})
    
    # Get the most recent data point (Q3 2024)
    current = occupancy_df[(occupancy_df['year'] == 2024) & (occupancy_df['quarter'] == 'Q3')].copy()
    current = current[['market', 'avg_occupancy_proportion']]
    current = current.rename(columns={'avg_occupancy_proportion': 'current_occupancy'})
    
    # Merge the data
    recovery_df = baseline.merge(pandemic_low, on='market').merge(current, on='market')
    
    # Calculate recovery percentage
    recovery_df['drop_percentage'] = (recovery_df['pandemic_low'] / recovery_df['baseline_occupancy']) * 100
    recovery_df['recovery_percentage'] = (recovery_df['current_occupancy'] / recovery_df['baseline_occupancy']) * 100
    
    # Sort by recovery percentage
    recovery_df = recovery_df.sort_values('recovery_percentage', ascending=False)
    
    return recovery_df

recovery_df = create_recovery_analysis()

# Create tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Market Recovery Dashboard", "Interactive Time Series", "Market Comparison", "Geospatial Analysis", "Formal Analysis"])

with tab1:
    st.header("COVID Recovery Analysis by Market")
    st.markdown("This dashboard shows how different markets have recovered from pandemic lows compared to their pre-pandemic baselines.")
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(
            label="Best Recovering Market", 
            value=f"{recovery_df['market'].iloc[0]}",
            delta=f"{recovery_df['recovery_percentage'].iloc[0]:.1f}% of baseline"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(
            label="Average Recovery Across Markets", 
            value=f"{recovery_df['recovery_percentage'].mean():.1f}%",
            delta=f"{recovery_df['recovery_percentage'].mean() - recovery_df['drop_percentage'].mean():.1f}% from low"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        st.metric(
            label="Weakest Recovering Market", 
            value=f"{recovery_df['market'].iloc[-1]}",
            delta=f"{recovery_df['recovery_percentage'].iloc[-1]:.1f}% of baseline",
            delta_color="inverse"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### Recovery Visualization")
    
    # Create an interactive recovery comparison chart
    fig = go.Figure()
    
    # Add pandemic low bars
    fig.add_trace(go.Bar(
        x=recovery_df['market'],
        y=recovery_df['drop_percentage'],
        name='Pandemic Low (% of Baseline)',
        marker_color='rgba(219, 39, 119, 0.7)',
        hovertemplate='<b>%{x}</b><br>Pandemic Low: %{y:.1f}% of baseline<extra></extra>'
    ))
    
    # Add current recovery bars
    fig.add_trace(go.Bar(
        x=recovery_df['market'],
        y=recovery_df['recovery_percentage'],
        name='Current (% of Baseline)',
        marker_color='rgba(16, 185, 129, 0.7)',
        hovertemplate='<b>%{x}</b><br>Current: %{y:.1f}% of baseline<extra></extra>'
    ))
    
    # Add a line for the baseline (100%)
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=100,
        x1=len(recovery_df) - 0.5,
        y1=100,
        line=dict(color="red", width=2, dash="dash")
    )
    
    # Add annotation for baseline
    fig.add_annotation(
        x=len(recovery_df) - 1,
        y=105,
        text="Pre-pandemic Baseline (Q1 2020)",
        showarrow=False,
        font=dict(size=12, color="red")
    )
    
    # Update layout
    fig.update_layout(
        title="Office Occupancy Recovery By Market",
        xaxis_title="Market",
        yaxis_title="Percentage of Baseline Occupancy",
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600,
        template="plotly_white",
        margin=dict(l=50, r=50, t=80, b=80)
    )
    
    # Display the figure
    st.plotly_chart(fig, use_container_width=True)
    
    # Display the recovery data table
    with st.expander("View Detailed Recovery Data"):
        # Format the dataframe for display
        display_df = recovery_df.copy()
        display_df['baseline_occupancy'] = display_df['baseline_occupancy'].map(lambda x: f"{x:.2f}")
        display_df['pandemic_low'] = display_df['pandemic_low'].map(lambda x: f"{x:.2f}")
        display_df['current_occupancy'] = display_df['current_occupancy'].map(lambda x: f"{x:.2f}")
        display_df['drop_percentage'] = display_df['drop_percentage'].map(lambda x: f"{x:.1f}%")
        display_df['recovery_percentage'] = display_df['recovery_percentage'].map(lambda x: f"{x:.1f}%")
        
        # Rename columns for better readability
        display_df = display_df.rename(columns={
            'market': 'Market',
            'baseline_occupancy': 'Pre-COVID Baseline',
            'pandemic_low': 'Pandemic Low',
            'current_occupancy': 'Current Value',
            'drop_percentage': 'Drop %',
            'recovery_percentage': 'Recovery %'
        })
        
        st.dataframe(display_df, use_container_width=True)

with tab2:
    st.header("Interactive Time Series Exploration")
    
    # Create market selector
    selected_markets = st.multiselect(
        "Select Markets to Compare:",
        options=sorted(occupancy_df['market'].unique()),
        default=["Manhattan", "San Francisco", "Austin"]
    )
    
    if not selected_markets:
        st.warning("Please select at least one market to display the visualization.")
    else:
        # Filter data based on selection
        filtered_df = occupancy_df[occupancy_df['market'].isin(selected_markets)]
        
        # Create a time series visualization
        fig = px.line(
            filtered_df, 
            x='period', 
            y='avg_occupancy_proportion',
            color='market',
            markers=True,
            line_shape='spline',
            title="Office Occupancy Trends Over Time",
            labels={
                'period': 'Time Period',
                'avg_occupancy_proportion': 'Average Occupancy Proportion',
                'market': 'Market'
            },
            height=600
        )
        
        # Add range slider to interact with time periods
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(count=2, label="2Y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            ),
            hovermode="x unified",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Enhance with annotations for key events
        fig.add_vline(x="2020-Q1", line_dash="dash", line_color="red", opacity=0.7)
        fig.add_annotation(x="2020-Q1", y=1.0, text="COVID-19 Outbreak", showarrow=False, yshift=10)
        
        fig.add_vline(x="2021-Q2", line_dash="dash", line_color="green", opacity=0.7)
        fig.add_annotation(x="2021-Q2", y=0.95, text="Vaccine Rollout", showarrow=False, yshift=10)
        
        fig.add_vline(x="2022-Q1", line_dash="dash", line_color="orange", opacity=0.7)
        fig.add_annotation(x="2022-Q1", y=0.9, text="Return to Office Policies Begin", showarrow=False, yshift=10)
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Add a slider to observe specific quarters
        selected_period = st.select_slider(
            "Select a specific period to analyze:",
            options=sorted(occupancy_df['period'].unique())
        )
        
        # Create a bar chart for the selected period
        period_df = occupancy_df[occupancy_df['period'] == selected_period]
        period_df = period_df.sort_values('avg_occupancy_proportion', ascending=False)
        
        # Period-specific visualization
        fig2 = px.bar(
            period_df,
            x='market',
            y='avg_occupancy_proportion',
            color='avg_occupancy_proportion',
            color_continuous_scale=px.colors.sequential.Viridis,
            title=f"Office Occupancy Comparison for {selected_period}",
            labels={
                'market': 'Market',
                'avg_occupancy_proportion': 'Average Occupancy Proportion'
            },
            height=500
        )
        
        fig2.update_layout(template="plotly_white", xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Market Comparison Dashboard")
    
    # Create two-market comparison tool
    st.markdown("### Direct Market Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        market1 = st.selectbox("Select First Market:", options=sorted(occupancy_df['market'].unique()), index=0)
    
    with col2:
        market2 = st.selectbox("Select Second Market:", options=sorted(occupancy_df['market'].unique()), index=1)
    
    # Filter data for the selected markets
    market1_data = occupancy_df[occupancy_df['market'] == market1]
    market2_data = occupancy_df[occupancy_df['market'] == market2]
    
    # Create a dual-axis time series
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add traces for both markets
    fig.add_trace(
        go.Scatter(
            x=market1_data['period'],
            y=market1_data['avg_occupancy_proportion'],
            name=market1,
            line=dict(color='royalblue', width=4),
            mode='lines+markers'
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=market2_data['period'],
            y=market2_data['avg_occupancy_proportion'],
            name=market2,
            line=dict(color='firebrick', width=4),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    # Set titles and labels
    fig.update_layout(
        title_text=f"Comparative Analysis: {market1} vs {market2}",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=600,
        hovermode="x unified"
    )
    
    fig.update_xaxes(title_text="Time Period")
    fig.update_yaxes(title_text=f"{market1} Occupancy", secondary_y=False)
    fig.update_yaxes(title_text=f"{market2} Occupancy", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate key metrics for comparison
    market1_recovery = recovery_df[recovery_df['market'] == market1]['recovery_percentage'].values[0]
    market2_recovery = recovery_df[recovery_df['market'] == market2]['recovery_percentage'].values[0]
    
    market1_low = recovery_df[recovery_df['market'] == market1]['drop_percentage'].values[0]
    market2_low = recovery_df[recovery_df['market'] == market2]['drop_percentage'].values[0]
    
    # Display comparative metrics
    metric_col1, metric_col2 = st.columns(2)
    
    with metric_col1:
        st.markdown(f"<div class='metric-container'><h3>{market1} Metrics</h3>", unsafe_allow_html=True)
        st.metric("Recovery Rate", f"{market1_recovery:.1f}%", f"{market1_recovery - market1_low:.1f}% from low")
        st.markdown(f"Pandemic Low: {market1_low:.1f}% of baseline</div>", unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"<div class='metric-container'><h3>{market2} Metrics</h3>", unsafe_allow_html=True)
        st.metric("Recovery Rate", f"{market2_recovery:.1f}%", f"{market2_recovery - market2_low:.1f}% from low")
        st.markdown(f"Pandemic Low: {market2_low:.1f}% of baseline</div>", unsafe_allow_html=True)
    
    # Market availability and pricing analysis
    st.markdown("### Market Availability and Pricing (Class A Properties)")
    
    # Get availability data for the markets
    try:
        # Market 1 availability data
        market1_avail = availability_df[(availability_df['market'] == market1) & 
                                       (availability_df['internal_class'] == 'A')].copy()
        market1_avail['period'] = market1_avail['year'].astype(str) + "-" + market1_avail['quarter']
        market1_avail = market1_avail.sort_values('period')
        
        # Market 2 availability data
        market2_avail = availability_df[(availability_df['market'] == market2) & 
                                       (availability_df['internal_class'] == 'A')].copy()
        market2_avail['period'] = market2_avail['year'].astype(str) + "-" + market2_avail['quarter']
        market2_avail = market2_avail.sort_values('period')
        
        # Create a figure with two y-axes for availability and rent
        fig = make_subplots(rows=1, cols=2, subplot_titles=(f"{market1} Trends", f"{market2} Trends"))
        
        # First market - availability
        fig.add_trace(
            go.Scatter(
                x=market1_avail['period'],
                y=market1_avail['availability_proportion'],
                name=f"{market1} Availability",
                line=dict(color='blue', width=3),
                mode='lines+markers'
            ),
            row=1, col=1
        )
        
        # First market - rent
        fig.add_trace(
            go.Scatter(
                x=market1_avail['period'],
                y=market1_avail['internal_class_rent'],
                name=f"{market1} Rent",
                line=dict(color='red', width=3),
                mode='lines+markers',
                yaxis="y2"
            ),
            row=1, col=1
        )
        
        # Second market - availability
        fig.add_trace(
            go.Scatter(
                x=market2_avail['period'],
                y=market2_avail['availability_proportion'],
                name=f"{market2} Availability",
                line=dict(color='blue', width=3, dash='dash'),
                mode='lines+markers'
            ),
            row=1, col=2
        )
        
        # Second market - rent
        fig.add_trace(
            go.Scatter(
                x=market2_avail['period'],
                y=market2_avail['internal_class_rent'],
                name=f"{market2} Rent",
                line=dict(color='red', width=3, dash='dash'),
                mode='lines+markers',
                yaxis="y4"
            ),
            row=1, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=600,
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            title="Availability vs. Rent Comparison (Class A Properties)"
        )
        
        # Update axes
        fig.update_xaxes(title_text="Time Period", row=1, col=1)
        fig.update_xaxes(title_text="Time Period", row=1, col=2)
        
        fig.update_yaxes(title_text="Availability Proportion", row=1, col=1)
        fig.update_yaxes(title_text="Rent ($ per sq ft)", row=1, col=1, secondary_y=True)
        
        fig.update_yaxes(title_text="Availability Proportion", row=1, col=2)
        fig.update_yaxes(title_text="Rent ($ per sq ft)", row=1, col=2, secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating comparison chart: {e}")
        st.warning("Some markets might not have complete availability data.")

with tab4:
    st.header("Geospatial Market Analysis")
    
    # Create map of markets with their recovery rates
    st.markdown("### Recovery Rates Across US Markets")
    
    # Prepare data for the map
    map_data = occupancy_map_df.copy()
    
    # Merge with recovery data
    map_data = map_data.merge(
        recovery_df[['market', 'recovery_percentage']],
        on='market',
        how='left'
    )
    
    # Filter for the most recent period
    latest_period = map_data['period'].max()
    map_data = map_data[map_data['period'] == latest_period]
    
    # Remove rows with missing coordinates
    map_data = map_data.dropna(subset=['lat', 'lon'])
    
    # Create a column for circle size based on recovery percentage
    map_data['size'] = map_data['recovery_percentage'] / 10
    
    # Different visualization options
    map_type = st.radio(
        "Select Map Visualization Type:",
        options=["3D Column Map", "Heatmap", "Scatter Plot"],
        horizontal=True
    )
    
    if map_type == "3D Column Map":
        # Create a 3D column map showing recovery rates
        view_state = pdk.ViewState(
            latitude=39.8283,
            longitude=-98.5795,
            zoom=3.5,
            pitch=45
        )
        
        column_layer = pdk.Layer(
            "ColumnLayer",
            data=map_data,
            get_position=["lon", "lat"],
            get_elevation="recovery_percentage * 500",
            elevation_scale=1,
            radius=50000,
            get_fill_color=["recovery_percentage * 2", "recovery_percentage", "255 - recovery_percentage * 2", 140],
            pickable=True,
            auto_highlight=True
        )
        
        tooltip = {
            "html": "<b>{market}</b><br>Recovery: {recovery_percentage:.1f}%<br>Current Occupancy: {avg_occupancy_proportion:.2f}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }
        
        r = pdk.Deck(
            layers=[column_layer],
            initial_view_state=view_state,
            tooltip=tooltip
        )
        
        st.pydeck_chart(r)
        
    elif map_type == "Heatmap":
        # Create a heatmap showing recovery intensity
        view_state = pdk.ViewState(
            latitude=39.8283,
            longitude=-98.5795,
            zoom=3.5,
            pitch=0
        )
        
        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=map_data,
            get_position=["lon", "lat"],
            get_weight="recovery_percentage",
            radiusPixels=100,
            intensity=0.8,
            threshold=0.1
        )
        
        r = pdk.Deck(
            layers=[heatmap_layer],
            initial_view_state=view_state
        )
        
        st.pydeck_chart(r)
        
    else:  # Scatter Plot
        # Create an interactive Plotly geo scatter plot
        fig = px.scatter_geo(
            map_data,
            lat='lat',
            lon='lon',
            color='recovery_percentage',
            size='size',
            hover_name='market',
            hover_data={
                'market': True,
                'recovery_percentage': ':.1f',
                'avg_occupancy_proportion': ':.2f',
                'lat': False,
                'lon': False,
                'size': False
            },
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=25,
            projection='albers usa',
            title='Office Space Recovery Across US Markets',
            labels={
                'recovery_percentage': 'Recovery %',
                'avg_occupancy_proportion': 'Current Occupancy'
            }
        )
        
        fig.update_layout(
            height=600,
            geo=dict(
                showland=True,
                landcolor='rgb(230, 230, 230)',
                showlakes=True,
                lakecolor='rgb(200, 230, 255)',
                subunitcolor='rgb(180, 180, 180)',
                countrycolor='rgb(180, 180, 180)',
                showcoastlines=True,
                coastlinecolor='rgb(180, 180, 180)',
                showsubunits=True
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Add time-based map animation
    st.markdown("### Animated Occupancy Changes Over Time")
    
    # Prepare data for animation
    anim_data = occupancy_map_df.copy()
    anim_data = anim_data.dropna(subset=['lat', 'lon'])
    
    # Create animation
    fig = px.scatter_geo(
        anim_data,
        lat='lat',
        lon='lon',
        color='avg_occupancy_proportion',
        size='avg_occupancy_proportion',
        animation_frame='period',
        hover_name='market',
        hover_data={
            'market': True,
            'avg_occupancy_proportion': ':.2f',
            'lat': False,
            'lon': False
        },
        color_continuous_scale=px.colors.sequential.Plasma,
        size_max=25,
        projection='albers usa',
        title='Office Occupancy Evolution (2020-2024)',
        labels={
            'avg_occupancy_proportion': 'Occupancy Rate'
        }
    )
    
    fig.update_layout(
        height=600,
        geo=dict(
            showland=True,
            landcolor='rgb(230, 230, 230)',
            showlakes=True,
            lakecolor='rgb(200, 230, 255)',
            subunitcolor='rgb(180, 180, 180)',
            countrycolor='rgb(180, 180, 180)',
            showcoastlines=True,
            coastlinecolor='rgb(180, 180, 180)',
            showsubunits=True
        ),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(
                label="Play",
                method="animate",
                args=[None, {"frame": {"duration": 800, "redraw": True}, "fromcurrent": True}]
            )]
        )]
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("Formal Analysis: Commercial Real Estate Market Recovery Patterns")
    
    # Function to read and display the analysis.md file
    @st.cache_data
    def load_analysis():
        try:
            with open("analysis.md", "r") as file:
                return file.read()
        except FileNotFoundError:
            return "Analysis file not found. Please make sure 'analysis.md' exists in the project directory."

    analysis_content = load_analysis()
    
    # Add custom styling for the paper view
    st.markdown("""
    <style>
    .paper-container {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        font-family: 'Times New Roman', Times, serif;
        line-height: 1.6;
    }
    .paper-container h1 {
        font-size: 24px;
        text-align: center;
        margin-bottom: 20px;
    }
    .paper-container h2 {
        font-size: 20px;
        margin-top: 30px;
        margin-bottom: 15px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 5px;
    }
    .paper-container h3 {
        font-size: 18px;
        margin-top: 25px;
    }
    .paper-container p {
        text-align: justify;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the analysis as a formal paper
    st.markdown(f'<div class="paper-container">{analysis_content}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("### Market Insights and Recommendations")
st.markdown("""
Based on our interactive data exploration, here are key insights for Savills clients:

1. **Tech-Driven Markets Show Resilience**: Austin and Dallas/Ft Worth have recovered most strongly compared to pre-pandemic baselines.

2. **Southern/Central Markets Outperforming Coastal Markets**: The strongest recovery is seen in Texas markets with recovery rates between 67-74% of pre-pandemic levels.

3. **Strong Negative Correlation Between Unemployment and Office Occupancy**: All markets show a negative correlation between unemployment rates and office occupancy.

4. **Market-Specific Strategies Required**: The data suggests different optimal timing for lease negotiations across markets.
""")

# Add instructions for using the dashboard
with st.expander("Dashboard Usage Tips"):
    st.markdown("""
    - **Interactive Elements**: Most visualizations are interactive - hover for details, click legends to toggle visibility, and use range selectors to zoom.
    - **Market Comparisons**: The Market Comparison tab allows direct comparison between any two markets.
    - **Geospatial Analysis**: The map visualizations show geographical patterns in recovery rates.
    - **Time Animation**: Use the play button on the animated map to see how occupancy has changed over time.
    - **Formal Analysis**: The Formal Analysis tab provides an in-depth scientific analysis of the commercial real estate market recovery patterns.
    """)