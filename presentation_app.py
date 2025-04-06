import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Commercial Real Estate Recovery",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 30px;
    }
    .slide-header {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        border-bottom: 2px solid #10B981;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    .content-container {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    .highlight {
        color: #3730A3;
        font-weight: bold;
    }
    /* Nav buttons */
    .stButton button {
        border-radius: 20px;
        font-weight: bold;
        padding: 10px 24px;
        background-color: #1E3A8A;
        color: white;
    }
    .stButton button:hover {
        background-color: #10B981;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data(ttl=3600)
def load_data():
    occupancy_df = pd.read_csv('Major Market Occupancy Data-revised.csv')
    availability_df = pd.read_csv('Price and Availability Data.csv')
    
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
        'Austin': {'lat': 30.2672, 'lon': -97.7431}
    }
    
    # Add coordinates to occupancy dataframe
    occupancy_map_df = occupancy_df.copy()
    occupancy_map_df['lat'] = occupancy_map_df['market'].map(lambda x: market_coordinates.get(x, {}).get('lat'))
    occupancy_map_df['lon'] = occupancy_map_df['market'].map(lambda x: market_coordinates.get(x, {}).get('lon'))
    
    return occupancy_df, availability_df, occupancy_map_df

# Creating the market recovery analysis
def create_recovery_analysis(occupancy_df):
    # Compute pre-pandemic baseline (Q1 2020)
    baseline = occupancy_df[(occupancy_df['year'] == 2020) & (occupancy_df['quarter'] == 'Q1')].copy()
    baseline = baseline[['market', 'avg_occupancy_proportion']]
    baseline = baseline.rename(columns={'avg_occupancy_proportion': 'baseline_occupancy'})
    
    # Find pandemic low point for each market
    pandemic_low = occupancy_df.loc[occupancy_df.groupby('market')['avg_occupancy_proportion'].idxmin()]
    pandemic_low = pandemic_low[['market', 'year', 'quarter', 'avg_occupancy_proportion']]
    pandemic_low = pandemic_low.rename(columns={'avg_occupancy_proportion': 'pandemic_low'})
    
    # Get the most recent data point
    latest_year = occupancy_df['year'].max()
    latest_quarter = occupancy_df[occupancy_df['year'] == latest_year]['quarter'].max()
    current = occupancy_df[(occupancy_df['year'] == latest_year) & (occupancy_df['quarter'] == latest_quarter)].copy()
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

# Create visualizations
def create_recovery_chart(recovery_df):
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
        height=500,
        template="plotly_white"
    )
    
    return fig

def create_3d_map(map_data):
    fig = px.scatter_3d(
        map_data,
        x='lon',
        y='lat',
        z='recovery_percentage',
        color='recovery_percentage',
        size='recovery_percentage',
        hover_name='market',
        hover_data={
            'recovery_percentage': ':.1f',
            'lat': False,
            'lon': False
        },
        color_continuous_scale=px.colors.sequential.Viridis,
        size_max=20,
        opacity=0.8,
        title="3D Visualization of Market Recovery"
    )
    
    fig.update_layout(
        height=600,
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Recovery Percentage',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1)
            )
        )
    )
    
    return fig

def create_occupancy_heatmap(occupancy_df):
    # Pivot the data for the heatmap
    pivot_df = occupancy_df.pivot(index='market', columns='period', values='avg_occupancy_proportion')
    
    # Create heatmap
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Time Period", y="Market", color="Occupancy Rate"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale="Viridis",
        title="Market Occupancy Patterns Over Time"
    )
    
    fig.update_layout(
        height=500,
        xaxis={'side': 'top'},
        coloraxis_colorbar=dict(
            title="Occupancy Rate",
            thicknessmode="pixels", thickness=20,
            lenmode="pixels", len=300
        )
    )
    
    return fig

