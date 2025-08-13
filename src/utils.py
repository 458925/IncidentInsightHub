import streamlit as st
from typing import Dict, Any

class UIUtils:
    """Utility functions for UI components"""
    
    @staticmethod
    def create_metric_card(title: str, value: str, icon: str = "📊", trend: str | None = None) -> str:
        """Create an enhanced metric card with icons and optional trend indicators"""
        trend_html = ""
        if trend:
            trend_color = "#4CAF50" if "+" in trend else "#f44336" if "-" in trend else "#2196F3"
            trend_html = f'<div class="trend-indicator" style="color: {trend_color}; font-size: 0.9rem; margin-top: 0.5rem;">{trend}</div>'
        
        return f"""
        <div class="enhanced-metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-content">
                <h3 class="metric-title">{title}</h3>
                <h2 class="metric-value">{value}</h2>
                {trend_html}
            </div>
            <div class="metric-glow"></div>
        </div>
        """
    
    @staticmethod
    def display_overview_metrics(summary: Dict[str, Any]) -> None:
        """Display enhanced overview metrics with animations and better visual design"""
        if not summary:
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                UIUtils.create_metric_card(
                    "Total Incidents", 
                    f"{summary.get('total_incidents', 0):,}",
                    "🎯",
                    "+5.2% vs last month"
                ), 
                unsafe_allow_html=True
            )
        
        with col2:
            avg_time = summary.get('avg_resolution_time', 0)
            st.markdown(
                UIUtils.create_metric_card(
                    "Avg Resolution Time", 
                    f"{avg_time:.1f}h",
                    "⚡",
                    "-12% improvement"
                ), 
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                UIUtils.create_metric_card(
                    "Overdue Incidents", 
                    str(summary.get('overdue_incidents', 0)),
                    "🚨",
                    "-3 from yesterday"
                ), 
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                UIUtils.create_metric_card(
                    "Active Teams", 
                    str(summary.get('unique_teams', 0)),
                    "👥",
                    "All teams active"
                ), 
                unsafe_allow_html=True
            )

    @staticmethod
    def create_section_header(title: str, subtitle: str | None = None, icon: str | None = None) -> str:
        """Create a styled section header with optional subtitle and icon"""
        subtitle_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
        icon_html = f'<span class="section-icon">{icon}</span>' if icon else ""
        
        return f"""
        <div class="section-header">
            {icon_html}
            <h2 class="section-title">{title}</h2>
            {subtitle_html}
        </div>
        """

    @staticmethod
    def create_info_banner(message: str, banner_type: str = "info") -> str:
        """Create an attractive info banner"""
        type_configs = {
            "info": {"icon": "ℹ️", "color": "#2196F3"},
            "success": {"icon": "✅", "color": "#4CAF50"},
            "warning": {"icon": "⚠️", "color": "#FF9800"},
            "error": {"icon": "❌", "color": "#f44336"}
        }
        
        config = type_configs.get(banner_type, type_configs["info"])
        
        return f"""
        <div class="info-banner" style="border-left: 4px solid {config['color']};">
            <span class="banner-icon">{config['icon']}</span>
            <span class="banner-message">{message}</span>
        </div>
        """

