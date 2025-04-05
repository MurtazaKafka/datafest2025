import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# Set default theme
pio.templates.default = "plotly_white"

# Load data
print("Loading data...")
occupancy_df = pd.read_csv('Major Market Occupancy Data-revised.csv')
availability_df = pd.read_csv('Price and Availability Data.csv')
unemployment_df = pd.read_csv('Unemployment.csv')

# Create period column for easier plotting
occupancy_df['period'] = occupancy_df['year'].astype(str) + "-" + occupancy_df['quarter']

# Add market coordinates (for potential map visualizations)
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

# Add coordinates to the dataframe
occupancy_df['lat'] = occupancy_df['market'].map(lambda x: market_coordinates.get(x, {}).get('lat'))
occupancy_df['lon'] = occupancy_df['market'].map(lambda x: market_coordinates.get(x, {}).get('lon'))

print("Processing recovery analysis...")
# Create recovery analysis
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

# Print some basic findings
print("\nMarket Recovery Analysis:")
print(f"Best recovering market: {recovery_df['market'].iloc[0]} ({recovery_df['recovery_percentage'].iloc[0]:.1f}%)")
print(f"Worst recovering market: {recovery_df['market'].iloc[-1]} ({recovery_df['recovery_percentage'].iloc[-1]:.1f}%)")
print(f"Average recovery across markets: {recovery_df['recovery_percentage'].mean():.1f}%")

# Create visualizations
print("\nGenerating visualizations...")

# 1. Interactive Recovery Comparison Chart
fig1 = go.Figure()

# Add pandemic low bars
fig1.add_trace(go.Bar(
    x=recovery_df['market'],
    y=recovery_df['drop_percentage'],
    name='Pandemic Low (% of Baseline)',
    marker_color='rgba(219, 39, 119, 0.7)',
    hovertemplate='<b>%{x}</b><br>Pandemic Low: %{y:.1f}% of baseline<extra></extra>'
))

# Add current recovery bars
fig1.add_trace(go.Bar(
    x=recovery_df['market'],
    y=recovery_df['recovery_percentage'],
    name='Current (% of Baseline)',
    marker_color='rgba(16, 185, 129, 0.7)',
    hovertemplate='<b>%{x}</b><br>Current: %{y:.1f}% of baseline<extra></extra>'
))

# Add a line for the baseline (100%)
fig1.add_shape(
    type="line",
    x0=-0.5,
    y0=100,
    x1=len(recovery_df) - 0.5,
    y1=100,
    line=dict(color="red", width=2, dash="dash")
)

# Add annotation for baseline
fig1.add_annotation(
    x=len(recovery_df) - 1,
    y=105,
    text="Pre-pandemic Baseline (Q1 2020)",
    showarrow=False,
    font=dict(size=12, color="red")
)

# Update layout
fig1.update_layout(
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
    height=600
)

# Save the figure
fig1.write_html("plots/recovery_comparison_interactive.html")
print("Created recovery comparison chart")

# 2. Interactive Time Series for All Markets
fig2 = go.Figure()

# Add traces for each market
for market in occupancy_df['market'].unique():
    market_data = occupancy_df[occupancy_df['market'] == market]
    fig2.add_trace(go.Scatter(
        x=market_data['period'],
        y=market_data['avg_occupancy_proportion'],
        mode='lines+markers',
        name=market,
        hovertemplate='<b>%{x}</b><br>%{y:.3f}<extra></extra>'
    ))

# Add key event annotations
fig2.add_vline(x="2020-Q1", line_dash="dash", line_color="red", opacity=0.7)
fig2.add_annotation(x="2020-Q1", y=1.0, text="COVID-19 Outbreak", showarrow=False, yshift=10)

fig2.add_vline(x="2021-Q2", line_dash="dash", line_color="green", opacity=0.7)
fig2.add_annotation(x="2021-Q2", y=0.95, text="Vaccine Rollout", showarrow=False, yshift=10)

