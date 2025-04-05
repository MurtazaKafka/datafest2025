# Commercial Real Estate Market Analysis: Post-Pandemic Recovery Patterns and Market Dynamics

## 1. Introduction

The commercial real estate (CRE) sector has undergone unprecedented disruption since the COVID-19 pandemic. The abrupt transition to remote work dramatically altered office space utilization across major metropolitan areas, creating significant challenges for real estate stakeholders. This analysis addresses the complex question posed by Savills, an international commercial real estate firm: what notable trends or microtrends in the commercial real estate market could be identified to advise clients on office location strategies?

The pandemic served as a natural experiment in workplace flexibility, forcing companies to rapidly adopt remote work policies. As these policies evolved over time, different markets have exhibited varying patterns of recovery and adaptation. Understanding these patterns is crucial for real estate decision-makers who must navigate a transformed landscape where traditional assumptions about office space demand may no longer apply.

This analysis focuses on identifying patterns within and across markets, with particular attention to recovery trajectories from pandemic lows, geographic variations in recovery strength, and the relationship between office occupancy and other economic indicators. By examining these patterns, we aim to provide actionable insights for stakeholders making strategic decisions about office space investments, leases, and portfolio management.

The significance of this work extends beyond simple market analysis. As organizations reconsider their real estate footprints in light of hybrid work models, understanding market-specific dynamics becomes essential for effective decision-making. This analysis leverages comprehensive datasets provided by Savills, including transaction records, occupancy rates, and market-level indicators, enhanced with unemployment data from government sources.

## 2. Methods

### 2.1 Data Sources and Preparation

This analysis utilized four primary datasets:

1. **Major Market Occupancy Data**: Provided by Kastle Systems, containing card-swipe-based occupancy estimates for ten major markets from 2020-2024. This dataset includes variables for starting, ending, and average occupancy proportions for each market and quarter.

2. **Price and Availability Data**: Market-level information about rental prices, available space, and availability proportions across different markets, with separate variables for Class A and other (Class O) buildings.

3. **Leases Data**: Comprehensive transaction-level data compiled from CoStar, Savills, and other sources, encompassing lease transactions from 2018-2024.

4. **Unemployment Data**: Government data from the U.S. Bureau of Labor Statistics, providing state-level unemployment rates across the study period.

Data preparation involved several key steps:

- Creating a unified time period indicator by combining year and quarter fields
- Mapping markets to their respective states for integration with unemployment data
- Calculating recovery metrics based on pre-pandemic baselines, pandemic lows, and current occupancy levels
- Categorizing markets into functional groups (Tech Hubs, Financial Centers, Regional Centers, etc.)
- Adding geographic coordinates for spatial visualization

### 2.2 Analytical Approaches

Our analytical framework combined descriptive, comparative, and geospatial methods to extract meaningful insights:

1. **Recovery Analysis**: We established Q1 2020 (pre-lockdown) as the occupancy baseline and computed both the pandemic low point and current occupancy as percentages of this baseline. This allowed for standardized comparison across markets with different absolute occupancy levels.

2. **Time Series Analysis**: We examined longitudinal trends in occupancy rates, identifying key inflection points and patterns of recovery or stagnation. Annotations for significant events (pandemic onset, vaccine rollout, return-to-office policies) provided contextual markers.

3. **Comparative Market Analysis**: Direct comparisons between markets with different characteristics (e.g., Tech Hubs vs. Financial Centers) revealed differential recovery patterns and potential driving factors.

4. **Geospatial Analysis**: Mapping recovery rates to geographic locations enabled identification of regional patterns that might be obscured in tabular data.

5. **Correlation Analysis**: We examined relationships between occupancy rates and economic indicators, particularly unemployment rates, to identify potential predictive factors.

### 2.3 Visualization Techniques

To effectively communicate complex patterns in the data, we employed several advanced visualization techniques:

