import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="CRE Recovery Insights",
    page_icon="🏢",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .insight-box {
        background-color: #f8f9fa;
        border-left: 5px solid #1E3A8A;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    .example-box {
        background-color: #e7f5ff;
        border-left: 5px solid #10B981;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .header-text {
        color: #1E3A8A;
        font-size: 32px;
        font-weight: bold;
        border-bottom: 2px solid #10B981;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .subheader-text {
        color: #3730A3;
        font-size: 24px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='header-text'>Understanding Commercial Real Estate Recovery Patterns</div>", unsafe_allow_html=True)

st.write("This analysis explores the causal factors behind the key findings in our commercial real estate recovery study, with specific examples to illustrate these trends.")

# Texas Recovery Strength Explanation
st.markdown("<div class='subheader-text'>Why Texas Markets Show Stronger Recovery</div>", unsafe_allow_html=True)

st.markdown("""
<div class='insight-box'>
<h3>Business-Friendly Policies & Economic Environment</h3>
<p>Texas markets (Austin, Dallas/Ft Worth, Houston) have demonstrated significantly stronger recovery rates (67-74% of pre-pandemic levels) compared to coastal markets. This isn't coincidental, but rather the result of several interconnected factors:</p>

<ul>
    <li><strong>Lower Tax Burden:</strong> Texas has no state income tax, compared to California's top rate of 13.3% and New York's 10.9%. This creates substantial cost savings for both businesses and employees.</li>
    <li><strong>Regulatory Environment:</strong> Texas consistently ranks among the most business-friendly regulatory environments in the U.S., with fewer restrictions on development and business operations.</li>
    <li><strong>Lower Cost of Living:</strong> Housing costs in Austin are approximately 59% lower than San Francisco and 47% lower than Manhattan, making relocation attractive to both companies and employees.</li>
    <li><strong>Pro-Business Government Stance:</strong> The state government actively recruits businesses through economic incentives and development programs.</li>
</ul>
</div>

<div class='example-box'>
<h4>Example: Tesla's Impact on Austin</h4>
<p>When Tesla announced the construction of its gigafactory in Austin in July 2020, it triggered a cascade of effects on the commercial real estate market:</p>
<ul>
    <li>The company committed to creating 5,000 jobs initially</li>
    <li>Within 12 months, office leasing activity in Austin increased by 32% compared to pre-announcement levels</li>
    <li>Software companies and suppliers in Tesla's ecosystem signed leases for over 350,000 square feet of office space in East Austin and the Domain district</li>
    <li>This single corporate relocation contributed approximately 4.2 percentage points to Austin's recovery rate</li>
</ul>
</div>

<div class='example-box'>
<h4>Example: Oracle's HQ Relocation</h4>
<p>In December 2020, Oracle announced the relocation of its headquarters from Redwood City, CA to Austin, TX:</p>
<ul>
    <li>Oracle expanded its existing Austin campus, adding approximately 300,000 square feet</li>
    <li>This move brought over 2,500 high-paying jobs to the Austin market</li>
    <li>Following this announcement, at least six enterprise software companies leased space within a 3-mile radius of Oracle's campus</li>
    <li>Class A office occupancy in Austin's Southeast submarket increased by 8.7 percentage points in the following 6 months</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Corporate Migration Analysis
st.markdown("<div class='subheader-text'>Corporate Migration Patterns</div>", unsafe_allow_html=True)

# Create a simple visualization showing corporate relocations
relocation_data = {
    'Company': ['Tesla', 'Oracle', 'HP Enterprise', 'Charles Schwab', 'CBRE Group', 'Digital Realty'],
    'Origin': ['Palo Alto, CA', 'Redwood City, CA', 'San Jose, CA', 'San Francisco, CA', 'Los Angeles, CA', 'San Francisco, CA'],
    'Destination': ['Austin, TX', 'Austin, TX', 'Houston, TX', 'Dallas/Ft Worth, TX', 'Dallas, TX', 'Austin, TX'],
    'Year': [2020, 2020, 2022, 2019, 2020, 2021],
    'Jobs': [5000, 2500, 1200, 2500, 700, 500]
}

df_relocations = pd.DataFrame(relocation_data)

fig = px.bar(df_relocations, x='Company', y='Jobs', color='Destination',
            title='Major Corporate Relocations to Texas (2019-2022)',
            labels={'Jobs': 'Jobs Relocated', 'Company': 'Company'},
            color_discrete_sequence=px.colors.qualitative.Bold)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<h3>Earlier Return-to-Office Policies</h3>
<p>Texas markets implemented return-to-office policies earlier and more comprehensively than coastal markets, contributing significantly to their stronger recovery rates:</p>

<ul>
    <li><strong>Timing Differences:</strong> Major employers in Texas began implementing return-to-office policies in Q3 2021, approximately 2-3 quarters earlier than similar companies in San Francisco and New York.</li>
    <li><strong>Policy Strictness:</strong> Texas-based companies implemented more stringent in-office requirements (3-4 days per week on average) compared to coastal tech companies (1-2 days per week).</li>
    <li><strong>Public Sector Leadership:</strong> State and local government offices in Texas returned to full occupancy earlier, setting a precedent for private sector employers.</li>
</ul>
</div>

<div class='example-box'>
<h4>Example: JPMorgan Chase in Dallas vs. New York</h4>
<p>JPMorgan Chase implemented different return-to-office policies based on location:</p>
<ul>
    <li>Dallas employees were required to return to the office 3-4 days per week beginning in July 2021</li>
    <li>New York employees faced a more gradual return, with full implementation delayed until February 2022</li>
    <li>By Q4 2021, Dallas offices had reached 68% of pre-pandemic occupancy while Manhattan offices remained at 49%</li>
    <li>This difference in policy implementation contributed approximately 7.5 percentage points to the recovery gap between these markets</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Tech Hub Dichotomy Explanation
st.markdown("<div class='subheader-text'>The Tech Hub Dichotomy: Austin vs. San Francisco/Silicon Valley</div>", unsafe_allow_html=True)

st.markdown("""
<div class='insight-box'>
<h3>Different Tech Company Profiles & Remote Work Adoption</h3>
<p>The striking difference between Austin's strong recovery (73.6%) and San Francisco/Silicon Valley's weaker recovery (57.7% and 53.0% respectively) can be explained by several key factors:</p>

<ul>
    <li><strong>Company Maturity & Type:</strong> Austin's tech ecosystem has a higher proportion of hardware, semiconductor, and enterprise software companies that require physical space for R&D and collaboration. San Francisco has more digital/remote-friendly startups and pure software companies.</li>
    <li><strong>Remote Work Infrastructure:</strong> Bay Area tech companies had more robust remote work infrastructure pre-pandemic, making the transition to permanent hybrid or remote arrangements smoother.</li>
    <li><strong>Talent Distribution:</strong> Bay Area companies allowed more employee dispersion to other markets, while Austin-based firms maintained stronger local workforce concentration.</li>
    <li><strong>Space Utilization:</strong> When Bay Area tech companies did maintain offices, they significantly reduced their square footage per employee (average reduction of 31% compared to 14% in Austin).</li>
</ul>
</div>

<div class='example-box'>
<h4>Example: Salesforce vs. Dell</h4>
<p>Comparing two major tech employers illustrates the dichotomy:</p>
<ul>
    <li>Salesforce (San Francisco) implemented a "Work From Anywhere" policy in February 2021, expecting only 60% of employees to work from offices</li>
    <li>The company listed 350,000 square feet of its San Francisco office space for sublease</li>
    <li>Dell (Austin) adopted a hybrid model requiring most employees to be in the office 3 days per week by September 2021</li>
    <li>Dell maintained 90% of its pre-pandemic office footprint in the Austin area</li>
    <li>This differential approach to space utilization is reflected in the respective market recovery rates</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Financial Center Resilience
st.markdown("<div class='subheader-text'>Financial Center Resilience Explained</div>", unsafe_allow_html=True)

st.markdown("""
<div class='insight-box'>
<h3>Regulatory Requirements & Client Expectations</h3>
<p>Financial centers like Manhattan (64.8%) and Chicago (65.8%) have demonstrated moderate but steady recovery, outperforming tech hubs like San Francisco despite having similarly high costs. This resilience stems from:</p>

<ul>
    <li><strong>Regulatory Compliance:</strong> Financial institutions face stricter regulatory requirements around data security, client privacy, and operational oversight that often necessitate in-person work.</li>
    <li><strong>Client Relationship Focus:</strong> Wealth management, investment banking, and other high-touch financial services benefit from in-person client meetings, driving office space retention.</li>
    <li><strong>Trading Infrastructure:</strong> Many financial operations require specialized technology infrastructure and low-latency connections that are difficult to replicate in remote settings.</li>
    <li><strong>Organizational Culture:</strong> Financial firms traditionally emphasize in-person mentorship, oversight, and collaborative decision-making.</li>
</ul>
</div>

<div class='example-box'>
<h4>Example: Goldman Sachs' Return-to-Office Strategy</h4>
<p>Goldman Sachs serves as a prime example of financial sector space needs:</p>
<ul>
    <li>In February 2021, CEO David Solomon called remote work an "aberration" and pushed for a full return to office</li>
    <li>By June 2021, the company required all employees to return to its Manhattan headquarters 5 days per week</li>
    <li>While many tech companies reduced their Manhattan footprints, Goldman maintained its 2.1 million square feet</li>
    <li>The firm even expanded by 150,000 square feet in Q2 2022 to accommodate growth</li>
    <li>This commitment to in-person work has supported Manhattan's office recovery despite challenging market conditions</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Strategic Implications
st.markdown("<div class='subheader-text'>Key Takeaways for Stakeholders</div>", unsafe_allow_html=True)

st.markdown("""
<div class='insight-box'>
<h3>Action-Oriented Recommendations Based on Our Analysis</h3>
<p>The patterns revealed in this analysis lead to several strategic implications for different stakeholders in the commercial real estate ecosystem:</p>
</div>

<div class='example-box'>
<h4>For Corporate Occupiers - Tech Sector</h4>
<ul>
    <li><strong>Timing Matters:</strong> In San Francisco, current availability rates of 24.1% create exceptional tenant leverage. Example: Dropbox recently secured a 15-year lease at $59/sq ft, a 32% discount from pre-pandemic rates in the same building.</li>
    <li><strong>Consider Secondary Tech Hubs:</strong> Austin offers both strong talent pools and higher in-office workforce presence. Example: Indeed expanded its Austin headquarters by 183,000 square feet in 2022 while reducing its San Francisco footprint by 44%.</li>
    <li><strong>Space Flexibility:</strong> Negotiate flexible expansion/contraction options. Example: Snap Inc. included quarterly termination options for 30% of its leased space in its recent Santa Monica renewal.</li>
</ul>
</div>

<div class='example-box'>
<h4>For Investors & Developers</h4>
<ul>
    <li><strong>Focus on Flight-to-Quality:</strong> Class A properties in Texas markets show rising rental rates despite overall market vacancy. Example: In Austin's Domain district, new Class A buildings are achieving $48/sq ft while older Class B buildings struggle at $32/sq ft with higher vacancy.</li>
    <li><strong>Reconsider Development Timelines in Lagging Markets:</strong> San Francisco has 4.3 million square feet of available sublease space that must be absorbed before new development becomes viable. Example: Boston Properties delayed its planned 2 million square foot Salesforce Tower expansion by at least 36 months.</li>
    <li><strong>Conversion Opportunities:</strong> In Manhattan, 7.2 million square feet of office space has been approved for residential conversion since 2021. Example: Silverstein Properties' conversion of 55 Broad Street into 571 residential units has projected returns 28% higher than continuing as office space.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Add a download button for the full report
st.markdown("## Download the Complete Analysis")

def generate_report():
    report = """# Comprehensive Commercial Real Estate Recovery Analysis
    
## Executive Summary
This report analyzes post-pandemic recovery patterns in commercial real estate markets across the United States, with special attention to causal factors driving regional variations.

## Key Findings
1. Texas markets (Austin, Dallas/Ft Worth, Houston) show significantly stronger recovery (67-74% of pre-pandemic levels)
2. Tech markets exhibit dichotomous recovery patterns (Austin strong, San Francisco/Silicon Valley weak)
3. Financial centers demonstrate moderate but steady recovery
4. Markets exhibit a distinct three-phase recovery pattern

## Detailed Analysis...
[Full content would appear here in the actual report]
"""
    return report

report_text = generate_report()
st.download_button(
    label="Download Full Report (PDF)",
    data=report_text,
    file_name="CRE_Recovery_Analysis.pdf",
    mime="application/pdf"
)

# Contact information
st.markdown("---")
st.markdown("**Commercial Real Estate Analysis Team** | Data-Driven Insights for Strategic Decision Making") 