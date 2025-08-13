import pandas as pd
import numpy as np
from typing import Optional, Dict, Any, List
from .logger_config import get_logger

class RecurringIssuesAnalyzer:
    """
    Analyzes recurring issues and patterns in incident data
    
    This class identifies which types of incidents occur most frequently,
    helping teams focus on preventing the most common problems.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize analyzer with incident data
        
        Args:
            data: Preprocessed DataFrame containing incident records
        """
        self.data = data                                    # Store incident data for analysis
        self.logger = get_logger("RecurringIssuesAnalyzer") # Logger for this analyzer
    
    def get_top_recurring_issues(self, top_n: int = 10) -> Optional[pd.DataFrame]:
        """Identify top recurring issues"""
        self.logger.info(f"Analyzing top {top_n} recurring issues")
        
        if self.data is None or self.data.empty:
            self.logger.warning("No data available for recurring issues analysis")
            return None
        
        try:
            recurring_issues = self.data.groupby(['category', 'title']).agg({
                'incident_id': 'count',
                'resolution_time': 'mean',
                'assigned_team': lambda x: x.mode().iloc[0] if not x.empty else 'Unknown'
            }).reset_index()
            
            recurring_issues = recurring_issues.rename(columns={'incident_id': 'frequency'})
            recurring_issues = recurring_issues.sort_values('frequency', ascending=False).head(top_n)
            
            self.logger.info(f"Found {len(recurring_issues)} recurring issue patterns")
            return recurring_issues
            
        except Exception as e:
            self.logger.error(f"Error analyzing recurring issues: {str(e)}", exc_info=True)
            return None

class SLAAnalyzer:
    """
    Analyzes Service Level Agreement (SLA) performance metrics
    
    This class evaluates how well teams meet resolution time targets
    for different priority levels of incidents.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize SLA analyzer with incident data and threshold definitions
        
        Args:
            data: Preprocessed DataFrame containing incident records
        """
        self.data = data                            # Store incident data for analysis
        self.logger = get_logger("SLAAnalyzer")     # Logger for this analyzer
        # Define SLA resolution time thresholds by priority (in hours)
        self.sla_thresholds = {
            'Critical': 4,   # Critical incidents must be resolved within 4 hours
            'High': 8,       # High priority incidents within 8 hours
            'Medium': 24,    # Medium priority incidents within 24 hours
            'Low': 72        # Low priority incidents within 72 hours (3 days)
        }
    
    def analyze_sla_performance(self) -> Optional[pd.DataFrame]:
        """
        Analyze SLA performance by priority level
        
        Returns:
            DataFrame with SLA metrics for each priority level, or None if no data
        """
        # Check if we have data to analyze
        if self.data is None or self.data.empty:
            return None
        
        sla_analysis = []
        
        # Calculate SLA metrics for each priority level
        for priority, threshold in self.sla_thresholds.items():
            # Filter incidents matching this priority (case-insensitive)
            priority_data = self.data[
                self.data['priority'].str.contains(priority, case=False, na=False)
            ]
            
            # Only analyze if we have incidents for this priority
            if len(priority_data) > 0:
                total_incidents = len(priority_data)
                # Count incidents resolved within SLA threshold
                met_sla = len(priority_data[priority_data['resolution_time'] <= threshold])
                # Calculate percentage of incidents meeting SLA
                sla_percentage = (met_sla / total_incidents) * 100
                # Calculate average resolution time for this priority
                avg_resolution_time = priority_data['resolution_time'].mean()
                
                # Store metrics for this priority level
                sla_analysis.append({
                    'Priority': priority,
                    'Total_Incidents': total_incidents,
                    'SLA_Met': met_sla,
                    'SLA_Percentage': sla_percentage,
                    'Avg_Resolution_Time': avg_resolution_time,
                    'SLA_Threshold': threshold
                })
        
        # Return results as DataFrame
        return pd.DataFrame(sla_analysis)

