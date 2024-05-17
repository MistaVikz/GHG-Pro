import unittest
from unittest.mock import patch
import pandas as pd
from utils.io import *
from io import StringIO

class TestValidProjectData(unittest.TestCase):
    def setUp(self):
        self.num_buckets = 3
        self.required_columns = ['project_id', 'project_name', 'contract_duration', 'country', 'technology', 'counterparty', 'start_year', 'screening_date']
        for year in range(1, 11):
            self.required_columns.append(f'offered_volume_year_{year}')
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                self.required_columns.append(f'risk_bucket_{bucket}_factor_{factor}')
                self.required_columns.append(f'risk_bucket_{bucket}_weight_{factor}')

    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_data(self, mock_stdout):
        data = {
            'project_id': [1],
            'project_name': ['Name'],
            'contract_duration': [5],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [2000],
            'screening_date': [pd.to_datetime('2022-01-01')]
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [100]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertTrue(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_missing_column(self, mock_stdout):
        data = {
            'project_id': [1],
            'project_name': ['Name'],
            'contract_duration': [5],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [2000],
            'screening_date': [pd.to_datetime('2022-01-01')]
        }
        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_null_project_id(self, mock_stdout):
        data = {
            'project_id': [None],
            'project_name': ['Name'],
            'contract_duration': [5],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [2000],
            'screening_date': [pd.to_datetime('2022-01-01')]
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [100]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_duplicate_project_id(self, mock_stdout):
        data = {
            'project_id': [1, 1],
            'project_name': ['Name', 'Name'],
            'contract_duration': [5, 5],
            'country': ['Country', 'Country'],
            'technology': ['Tech', 'Tech'],
            'counterparty': ['Counter', 'Counter'],
            'start_year': [2000, 2000],
            'screening_date': [pd.to_datetime('2022-01-01'), pd.to_datetime('2022-01-01')]
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [100, 100]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1, 1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2, 0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_contract_duration(self, mock_stdout):
        data = {
            'project_id': [1],
            'project_name': ['Name'],
            'contract_duration': [15],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [2000],
            'screening_date': [pd.to_datetime('2022-01-01')]
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [100]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_start_year(self, mock_stdout):
        data = {
            'project_id': [1],
            'project_name': ['Name'],
            'contract_duration': [5],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [1999],
            'screening_date': [pd.to_datetime('2022-01-01')]
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [100]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_offered_volume(self, mock_stdout):
        data = {
            'project_id': [1],
            'project_name': ['Name'],
            'contract_duration': [5],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [2000],
            'screening_date': [pd.to_datetime('2022-01-01')]
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [0]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_screening_date(self, mock_stdout):
        data = {
            'project_id': [1],
            'project_name': ['Name'],
            'contract_duration': [5],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [2000],
            'screening_date': ['Invalid Date']
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [100]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_string_columns(self, mock_stdout):
        data = {
            'project_id': [1],
            'project_name': [1],
            'contract_duration': [5],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [2000],
            'screening_date': [pd.to_datetime('2022-01-01')]
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [100]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    @patch('sys.stdout', new_callable=StringIO)
    def test_risk_bucket_weights_sum(self, mock_stdout):
        data = {
            'project_id': [1],
            'project_name': ['Name'],
            'contract_duration': [5],
            'country': ['Country'],
            'technology': ['Tech'],
            'counterparty': ['Counter'],
            'start_year': [2000],
            'screening_date': [pd.to_datetime('2022-01-01')]
        }
        for year in range(1, 11):
            data[f'offered_volume_year_{year}'] = [100]
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, 6):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                if factor == 1:
                    data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.9]  # Set weight to 0.9 instead of 1
                else:
                    data[f'risk_bucket_{bucket}_weight_{factor}'] = [0]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets))

    
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