- **Interactive Dashboards**: Enabling stakeholders to explore different facets of the data through user-directed filtering and selection.
- **Dual-Axis Charts**: Simultaneously displaying related but differently-scaled metrics (e.g., availability and rental rates).
- **Heatmaps**: Providing at-a-glance views of occupancy patterns across markets and time periods.
- **3D Visualizations**: Adding an extra dimension to geographic data to highlight regional patterns.
- **Animated Time Series**: Demonstrating temporal evolution of occupancy rates.
- **Hierarchical Visualizations**: Organizing markets into functional categories to identify group-level patterns.

All visualizations were implemented using the Plotly and Streamlit libraries in Python, with additional support from Pandas for data manipulation and Pydeck for geospatial rendering.

## 3. Results

### 3.1 Market Recovery Patterns

The analysis revealed substantial variation in recovery rates across markets. Key findings include:

- **Tech-Driven Markets Show Dichotomous Recovery**: Austin has demonstrated the strongest recovery at 73.6% of pre-pandemic baseline, while other tech hubs like San Francisco (57.7%) and South Bay/San Jose (53.0%) show significantly weaker recovery.

- **Regional Variation is Pronounced**: Southern and Central U.S. markets consistently outperformed coastal markets, with Texas markets (Austin, Dallas/Ft Worth, Houston) achieving the highest recovery rates (67-74% of pre-pandemic levels).

- **Financial Centers Show Moderate Recovery**: Manhattan (64.8%) and Chicago (65.8%) have recovered approximately two-thirds of their pre-pandemic occupancy, suggesting resilience in traditional financial hubs.

- **Pandemic Impact Varied Significantly**: The initial impact of the pandemic (measured as the drop from baseline to pandemic low) ranged from 7.1% (Manhattan) to 32.5% (Dallas/Ft Worth) of baseline occupancy. Markets with more severe initial drops have not necessarily shown weaker recovery.

### 3.2 Temporal Patterns

Time series analysis revealed several important patterns:

- **Universal Initial Decline**: All markets experienced sharp occupancy declines in Q2 2020, with occupancy rates falling to below 30% of pre-pandemic levels in most markets.

- **Three-Phase Recovery Pattern**: Most markets exhibited a three-phase pattern: sharp decline (Q1-Q2 2020), gradual recovery (Q3 2020-Q1 2022), and stabilization (Q2 2022-present).

- **Seasonal Fluctuations**: Post-2022, markets began showing seasonal patterns with slight declines in Q4, potentially reflecting holiday-related occupancy decreases.

- **Recovery Acceleration Points**: Key inflection points in recovery correspond to vaccine availability (Q1-Q2 2021) and formalized return-to-office policies (Q1 2022).

### 3.3 Relationship Between Availability and Pricing

Analysis of Class A properties revealed complex relationships between space availability and rental rates:

- **Inverse Relationship in Recovering Markets**: In strongly recovering markets like Austin, increasing occupancy rates corresponded with rising rental rates, suggesting demand-driven pricing.

- **Lagged Price Adjustment in Weaker Markets**: In slower-recovering markets like San Francisco, rental rates remained relatively stable despite increased availability, suggesting institutional factors delaying price adjustments.

- **Price Stability Despite Occupancy Changes**: Most markets showed relatively stable rental rates despite significant occupancy fluctuations, particularly in premium (Class A) properties.

### 3.4 Correlation with Economic Indicators

The analysis identified significant negative correlations between unemployment rates and office occupancy across all markets:

- **Strongest Negative Correlations**: Austin (-0.84), Manhattan (-0.82), and Houston (-0.80) showed the strongest negative correlations between unemployment and occupancy.

- **Moderate Negative Correlations**: Los Angeles (-0.59) and Philadelphia (-0.56) showed more moderate negative correlations.

- **Predictive Potential**: The consistent negative correlation suggests unemployment rates may serve as a leading indicator for office occupancy trends.

## 4. Discussion

### 4.1 Implications for Commercial Real Estate Strategy

The findings from this analysis have several important implications for commercial real estate stakeholders:

