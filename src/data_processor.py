import pandas as pd
import streamlit as st
from datetime import datetime
from typing import List, Optional, Dict, Any
from .logger_config import get_logger

class DataProcessor:
    """
    Handles Excel file loading and data preprocessing for incident analysis
    
    This class manages the entire data pipeline from raw Excel files to cleaned,
    standardized data ready for analysis.
    """
    
    def __init__(self):
        """Initialize data processor with empty data containers and logger"""
        self.raw_data = None          # Stores combined raw data from Excel files
        self.processed_data = None    # Stores cleaned and standardized data
        self.logger = get_logger("DataProcessor")  # Logger for this module
    
    def load_excel_files(self, uploaded_files: List) -> bool:
        """Load and combine multiple Excel files"""
        self.logger.info(f"Starting to load {len(uploaded_files)} Excel files")
        all_data = []
        
        for file in uploaded_files:
            try:
                self.logger.debug(f"Loading file: {file.name}")
                df = pd.read_excel(file, engine='openpyxl')
                df['source_file'] = file.name
                all_data.append(df)
                self.logger.info(f"Successfully loaded {file.name} with {len(df)} rows")
                st.success(f"✅ Successfully loaded: {file.name}")
            except Exception as e:
                self.logger.error(f"Error loading {file.name}: {str(e)}")
                st.error(f"❌ Error loading {file.name}: {str(e)}")
        
        if all_data:
            self.raw_data = pd.concat(all_data, ignore_index=True)
            self.logger.info(f"Combined data: {len(self.raw_data)} total rows from {len(all_data)} files")
            return True
        
        self.logger.warning("No data files were successfully loaded")
        return False
    
    def get_column_mappings(self) -> Dict[str, List[str]]:
        """
        Define standard column names and their common variations found in Excel files
        
        Returns:
            Dictionary mapping standard names to lists of possible column variations
        """
        return {
            # Unique identifier for each incident
            'incident_id': ['incident_id', 'id', 'ticket_id', 'case_id', 'incident_number'],
            # Brief description or title of the incident
            'title': ['title', 'summary', 'description', 'issue_title', 'incident_title'],
            # Type or category of the incident (e.g., Infrastructure, Application)
            'category': ['category', 'type', 'issue_type', 'incident_type'],
            # Urgency level (Critical, High, Medium, Low)
            'priority': ['priority', 'severity', 'impact'],
            # Current state (Open, Resolved, Closed, etc.)
            'status': ['status', 'state', 'current_status'],
            # When the incident was first reported
            'created_date': ['created_date', 'create_date', 'date_created', 'incident_date', 'created'],
            # When the incident was resolved/closed
            'resolved_date': ['resolved_date', 'resolution_date', 'closed_date', 'date_resolved'],
            # Team responsible for handling the incident
            'assigned_team': ['assigned_team', 'team', 'backend_team', 'responsible_team'],
            # Time taken to resolve (hours)
            'resolution_time': ['resolution_time', 'time_to_resolve', 'sla_time']
        }
    
    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names to consistent format across different Excel files
        
        Args:
            df: DataFrame with potentially varied column names
            
        Returns:
            DataFrame with standardized column names
        """
        column_mappings = self.get_column_mappings()
        standardized_columns = {}
        
        # Find matching columns for each standard name
        for standard_name, variations in column_mappings.items():
            for col in df.columns:
                # Case-insensitive matching against known variations
                if col.lower() in [v.lower() for v in variations]:
                    standardized_columns[col] = standard_name
                    break  # Use first match found
        
        # Apply column name changes
        return df.rename(columns=standardized_columns)
    
    def add_missing_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add default values for missing required columns to ensure data completeness
        
        Args:
            df: DataFrame that may be missing some required columns
            
        Returns:
            DataFrame with all required columns present
        """
        # Define columns that must be present for analysis
        required_columns = ['incident_id', 'title', 'category', 'priority', 'status', 
                          'created_date', 'resolved_date', 'assigned_team']
        
        for col in required_columns:
            if col not in df.columns:
                # Generate sequential IDs if incident_id is missing
                if col == 'incident_id':
                    df[col] = range(1, len(df) + 1)
                # Use 'Unknown' placeholder for text fields
                elif col in ['title', 'category', 'priority', 'status', 'assigned_team']:
                    df[col] = 'Unknown'
                # Use current timestamp for missing dates
                elif col in ['created_date', 'resolved_date']:
                    df[col] = datetime.now()
        
        return df
    
    def convert_date_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert date columns from various formats to standard pandas datetime
        
        Args:
            df: DataFrame with date columns in potentially different formats
            
        Returns:
            DataFrame with properly formatted datetime columns
        """
        date_columns = ['created_date', 'resolved_date']
        for col in date_columns:
            if col in df.columns:
                # Convert to datetime, handling various formats automatically
                # errors='coerce' converts invalid dates to NaT (Not a Time)
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    
    def calculate_derived_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate additional fields needed for analysis from existing data
        
        Args:
            df: DataFrame with basic incident data
            
        Returns:
            DataFrame with additional calculated fields for analysis
        """
        # Calculate resolution time in hours if not already present
        if 'resolution_time' not in df.columns:
            # Subtract created_date from resolved_date and convert to hours
            df['resolution_time'] = (df['resolved_date'] - df['created_date']).dt.total_seconds() / 3600
        
        # Add time-based grouping fields - convert to string to avoid JSON serialization issues
        df['month_year'] = df['created_date'].dt.strftime('%Y-%m')    # Format: "2024-01"
        df['week_year'] = df['created_date'].dt.strftime('%Y-W%U')   # Format: "2024-W05"
        
        # Create SLA compliance indicator (24 hours default threshold)
        df['is_overdue'] = df['resolution_time'] > 24  # Boolean: True if over 24 hours
        
        return df
    
    def preprocess_data(self) -> bool:
        """Main preprocessing pipeline"""
        if self.raw_data is None:
            self.logger.error("No raw data available for preprocessing")
            return False
        
        try:
            self.logger.info("Starting data preprocessing pipeline")
            df = self.raw_data.copy()
            
            # Apply preprocessing steps
            self.logger.debug("Standardizing column names")
            df = self.standardize_columns(df)
            
            self.logger.debug("Adding missing columns")
            df = self.add_missing_columns(df)
            
            self.logger.debug("Converting date columns")
            df = self.convert_date_columns(df)
            
            self.logger.debug("Calculating derived fields")
            df = self.calculate_derived_fields(df)
            
            self.processed_data = df
            self.logger.info(f"Data preprocessing completed successfully. Final dataset: {len(df)} rows, {len(df.columns)} columns")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during data preprocessing: {str(e)}", exc_info=True)
            st.error(f"Error during data preprocessing: {str(e)}")
            return False
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the processed data"""
        if self.processed_data is None:
            return {}
        
        return {
            'total_incidents': len(self.processed_data),
            'avg_resolution_time': self.processed_data['resolution_time'].mean(),
            'overdue_incidents': self.processed_data['is_overdue'].sum(),
            'unique_teams': self.processed_data['assigned_team'].nunique(),
            'date_range': {
                'start': self.processed_data['created_date'].min(),
                'end': self.processed_data['created_date'].max()
            }
        } 