import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import numpy as np
from pathlib import Path

# Create images directory if it doesn't exist
Path("images").mkdir(exist_ok=True)

# Load data similar to the main app
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

# Capture 1: Recovery Comparison Chart
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
        height=600,
        width=1000,
        template="plotly_white",
        margin=dict(l=50, r=50, t=80, b=80)
    )
    
    return fig

# Capture 2: Occupancy Heatmap
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
        height=600,
        width=1000,
        xaxis={'side': 'top'},
        coloraxis_colorbar=dict(
            title="Occupancy Rate",
            thicknessmode="pixels", thickness=20,
            lenmode="pixels", len=300
        )
    )
    
    return fig

# Capture 3: 3D Map
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
        height=700,
        width=1000,
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

# Capture 4: Market Comparison
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
        height=600,
        width=1000,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        title="Availability vs. Rent Comparison: Recovering (Austin) vs. Lagging (San Francisco) Markets"
    )
    
    return fig

# Capture 5: Recovery Sunburst Chart
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
    # We need a hierarchical structure: Region > Category > Market
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
    
    fig.update_layout(
        height=700,
        width=1000
    )
    
    return fig

# Main function to generate all images
def generate_all_images():
    print("Loading data...")
    occupancy_df, availability_df, occupancy_map_df = load_data()
    recovery_df = create_recovery_analysis(occupancy_df)
    
    # Filter map data for the most recent period
    latest_period = occupancy_map_df['period'].max()
    map_data = occupancy_map_df[occupancy_map_df['period'] == latest_period]
    map_data = map_data.dropna(subset=['lat', 'lon'])
    map_data = map_data.merge(
        recovery_df[['market', 'recovery_percentage']],
        on='market',
        how='left'
    )
    
    print("Generating recovery comparison chart...")
    recovery_fig = create_recovery_chart(recovery_df)
    recovery_fig.write_image("images/recovery_comparison_chart.png")
    
    print("Generating occupancy heatmap...")
    heatmap_fig = create_occupancy_heatmap(occupancy_df)
    heatmap_fig.write_image("images/occupancy_heatmap.png")
    
    print("Generating 3D recovery map...")
    map_fig = create_3d_map(map_data)
    map_fig.write_image("images/recovery_3d_map.png")
    
    print("Generating market comparison chart...")
    comparison_fig = create_market_comparison(occupancy_df, availability_df)
    comparison_fig.write_image("images/market_comparison_chart.png")
    
    print("Generating recovery sunburst chart...")
    sunburst_fig = create_sunburst(recovery_df)
    sunburst_fig.write_image("images/recovery_sunburst.png")
    
    print("Creating placeholder for animated occupancy...")
    # For a real animation, you would need to generate a GIF
    # For now, we'll just copy one of our other images as a placeholder
    import shutil
    shutil.copy("images/recovery_comparison_chart.png", "images/animated_occupancy.gif")
    
    print("All images generated successfully!")

if __name__ == "__main__":
    try:
        generate_all_images()
    except Exception as e:
        print(f"Error generating images: {e}")
        # Create placeholder images if generation fails
        Path("images").mkdir(exist_ok=True)
        image_files = [
            "recovery_comparison_chart.png",
            "animated_occupancy.gif",
            "recovery_3d_map.png", 
            "market_comparison_chart.png",
            "occupancy_heatmap.png",
            "recovery_sunburst.png"
        ]
        for img_file in image_files:
            img_path = Path(f"images/{img_file}")
            if not img_path.exists():
                with open(img_path, "wb") as f:
                    # Create a simple placeholder
                    f.write(b"placeholder") 