fig2.add_vline(x="2022-Q1", line_dash="dash", line_color="orange", opacity=0.7)
fig2.add_annotation(x="2022-Q1", y=0.9, text="Return to Office Policies Begin", showarrow=False, yshift=10)

# Update layout
fig2.update_layout(
    title="Office Occupancy Trends By Market (2020-2024)",
    xaxis_title="Time Period",
    yaxis_title="Average Occupancy Proportion",
    height=700,
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# Add range slider and buttons
fig2.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1Y", step="year", stepmode="backward"),
                dict(count=2, label="2Y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="category"
    )
)

# Save the figure
fig2.write_html("plots/occupancy_trends_interactive.html")
print("Created interactive time series chart")

# 3. Market Heatmap
pivot_df = occupancy_df.pivot(index='market', columns='period', values='avg_occupancy_proportion')

fig3 = px.imshow(
    pivot_df,
    labels=dict(x="Time Period", y="Market", color="Occupancy Rate"),
    x=pivot_df.columns,
    y=pivot_df.index,
    color_continuous_scale="Viridis",
    aspect="auto",
    zmin=0,
    zmax=1
)

fig3.update_layout(
    title="Occupancy Rates by Market and Period",
    height=600,
    coloraxis_colorbar=dict(
        title="Occupancy Rate",
        thicknessmode="pixels", thickness=20,
        lenmode="pixels", len=300
    )
)

# Customize hover information
fig3.update_traces(
    hovertemplate="<b>Market:</b> %{y}<br><b>Period:</b> %{x}<br><b>Occupancy:</b> %{z:.3f}<extra></extra>"
)

# Save the figure
fig3.write_html("plots/occupancy_heatmap_interactive.html")
print("Created interactive heatmap")

# 4. Market Comparison Tool
def create_market_comparison(market1, market2):
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
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=600,
        hovermode="x unified"
    )
    
    fig.update_xaxes(title_text="Time Period")
    fig.update_yaxes(title_text=f"{market1} Occupancy", secondary_y=False)
    fig.update_yaxes(title_text=f"{market2} Occupancy", secondary_y=True)
    
    return fig

# Create comparison between San Francisco and Austin (tech hubs with different recovery patterns)
comparison_fig = create_market_comparison("San Francisco", "Austin")
comparison_fig.write_html("plots/market_comparison_sf_austin.html")
print("Created market comparison chart")

# 5. Create a 3D visualization of recovery rates
fig5 = go.Figure(data=[go.Scatter3d(
    x=[coord.get('lon', 0) for coord in [market_coordinates.get(m, {}) for m in recovery_df['market']]],
    y=[coord.get('lat', 0) for coord in [market_coordinates.get(m, {}) for m in recovery_df['market']]],
    z=recovery_df['recovery_percentage'],
    mode='markers',
    marker=dict(
        size=recovery_df['recovery_percentage']/3,
        color=recovery_df['recovery_percentage'],
        colorscale='Viridis',
        opacity=0.8,
        colorbar=dict(title="Recovery %"),
    ),
    text=recovery_df['market'],
    hovertemplate=
    '<b>%{text}</b><br>' +
    'Recovery: %{z:.1f}%<br>' +
    '<extra></extra>'
)])

fig5.update_layout(
    title='3D Visualization of Market Recovery Rates',
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Recovery Percentage',
        aspectmode='manual',
        aspectratio=dict(x=2, y=1, z=1)
    ),
    height=700
)

fig5.write_html("plots/recovery_3d_visualization.html")
print("Created 3D recovery visualization")

# 6. Animated Time Series
fig6 = px.scatter(
    occupancy_df,
    x="period",
    y="avg_occupancy_proportion",
    color="market",
    size="avg_occupancy_proportion",
    hover_name="market",
    animation_frame="quarter",
    animation_group="market",
    size_max=15,
    range_y=[0, 1],
    title="Animated Office Occupancy by Quarter"
)

fig6.update_layout(
    xaxis=dict(
        tickangle=45,
        title_text="Time Period"
    ),
    yaxis=dict(
        title_text="Average Occupancy Proportion"
    ),
    height=600
)