class TeamAnalyzer:
    """Analyzes team performance and trends"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def analyze_team_trends(self) -> Optional[pd.DataFrame]:
        """Analyze team performance over time"""
        if self.data is None or self.data.empty:
            return None
        
        team_analysis = self.data.groupby(['assigned_team', 'month_year']).agg({
            'incident_id': 'count',
            'resolution_time': 'mean',
            'is_overdue': 'sum'
        }).reset_index()
        
        team_analysis = team_analysis.rename(columns={
            'incident_id': 'total_incidents',
            'is_overdue': 'overdue_incidents'
        })
        
        team_analysis['overdue_percentage'] = (
            team_analysis['overdue_incidents'] / team_analysis['total_incidents'] * 100
        )
        
        return team_analysis
    
    def get_team_performance_summary(self) -> Optional[pd.DataFrame]:
        """Get overall team performance summary"""
        if self.data is None or self.data.empty:
            return None
        
        return self.data.groupby('assigned_team').agg({
            'incident_id': 'count',
            'resolution_time': 'mean',
            'is_overdue': 'sum'
        }).reset_index().rename(columns={
            'incident_id': 'total_incidents',
            'is_overdue': 'overdue_incidents'
        })

class TechDebtAnalyzer:
    """Analyzes technical debt indicators"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.logger = get_logger("TechDebtAnalyzer")
        self.tech_debt_keywords = [
            'legacy', 'outdated', 'deprecated', 'technical debt', 'refactor',
            'workaround', 'hack', 'temporary fix', 'hotfix', 'patch'
        ]
    
    def identify_tech_debt_incidents(self):
        """Identify incidents related to technical debt"""
        if self.data is None or self.data.empty:
            return pd.DataFrame()
        
        tech_debt_mask = self.data['title'].str.contains(
            '|'.join(self.tech_debt_keywords), case=False, na=False
        )
        
        return self.data[tech_debt_mask]
    
    def calculate_tech_debt_indicators(self) -> Dict[str, Any]:
        """Calculate comprehensive tech debt metrics"""
        tech_debt_incidents = self.identify_tech_debt_incidents()
        
        total_incidents = len(self.data)
        debt_incidents = len(tech_debt_incidents)
        debt_percentage = (debt_incidents / total_incidents) * 100 if total_incidents > 0 else 0
        
        # Debt by team
        debt_by_team = pd.DataFrame()
        if not tech_debt_incidents.empty:
            debt_by_team = tech_debt_incidents.groupby('assigned_team').size().reset_index()
            debt_by_team.columns = ['assigned_team', 'debt_count']
        
        # Monthly debt trend
        debt_trend = pd.DataFrame()
        if not tech_debt_incidents.empty:
            debt_trend = tech_debt_incidents.groupby('month_year').size().reset_index()
            debt_trend.columns = ['month_year', 'debt_incidents']
        
        return {
            'total_debt_percentage': debt_percentage,
            'debt_by_team': debt_by_team,
            'debt_trend': debt_trend,
            'debt_incidents': tech_debt_incidents
        }

class TrendAnalyzer:
    """Analyzes trends and patterns in incident data"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def get_monthly_trends(self) -> Optional[pd.DataFrame]:
        """Get monthly incident trends"""
        if self.data is None or self.data.empty:
            return None
        
        monthly_data = self.data.groupby('month_year').size().reset_index()
        monthly_data.columns = ['month_year', 'incident_count']
        return monthly_data
    
    def get_category_distribution(self) -> Optional[pd.DataFrame]:
        """Get incident distribution by category"""
        if self.data is None or self.data.empty:
            return None
        
        category_dist = self.data['category'].value_counts().reset_index()
        category_dist.columns = ['category', 'count']
        return category_dist
    
    def get_priority_analysis(self) -> Optional[pd.DataFrame]:
        """Analyze incidents by priority"""
        if self.data is None or self.data.empty:
            return None
        
        return self.data.groupby('priority').agg({
            'incident_id': 'count',
            'resolution_time': ['mean', 'median', 'std']
        }).reset_index() 