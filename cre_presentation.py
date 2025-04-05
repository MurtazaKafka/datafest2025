import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import time

# Page configuration
st.set_page_config(
    page_title="CRE Recovery Analysis",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for presentation aesthetics
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Slide container */
    .slide-container {
        background-color: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
        animation: fadeIn 1s ease-in-out;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Headers */
    .slide-title {
        color: #1E3A8A;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 20px;
        border-bottom: 3px solid #10B981;
        padding-bottom: 10px;
    }
    
    .slide-subtitle {
        color: #3730A3;
        font-size: 24px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    
    /* Content boxes */
    .insight-box {
        background-color: #f8f9fa;
        border-left: 5px solid #1E3A8A;
        padding: 20px;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    .example-box {
        background-color: #e7f5ff;
        border-left: 5px solid #10B981;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
    }
    
    /* Navigation buttons */
    .nav-btn {
        background-color: #1E3A8A;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .nav-btn:hover {
        background-color: #10B981;
    }
    
    /* Progress indicator */
    .progress-indicator {
        height: 8px;
        background-color: #e9ecef;
        border-radius: 4px;
        margin: 15px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background-color: #1E3A8A;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    /* Highlight text */
    .highlight {
        color: #1E3A8A;
        font-weight: bold;
    }
    
    /* Key metrics */
    .metric-container {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin: 10px 0;
        text-align: center;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #1E3A8A;
    }
    
    .metric-label {
        font-size: 14px;
        color: #6c757d;
    }
    
    /* Lists */
    ul.styled-list {
        list-style-type: none;
        padding-left: 0;
    }
    
    ul.styled-list li {
        position: relative;
        padding-left: 25px;
        margin-bottom: 12px;
        line-height: 1.6;
    }
    
    ul.styled-list li:before {
        content: '→';
        position: absolute;
        left: 0;
        color: #10B981;
        font-weight: bold;
    }
    
    /* Footer */
    .footer {
        color: #6c757d;
        font-size: 12px;
        text-align: center;
        margin-top: 30px;
        border-top: 1px solid #dee2e6;
        padding-top: 15px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# Data preparation functions
@st.cache_data
def load_sample_data():
    # Recovery rates data
    recovery_data = {
        'Market': ['Austin', 'Dallas/Ft Worth', 'Houston', 'Chicago', 'Manhattan', 'Los Angeles', 'San Francisco', 'South Bay/San Jose', 'Washington D.C.', 'Philadelphia'],
        'Recovery_Rate': [73.6, 70.2, 67.4, 65.8, 64.8, 62.3, 57.7, 53.0, 61.8, 59.5],
        'Region': ['Texas', 'Texas', 'Texas', 'Midwest', 'East', 'West', 'West', 'West', 'East', 'East']
    }
    
    # Corporate relocation data
    relocation_data = {
        'Company': ['Tesla', 'Oracle', 'HP Enterprise', 'Charles Schwab', 'CBRE Group', 'Digital Realty'],
        'Origin': ['Palo Alto, CA', 'Redwood City, CA', 'San Jose, CA', 'San Francisco, CA', 'Los Angeles, CA', 'San Francisco, CA'],
        'Destination': ['Austin, TX', 'Austin, TX', 'Houston, TX', 'Dallas/Ft Worth, TX', 'Dallas, TX', 'Austin, TX'],
        'Year': [2020, 2020, 2022, 2019, 2020, 2021],
        'Jobs': [5000, 2500, 1200, 2500, 700, 500]
    }
    
    # Policy data
    policy_data = {
        'Market': ['Austin', 'Dallas', 'Manhattan', 'San Francisco', 'Chicago', 'Los Angeles'],
        'Return_Date': ['2021-07', '2021-08', '2022-02', '2022-03', '2021-10', '2022-01'],
        'Office_Days': [3.5, 3.2, 2.1, 1.8, 2.9, 2.0],
        'Current_Occupancy': [73.6, 70.2, 64.8, 57.7, 65.8, 62.3]
    }
    
    # Tech vs Financial sector data
    sector_data = {
        'Market': ['Austin', 'San Francisco', 'Manhattan', 'Dallas', 'Chicago', 'Los Angeles'],
        'Tech_Recovery': [77.5, 56.2, 59.8, 72.1, 63.5, 61.9],
        'Financial_Recovery': [69.8, 60.3, 68.5, 67.9, 68.4, 62.8],
        'Hybrid_Policy': ['Moderate', 'Extensive', 'Limited', 'Moderate', 'Limited', 'Extensive']
    }
    
    # Return all data
    return pd.DataFrame(recovery_data), pd.DataFrame(relocation_data), pd.DataFrame(policy_data), pd.DataFrame(sector_data)

# Load data
recovery_df, relocation_df, policy_df, sector_df = load_sample_data()

# Create visualizations
def create_recovery_chart(recovery_df):
    # Sort by recovery rate
    df = recovery_df.sort_values('Recovery_Rate', ascending=False)
    
    # Create color mapping for regions
    color_map = {'Texas': '#10B981', 'East': '#3730A3', 'West': '#DB2777', 'Midwest': '#F59E0B'}
    
    # Create the bar chart
    fig = px.bar(
        df, 
        x='Market', 
        y='Recovery_Rate',
        color='Region',
        color_discrete_map=color_map,
        labels={'Recovery_Rate': 'Recovery Rate (% of Pre-Pandemic)', 'Market': ''},
        title='Market Recovery Rates Comparison',
        text=df['Recovery_Rate'].apply(lambda x: f'{x:.1f}%')
    )
    
    # Add horizontal line for pre-pandemic baseline
    fig.add_shape(
        type="line",
        x0=-0.5, x1=len(df)-0.5,
        y0=100, y1=100,
        line=dict(color="red", width=2, dash="dash")
    )
    
    # Add annotation for baseline
    fig.add_annotation(
        x=len(df)-1, y=105,
        text="Pre-Pandemic Baseline (100%)",
        showarrow=False,
        font=dict(color="red")
    )
    
    # Improve layout
    fig.update_layout(
        height=450,
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(categoryorder='total descending'),
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Improve bar appearance
    fig.update_traces(
        marker_line_width=0,
        textposition='outside'
    )
    
    return fig

def create_relocation_chart(relocation_df):
    # Categorize by destination city
    fig = px.bar(
        relocation_df,
        x='Company',
        y='Jobs',
        color='Destination',
        color_discrete_sequence=px.colors.qualitative.Bold,
        labels={'Jobs': 'Jobs Relocated', 'Company': ''},
        title='Major Corporate Relocations to Texas (2019-2022)'
    )
    
    # Add total jobs number above each bar
    fig.update_traces(
        text=relocation_df['Jobs'],
        textposition='outside'
    )
    
    # Improve layout
    fig.update_layout(
        height=450,
        template='plotly_white',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        bargap=0.35,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

def create_tech_financial_comparison(sector_df):
    # Create bubble chart
    fig = px.scatter(
        sector_df,
        x='Tech_Recovery',
        y='Financial_Recovery',
        size=[50, 40, 45, 35, 30, 35],  # Size based on importance
        color='Market',
        hover_name='Market',
        text='Market',
        labels={
            'Tech_Recovery': 'Tech Sector Recovery (%)',
            'Financial_Recovery': 'Financial Sector Recovery (%)'
        },
        title='Tech vs. Financial Sector Recovery by Market'
    )
    
    # Add diagonal reference line (x=y)
    fig.add_shape(
        type="line",
        x0=50, x1=80,
        y0=50, y1=80,
        line=dict(color="gray", width=1, dash="dot")
    )
    
    # Add tech dominance and financial dominance regions
    fig.add_shape(
        type="rect",
        x0=50, x1=80,
        y0=50, y1=55,
        fillcolor="rgba(16, 185, 129, 0.1)",
        line=dict(width=0),
        layer="below"
    )
    
    fig.add_shape(
        type="rect",
        x0=50, x1=55,
        y0=55, y1=80,
        fillcolor="rgba(55, 48, 163, 0.1)",
        line=dict(width=0),
        layer="below"
    )
    
    # Add annotations
    fig.add_annotation(
        x=70, y=52.5,
        text="Tech-Driven Recovery",
        showarrow=False,
        font=dict(color="#10B981", size=12)
    )
    
    fig.add_annotation(
        x=52.5, y=70,
        text="Financial-Driven Recovery",
        showarrow=False,
        textangle=-90,
        font=dict(color="#3730A3", size=12)
    )
    
    # Improve layout
    fig.update_layout(
        height=500,
        template='plotly_white',
        xaxis=dict(range=[50, 80]),
        yaxis=dict(range=[50, 80]),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Improve text positioning
    fig.update_traces(
        textposition='top center'
    )
    
    return fig

def create_strategic_recommendations():
    # Create a multi-panel visualization for recommendations
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Corporate Occupiers", "Investors & Developers", "Advisory Firms"),
        specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]]
    )
    
    # Data for Corporate Occupiers pie chart
    corporate_labels = ["Leverage in SF", "Expand in Texas", "Hybrid Strategy"]
    corporate_values = [35, 45, 20]
    corporate_colors = ['#DB2777', '#10B981', '#F59E0B']
    
    # Data for Investors pie chart
    investor_labels = ["Class A in Strong Markets", "Reposition in Weak Markets", "Residential Conversion"]
    investor_values = [50, 20, 30]
    investor_colors = ['#10B981', '#F59E0B', '#3730A3']
    
    # Data for Advisory pie chart
    advisory_labels = ["Market-Specific Frameworks", "Economic Indicator Tracking", "Client-Specific Strategies"]
    advisory_values = [40, 25, 35]
    advisory_colors = ['#3730A3', '#F59E0B', '#10B981']
    
    # Add pie charts
    fig.add_trace(
        go.Pie(
            labels=corporate_labels,
            values=corporate_values,
            marker=dict(colors=corporate_colors),
            textinfo='label+percent',
            insidetextorientation='radial',
            pull=[0.1, 0, 0],
            hole=0.3
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Pie(
            labels=investor_labels,
            values=investor_values,
            marker=dict(colors=investor_colors),
            textinfo='label+percent',
            insidetextorientation='radial',
            pull=[0, 0, 0.1],
            hole=0.3
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Pie(
            labels=advisory_labels,
            values=advisory_values,
            marker=dict(colors=advisory_colors),
            textinfo='label+percent',
            insidetextorientation='radial',
            pull=[0.1, 0, 0],
            hole=0.3
        ),
        row=1, col=3
    )
    
    # Update layout
    fig.update_layout(
        title="Strategic Recommendations by Stakeholder Type",
        height=450,
        template='plotly_white',
        margin=dict(l=20, r=20, t=80, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5)
    )
    
    # Update subplot titles
    fig.update_annotations(font_size=14, font_color='#1E3A8A')
    
    return fig

def create_recovery_map():
    # Create dataframe with coordinates
    map_data = pd.DataFrame({
        'Market': ['Austin', 'Dallas/Ft Worth', 'Houston', 'Chicago', 'Manhattan', 'Los Angeles', 
                  'San Francisco', 'Silicon Valley', 'Washington D.C.', 'Philadelphia'],
        'Recovery': [73.6, 70.2, 67.4, 65.8, 64.8, 62.3, 57.7, 53.0, 61.8, 59.5],
        'lat': [30.2672, 32.7767, 29.7604, 41.8781, 40.7831, 34.0522, 
                37.7749, 37.3382, 38.9072, 39.9526],
        'lon': [-97.7431, -96.7970, -95.3698, -87.6298, -73.9712, -118.2437,
                -122.4194, -121.8863, -77.0369, -75.1652]
    })
    
    # Create chloropleth map
    fig = px.scatter_mapbox(
        map_data,
        lat='lat',
        lon='lon',
        color='Recovery',
        size='Recovery',
        color_continuous_scale='Viridis',
        size_max=25,
        zoom=3,
        mapbox_style='carto-positron',
        hover_name='Market',
        hover_data={'Recovery': True, 'lat': False, 'lon': False},
        labels={'Recovery': 'Recovery Rate (%)'},
        title='Geographic Distribution of Market Recovery Rates'
    )
    
    # Improve layout
    fig.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(title='Recovery %')
    )
    
    return fig

# Create a function for each slide
def slide_1():
    st.markdown('<div class="slide-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Commercial Real Estate Recovery Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="slide-subtitle">Post-Pandemic Patterns & Strategic Insights</h2>', unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('''
        <div class="metric-container">
            <div class="metric-value">73.6%</div>
            <div class="metric-label">Austin's Recovery Rate<br>(Highest)</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="metric-container">
            <div class="metric-value">53.0%</div>
            <div class="metric-label">Silicon Valley's Recovery Rate<br>(Lowest)</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="metric-container">
            <div class="metric-value">67-74%</div>
            <div class="metric-label">Texas Markets<br>Recovery Range</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div class="metric-container">
            <div class="metric-value">20.6%</div>
            <div class="metric-label">Recovery Gap<br>(Highest vs Lowest)</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Main visualization
    fig = create_recovery_map()
    st.plotly_chart(fig, use_container_width=True)
    
    # Key findings
    st.markdown('<h3 class="slide-subtitle">Key Findings</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="insight-box">
            <h4>Regional Divergence</h4>
            <ul class="styled-list">
                <li>Southern/Central markets consistently outperforming coastal markets</li>
                <li>Texas markets leading recovery (67-74% of pre-pandemic levels)</li>
                <li>Clear east-west divergence in recovery patterns</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="insight-box">
            <h4>Tech Hub Dichotomy</h4>
            <ul class="styled-list">
                <li>Austin (73.6%) vs San Francisco (57.7%) and Silicon Valley (53.0%)</li>
                <li>Financial centers show moderate but steady recovery (64-66%)</li>
                <li>Distinct three-phase recovery pattern across all markets</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

def slide_2():
    st.markdown('<div class="slide-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Why Texas Markets Lead the Recovery</h1>', unsafe_allow_html=True)
    
    # Main chart
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig = create_recovery_chart(recovery_df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('''
        <h3>Business-Friendly Environment</h3>
        <ul class="styled-list">
            <li><span class="highlight">No state income tax</span> vs California's 13.3% and New York's 10.9%</li>
            <li><span class="highlight">Lower housing costs</span> - 59% lower in Austin vs San Francisco</li>
            <li><span class="highlight">Fewer regulatory restrictions</span> on development and operations</li>
            <li><span class="highlight">Pro-business government</span> with economic incentives</li>
        </ul>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Corporate relocations
    st.markdown('<h3 class="slide-subtitle">Corporate Migration Driving Recovery</h3>', unsafe_allow_html=True)
    
    fig = create_relocation_chart(relocation_df)
    st.plotly_chart(fig, use_container_width=True)
    
    # Example boxes
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div class="example-box">
            <h4>Tesla's Cascade Effect</h4>
            <p>Tesla's Austin gigafactory announcement (July 2020) triggered:</p>
            <ul>
                <li>32% increase in office leasing activity within 12 months</li>
                <li>350,000 sq ft of new leases from Tesla's ecosystem</li>
                <li>4.2 percentage point contribution to Austin's recovery</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="example-box">
            <h4>Earlier Return-to-Office Policies</h4>
            <p>Texas employers implemented stricter in-office requirements:</p>
            <ul>
                <li>Return policies began Q3 2021 (2-3 quarters earlier than coastal)</li>
                <li>Texas average: 3-4 days in-office vs 1-2 days for coastal tech</li>
                <li>JPMorgan Chase Dallas: 68% occupancy by Q4 2021 vs 49% in Manhattan</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def slide_3():
    st.markdown('<div class="slide-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Tech Hub Dichotomy & Financial Center Resilience</h1>', unsafe_allow_html=True)
    
    # Tech vs Financial
    fig = create_tech_financial_comparison(sector_df)
    st.plotly_chart(fig, use_container_width=True)
    
    # Explanations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('''
        <h3>Why Tech Markets Diverge</h3>
        <ul class="styled-list">
            <li><span class="highlight">Company Profile Differences</span> - Austin has more hardware/semiconductor companies requiring physical presence</li>
            <li><span class="highlight">Remote Work Readiness</span> - SF/Silicon Valley had stronger remote infrastructure pre-pandemic</li>
            <li><span class="highlight">Space Utilization</span> - Bay Area tech reduced sq ft/employee by 31% vs 14% in Austin</li>
        </ul>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="example-box" style="margin-top: 20px;">
            <h4>Salesforce vs. Dell Example</h4>
            <ul>
                <li>Salesforce (SF) implemented "Work From Anywhere" in Feb 2021</li>
                <li>Subleased 350,000 sq ft of office space</li>
                <li>Dell (Austin) required 3 days in-office by Sept 2021</li>
                <li>Maintained 90% of pre-pandemic office footprint</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="insight-box">', unsafe_allow_html=True)
        st.markdown('''
        <h3>Financial Center Resilience</h3>
        <ul class="styled-list">
            <li><span class="highlight">Regulatory Requirements</span> - Data security and client privacy necessitate in-person work</li>
            <li><span class="highlight">Client Relationship Focus</span> - High-touch services benefit from in-person meetings</li>
            <li><span class="highlight">Specialized Infrastructure</span> - Trading systems require on-site presence</li>
            <li><span class="highlight">Traditional Culture</span> - Emphasis on mentorship and supervision</li>
        </ul>
        ''', unsafe_allow_html=True)
        
        st.markdown('''
        <div class="example-box" style="margin-top: 20px;">
            <h4>Goldman Sachs Example</h4>
            <ul>
                <li>CEO called remote work an "aberration" in Feb 2021</li>
                <li>Required full 5-day return to Manhattan HQ by June 2021</li>
                <li>Maintained 2.1M sq ft footprint while tech firms reduced space</li>
                <li>Expanded by 150,000 sq ft in Q2 2022 for growth</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def slide_4():
    st.markdown('<div class="slide-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="slide-title">Strategic Recommendations & Opportunities</h1>', unsafe_allow_html=True)
    
    # Strategic recommendations visualization
    fig = create_strategic_recommendations()
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed recommendations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div class="example-box">
            <h4>For Corporate Occupiers</h4>
            <ul class="styled-list">
                <li><span class="highlight">Leverage in San Francisco</span>: 24.1% availability creates tenant advantage (Dropbox secured 32% discount on 15-year lease)</li>
                <li><span class="highlight">Consider Texas Markets</span>: Indeed expanded Austin HQ by 183,000 sq ft while reducing SF footprint by 44%</li>
                <li><span class="highlight">Negotiate Flexibility</span>: Snap Inc. secured quarterly termination options for 30% of leased space</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="example-box">
            <h4>For Investors & Developers</h4>
            <ul class="styled-list">
                <li><span class="highlight">Focus on Flight-to-Quality</span>: Austin's Domain district Class A buildings achieving $48/sq ft vs $32/sq ft for Class B</li>
                <li><span class="highlight">Reconsider Timelines</span>: Boston Properties delayed Salesforce Tower expansion by 36+ months</li>
                <li><span class="highlight">Conversion Opportunities</span>: Manhattan has 7.2M sq ft approved for residential conversion</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="example-box">
            <h4>For Advisory Firms</h4>
            <ul class="styled-list">
                <li><span class="highlight">Market-Specific Frameworks</span>: Create tailored advice addressing divergent recovery patterns</li>
                <li><span class="highlight">Track Leading Indicators</span>: Monitor unemployment rates as predictors of office demand</li>
                <li><span class="highlight">Sector-Specific Analysis</span>: Develop tech vs financial sector strategies based on location</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    # Concluding statement
    st.markdown('''
    <div class="insight-box" style="margin-top: 20px;">
        <h3>Key Takeaway: Market-Specific Strategies Are Essential</h3>
        <p>The commercial real estate landscape has undergone fundamental transformation, with recovery patterns reflecting structural shifts rather than temporary fluctuations. Success now requires nuanced, market-specific strategies rather than national approaches. Organizations must consider both the cyclical timing advantages in markets like San Francisco and the structural advantages of markets like Austin when making long-term real estate decisions.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Navigation setup
def main():
    # Initialize session state for tracking current slide
    if 'slide' not in st.session_state:
        st.session_state.slide = 0
    
    # Create progress bar
    progress = st.session_state.slide / 3  # 4 slides (0-indexed)
    st.markdown(f'<div class="progress-indicator"><div class="progress-bar" style="width: {progress * 100}%;"></div></div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])
    
    # Button colors based on current slide
    slide1_style = "background-color: #10B981;" if st.session_state.slide == 0 else ""
    slide2_style = "background-color: #10B981;" if st.session_state.slide == 1 else ""
    slide3_style = "background-color: #10B981;" if st.session_state.slide == 2 else ""
    slide4_style = "background-color: #10B981;" if st.session_state.slide == 3 else ""
    
    with col1:
        if st.button("◀ Prev", disabled=(st.session_state.slide == 0), key="prev_top"):
            st.session_state.slide = max(0, st.session_state.slide - 1)
            st.rerun()
    
    with col2:
        if st.button("Slide 1", key="slide1_btn", help="Overview"):
            st.session_state.slide = 0
            st.rerun()
    
    with col3:
        if st.button("Slide 2", key="slide2_btn", help="Texas Recovery"):
            st.session_state.slide = 1
            st.rerun()
    
    with col4:
        if st.button("Slide 3", key="slide3_btn", help="Tech & Financial"):
            st.session_state.slide = 2
            st.rerun()
    
    with col5:
        if st.button("Slide 4", key="slide4_btn", help="Recommendations"):
            st.session_state.slide = 3
            st.rerun()
    
    with col6:
        if st.button("Next ▶", disabled=(st.session_state.slide == 3), key="next_top"):
            st.session_state.slide = min(3, st.session_state.slide + 1)
            st.rerun()
    
    # Display current slide
    slides = [slide_1, slide_2, slide_3, slide_4]
    current_slide = slides[st.session_state.slide]
    current_slide()
    
    # Bottom navigation
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        if st.button("◀ Previous", disabled=(st.session_state.slide == 0), key="prev_bottom"):
            st.session_state.slide = max(0, st.session_state.slide - 1)
            st.rerun()
    
    with col2:
        st.markdown(f'<div style="text-align: center; font-size: 18px;">Slide {st.session_state.slide + 1}/4</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("Next ▶", disabled=(st.session_state.slide == 3), key="next_bottom"):
            st.session_state.slide = min(3, st.session_state.slide + 1)
            st.rerun()
    
    # Footer
    st.markdown('<div class="footer">Commercial Real Estate Recovery Analysis | Data-Driven Insights for Strategic Decision Making</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main() 