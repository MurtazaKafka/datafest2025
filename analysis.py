#!/usr/bin/env python3

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

print("# Commercial Real Estate Market Analysis")
print("Analyzing commercial real estate trends from Savills dataset")

# Load occupancy data
print("\nLoading the occupancy data...")
occupancy_df = pd.read_csv('Major Market Occupancy Data-revised.csv')
print(f"Occupancy data shape: {occupancy_df.shape}")
print(occupancy_df.head())

# Load price and availability data
print("\nLoading the price and availability data...")
availability_df = pd.read_csv('Price and Availability Data.csv')
print(f"Price and availability data shape: {availability_df.shape}")
print(availability_df.head())

# Load unemployment data
print("\nLoading the unemployment data...")
unemployment_df = pd.read_csv('Unemployment.csv')
print(f"Unemployment data shape: {unemployment_df.shape}")
print(unemployment_df.head())

# Try to load a sample of the leases data (it's large, so we'll limit rows)
print("\nAttempting to load a sample of the leases data...")
try:
    leases_df = pd.read_csv('Leases.csv', nrows=10000)
    print(f"Leases data sample shape: {leases_df.shape}")
    print(leases_df.head())
except Exception as e:
    print(f"Error loading leases data: {e}")

# Create output directory for plots
import os
if not os.path.exists('plots'):
    os.makedirs('plots')

print("\n# Explore Occupancy Trends Before and After COVID")

# Create period column (year + quarter) for easier x-axis plotting
occupancy_df['period'] = occupancy_df['year'].astype(str) + "-" + occupancy_df['quarter']

# Plot occupancy trends over time for all markets
plt.figure(figsize=(14, 10))

# Get unique markets and periods for plotting
markets = occupancy_df['market'].unique()
periods = sorted(occupancy_df['period'].unique())

# Plot average occupancy for each market over time
for market in markets:
    market_data = occupancy_df[occupancy_df['market'] == market]
    plt.plot(market_data['period'], market_data['avg_occupancy_proportion'], label=market, marker='o')

plt.title('Average Office Occupancy by Market (2020-2024)', fontsize=16)
plt.xlabel('Time Period', fontsize=14)
plt.ylabel('Average Occupancy Proportion', fontsize=14)
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.grid(True)
plt.savefig('plots/occupancy_trends.png')
plt.close()

print("Generated occupancy trends plot")

# Create a heatmap of occupancy rates by market and time period
pivot_df = occupancy_df.pivot(index='market', columns='period', values='avg_occupancy_proportion')

