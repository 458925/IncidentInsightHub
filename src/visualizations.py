import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional
from .logger_config import get_logger
import numpy as np

class ChartGenerator:
    """Generates enhanced charts and visualizations with modern styling"""
    
    # Enhanced color palettes for consistent theming
    PRIMARY_COLORS = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
    GRADIENT_COLORS = ['#667eea', '#764ba2', '#8b5fbf', '#a855c5', '#c44bc9', '#e041cd']
    
    @staticmethod
    def get_base_layout():
        """Get base layout configuration for all charts"""
        return {
            'font': {'family': 'Inter, sans-serif', 'size': 12},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
            'title': {
                'font': {'size': 18, 'color': '#333', 'family': 'Inter, sans-serif'},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'showgrid': True,
                'gridcolor': 'rgba(0,0,0,0.1)',
                'showline': True,
                'linecolor': 'rgba(0,0,0,0.2)',
                'title': {'font': {'size': 14, 'color': '#666'}}
            },
            'yaxis': {
                'showgrid': True,
                'gridcolor': 'rgba(0,0,0,0.1)',
                'showline': True,
                'linecolor': 'rgba(0,0,0,0.2)',
                'title': {'font': {'size': 14, 'color': '#666'}}
            },
            'hoverlabel': {
                'bgcolor': 'white',
                'bordercolor': '#667eea',
                'font': {'size': 12, 'color': '#333'}
            }
        }
    
    @staticmethod
    def create_pareto_chart(data: pd.DataFrame, title: str = "Pareto Chart") -> go.Figure:
        """Create an enhanced Pareto chart with modern styling"""
        if data is None or data.empty:
            return go.Figure()
        
        # Sort data by frequency
        sorted_data = data.sort_values('frequency', ascending=False)
        
        # Calculate cumulative percentage
        total = sorted_data['frequency'].sum()
        sorted_data['cumulative_percentage'] = (sorted_data['frequency'].cumsum() / total) * 100
        
        # Create the chart with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Enhanced bar chart for frequency
        fig.add_trace(
            go.Bar(
                x=list(range(len(sorted_data))),
                y=sorted_data['frequency'].tolist(),
                name="Frequency",
                marker=dict(
                    color=ChartGenerator.PRIMARY_COLORS[0],
                    line=dict(color='rgba(255,255,255,0.8)', width=1)
                ),
                hovertemplate="<b>%{text}</b><br>Frequency: %{y}<br>Percentage: %{customdata:.1f}%<extra></extra>",
                text=[f"{cat} - {title}" for cat, title in zip(sorted_data['category'], sorted_data['title'])],
                customdata=sorted_data['frequency'] / total * 100
            ),
            secondary_y=False,
        )
        
        # Enhanced line chart for cumulative percentage
        fig.add_trace(
            go.Scatter(
                x=list(range(len(sorted_data))),
                y=sorted_data['cumulative_percentage'].tolist(),
                mode='lines+markers',
                name="Cumulative %",
                line=dict(color=ChartGenerator.PRIMARY_COLORS[1], width=3),
                marker=dict(size=8, color=ChartGenerator.PRIMARY_COLORS[1], 
                          line=dict(color='white', width=2)),
                hovertemplate="Cumulative: %{y:.1f}%<extra></extra>"
            ),
            secondary_y=True,
        )
        
        # Add 80% line
        fig.add_hline(y=80, line_dash="dash", line_color="red", 
                     annotation_text="80% Rule", secondary_y=True)
        
        # Set x-axis properties
        fig.update_xaxes(title_text="Issue Rank", tickmode='linear')
        
        # Set y-axes titles
        fig.update_yaxes(title_text="<b>Frequency</b>", secondary_y=False, color=ChartGenerator.PRIMARY_COLORS[0])
        fig.update_yaxes(title_text="<b>Cumulative Percentage (%)</b>", secondary_y=True, color=ChartGenerator.PRIMARY_COLORS[1])
        
        # Update layout with enhanced styling
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = f"📊 {title}"
        fig.update_layout(
            **base_layout,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @staticmethod
    def create_sla_performance_chart(sla_data: pd.DataFrame) -> go.Figure:
        """Create enhanced SLA performance chart"""
        if sla_data is None or sla_data.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # SLA Met bars
        fig.add_trace(go.Bar(
            name='SLA Met',
            x=sla_data['Priority'],
            y=sla_data['SLA_Met'],
            marker_color=ChartGenerator.PRIMARY_COLORS[0],
            hovertemplate="<b>%{x}</b><br>SLA Met: %{y}<br>Percentage: %{customdata:.1f}%<extra></extra>",
            customdata=sla_data['SLA_Percentage']
        ))
        
        # SLA Missed bars
        sla_data['SLA_Missed'] = sla_data['Total_Incidents'] - sla_data['SLA_Met']
        fig.add_trace(go.Bar(
            name='SLA Missed',
            x=sla_data['Priority'],
            y=sla_data['SLA_Missed'],
            marker_color=ChartGenerator.PRIMARY_COLORS[3],
            hovertemplate="<b>%{x}</b><br>SLA Missed: %{y}<extra></extra>"
        ))
        
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = "⏰ SLA Performance Analysis"
        base_layout['xaxis']['title']['text'] = "Priority Level"
        base_layout['yaxis']['title']['text'] = "Number of Incidents"
        base_layout['barmode'] = 'stack'
        fig.update_layout(**base_layout)
        
        return fig
    
    @staticmethod
    def create_team_incident_trends(team_trends: pd.DataFrame) -> go.Figure:
        """Create enhanced team incident trends chart"""
        if team_trends is None or team_trends.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        teams = team_trends['assigned_team'].unique()
        colors = ChartGenerator.PRIMARY_COLORS[:len(teams)]
        
        for i, team in enumerate(teams):
            team_data = team_trends[team_trends['assigned_team'] == team]
            fig.add_trace(go.Scatter(
                x=team_data['month_year'],
                y=team_data['total_incidents'],
                mode='lines+markers',
                name=team,
                line=dict(color=colors[i % len(colors)], width=3),
                marker=dict(size=8, color=colors[i % len(colors)], 
                          line=dict(color='white', width=2)),
                hovertemplate="<b>%{fullData.name}</b><br>Month: %{x}<br>Incidents: %{y}<extra></extra>"
            ))
        
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = "👥 Team Incident Volume Over Time"
        base_layout['xaxis']['title']['text'] = "Month"
        base_layout['yaxis']['title']['text'] = "Number of Incidents"
        fig.update_layout(
            **base_layout,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @staticmethod
    def create_team_resolution_chart(data: pd.DataFrame) -> go.Figure:
        """Create enhanced team average resolution time chart"""
        if data is None or data.empty:
            return go.Figure()
        
        team_avg = data.groupby('assigned_team')['resolution_time'].mean().reset_index()
        team_avg = team_avg.sort_values('resolution_time', ascending=True)
        
        # Create gradient colors based on performance
        colors = []
        max_time = team_avg['resolution_time'].max()
        for time in team_avg['resolution_time']:
            intensity = time / max_time
            if intensity < 0.5:
                colors.append('#4CAF50')  # Good performance - green
            elif intensity < 0.8:
                colors.append('#FF9800')  # Average performance - orange  
            else:
                colors.append('#f44336')  # Poor performance - red
        
        fig = go.Figure(data=[
            go.Bar(
                x=team_avg['assigned_team'],
                y=team_avg['resolution_time'],
                marker=dict(
                    color=colors,
                    line=dict(color='rgba(255,255,255,0.8)', width=1)
                ),
                hovertemplate="<b>%{x}</b><br>Avg Resolution: %{y:.1f} hours<extra></extra>"
            )
        ])
        
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = "⚡ Average Resolution Time by Team"
        base_layout['xaxis']['title']['text'] = "Team"
        base_layout['xaxis']['tickangle'] = 45
        base_layout['yaxis']['title']['text'] = "Average Resolution Time (hours)"
        fig.update_layout(**base_layout)
        
        return fig
    
    @staticmethod
    def create_monthly_trends_chart(monthly_data: pd.DataFrame) -> go.Figure:
        """Create enhanced monthly incident trends chart"""
        if monthly_data is None or monthly_data.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Area chart for better visual impact
        fig.add_trace(go.Scatter(
            x=monthly_data['month_year'],
            y=monthly_data['incident_count'],
            mode='lines+markers',
            fill='tonexty',
            line=dict(color=ChartGenerator.PRIMARY_COLORS[0], width=3),
            marker=dict(size=10, color=ChartGenerator.PRIMARY_COLORS[0], 
                      line=dict(color='white', width=2)),
            fillcolor=f'rgba(102, 126, 234, 0.2)',
            name='Incidents',
            hovertemplate="<b>%{x}</b><br>Incidents: %{y}<extra></extra>"
        ))
        
        # Add trend line
        if len(monthly_data) > 1:
            z = np.polyfit(range(len(monthly_data)), monthly_data['incident_count'], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=monthly_data['month_year'],
                y=p(range(len(monthly_data))),
                mode='lines',
                line=dict(color=ChartGenerator.PRIMARY_COLORS[1], width=2, dash='dash'),
                name='Trend',
                hovertemplate="Trend: %{y:.0f}<extra></extra>"
            ))
        
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = "📈 Monthly Incident Trends"
        base_layout['xaxis']['title']['text'] = "Month"
        base_layout['yaxis']['title']['text'] = "Number of Incidents"
        fig.update_layout(**base_layout)
        
        return fig
    
    @staticmethod
    def create_category_pie_chart(category_data: pd.DataFrame) -> go.Figure:
        """Create enhanced category distribution pie chart"""
        if category_data is None or category_data.empty:
            return go.Figure()
        
        fig = go.Figure(data=[go.Pie(
            labels=category_data['category'],
            values=category_data['count'],
            hole=.4,  # Donut chart for modern look
            marker=dict(
                colors=ChartGenerator.GRADIENT_COLORS,
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
        )])
        
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = "🎯 Incident Distribution by Category"
        fig.update_layout(
            **base_layout,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        
        return fig
    
    @staticmethod
    def create_priority_box_plot(data: pd.DataFrame) -> go.Figure:
        """Create enhanced priority vs resolution time box plot"""
        if data is None or data.empty:
            return go.Figure()
        
        priorities = data['priority'].unique()
        colors = ChartGenerator.PRIMARY_COLORS[:len(priorities)]
        
        fig = go.Figure()
        
        for i, priority in enumerate(priorities):
            priority_data = data[data['priority'] == priority]['resolution_time']
            fig.add_trace(go.Box(
                y=priority_data,
                name=priority,
                marker=dict(color=colors[i % len(colors)]),
                boxmean=True,  # Show mean line
                hovertemplate="<b>%{fullData.name}</b><br>Resolution Time: %{y:.1f}h<extra></extra>"
            ))
        
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = "📊 Resolution Time Distribution by Priority"
        base_layout['xaxis']['title']['text'] = "Priority Level"
        base_layout['yaxis']['title']['text'] = "Resolution Time (hours)"
        fig.update_layout(**base_layout)
        
        return fig
    
    @staticmethod
    def create_tech_debt_trend_chart(debt_data: pd.DataFrame) -> go.Figure:
        """Create tech debt trend chart"""
        if debt_data is None or debt_data.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=debt_data['month_year'],
            y=debt_data['debt_incidents'],
            mode='lines+markers',
            fill='tonexty',
            line=dict(color=ChartGenerator.PRIMARY_COLORS[3], width=3),
            marker=dict(size=10, color=ChartGenerator.PRIMARY_COLORS[3], 
                      line=dict(color='white', width=2)),
            fillcolor=f'rgba(245, 87, 108, 0.2)',
            name='Tech Debt Incidents',
            hovertemplate="<b>%{x}</b><br>Tech Debt: %{y}<extra></extra>"
        ))
        
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = "🔧 Technical Debt Trend Over Time"
        base_layout['xaxis']['title']['text'] = "Month"
        base_layout['yaxis']['title']['text'] = "Tech Debt Incidents"
        fig.update_layout(**base_layout)
        
        return fig
    
    @staticmethod
    def create_debt_by_team_pie(debt_data: pd.DataFrame) -> go.Figure:
        """Create tech debt by team pie chart"""
        if debt_data is None or debt_data.empty:
            return go.Figure()
        
        fig = go.Figure(data=[go.Pie(
            labels=debt_data['assigned_team'],
            values=debt_data['debt_count'],
            hole=.4,
            marker=dict(
                colors=ChartGenerator.GRADIENT_COLORS,
                line=dict(color='white', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>Tech Debt: %{value}<br>Percentage: %{percent}<extra></extra>"
        )])
        
        base_layout = ChartGenerator.get_base_layout()
        base_layout['title']['text'] = "🔧 Technical Debt Distribution by Team"
        fig.update_layout(
            **base_layout,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle", 
                y=0.5,
                xanchor="left",
                x=1.05
            )
        )
        
        return fig 