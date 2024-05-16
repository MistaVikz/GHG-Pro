import unittest
from unittest.mock import patch
import pandas as pd
from utils.io import *
from io import StringIO

class TestValidProjectData(unittest.TestCase):
    def setUp(self):
        # Create a DataFrame with valid data
        data = {
            'project_id': [1, 2, 3],
            'project_name': ['Project 1', 'Project 2', 'Project 3'],
            'contract_duration': [5, 5, 5],
            'country': ['Country 1', 'Country 2', 'Country 3'],
            'technology': ['Tech 1', 'Tech 2', 'Tech 3'],
            'counterparty': ['Counterparty 1', 'Counterparty 2', 'Counterparty 3'],
            'start_year': [2000, 2001, 2002],
            'screening_date': pd.to_datetime(['2022-01-01', '2022-02-01', '2022-03-01']),
            'offered_volume_year_1': [100, 200, 300],
            'offered_volume_year_2': [100, 200, 300],
            'offered_volume_year_3': [100, 200, 300],
            'offered_volume_year_4': [100, 200, 300],
            'offered_volume_year_5': [100, 200, 300],
            'offered_volume_year_6': [100, 200, 300],
            'offered_volume_year_7': [100, 200, 300],
            'offered_volume_year_8': [100, 200, 300],
            'offered_volume_year_9': [100, 200, 300],
            'offered_volume_year_10': [100, 200, 300],
            'risk_bucket_1_factor_1': [0.1, 0.2, 0.3],
            'risk_bucket_1_weight_1': [0.2, 0.2, 0.2],
            'risk_bucket_1_factor_2': [0.1, 0.2, 0.3],
            'risk_bucket_1_weight_2': [0.2, 0.2, 0.2],
            'risk_bucket_1_factor_3': [0.1, 0.2, 0.3],
            'risk_bucket_1_weight_3': [0.2, 0.2, 0.2],
            'risk_bucket_1_factor_4': [0.1, 0.2, 0.3],
            'risk_bucket_1_weight_4': [0.2, 0.2, 0.2],
            'risk_bucket_1_factor_5': [0.1, 0.2, 0.3],
            'risk_bucket_1_weight_5': [0.2, 0.2, 0.2],
            'risk_bucket_2_factor_1': [0.1, 0.2, 0.3],
            'risk_bucket_2_weight_1': [0.2, 0.2, 0.2],
            'risk_bucket_2_factor_2': [0.1, 0.2, 0.3],
            'risk_bucket_2_weight_2': [0.2, 0.2, 0.2],
            'risk_bucket_2_factor_3': [0.1, 0.2, 0.3],
            'risk_bucket_2_weight_3': [0.2, 0.2, 0.2],
            'risk_bucket_2_factor_4': [0.1, 0.2, 0.3],
            'risk_bucket_2_weight_4': [0.2, 0.2, 0.2],
            'risk_bucket_2_factor_5': [0.1, 0.2, 0.3],
            'risk_bucket_2_weight_5': [0.2, 0.2, 0.2],
            'risk_bucket_3_factor_1': [0.1, 0.2, 0.3],
            'risk_bucket_3_weight_1': [0.2, 0.2, 0.2],
            'risk_bucket_3_factor_2': [0.1, 0.2, 0.3],
            'risk_bucket_3_weight_2': [0.2, 0.2, 0.2],
            'risk_bucket_3_factor_3': [0.1, 0.2, 0.3],
            'risk_bucket_3_weight_3': [0.2, 0.2, 0.2],
            'risk_bucket_3_factor_4': [0.1, 0.2, 0.3],
            'risk_bucket_3_weight_4': [0.2, 0.2, 0.2],
            'risk_bucket_3_factor_5': [0.1, 0.2, 0.3],
            'risk_bucket_3_weight_5': [0.2, 0.2, 0.2],
            'risk_bucket_4_factor_1': [0.1, 0.2, 0.3],
            'risk_bucket_4_weight_1': [0.2, 0.2, 0.2],
            'risk_bucket_4_factor_2': [0.1, 0.2, 0.3],
            'risk_bucket_4_weight_2': [0.2, 0.2, 0.2],
            'risk_bucket_4_factor_3': [0.1, 0.2, 0.3],
            'risk_bucket_4_weight_3': [0.2, 0.2, 0.2],
            'risk_bucket_4_factor_4': [0.1, 0.2, 0.3],
            'risk_bucket_4_weight_4': [0.2, 0.2, 0.2],
            'risk_bucket_4_factor_5': [0.1, 0.2, 0.3],
            'risk_bucket_4_weight_5': [0.2, 0.2, 0.2],
            'risk_bucket_5_factor_1': [0.1, 0.2, 0.3],
            'risk_bucket_5_weight_1': [0.2, 0.2, 0.2],
            'risk_bucket_5_factor_2': [0.1, 0.2, 0.3],
            'risk_bucket_5_weight_2': [0.2, 0.2, 0.2],
            'risk_bucket_5_factor_3': [0.1, 0.2, 0.3],
            'risk_bucket_5_weight_3': [0.2, 0.2, 0.2],
            'risk_bucket_5_factor_4': [0.1, 0.2, 0.3],
            'risk_bucket_5_weight_4': [0.2, 0.2, 0.2],
            'risk_bucket_5_factor_5': [0.1, 0.2, 0.3],
            'risk_bucket_5_weight_5': [0.2, 0.2, 0.2]
        }
        self.df = pd.DataFrame(data)

    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_project_data(self, mock_stdout):
        self.assertTrue(valid_project_data(self.df))
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

    @patch('sys.stdout', new_callable=StringIO)
    def test_missing_column(self, mock_stdout):
        df = self.df.drop('project_id', axis=1)
        self.assertFalse(valid_project_data(df))
        output = mock_stdout.getvalue()
        self.assertIn("Error: Not all required columns are present.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_contract_duration(self, mock_stdout):
        self.df['contract_duration'] = ['5 years', '5 years', '5 years']
        self.assertFalse(valid_project_data(self.df))
        output = mock_stdout.getvalue()
        self.assertIn("Error: Contract Duration column contains invalid values. Values must be integers between 1 and 10.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_start_year(self, mock_stdout):
        self.df['start_year'] = [1999, 2001, 2002]
        self.assertFalse(valid_project_data(self.df))
        output = mock_stdout.getvalue()
        self.assertIn("Error: Start Year column contains invalid values. Values must be integers greater or equal to 2000.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_offered_volume(self, mock_stdout):
        self.df['offered_volume_year_1'] = [-100, 200, 300]
        self.assertFalse(valid_project_data(self.df))
        output = mock_stdout.getvalue()
        self.assertIn("Error: offered_volume_year_1 column contains invalid values. Values must be integers greater than 0.", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_risk_bucket_weights(self, mock_stdout):
        self.df['risk_bucket_1_weight_1'] = [0.1, 0.2, 0.3]
        self.assertFalse(valid_project_data(self.df))
        output = mock_stdout.getvalue()
        self.assertIn("Error: risk_bucket_1_weight_1 + risk_bucket_1_weight_2 + risk_bucket_1_weight_3 + risk_bucket_1_weight_4 + risk_bucket_1_weight_5 must be equal to 1.", output)

class TestDisplayProjectRiskOutput(unittest.TestCase):
    def setUp(self):
        self.df_counts = pd.DataFrame({'Rating': ['A', 'B', 'C'], 'Count': [10, 20, 30]})
        self.top_projects = pd.DataFrame({'Project ID': [1, 2, 3], 'Rating': ['A', 'A', 'B']})
        self.bottom_projects = pd.DataFrame({'Project ID': [4, 5, 6], 'Rating': ['C', 'C', 'C']})
        self.country_table = pd.DataFrame({'Country': ['USA', 'Canada', 'Mexico'], 'Count': [10, 20, 30]})
        self.technology_table = pd.DataFrame({'Technology': ['Tech 1', 'Tech 2', 'Tech 3'], 'Count': [10, 20, 30]})
        self.counterparty_table = pd.DataFrame({'Counterparty': ['Counterparty 1', 'Counterparty 2', 'Counterparty 3'], 'Count': [10, 20, 30]})
        self.total_volumes_per_year = pd.DataFrame({'Year': [2020, 2021, 2022], 'Volume': [100, 200, 300]})

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_project_risk_output(self, mock_stdout):
        display_project_risk_output(self.df_counts, self.top_projects, self.bottom_projects, self.country_table, self.technology_table, self.counterparty_table, self.total_volumes_per_year)
        output = mock_stdout.getvalue()
        self.assertIn("Project Rating Distribution", output)
        self.assertIn("Highest Performing Projects", output)
        self.assertIn("Lowest Performing Projects", output)
        self.assertIn("Overall Project Rating Distribution by Country", output)
        self.assertIn("Overall Project Rating Distribution by Technology", output)
        self.assertIn("Overall Project Rating Distribution by Counterparty", output)
        self.assertIn("Annual Project Volumes", output)

    @patch('sys.argv', ['script_name', '--noprint'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_project_risk_output_noprint(self, mock_stdout):
        display_project_risk_output(self.df_counts, self.top_projects, self.bottom_projects, self.country_table, self.technology_table, self.counterparty_table, self.total_volumes_per_year)
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")

class TestCheckDfFormat(unittest.TestCase):
    def test_dataframes_with_correct_format(self):
        df1 = pd.DataFrame({i: [1, 2, 3] for i in range(1, 11)}, index=['Investment', 'Speculative', 'C'])
        df2 = pd.DataFrame({i: [4, 5, 6] for i in range(1, 11)}, index=['Investment', 'Speculative', 'C'])
        self.assertTrue(check_df_format(df1, df2))

    def test_dataframes_with_incorrect_shape(self):
        df1 = pd.DataFrame({i: [1, 2, 3] for i in range(1, 11)}, index=['Investment', 'Speculative', 'C'])
        df2 = pd.DataFrame({i: [4, 5] for i in range(1, 11)}, index=['Investment', 'Speculative'])
        self.assertFalse(check_df_format(df1, df2))

    def test_dataframes_with_incorrect_row_names(self):
        df1 = pd.DataFrame({i: [1, 2, 3] for i in range(1, 11)}, index=['Investment', 'Speculative', 'C'])
        df2 = pd.DataFrame({i: [4, 5, 6] for i in range(1, 11)}, index=['X', 'Y', 'Z'])
        self.assertFalse(check_df_format(df1, df2))

    def test_dataframes_with_incorrect_column_names(self):
        df1 = pd.DataFrame({i: [1, 2, 3] for i in range(1, 11)}, index=['Investment', 'Speculative', 'C'])
        df2 = pd.DataFrame({i: [4, 5, 6] for i in range(2, 12)}, index=['Investment', 'Speculative', 'C'])
        self.assertFalse(check_df_format(df1, df2))

    def test_dataframes_with_negative_values(self):
        df1 = pd.DataFrame({i: [1, 2, 3] for i in range(1, 11)}, index=['Investment', 'Speculative', 'C'])
        df2 = pd.DataFrame({i: [-1, -2, -3] for i in range(1, 11)}, index=['Investment', 'Speculative', 'C'])
        self.assertFalse(check_df_format(df1, df2))

if __name__ == '__main__':
    unittest.main()