fig6.write_html("plots/animated_occupancy.html")
print("Created animated time series")

# 7. Availability vs Rent Trends for Tech Hubs
tech_hubs = ['San Francisco', 'South Bay', 'Austin']

# Create subplots - one row per market
fig7 = make_subplots(
    rows=len(tech_hubs),
    cols=1,
    subplot_titles=[f"{market} Availability & Rent Trends" for market in tech_hubs],
    shared_xaxes=True,
    specs=[[{"secondary_y": True}] for _ in range(len(tech_hubs))],
    vertical_spacing=0.1
)

for i, market in enumerate(tech_hubs):
    try:
        # Get availability data for Class A properties
        market_data = availability_df[(availability_df['market'] == market) & 
                                    (availability_df['internal_class'] == 'A')].copy()
        market_data['period'] = market_data['year'].astype(str) + "-" + market_data['quarter']
        market_data = market_data.sort_values('period')
        
        # Plot availability on primary y-axis
        fig7.add_trace(
            go.Scatter(
                x=market_data['period'],
                y=market_data['availability_proportion'],
                name=f"{market} Availability",
                line=dict(color='blue'),
                showlegend=i==0  # only show legend for first trace
            ),
            row=i+1, col=1, secondary_y=False
        )
        
        # Plot rent on secondary y-axis
        fig7.add_trace(
            go.Scatter(
                x=market_data['period'],
                y=market_data['internal_class_rent'],
                name=f"{market} Rent",
                line=dict(color='red'),
                showlegend=i==0  # only show legend for first trace
            ),
            row=i+1, col=1, secondary_y=True
        )
    except Exception as e:
        print(f"Error adding {market} to plot: {e}")

# Update layout
fig7.update_layout(
    height=900,
    title_text="Tech Hub Markets: Availability vs. Rent (Class A Properties)",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    )
)

# Update y-axis titles
for i, market in enumerate(tech_hubs):
    fig7.update_yaxes(title_text="Availability", row=i+1, col=1, secondary_y=False)
    fig7.update_yaxes(title_text="Rent ($/sq ft)", row=i+1, col=1, secondary_y=True)

# Update x-axis titles for the bottom subplot only
fig7.update_xaxes(title_text="Time Period", row=len(tech_hubs), col=1)

fig7.write_html("plots/tech_hubs_analysis.html")
print("Created tech hubs analysis chart")

# 8. Sunburst Chart of Recovery by Market Category
# Define market categories
market_categories = {
    'Tech Hubs': ['San Francisco', 'South Bay/San Jose', 'Austin'],
    'Financial Centers': ['Manhattan', 'Chicago'],
    'Regional Centers': ['Dallas/Ft Worth', 'Houston', 'Philadelphia'],
    'Government Centers': ['Washington D.C.'],
    'Creative Centers': ['Los Angeles']
}

# Create a dataframe for the sunburst chart
sunburst_data = []
for category, markets in market_categories.items():
    for market in markets:
        if market in recovery_df['market'].values:
            market_recovery = recovery_df[recovery_df['market'] == market]['recovery_percentage'].values[0]
            sunburst_data.append({
                'Category': category,
                'Market': market,
                'Recovery': market_recovery
            })

sunburst_df = pd.DataFrame(sunburst_data)

# Create sunburst chart
fig8 = px.sunburst(
    sunburst_df,
    path=['Category', 'Market'],
    values='Recovery',
    color='Recovery',
    color_continuous_scale='RdYlGn',
    branchvalues='total',
    title='Market Recovery by Category',
    hover_data=['Recovery']
)

fig8.update_layout(height=700)
fig8.update_traces(
    hovertemplate='<b>%{label}</b><br>Recovery: %{color:.1f}%<extra></extra>'
)

fig8.write_html("plots/recovery_sunburst.html")
print("Created recovery sunburst chart")

print("\nAll interactive visualizations have been saved to the 'plots' directory.")
print("Open the HTML files in your browser to explore the interactive visualizations.") 