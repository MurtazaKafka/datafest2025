import streamlit as st
import markdown
import base64
from pathlib import Path
import re
import numpy as np
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="CRE Market Recovery Presentation",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to read markdown file
def read_markdown_file(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        return file.read()

# Function to extract slides from markdown content
def extract_slides(content):
    # Split content by horizontal rule
    slides = re.split(r'\n---\n', content)
    # Remove the style section from the last slide
    if '<style>' in slides[-1]:
        style_content = re.search(r'<style>(.*?)</style>', slides[-1], re.DOTALL).group(1)
        slides[-1] = re.sub(r'<style>.*?</style>', '', slides[-1], flags=re.DOTALL)
        return slides, style_content
    return slides, None

# Function to create navigation buttons
def create_navigation(current_slide, total_slides, position="top"):
    cols = st.columns([1, 1, 3, 1, 1])
    
    with cols[0]:
        if current_slide > 0:
            if st.button("⏮️ First", key=f"first_{position}"):
                st.session_state.current_slide = 0
                st.rerun()
    
    with cols[1]:
        if current_slide > 0:
            if st.button("◀️ Previous", key=f"prev_{position}"):
                st.session_state.current_slide -= 1
                st.rerun()
    
    with cols[2]:
        st.markdown(f"<h3 style='text-align: center;'>Slide {current_slide + 1}/{total_slides}</h3>", unsafe_allow_html=True)
    
    with cols[3]:
        if current_slide < total_slides - 1:
            if st.button("Next ▶️", key=f"next_{position}"):
                st.session_state.current_slide += 1
                st.rerun()
    
    with cols[4]:
        if current_slide < total_slides - 1:
            if st.button("Last ⏭️", key=f"last_{position}"):
                st.session_state.current_slide = total_slides - 1
                st.rerun()

# Function to apply custom styling
def apply_custom_style(style_content):
    if style_content:
        st.markdown(f"<style>{style_content}</style>", unsafe_allow_html=True)

# Additional styling for the presentation
def apply_slide_styling():
    st.markdown("""
    <style>
    .slide-container {
        background-color: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        margin: 20px 0;
        transition: all 0.5s ease;
    }
    
    /* Override Streamlit's default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #1E3A8A;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        background-color: #1E3A8A;
        color: white;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        background-color: #10B981;
    }
    
    /* Make sure images don't overflow */
    img {
        max-width: 100%;
        height: auto;
    }
    
    /* Animation for slide transitions */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .slide-container {
        animation: slideIn 0.5s ease-out forwards;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #F3F4F6;
    }
    
    /* Font improvements */
    body {
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Footer styling */
    footer {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# Save images from the presentation to local files if they don't exist yet
def save_presentation_images():
    # Directory to save images
    Path("images").mkdir(exist_ok=True)
    
    # Create placeholder images with the right names
    image_files = {
        "recovery_comparison_chart.png": (800, 500),
        "animated_occupancy.gif": (800, 500),
        "recovery_3d_map.png": (800, 600),
        "market_comparison_chart.png": (800, 500),
        "occupancy_heatmap.png": (800, 500),
        "recovery_sunburst.png": (800, 600)
    }
    
    # Generate actual image placeholders
    for img_file, size in image_files.items():
        img_path = Path(f"images/{img_file}")
        if not img_path.exists():
            # Create a gradient colored image as placeholder
            if img_file.endswith('.gif'):
                # For GIF, create a simple animation
                frames = []
                for i in range(10):
                    array = np.zeros((size[1], size[0], 3), dtype=np.uint8)
                    # Create gradient
                    for y in range(size[1]):
                        for x in range(size[0]):
                            array[y, x, 0] = int(255 * x / size[0])  # R
                            array[y, x, 1] = int(255 * y / size[1])  # G
                            array[y, x, 2] = int(255 * (i/10))      # B
                    frames.append(Image.fromarray(array))
                
                # Save as animated GIF
                frames[0].save(
                    img_path, 
                    save_all=True, 
                    append_images=frames[1:], 
                    duration=200, 
                    loop=0
                )
            else:
                # For PNG, create a static image
                array = np.zeros((size[1], size[0], 3), dtype=np.uint8)
                # Create gradient
                for y in range(size[1]):
                    for x in range(size[0]):
                        array[y, x, 0] = int(255 * x / size[0])  # R
                        array[y, x, 1] = int(255 * y / size[1])  # G
                        array[y, x, 2] = 100  # B
                
                img = Image.fromarray(array)
                # Add title text
                img.save(img_path)

# Function to fix image paths in the markdown content
def fix_image_paths(content):
    # Replace GitHub raw URLs with local paths
    fixed_content = re.sub(
        r'https://raw.githubusercontent.com/MurtazaKafka/datafest2025/main/images/([^)]+)',
        r'images/\1',
        content
    )
    return fixed_content

# Add sidebar with tutorial
def add_sidebar():
    with st.sidebar:
        st.title("Presentation Guide")
        st.markdown("""
        > **How to Navigate**
        
        1. Use the navigation buttons at the top or bottom to move between slides
        2. Click "Next ▶️" to advance to the next slide
        3. Click "◀️ Previous" to go back
        4. Use "⏮️ First" or "Last ⏭️" to jump to the beginning or end
        
        > **Key Insights**
        
        - Southern/Central markets show strongest recovery (Austin at 73.6%)
        - Strong negative correlation between unemployment and office occupancy
        - Texas markets present the most strategic opportunity
        - Market-specific strategies are essential in the post-pandemic landscape
        """)
        
        st.markdown("---")
        st.markdown("**Commercial Real Estate Market Analysis**  \nPost-Pandemic Recovery Patterns")

# Main application
def main():
    apply_slide_styling()
    add_sidebar()
    
    # Create local image files if needed
    save_presentation_images()
    
    # Read and process the markdown presentation
    md_content = read_markdown_file("presentation.md")
    md_content = fix_image_paths(md_content)
    slides, style_content = extract_slides(md_content)
    
    # Apply custom styling from the markdown
    apply_custom_style(style_content)
    
    # Initialize session state for tracking current slide
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0
    
    # Navigation controls at the top
    create_navigation(st.session_state.current_slide, len(slides), position="top")
    
    # Display progress bar
    progress = (st.session_state.current_slide) / (len(slides) - 1)
    st.progress(progress)
    
    # Display the current slide
    with st.container():
        st.markdown(f'<div class="slide-container">{slides[st.session_state.current_slide]}</div>', unsafe_allow_html=True)
        
        # Add this line to display dynamic visualizations
        display_slide_visualizations(st.session_state.current_slide)
    
    # Navigation controls at the bottom
    create_navigation(st.session_state.current_slide, len(slides), position="bottom")
    
    # Add a reference footer
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Commercial Real Estate Analysis** | Data-Driven Insights for Strategic Decision Making")
    with col2:
        st.markdown("Slide: " + str(st.session_state.current_slide + 1) + "/" + str(len(slides)))

# Edit the presentation_app.py file to include this for all slides

def display_slide_visualizations(slide_number):
    """Display interactive visualizations based on the current slide."""
    # Import necessary visualization functions
    from capture_images import (load_data, create_recovery_analysis, 
                               create_recovery_chart, create_occupancy_heatmap,
                               create_3d_map, create_market_comparison,
                               create_sunburst)
    
    # Load data once
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
    
    # Display visualization based on slide number
    if slide_number == 1:  # Recovery Patterns slide
        with st.expander("Interactive Recovery Chart", expanded=True):
            fig = create_recovery_chart(recovery_df)
            st.plotly_chart(fig, use_container_width=True)
            
        with st.expander("Animated Occupancy Trends", expanded=False):
            # Create a simple animation using Plotly
            import plotly.express as px
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
                title='Office Occupancy Evolution (2020-2024)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
    elif slide_number == 2:  # Economic Correlations slide
        with st.expander("3D Recovery Visualization", expanded=True):
            fig = create_3d_map(map_data)
            st.plotly_chart(fig, use_container_width=True)
            
        with st.expander("Market Comparison", expanded=False):
            fig = create_market_comparison(occupancy_df, availability_df)
            st.plotly_chart(fig, use_container_width=True)
            
    elif slide_number == 3:  # Strategic Implications slide
        with st.expander("Market Occupancy Heatmap", expanded=True):
            fig = create_occupancy_heatmap(occupancy_df)
            st.plotly_chart(fig, use_container_width=True)
            
    elif slide_number == 4:  # Conclusions slide
        with st.expander("Recovery Sunburst Visualization", expanded=True):
            fig = create_sunburst(recovery_df)
            st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main() 