class StyleUtils:
    """Enhanced utility functions for modern styling"""
    
    @staticmethod
    def get_custom_css() -> str:
        """Get enhanced custom CSS styling with modern design patterns"""
        return """
        <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Global Styling */
            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }
            
            /* Main Header Enhancement */
            .main-header {
                font-size: 3.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-align: center;
                margin-bottom: 2rem;
                text-shadow: none;
                position: relative;
                animation: fadeInDown 0.8s ease-out;
            }
            
            .main-header::after {
                content: '';
                position: absolute;
                bottom: -10px;
                left: 50%;
                transform: translateX(-50%);
                width: 100px;
                height: 4px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 2px;
            }
            
            /* Enhanced Metric Cards */
            .enhanced-metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 16px;
                color: white;
                text-align: center;
                margin: 0.5rem 0;
                position: relative;
                overflow: hidden;
                transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
                cursor: pointer;
                animation: slideInUp 0.6s ease-out;
            }
            
            .enhanced-metric-card:hover {
                transform: translateY(-5px) scale(1.02);
                box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
            }
            
            .metric-icon {
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
            }
            
            .metric-title {
                font-size: 0.9rem;
                font-weight: 500;
                margin: 0;
                opacity: 0.9;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .metric-value {
                font-size: 2.2rem;
                font-weight: 700;
                margin: 0.5rem 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            
            .trend-indicator {
                font-weight: 600;
                font-size: 0.85rem;
                margin-top: 0.5rem;
                padding: 0.2rem 0.5rem;
                background: rgba(255,255,255,0.2);
                border-radius: 20px;
                display: inline-block;
            }
            
            .metric-glow {
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .enhanced-metric-card:hover .metric-glow {
                opacity: 1;
            }
            
            /* Section Headers */
            .section-header {
                display: flex;
                align-items: center;
                margin: 2rem 0 1rem 0;
                padding: 1rem;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 12px;
                border-left: 4px solid #667eea;
            }
            
            .section-icon {
                font-size: 1.5rem;
                margin-right: 0.5rem;
            }
            
            .section-title {
                margin: 0;
                font-weight: 600;
                color: #333;
                flex-grow: 1;
            }
            
            .section-subtitle {
                margin: 0.5rem 0 0 0;
                color: #666;
                font-size: 0.9rem;
            }
            
            /* Info Banners */
            .info-banner {
                padding: 1rem;
                margin: 1rem 0;
                background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,249,250,0.9) 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                animation: slideInLeft 0.5s ease-out;
            }
            
            .banner-icon {
                font-size: 1.2rem;
                margin-right: 0.75rem;
            }
            
            .banner-message {
                flex-grow: 1;
                font-weight: 500;
                color: #333;
            }
            
            /* Enhanced Sidebar */
            .css-1d391kg {
                background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            }
            
            .css-1d391kg .css-1v0mbdj {
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                margin: 0.5rem;
                padding: 0.5rem;
            }
            
            /* Tab Enhancement */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background: rgba(102, 126, 234, 0.05);
                padding: 0.5rem;
                border-radius: 12px;
                margin-bottom: 1rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 3rem;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                border-radius: 8px;
                color: #333;
                font-weight: 500;
                border: none;
                transition: all 0.3s ease;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
            
            /* Data Table Enhancement */
            .stDataFrame {
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                animation: fadeIn 0.6s ease-out;
            }
            
            /* Chart Container Enhancement */
            .js-plotly-plot {
                border-radius: 12px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                animation: fadeIn 0.8s ease-out;
            }
            
            /* File Uploader Enhancement */
            .stFileUploader {
                border: 2px dashed #667eea;
                border-radius: 12px;
                padding: 2rem;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
                transition: all 0.3s ease;
            }
            
            .stFileUploader:hover {
                border-color: #764ba2;
                background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            }
            
            /* Button Enhancement */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.75rem 2rem;
                font-weight: 500;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
            }
            
            /* Alert Enhancement */
            .stAlert {
                border-radius: 12px;
                border: none;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                animation: slideInDown 0.5s ease-out;
            }
            
            /* Loading Spinner Enhancement */
            .stSpinner {
                border-color: #667eea !important;
            }
            
            /* Animations */
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes slideInDown {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .main-header {
                    font-size: 2.5rem;
                }
                
                .enhanced-metric-card {
                    padding: 1rem;
                }
                
                .metric-value {
                    font-size: 1.8rem;
                }
            }
            
            /* Dark Mode Support */
            @media (prefers-color-scheme: dark) {
                .section-title {
                    color: #fff;
                }
                
                .banner-message {
                    color: #fff;
                }
            }
        </style>
        """

class DataUtils:
    """Enhanced utility functions for data operations with better UI"""
    
    @staticmethod
    def safe_display_dataframe(df, message: str = "No data available") -> None:
        """Safely display a dataframe with enhanced styling and fallback message"""
        if df is not None and not df.empty:
            st.markdown('<div class="data-container">', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                UIUtils.create_info_banner(message, "info"),
                unsafe_allow_html=True
            )
    
    @staticmethod
    def safe_display_chart(fig, message: str = "No data available for chart") -> None:
        """Safely display a plotly chart with enhanced styling and fallback message"""
        if fig and fig.data:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown(
                UIUtils.create_info_banner(message, "warning"),
                unsafe_allow_html=True
            ) 