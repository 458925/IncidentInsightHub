import streamlit as st
import sys
import os

# Add src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Initialize logging first
from src.logger_config import setup_logger, get_logger
logger = setup_logger("IncidentInsightHub", "INFO")

from src.data_processor import DataProcessor
from src.analyzers import (
    RecurringIssuesAnalyzer, 
    SLAAnalyzer, 
    TeamAnalyzer, 
    TechDebtAnalyzer, 
    TrendAnalyzer
)
from src.visualizations import ChartGenerator
from src.utils import UIUtils, StyleUtils, DataUtils

# Set page configuration
st.set_page_config(
    page_title="Incident Insight Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def create_welcome_screen():
    """Create an enhanced welcome screen with better visual design"""
    
    # Welcome message with enhanced styling
    st.markdown(
        UIUtils.create_info_banner(
            "👋 Welcome! Upload your Excel files using the sidebar to begin comprehensive incident analysis.", 
            "info"
        ), 
        unsafe_allow_html=True
    )
    
    # Feature showcase
    st.markdown(
        UIUtils.create_section_header(
            "🎯 What this tool analyzes", 
            "Comprehensive incident management and analysis capabilities",
            "🔍"
        ), 
        unsafe_allow_html=True
    )
    
    # Create feature cards in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <h4 style="color: #667eea; margin-bottom: 1rem;">📊 Advanced Analytics</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li style="margin-bottom: 0.5rem;"><strong>Recurring Issues:</strong> Pareto analysis of frequent problems</li>
                <li style="margin-bottom: 0.5rem;"><strong>SLA Performance:</strong> Service level agreement compliance tracking</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <h4 style="color: #667eea; margin-bottom: 1rem;">👥 Team Intelligence</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li style="margin-bottom: 0.5rem;"><strong>Team Trends:</strong> Performance and workload distribution</li>
                <li style="margin-bottom: 0.5rem;"><strong>Tech Debt:</strong> Technical debt patterns and indicators</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Data format information
    st.markdown(
        UIUtils.create_section_header(
            "📋 Expected Excel Format", 
            "Your data should contain these columns for optimal analysis",
            "📁"
        ), 
        unsafe_allow_html=True
    )
    
    # Format specification in a nice layout
    format_cols = st.columns(3)
    
    with format_cols[0]:
        st.markdown("""
        **🆔 Identification:**
        - Incident ID
        - Title/Description
        - Category/Type
        """)
    
    with format_cols[1]:
        st.markdown("""
        **📊 Classification:**
        - Priority/Severity
        - Status
        - Assigned Team
        """)
    
    with format_cols[2]:
        st.markdown("""
        **⏰ Timestamps:**
        - Created Date
        - Resolved Date
        - Resolution Time
        """)
    
    st.markdown(
        UIUtils.create_info_banner(
            "💡 Pro Tip: The tool automatically maps common column name variations, so don't worry about exact naming!", 
            "success"
        ), 
        unsafe_allow_html=True
    )

def main():
    """
    Main application function that orchestrates the entire Streamlit interface
    
    This function handles:
    - UI setup and styling
    - File upload and processing
    - Data analysis coordination
    - Results display across multiple tabs
    """
    logger.info("Starting Incident Insight Hub application")
    
    # Apply custom CSS styling for professional appearance
    st.markdown(StyleUtils.get_custom_css(), unsafe_allow_html=True)
    
    # Display main application header
    st.markdown('<h1 class="main-header">📊 Incident Insight Hub</h1>', unsafe_allow_html=True)
    st.markdown("### 🔍 Comprehensive Incident Analysis & Debt Management Tool")
    
    # Initialize data processor in session state (persists across reruns)
    if 'data_processor' not in st.session_state:
        st.session_state.data_processor = DataProcessor()
    
    # Enhanced sidebar design
    with st.sidebar:
        st.markdown(
            UIUtils.create_section_header("📁 Data Upload", "", "📤"), 
            unsafe_allow_html=True
        )
        
        uploaded_files = st.file_uploader(
            "Upload Excel Files",
            accept_multiple_files=True,        # Allow multiple file selection
            type=['xlsx', 'xls'],             # Restrict to Excel formats
            help="📎 Upload one or more Excel files containing incident data"
        )
        
        if uploaded_files:
            # Show file information
            st.markdown("**📋 Selected Files:**")
            for file in uploaded_files:
                file_size = len(file.getvalue()) / 1024  # Size in KB
                st.markdown(f"• {file.name} ({file_size:.1f} KB)")
            
            if st.button("🔄 Process Files", type="primary"):
                logger.info(f"User initiated file processing for {len(uploaded_files)} files")
                
                # Enhanced loading with progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner("🔄 Loading and processing files..."):
                    processor = st.session_state.data_processor
                    
                    status_text.text("📂 Loading files...")
                    progress_bar.progress(25)
                    
                    if processor.load_excel_files(uploaded_files):
                        status_text.text("🔧 Processing data...")
                        progress_bar.progress(75)
                        
                        if processor.preprocess_data():
                            progress_bar.progress(100)
                            status_text.text("✅ Processing complete!")
                            logger.info("File processing completed successfully")
                            st.success("✅ Files processed successfully!")
                            st.session_state.data_loaded = True
                            st.balloons()  # Celebration effect
                        else:
                            logger.error("Data preprocessing failed")
                            st.error("❌ Error processing data")
                    else:
                        logger.error("File loading failed")
                        st.error("❌ Error loading files")
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
    
    # Main content
    if hasattr(st.session_state, 'data_loaded') and st.session_state.data_loaded:
        processor = st.session_state.data_processor
        data = processor.processed_data
        
        # Ensure data is valid before proceeding
        if data is None or data.empty:
            logger.warning("No processed data available for analysis")
            st.error("No data available for analysis")
            return
        
        logger.info(f"Starting analysis with {len(data)} incident records")
        
        # Display high-level metrics dashboard with enhanced header
        st.markdown(
            UIUtils.create_section_header(
                "📈 Overview Dashboard", 
                f"Real-time insights from {len(data):,} incident records",
                "📊"
            ), 
            unsafe_allow_html=True
        )
        
        summary = processor.get_data_summary()              # Get summary statistics
        UIUtils.display_overview_metrics(summary)          # Display as enhanced metric cards
        
        # Create tabs for different analysis views with enhanced styling
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔄 Recurring Issues",   # Pareto analysis of frequent problems
            "⏰ SLA Performance",    # Service level agreement compliance
            "👥 Team Trends",        # Team performance over time
            "🔧 Tech Debt",         # Technical debt indicators
            "📊 Visual Analytics"   # Additional charts and visualizations
        ])
        
        # Tab 1: Recurring Issues Analysis
        with tab1:
            st.markdown(
                UIUtils.create_section_header(
                    "Top Recurring Issues", 
                    "Identify patterns using Pareto analysis (80/20 rule)",
                    "🔄"
                ), 
                unsafe_allow_html=True
            )
            
            # Create analyzer instance and get recurring issues data
            recurring_analyzer = RecurringIssuesAnalyzer(data)
            recurring_issues = recurring_analyzer.get_top_recurring_issues()
            
            # Display results table with safe error handling
            DataUtils.safe_display_dataframe(recurring_issues, "No recurring issues data available")
            
            # Generate and display Pareto chart if data exists
            if recurring_issues is not None and not recurring_issues.empty:
                fig = ChartGenerator.create_pareto_chart(recurring_issues, "Pareto Chart - Recurring Issues")
                DataUtils.safe_display_chart(fig)
        
        # SLA Performance Tab
        with tab2:
            st.markdown(
                UIUtils.create_section_header(
                    "SLA Performance Analysis", 
                    "Service Level Agreement compliance and breach monitoring",
                    "⏰"
                ), 
                unsafe_allow_html=True
            )
            
            sla_analyzer = SLAAnalyzer(data)
            sla_analysis = sla_analyzer.analyze_sla_performance()
            
            DataUtils.safe_display_dataframe(sla_analysis, "No SLA performance data available")
            
            if sla_analysis is not None and not sla_analysis.empty:
                fig = ChartGenerator.create_sla_performance_chart(sla_analysis)
                DataUtils.safe_display_chart(fig)
        
        # Team Trends Tab
        with tab3:
            st.markdown(
                UIUtils.create_section_header(
                    "Backend Team Trends", 
                    "Team performance comparison and workload distribution",
                    "👥"
                ), 
                unsafe_allow_html=True
            )
            
            team_analyzer = TeamAnalyzer(data)
            team_trends = team_analyzer.analyze_team_trends()
            
            if team_trends is not None and not team_trends.empty:
                # Team trends over time
                fig1 = ChartGenerator.create_team_incident_trends(team_trends)
                DataUtils.safe_display_chart(fig1, "No team trends data available")
                
                # Team resolution time comparison
                fig2 = ChartGenerator.create_team_resolution_chart(data)
                DataUtils.safe_display_chart(fig2, "No team resolution data available")
                
                DataUtils.safe_display_dataframe(team_trends, "No team trends data available")
            else:
                st.markdown(
                    UIUtils.create_info_banner("No team trends data available", "info"),
                    unsafe_allow_html=True
                )
        
        # Tech Debt Tab
        with tab4:
            st.markdown(
                UIUtils.create_section_header(
                    "Technical Debt Indicators", 
                    "Pattern-based detection and trend analysis of technical debt",
                    "🔧"
                ), 
                unsafe_allow_html=True
            )
            
            debt_analyzer = TechDebtAnalyzer(data)
            debt_analysis = debt_analyzer.calculate_tech_debt_indicators()
            
            if debt_analysis:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Tech Debt Percentage", 
                        f"{debt_analysis['total_debt_percentage']:.1f}%"
                    )
                
                with col2:
                    if not debt_analysis['debt_by_team'].empty:
                        top_debt_team = debt_analysis['debt_by_team'].iloc[0]
                        st.metric(
                            "Highest Debt Team", 
                            f"{top_debt_team['assigned_team']} ({top_debt_team['debt_count']} incidents)"
                        )
                
                # Charts
                if not debt_analysis['debt_trend'].empty:
                    fig1 = ChartGenerator.create_tech_debt_trend_chart(debt_analysis['debt_trend'])
                    DataUtils.safe_display_chart(fig1)
                
                if not debt_analysis['debt_by_team'].empty:
                    fig2 = ChartGenerator.create_debt_by_team_pie(debt_analysis['debt_by_team'])
                    DataUtils.safe_display_chart(fig2)
            else:
                st.markdown(
                    UIUtils.create_info_banner("No technical debt data available", "info"),
                    unsafe_allow_html=True
                )
        
        # Visual Analytics Tab
        with tab5:
            st.markdown(
                UIUtils.create_section_header(
                    "Visual Analytics Dashboard", 
                    "Comprehensive charts and trend analysis",
                    "📊"
                ), 
                unsafe_allow_html=True
            )
            
            trend_analyzer = TrendAnalyzer(data)
            
            # Monthly trends
            monthly_trends = trend_analyzer.get_monthly_trends()
            if monthly_trends is not None:
                fig1 = ChartGenerator.create_monthly_trends_chart(monthly_trends)
                DataUtils.safe_display_chart(fig1)
            
            # Category distribution
            category_dist = trend_analyzer.get_category_distribution()
            if category_dist is not None:
                fig2 = ChartGenerator.create_category_pie_chart(category_dist)
                DataUtils.safe_display_chart(fig2)
            
            # Priority analysis
            fig3 = ChartGenerator.create_priority_box_plot(data)
            DataUtils.safe_display_chart(fig3)
    
    else:
        # Enhanced welcome screen
        create_welcome_screen()

if __name__ == "__main__":
    main() 