plt.figure(figsize=(16, 10))
sns.heatmap(pivot_df, cmap='YlGnBu', annot=True, fmt='.2f', linewidths=.5)
plt.title('Office Occupancy Rates by Market and Period', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('plots/occupancy_heatmap.png')
plt.close()

print("Generated occupancy heatmap")

print("\n# Analyze Recovery Patterns Across Markets")

# Compute pre-pandemic baseline (Q1 2020), pandemic low, and current occupancy
baseline = occupancy_df[(occupancy_df['year'] == 2020) & (occupancy_df['quarter'] == 'Q1')].copy()
baseline = baseline[['market', 'avg_occupancy_proportion']]
baseline = baseline.rename(columns={'avg_occupancy_proportion': 'baseline_occupancy'})

# Find the pandemic low point for each market (typically Q2 2020)
pandemic_low = occupancy_df.loc[occupancy_df.groupby('market')['avg_occupancy_proportion'].idxmin()]
pandemic_low = pandemic_low[['market', 'year', 'quarter', 'avg_occupancy_proportion']]
pandemic_low = pandemic_low.rename(columns={'avg_occupancy_proportion': 'pandemic_low', 
                                         'year': 'low_year',
                                         'quarter': 'low_quarter'})

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
print(recovery_df)

# Visualize the recovery patterns
plt.figure(figsize=(14, 8))

x = np.arange(len(recovery_df))
width = 0.35

plt.bar(x - width/2, recovery_df['drop_percentage'], width, label='Pandemic Low (% of Baseline)')
plt.bar(x + width/2, recovery_df['recovery_percentage'], width, label='Current (% of Baseline)')

plt.axhline(y=100, color='r', linestyle='-', alpha=0.3, label='Baseline (Q1 2020)')

plt.xlabel('Market', fontsize=14)
plt.ylabel('Percentage of Baseline Occupancy', fontsize=14)
plt.title('Office Occupancy Recovery by Market', fontsize=16)
plt.xticks(x, recovery_df['market'], rotation=45, ha='right')
plt.legend()
plt.tight_layout()
plt.grid(True, axis='y', alpha=0.3)
plt.savefig('plots/recovery_comparison.png')
plt.close()

print("Generated recovery comparison plot")

print("\n# Analyze Market-Specific Trends in Availability and Pricing")

# Create a function to plot availability and pricing trends for specific markets
def plot_market_trends(market_name, class_type='A'):
    market_data = availability_df[(availability_df['market'] == market_name) & 
                              (availability_df['internal_class'] == class_type)].copy()
    
    # Create period column
    market_data['period'] = market_data['year'].astype(str) + "-" + market_data['quarter']
    market_data = market_data.sort_values('period')
    
    # Set up the figure with two y-axes
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # Plot availability on the first y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Time Period', fontsize=14)
    ax1.set_ylabel('Availability Proportion', color=color, fontsize=14)
    ax1.plot(market_data['period'], market_data['availability_proportion'], color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, max(market_data['availability_proportion']) * 1.1 if len(market_data) > 0 else 1)
    
    # Create a second y-axis for rent
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Rent ($ per sq ft)', color=color, fontsize=14)
    ax2.plot(market_data['period'], market_data['internal_class_rent'], color=color, marker='s')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Add a title and adjust the layout
    plt.title(f'Availability and Rent Trends for {market_name} (Class {class_type})', fontsize=16)
    plt.xticks(rotation=45)
    fig.tight_layout()
    
    # Add a legend
    ax1.plot([], [], color='tab:blue', marker='o', label='Availability')
    ax2.plot([], [], color='tab:red', marker='s', label='Rent')
    fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
    
    # Add grid lines
    ax1.grid(True, alpha=0.3)
    
    plt.savefig(f'plots/{market_name.replace("/", "_")}_trends.png')
    plt.close()
    
    return market_data

# Look at trends for major markets
print("Generating market-specific trends for major markets...")
key_markets = ['San Francisco', 'Manhattan', 'Austin', 'Chicago', 'Washington DC']
for market in key_markets:
    try:
        plot_market_trends(market)
        print(f"Generated trends plot for {market}")
    except Exception as e:
        print(f"Error plotting {market}: {e}")

print("\n# Compare Trends Across Different Markets")

# Group markets into categories: Tech Hubs, Financial Centers, and Regional Centers
tech_hubs = ['San Francisco', 'South Bay', 'Seattle', 'Austin']
financial_centers = ['Manhattan', 'Chicago', 'Boston']
regional_centers = ['Dallas-Ft. Worth', 'Atlanta', 'Houston', 'Philadelphia']

# Create a function to plot availability trends for a group of markets
def plot_market_group_trends(market_group, group_name, class_type='A'):
    plt.figure(figsize=(14, 8))
    
    for market in market_group:
        try:
            market_data = availability_df[(availability_df['market'] == market) & 
                                     (availability_df['internal_class'] == class_type)].copy()
            
            # Create period column
            market_data['period'] = market_data['year'].astype(str) + "-" + market_data['quarter']
            market_data = market_data.sort_values('period')
            
            # Plot availability trend
            plt.plot(market_data['period'], market_data['availability_proportion'], marker='o', label=market)
        except Exception as e:
            print(f"Error plotting {market}: {e}")
    
    plt.title(f'Availability Trends for {group_name} (Class {class_type})', fontsize=16)
    plt.xlabel('Time Period', fontsize=14)
    plt.ylabel('Availability Proportion', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'plots/{group_name.replace(" ", "_")}_availability.png')
    plt.close()

# Plot trends for each market group
print("Generating market group comparison plots...")
plot_market_group_trends(tech_hubs, 'Tech Hubs')
print("Generated Tech Hubs plot")
plot_market_group_trends(financial_centers, 'Financial Centers')
print("Generated Financial Centers plot")
plot_market_group_trends(regional_centers, 'Regional Centers')
print("Generated Regional Centers plot")

print("\n# Correlation Analysis with Unemployment")

# Create a mapping of markets to their primary states
market_to_state = {
    'Manhattan': 'NY',
    'San Francisco': 'CA',
    'Los Angeles': 'CA',
    'Chicago': 'IL', 
    'Boston': 'MA',
    'Dallas/Ft Worth': 'TX',
    'Houston': 'TX',
    'Washington D.C.': 'DC',
    'Philadelphia': 'PA',
    'South Bay/San Jose': 'CA',
    'Austin': 'TX'
}

# Prepare unemployment data
unemployment_quarterly = unemployment_df.groupby(['year', 'quarter', 'state'])['unemployment_rate'].mean().reset_index()

# Join occupancy data with unemployment using the market-to-state mapping
occupancy_with_unemployment = occupancy_df.copy()
occupancy_with_unemployment['state'] = occupancy_with_unemployment['market'].map(market_to_state)

# Join with unemployment data
occupancy_with_unemployment = occupancy_with_unemployment.merge(
    unemployment_quarterly, on=['year', 'quarter', 'state'], how='left')

# Display the merged data
print("Occupancy data with unemployment rates:")
print(occupancy_with_unemployment.head())

# Plot correlation between unemployment and office occupancy
plt.figure(figsize=(14, 8))

for market in occupancy_with_unemployment['market'].unique():
    market_data = occupancy_with_unemployment[occupancy_with_unemployment['market'] == market]
    if not market_data['unemployment_rate'].isna().all():  # Only plot if we have unemployment data
        plt.scatter(market_data['unemployment_rate'], market_data['avg_occupancy_proportion'], 
                    label=market, alpha=0.7, s=80)

plt.title('Relationship Between Unemployment Rate and Office Occupancy', fontsize=16)
plt.xlabel('Unemployment Rate (%)', fontsize=14)
plt.ylabel('Average Office Occupancy Proportion', fontsize=14)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plots/unemployment_correlation.png')
plt.close()

print("Generated unemployment correlation plot")

# Calculate correlation coefficients by market
correlations = []

for market in occupancy_with_unemployment['market'].unique():
    market_data = occupancy_with_unemployment[occupancy_with_unemployment['market'] == market]
    if not market_data['unemployment_rate'].isna().all():  # Only calculate if we have unemployment data
        corr = market_data['unemployment_rate'].corr(market_data['avg_occupancy_proportion'])
        correlations.append({'Market': market, 'Correlation': corr})

corr_df = pd.DataFrame(correlations).sort_values('Correlation')
print("\nCorrelation between unemployment rate and office occupancy by market:")
print(corr_df)

print("\n# Key Insights and Recommendations")
print("Analysis complete. Check the 'plots' directory for all generated visualizations.") 