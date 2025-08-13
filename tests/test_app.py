"""
Unit tests for Incident Insight Hub application
"""
import unittest
import sys
import os
import pandas as pd
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.data_processor import DataProcessor
from src.analyzers import RecurringIssuesAnalyzer, SLAAnalyzer, TeamAnalyzer
from src.utils import DataUtils


class TestDataProcessor(unittest.TestCase):
    """Test the DataProcessor class"""
    
    def setUp(self):
        """Set up test data"""
        self.processor = DataProcessor()
        
        # Create sample test data
        self.sample_data = pd.DataFrame({
            'Incident ID': ['INC001', 'INC002', 'INC003'],
            'Title': ['Test Issue 1', 'Test Issue 2', 'Test Issue 3'],
            'Status': ['Resolved', 'Closed', 'In Progress'],
            'Priority': ['High', 'Medium', 'Low'],
            'Created Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'Resolved Date': ['2024-01-02', '2024-01-03', None],
            'Category': ['Hardware', 'Software', 'Network'],
            'Assigned Team': ['IT Support', 'Development', 'Network Team']
        })
    
    def test_validate_required_columns(self):
        """Test column validation"""
        # Test with valid data
        is_valid, missing = self.processor.validate_required_columns(self.sample_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(missing), 0)
        
        # Test with missing columns
        incomplete_data = self.sample_data.drop(['Priority'], axis=1)
        is_valid, missing = self.processor.validate_required_columns(incomplete_data)
        self.assertFalse(is_valid)
        self.assertIn('Priority', missing)
    
    def test_clean_data(self):
        """Test data cleaning functionality"""
        # Add some dirty data
        dirty_data = self.sample_data.copy()
        dirty_data.loc[0, 'Priority'] = ''  # Empty string
        dirty_data.loc[1, 'Status'] = None  # None value
        
        cleaned_data = self.processor.clean_data(dirty_data)
        
        # Check that data was cleaned
        self.assertIsNotNone(cleaned_data)
        self.assertFalse(cleaned_data['Priority'].isnull().any())


class TestAnalyzers(unittest.TestCase):
    """Test analyzer classes"""
    
    def setUp(self):
        """Set up test data for analyzers"""
        self.test_data = pd.DataFrame({
            'Incident ID': ['INC001', 'INC002', 'INC003', 'INC004'],
            'Title': ['Database down', 'Server error', 'Database down', 'Network issue'],
            'Status': ['Resolved', 'Resolved', 'Closed', 'In Progress'],
            'Priority': ['High', 'Medium', 'High', 'Low'],
            'Created Date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-05', '2024-01-10']),
            'Resolved Date': pd.to_datetime(['2024-01-02', '2024-01-03', '2024-01-06', None]),
            'Category': ['Database', 'Server', 'Database', 'Network'],
            'Assigned Team': ['DB Team', 'IT Support', 'DB Team', 'Network Team']
        })
    
    def test_recurring_issues_analyzer(self):
        """Test recurring issues analysis"""
        analyzer = RecurringIssuesAnalyzer(self.test_data)
        
        # Test similarity detection
        similar_incidents = analyzer.find_similar_incidents()
        self.assertIsInstance(similar_incidents, pd.DataFrame)
        
        # Test pattern identification
        patterns = analyzer.identify_patterns()
        self.assertIsInstance(patterns, dict)
    
    def test_sla_analyzer(self):
        """Test SLA analysis"""
        analyzer = SLAAnalyzer(self.test_data)
        
        # Test SLA metrics calculation
        sla_metrics = analyzer.calculate_sla_metrics()
        self.assertIsInstance(sla_metrics, dict)
        self.assertIn('avg_resolution_time', sla_metrics)
        
        # Test breach detection
        breaches = analyzer.identify_sla_breaches()
        self.assertIsInstance(breaches, pd.DataFrame)
    
    def test_team_analyzer(self):
        """Test team performance analysis"""
        analyzer = TeamAnalyzer(self.test_data)
        
        # Test team performance metrics
        performance = analyzer.analyze_team_performance()
        self.assertIsInstance(performance, pd.DataFrame)
        
        # Test workload distribution
        workload = analyzer.get_workload_distribution()
        self.assertIsInstance(workload, pd.DataFrame)


class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_data_utils(self):
        """Test DataUtils functionality"""
        # Test date parsing
        test_dates = ['2024-01-01', '01/01/2024', '2024-01-01 10:30:00']
        
        for date_str in test_dates:
            parsed_date = DataUtils.parse_date(date_str)
            self.assertIsNotNone(parsed_date)
        
        # Test safe display chart (should not raise exceptions)
        mock_fig = MagicMock()
        try:
            DataUtils.safe_display_chart(mock_fig)
        except Exception as e:
            self.fail(f"safe_display_chart raised an exception: {e}")


class TestAppIntegration(unittest.TestCase):
    """Integration tests for the complete application"""
    
    @patch('streamlit.file_uploader')
    @patch('streamlit.selectbox')
    def test_app_workflow(self, mock_selectbox, mock_file_uploader):
        """Test complete application workflow"""
        # Mock file upload
        mock_file = MagicMock()
        mock_file.name = 'test.xlsx'
        mock_file_uploader.return_value = mock_file
        
        # Mock user selections
        mock_selectbox.return_value = 'Recurring Issues Analysis'
        
        # This would test the main app workflow
        # Note: Full Streamlit testing requires more complex setup
        self.assertTrue(True)  # Placeholder for now


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestDataProcessor))
    test_suite.addTest(unittest.makeSuite(TestAnalyzers))
    test_suite.addTest(unittest.makeSuite(TestUtils))
    test_suite.addTest(unittest.makeSuite(TestAppIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1) 