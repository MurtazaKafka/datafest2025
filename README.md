# Commercial Real Estate Interactive Visualizations

This project provides sophisticated, interactive visualizations of commercial real estate trends across major US markets, focusing on COVID-19 recovery patterns, office occupancy, and market dynamics.

## Interactive Visualizations

Eight dynamic, interactive visualizations have been created to showcase different aspects of the commercial real estate data:

### 1. Recovery Comparison Chart
**File**: `plots/recovery_comparison_interactive.html`

This visualization compares how different markets have recovered from their pandemic lows compared to pre-pandemic baselines. It shows both the pandemic drop and current recovery as percentages of the Q1 2020 baseline.

### 2. Occupancy Trends Time Series
**File**: `plots/occupancy_trends_interactive.html`

An interactive time series showing occupancy trends for all markets from 2020-2024. Features include:
- Range slider to zoom in on specific time periods
- Toggle markets on/off by clicking the legend
- Hover for detailed data points
- Annotations for key events (COVID outbreak, vaccine rollout, return-to-office policies)

### 3. Market Occupancy Heatmap
**File**: `plots/occupancy_heatmap_interactive.html`

A color-coded heatmap showing occupancy rates across all markets and time periods, providing an at-a-glance view of patterns and outliers.

### 4. Market Comparison Tool
**File**: `plots/market_comparison_sf_austin.html`

A direct comparison between San Francisco and Austin (representing tech hubs with different recovery patterns), with dual y-axes to easily compare their occupancy trends despite different scales.

### 5. 3D Recovery Visualization
**File**: `plots/recovery_3d_visualization.html`

A 3D scatter plot showing recovery percentages mapped to market geographic locations. The visualization can be rotated, zoomed, and explored from different angles.

### 6. Animated Occupancy Time Series
**File**: `plots/animated_occupancy.html`

An animated visualization showing how occupancy changed quarter by quarter across all markets. Use the play button to watch the animation unfold.

### 7. Tech Hubs Analysis
**File**: `plots/tech_hubs_analysis.html`

A multi-panel visualization showing availability and rent trends for key tech hub markets (San Francisco, South Bay, Austin), with dual y-axes to explore the relationship between space availability and rental rates.

### 8. Recovery Sunburst Chart
**File**: `plots/recovery_sunburst.html`

A hierarchical visualization that categorizes markets by type (Tech Hubs, Financial Centers, etc.) and shows their recovery percentages, allowing exploration of patterns among similar market types.

## How to View the Visualizations

1. The visualizations are HTML files in the `plots` directory.
2. Open any of these HTML files in a modern web browser (Chrome, Firefox, Edge, or Safari).
3. No internet connection is required as all visualization code is embedded in the HTML files.

## Key Findings

The interactive visualizations reveal several important trends:

1. **Tech-Driven Markets Show Resilience**: Austin (73.6% recovery) and Dallas/Ft Worth (68.5% recovery) have recovered most strongly compared to pre-pandemic baselines.

2. **Southern/Central Markets Outperforming Coastal Markets**: The strongest recovery is seen in Texas markets (Austin, Dallas/Ft Worth, Houston) with recovery rates between 67-74% of pre-pandemic levels.

3. **Coastal Tech Hubs Lagging**: San Francisco (57.7% recovery) and South Bay/San Jose (53% recovery) are showing weaker recovery patterns.

4. **Market-Specific Strategies Required**: The data suggests different optimal timing for lease negotiations across markets.

## Visualization Types and Features

These visualizations utilize advanced features of the Plotly library:
- Interactive zooming and panning
- Hover information for detailed data points
- Animated transitions to show change over time
- 3D visualizations to add an extra dimension to the data
- Dual-axis charts to show related but differently-scaled metrics
- Time series with range selectors and sliders
- Multi-panel coordinated views

## Regenerating the Visualizations

To regenerate the visualizations:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the presentation script:
   ```
   streamlit run cre_presentation.py
   ```

This will recreate all the interactive HTML files in the `plots` directory. 