1. **Market-Specific Strategies are Essential**: The significant variation in recovery patterns across markets underscores the need for localized rather than national strategies. Stakeholders should develop market-specific approaches that account for local recovery trajectories, economic conditions, and industry composition.

2. **Texas Markets Present Opportunity**: The strong recovery in Texas markets suggests potential opportunities for expansion or relocation, particularly for organizations with flexibility in their location choices. The combination of strong recovery, relative affordability compared to coastal markets, and favorable economic indicators makes these markets attractive for strategic investment.

3. **Coastal Tech Hubs Require Careful Evaluation**: The lagging recovery in traditional coastal tech hubs like San Francisco and Silicon Valley suggests that stakeholders should carefully evaluate long-term commitments in these markets. For tenants, this may represent an opportunity to negotiate favorable terms; for owners, it may necessitate reimagining space utilization or amenity offerings to attract tenants.

4. **Financial Centers Demonstrate Resilience**: The moderate but steady recovery in financial centers suggests these markets will likely maintain their importance, though possibly with reduced overall space requirements. Organizations in financial services should consider hybrid strategies that maintain presence in these centers while potentially distributing some functions to stronger-recovering markets.

### 4.2 Limitations and Future Research

Several limitations of this analysis should be acknowledged:

1. **Card Swipe Data Limitations**: The occupancy data relies on card swipe systems, which may not perfectly capture actual occupancy, particularly as access protocols changed during the pandemic.

2. **Limited Industry-Specific Analysis**: While we categorized markets by their predominant character (tech hub, financial center, etc.), more granular analysis of industry-specific patterns within markets was limited by data availability.

3. **Forward-Looking Indicators**: This analysis focused primarily on historical and current patterns rather than predictive modeling of future trends.

Future research directions could address these limitations through:

- Incorporating additional data sources like mobile device movement data for more accurate occupancy measurement
- Developing predictive models that forecast occupancy trends based on economic indicators and company policy announcements
- Conducting more granular analysis of submarkets within major metropolitan areas
- Examining the impact of building amenities and ESG factors on recovery patterns

### 4.3 Strategic Recommendations

Based on our analysis, we offer the following strategic recommendations for different stakeholders:

**For Corporate Occupiers:**
- Consider expanding in strongly recovering markets like Austin and Dallas for cost-effective access to talent
- Negotiate favorable terms in weakly recovering markets like San Francisco, potentially securing premium space at competitive rates
- Implement hybrid location strategies that balance presence in traditional centers with distributed teams in stronger-recovering markets

**For Investors and Developers:**
- Focus on Class A properties in strongly recovering markets, where demand and rental rates show positive correlation
- Consider repositioning strategies for properties in weakly recovering markets, potentially converting to mixed-use or adding amenities that support hybrid work models
- Monitor unemployment rates as a potential leading indicator for market performance

**For Brokerage and Advisory Firms:**
- Develop market-specific advisory frameworks that account for the divergent recovery patterns identified in this analysis
- Create tools that help clients evaluate the trade-offs between market recovery strength, talent access, and cost considerations
- Establish ongoing monitoring of key inflection points that might signal changes in recovery trajectories

### 4.4 Conclusion

The commercial real estate market has undergone a profound transformation since the pandemic's onset, with recovery patterns varying significantly across markets. This analysis has demonstrated that understanding these market-specific dynamics is essential for effective decision-making in this new landscape.

The strong recovery in Texas markets, moderate recovery in financial centers, and continued challenges in some coastal tech hubs represent more than temporary fluctuations—they signal structural changes in how organizations utilize office space across different geographic areas. By leveraging the insights from this analysis, stakeholders can develop more nuanced, market-specific strategies that account for these evolving patterns.

As the commercial real estate market continues to adapt to post-pandemic realities, ongoing analysis of occupancy trends, economic indicators, and market-specific factors will remain crucial. The visualizations and analytical approaches developed in this project provide a foundation for this continued evaluation, enabling data-driven decision-making in an increasingly complex real estate landscape. 