def create_market_comparison(occupancy_df, availability_df):
    market1 = 'Austin'
    market2 = 'San Francisco'
    
    # Filter data for the selected markets
    market1_data = occupancy_df[occupancy_df['market'] == market1]
    market2_data = occupancy_df[occupancy_df['market'] == market2]
    
    # Filter availability data
    market1_avail = availability_df[(availability_df['market'] == market1) & 
                                   (availability_df['internal_class'] == 'A')].copy()
    market1_avail['period'] = market1_avail['year'].astype(str) + "-" + market1_avail['quarter']
    market1_avail = market1_avail.sort_values('period')
    
    market2_avail = availability_df[(availability_df['market'] == market2) & 
                                   (availability_df['internal_class'] == 'A')].copy()
    market2_avail['period'] = market2_avail['year'].astype(str) + "-" + market2_avail['quarter']
    market2_avail = market2_avail.sort_values('period')
    
    # Create a figure with two y-axes
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
        height=500,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        title="Availability vs. Rent Comparison: Recovering (Austin) vs. Lagging (San Francisco) Markets"
    )
    
    return fig

def create_sunburst(recovery_df):
    # Create market categories for visualization
    def categorize_market(market):
        tech_hubs = ['San Francisco', 'South Bay/San Jose', 'Austin', 'Seattle']
        financial_centers = ['Manhattan', 'Chicago', 'Boston']
        regional_centers = ['Philadelphia', 'Washington D.C.', 'Los Angeles']
        southern_markets = ['Dallas/Ft Worth', 'Houston', 'Austin']
        
        categories = []
        if market in tech_hubs:
            categories.append('Tech Hub')
        if market in financial_centers:
            categories.append('Financial Center')
        if market in regional_centers:
            categories.append('Regional Center')
        if market in southern_markets:
            categories.append('Southern Market')
        
        # Default category if none match
        if not categories:
            categories.append('Other')
        
        return categories[0]  # Return the first matching category
    
    # Add category and region information
    sunburst_df = recovery_df.copy()
    sunburst_df['category'] = sunburst_df['market'].apply(categorize_market)
    
    def get_region(market):
        west = ['San Francisco', 'Los Angeles', 'Seattle', 'South Bay/San Jose']
        south = ['Austin', 'Dallas/Ft Worth', 'Houston']
        east = ['Manhattan', 'Boston', 'Philadelphia', 'Washington D.C.']
        midwest = ['Chicago']
        
        if market in west:
            return 'West'
        elif market in south:
            return 'South'
        elif market in east:
            return 'East'
        elif market in midwest:
            return 'Midwest'
        else:
            return 'Other'
    
    sunburst_df['region'] = sunburst_df['market'].apply(get_region)
    
    # Prepare data for sunburst chart
    hierarchical_data = []
    
    for _, row in sunburst_df.iterrows():
        hierarchical_data.append({
            'Region': row['region'],
            'Category': row['category'],
            'Market': row['market'],
            'Recovery': row['recovery_percentage']
        })
    
    # Create dataframe with hierarchical data
    hierarchy_df = pd.DataFrame(hierarchical_data)
    
    # Create sunburst chart
    fig = px.sunburst(
        hierarchy_df,
        path=['Region', 'Category', 'Market'],
        values='Recovery',
        color='Recovery',
        color_continuous_scale='Viridis',
        title='Market Recovery by Region and Category',
        hover_data={'Recovery': ':.1f%'}
    )
    
    fig.update_layout(height=600)
    
    return fig

def create_animated_occupancy(occupancy_map_df):
    anim_data = occupancy_map_df.copy().dropna(subset=['lat', 'lon'])
    fig = px.scatter_geo(
        anim_data,
        lat='lat',
        lon='lon',
        color='avg_occupancy_proportion',
        size='avg_occupancy_proportion',
        animation_frame='period',
        hover_name='market',
        scope='usa',
        title='Office Occupancy Evolution (2020-2024)',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    fig.update_layout(
        height=500,
        geo=dict(
            showland=True,
            landcolor='rgb(230, 230, 230)',
            showlakes=True,
            lakecolor='rgb(200, 230, 255)',
            showcoastlines=True
        )
    )
    
    return fig

# Main application
def main():
    # Load data
    occupancy_df, availability_df, occupancy_map_df = load_data()
    recovery_df = create_recovery_analysis(occupancy_df)
    
    # Filter map data for 3D visualization
    latest_period = occupancy_map_df['period'].max()
    map_data = occupancy_map_df[occupancy_map_df['period'] == latest_period]
    map_data = map_data.dropna(subset=['lat', 'lon'])
    map_data = map_data.merge(
        recovery_df[['market', 'recovery_percentage']],
        on='market',
        how='left'
    )
    
    # Create navigation
    st.markdown('<h1 class="main-title">Commercial Real Estate Market Recovery</h1>', unsafe_allow_html=True)
    st.markdown("**Post-Pandemic Patterns & Strategic Insights**")
    
    # Sidebar
    with st.sidebar:
        st.title("Presentation Navigation")
        st.markdown("""
        > **Key Insights**
        
        - Southern/Central markets show strongest recovery (Austin at 73.6%)
        - Strong negative correlation between unemployment and office occupancy
        - Texas markets present the most strategic opportunity
        - Market-specific strategies are essential in the post-pandemic landscape
        """)
        
    # Initialize session state
    if 'slide' not in st.session_state:
        st.session_state.slide = 0
    
    # Navigation
    slides = ["Title", "Recovery Patterns", "Economic Correlations", "Strategic Implications", "Conclusions"]
    cols = st.columns([1, 1, 3, 1, 1])
    
    with cols[0]:
        if st.session_state.slide > 0:
            if st.button("⏮️ First"):
                st.session_state.slide = 0
                st.rerun()
    
    with cols[1]:
        if st.session_state.slide > 0:
            if st.button("◀️ Previous"):
                st.session_state.slide -= 1
                st.rerun()
    
    with cols[2]:
        progress = st.session_state.slide / (len(slides) - 1)
        st.progress(progress)
    
    with cols[3]:
        if st.session_state.slide < len(slides) - 1:
            if st.button("Next ▶️"):
                st.session_state.slide += 1
                st.rerun()
    
    with cols[4]:
        if st.session_state.slide < len(slides) - 1:
            if st.button("Last ⏭️"):
                st.session_state.slide = len(slides) - 1
                st.rerun()
                
    st.markdown(f"<h3 style='text-align: center;'>Slide {st.session_state.slide + 1}/{len(slides)}</h3>", unsafe_allow_html=True)
    
    # Slide content container
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    # Display slides based on current slide index
    if st.session_state.slide == 0:  # Title slide
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("# Commercial Real Estate Market Recovery")
            st.markdown("## Post-Pandemic Patterns & Strategic Insights")
            st.markdown("---")
            st.markdown("*Data-Driven Analysis for Strategic Decision Making*")
        
        with col2:
            # Corporate building image
            try:
                img = Image.open("images/building.jpg")
                st.image(img, use_column_width=True)
            except:
                st.image("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80")
    
    elif st.session_state.slide == 1:  # Recovery Patterns
        st.markdown('<h2 class="slide-header">Recovery Patterns Across Markets</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            fig = create_recovery_chart(recovery_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("## Key Findings")
            st.markdown("""
            - **Regional Divergence**: Southern/Central markets (73.6% recovery in Austin) consistently outperforming coastal markets (57.7% in San Francisco)
            
            - **Tech Market Dichotomy**: Austin leads recovery while other tech hubs like San Francisco and Silicon Valley show significantly weaker recovery
            
            - **Three-Phase Pattern**: Universal sharp decline (Q1-Q2 2020), gradual recovery (Q3 2020-Q1 2022), stabilization with seasonal fluctuations (Q2 2022-present)
            
            - **Financial Center Resilience**: Manhattan and Chicago recovered approximately two-thirds of pre-pandemic occupancy (64.8% and 65.8% respectively)
            """)
        
        st.markdown("### Animated Occupancy Changes")
        fig = create_animated_occupancy(occupancy_map_df)
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.slide == 2:  # Economic Correlations
        st.markdown('<h2 class="slide-header">Economic Correlations & Market Dynamics</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            fig = create_3d_map(map_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("## Economic Relationships")
            st.markdown("""
            - **Unemployment Correlation**: Strong negative correlation between unemployment rates and office occupancy
              - Austin: -0.84
              - Manhattan: -0.82
              - Houston: -0.80
            
            - **Pricing Dynamics**:
              - Inverse relationship in recovering markets (Austin shows rising rates with increasing occupancy)
              - Lagged price adjustment in weaker markets (San Francisco rental rates stable despite increased availability)
              - Class A properties show remarkable price stability despite occupancy fluctuations
            """)
        
        st.markdown("### Market Comparison: Austin vs. San Francisco")
        fig = create_market_comparison(occupancy_df, availability_df)
        st.plotly_chart(fig, use_container_width=True)
    
    elif st.session_state.slide == 3:  # Strategic Implications
        st.markdown('<h2 class="slide-header">Strategic Implications</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            fig = create_occupancy_heatmap(occupancy_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("## For Corporate Occupiers")
            st.markdown("""
            - Leverage negotiating power in weak-recovery markets like San Francisco
            - Consider expansion in Texas markets for cost-effective talent access
            - Implement hybrid location strategies balancing financial centers and emerging hubs
            """)
            
            st.markdown("## For Investors & Developers")
            st.markdown("""
            - Focus on Class A properties in strongly recovering markets
            - Consider repositioning strategies in weaker markets
            - Monitor unemployment as leading indicator for market performance
            """)
            
            st.markdown("## For Brokerage & Advisory")
            st.markdown("""
            - Develop market-specific advisory frameworks
            - Create tools to evaluate market recovery strength vs. talent access
            - Establish monitoring of key inflection points
            """)
    
    elif st.session_state.slide == 4:  # Conclusions
        st.markdown('<h2 class="slide-header">Conclusions & Next Steps</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("## Market-Specific Strategies Are Essential")
            st.markdown("The commercial real estate landscape has undergone fundamental transformation, requiring nuanced, market-specific strategies rather than national approaches.")
            
            st.markdown("## Texas Markets Present Strategic Opportunity")
            st.markdown("Strong recovery (67-74% of pre-pandemic levels), favorable economics, and positive momentum make Texas markets attractive for strategic investment.")
            
            st.markdown("## Recovery Patterns Signal Structural Changes")
            st.markdown("The divergent recovery patterns represent structural shifts in how organizations utilize office space across geographic areas rather than temporary fluctuations.")
            
            st.markdown("## Forward-Looking Research")
            st.markdown("""
            Future analysis will focus on:
            - Predictive modeling based on economic indicators
            - Examining impact of building amenities and ESG factors
            - More granular submarket analysis
            - Impact of hybrid work policies on long-term occupancy
            """)
        
        with col2:
            fig = create_sunburst(recovery_df)
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bottom navigation
    st.markdown("---")
    cols = st.columns([1, 1, 3, 1, 1])
    
    with cols[0]:
        if st.session_state.slide > 0:
            if st.button("⏮️ First", key="first_bottom"):
                st.session_state.slide = 0
                st.rerun()
    
    with cols[1]:
        if st.session_state.slide > 0:
            if st.button("◀️ Previous", key="prev_bottom"):
                st.session_state.slide -= 1
                st.rerun()
    
    with cols[2]:
        st.markdown(f"<h3 style='text-align: center;'>Slide {st.session_state.slide + 1}/{len(slides)}</h3>", unsafe_allow_html=True)
    
    with cols[3]:
        if st.session_state.slide < len(slides) - 1:
            if st.button("Next ▶️", key="next_bottom"):
                st.session_state.slide += 1
                st.rerun()
    
    with cols[4]:
        if st.session_state.slide < len(slides) - 1:
            if st.button("Last ⏭️", key="last_bottom"):
                st.session_state.slide = len(slides) - 1
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("**Commercial Real Estate Analysis** | Data-Driven Insights for Strategic Decision Making")

if __name__ == "__main__":
    main() 