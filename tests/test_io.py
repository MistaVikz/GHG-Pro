import unittest
from unittest.mock import patch
import pandas as pd
from utils.io import *
from io import StringIO

class TestValidProjectData(unittest.TestCase):
    def setUp(self):
        self.num_buckets = 3
        self.num_factors = 6
        self.required_columns = ['project_id', 'project_name', 'contract_duration', 'country', 'technology', 'counterparty', 'start_year', 'screening_date']
        for year in range(1, 11):
            self.required_columns.append(f'offered_volume_year_{year}')
        for bucket in range(1, self.num_buckets + 1):
            for factor in range(1, self.num_factors + 1):
                self.required_columns.append(f'risk_bucket_{bucket}_factor_{factor}')
                self.required_columns.append(f'risk_bucket_{bucket}_weight_{factor}')

    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_data(self,mock_stdout):
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
            for factor in range(1, self.num_factors + 1):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                if factor == self.num_factors:  # Last factor
                    data[f'risk_bucket_{bucket}_weight_{factor}'] = [1 - (factor - 1) * 0.1667]  # Adjust weight to make sum equal to 1
                else:
                    data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.1667]

        df = pd.DataFrame(data)
        self.assertTrue(valid_project_data(df, self.num_buckets, self.num_factors))

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
        self.assertFalse(valid_project_data(df, self.num_buckets, self.num_factors))

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
            for factor in range(1, self.num_factors + 1):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets, self.num_factors))

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
            for factor in range(1, self.num_factors + 1):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1, 1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2, 0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets, self.num_factors))

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
            for factor in range(1, self.num_factors + 1):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets, self.num_factors))

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
            for factor in range(1, self.num_factors + 1):
                data[f'risk_bucket_{bucket}_factor_{factor}'] = [1]
                data[f'risk_bucket_{bucket}_weight_{factor}'] = [0.2]

        df = pd.DataFrame(data)
        self.assertFalse(valid_project_data(df, self.num_buckets, self.num_factors))

    
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
    def setUp(self):
        self.df_default_rates = pd.DataFrame(index=['Investment', 'Speculative', 'C'], columns=range(1, 11), data=0)
        self.df_recovery_potential = pd.DataFrame(index=['Investment', 'Speculative', 'C'], columns=range(1, 11), data=0)

    @patch('sys.stdout', new_callable=StringIO)
    def test_dataframes_with_same_shape(self, mock_stdout):
        self.assertTrue(check_df_format(self.df_default_rates, self.df_recovery_potential))

    @patch('sys.stdout', new_callable=StringIO)
    def test_dataframes_with_different_shape(self, mock_stdout):
        self.df_recovery_potential = pd.DataFrame(index=['Investment', 'Speculative', 'C'], columns=range(1, 12), data=0)
        self.assertFalse(check_df_format(self.df_default_rates, self.df_recovery_potential))

    @patch('sys.stdout', new_callable=StringIO)
    def test_dataframes_with_incorrect_row_names(self, mock_stdout):
        self.df_recovery_potential = pd.DataFrame(index=['Investment', 'Speculative', 'D'], columns=range(1, 11), data=0)
        self.assertFalse(check_df_format(self.df_default_rates, self.df_recovery_potential))

    @patch('sys.stdout', new_callable=StringIO)
    def test_dataframes_with_incorrect_column_names(self, mock_stdout):
        self.df_recovery_potential = pd.DataFrame(index=['Investment', 'Speculative', 'C'], columns=range(1, 12), data=0)
        self.assertFalse(check_df_format(self.df_default_rates, self.df_recovery_potential))

    @patch('sys.stdout', new_callable=StringIO)
    def test_dataframes_with_invalid_values(self, mock_stdout):
        self.df_default_rates.loc['Investment', 1] = -1
        self.assertFalse(check_df_format(self.df_default_rates, self.df_recovery_potential))

class TestValidModel(unittest.TestCase):
    def setUp(self):
        self.risk_bucket_count = 2
        self.risk_factor_count = 2
        self.required_columns = ['model_id', 'model_name', 'num_buckets', 'num_factors', 'last_saved']
        for i in range(1, self.risk_bucket_count + 1):
            self.required_columns.append(f'risk_bucket_{i}_name')
            for j in range(1, self.risk_factor_count + 1):
                self.required_columns.append(f'risk_bucket_{i}_factor_{j}_name')
                self.required_columns.append(f'risk_bucket_{i}_factor_{j}_rules')

    @patch('sys.stdout', new_callable=StringIO)
    def test_valid_model(self, mock_stdout):
        data = {col: [0] for col in self.required_columns}
        df_model = pd.DataFrame(data)
        self.assertTrue(valid_model(df_model, self.risk_bucket_count, self.risk_factor_count))

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_model_missing_columns(self, mock_stdout):
        data = {col: [0] for col in self.required_columns[:-1]}
        df_model = pd.DataFrame(data)
        self.assertFalse(valid_model(df_model, self.risk_bucket_count, self.risk_factor_count))

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_model_extra_columns(self, mock_stdout):
        data = {col: [0] for col in self.required_columns}
        data['extra_column'] = [0]
        df_model = pd.DataFrame(data)
        self.assertFalse(valid_model(df_model, self.risk_bucket_count, self.risk_factor_count))

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_model_multiple_rows(self, mock_stdout):
        data = {col: [0, 0] for col in self.required_columns}
        df_model = pd.DataFrame(data)
        self.assertFalse(valid_model(df_model, self.risk_bucket_count, self.risk_factor_count))

class TestLoadAndProcessData(unittest.TestCase):
    @patch('pandas.read_excel')
    def test_load_and_process_data(self, mock_read_excel):
        # Create mock dataframes
        df_project = pd.DataFrame({'project_id': [1, 2], 'project_name': ['Project 1', 'Project 2']})
        df_project['screening_date'] = pd.to_datetime(['2022-01-01', '2022-01-02'])
        df_project['risk_bucket_1_factor_1'] = [0.1, 0.2]
        df_project['risk_bucket_1_factor_2'] = [0.3, 0.4]
        df_project['risk_bucket_2_factor_1'] = [0.5, 0.6]
        df_project['risk_bucket_2_factor_2'] = [0.7, 0.8]
        df_default_rates = pd.DataFrame({'Unnamed: 0': ['Investment', 'Speculative'], 1: [0.1, 0.2]})
        df_recovery_potential = pd.DataFrame({'Unnamed: 0': ['Investment', 'Speculative'], 1: [0.1, 0.2]})
        df_model = pd.DataFrame({'model_id': [1], 'model_name': ['Model 1']})

        # Mock read_excel function to return mock dataframes
        mock_read_excel.side_effect = [df_project, df_default_rates, df_recovery_potential, df_model]

        # Load and process data from mock Excel file
        num_buckets, num_risk_factors, df_project, df_default_rates, df_recovery_potential, df_model = load_and_process_data('mock_file.xlsx')

        # Verify output
        self.assertEqual(num_buckets, 2)
        self.assertEqual(num_risk_factors, 2)
        self.assertTrue(df_project.equals(pd.DataFrame({'project_id': [1, 2], 'project_name': ['Project 1', 'Project 2'], 'screening_date': pd.to_datetime(['2022-01-01', '2022-01-02']), 'risk_bucket_1_factor_1': [0.1, 0.2], 'risk_bucket_1_factor_2': [0.3, 0.4], 'risk_bucket_2_factor_1': [0.5, 0.6], 'risk_bucket_2_factor_2': [0.7, 0.8]})))
        self.assertTrue(df_default_rates.equals(pd.DataFrame({1: [0.1, 0.2]}, index=['Investment', 'Speculative'])))
        self.assertTrue(df_recovery_potential.equals(pd.DataFrame({1: [0.1, 0.2]}, index=['Investment', 'Speculative'])))
        self.assertTrue(df_model.equals(pd.DataFrame({'model_id': [1], 'model_name': ['Model 1']})))

    @patch('pandas.read_excel')
    def test_load_and_process_data_failure(self, mock_read_excel):
        # Mock read_excel function to raise an exception
        mock_read_excel.side_effect = ValueError('Worksheet not found')

        # Load and process data from mock Excel file
        with self.assertRaises(ValueError):
            load_and_process_data('mock_file.xlsx')

class TestCreateOutputFolder(unittest.TestCase):
    @patch('os.makedirs')
    def test_create_output_folder_success(self, mock_makedirs):
        # Mock the current date and time
        now = datetime.datetime(2022, 1, 1, 12, 0, 0)
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = now

            # Call the function
            folder_name = create_output_folder()

            # Check that the correct path was passed to os.makedirs
            current_dir = os.path.dirname(create_output_folder.__code__.co_filename)
            output_dir = os.path.join(current_dir, '..', 'output')
            expected_folder_name = os.path.join(output_dir, '20220101_120000')
            mock_makedirs.assert_called_once_with(expected_folder_name, exist_ok=True)

            # Check that the function returned the correct folder name
            self.assertEqual(folder_name, expected_folder_name)

    @patch('os.makedirs')
    def test_create_output_folder_failure(self, mock_makedirs):
        # Mock the current date and time
        now = datetime.datetime(2022, 1, 1, 12, 0, 0)
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = now

            # Set up os.makedirs to raise an error
            mock_makedirs.side_effect = OSError('Test error')

            # Call the function and check that it raises an error
            with self.assertRaises(OSError):
                create_output_folder()

class TestExportGHGData(unittest.TestCase):
    def test_export_ghg_data(self):
        # Create some sample DataFrames
        df_project = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df_default_rates = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=['Investment', 'Speculative', 'C'])
        df_recovery_potential = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}, index=['Investment', 'Speculative', 'C'])
        df_model = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

        # Create a mock object for the open function
        with patch('openpyxl.workbook.workbook.save_workbook') as mock_save:
            # Call the function with the mock object
            export_ghg_data('', df_project, df_default_rates, df_recovery_potential, df_model)

            # Check that the save_workbook function was called
            mock_save.assert_called_once()
    
    def test_export_ghg_data_error(self):
        # Create some sample DataFrames
        df_project = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df_default_rates = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df_recovery_potential = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df_model = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

        # Create a mock object for the open function
        with patch('openpyxl.workbook.workbook.save_workbook') as mock_save:
            # Call the function with the mock object
            with self.assertRaises(KeyError):
                export_ghg_data('', df_project, df_default_rates, df_recovery_potential, df_model)

            # Check that the save_workbook function was not called
            mock_save.assert_not_called()

class TestExportProjectRiskOutput(unittest.TestCase):
    def test_export_project_risk_output(self):
        # Create some sample DataFrames
        top_projects = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        bottom_projects = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        country_table = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        technology_table = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        counterparty_table = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df_counts = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        total_volumes_per_year = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

        # Create a mock object for the open function
        with patch('openpyxl.workbook.workbook.save_workbook') as mock_save:
            # Call the function with the mock object
            export_project_risk_output('', top_projects, bottom_projects, country_table, technology_table, counterparty_table, df_counts, total_volumes_per_year)

            # Check that the save_workbook function was called
            mock_save.assert_called_once()

    def test_export_project_risk_output_fails(self):
        # Create some sample DataFrames
        top_projects = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        bottom_projects = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        country_table = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        technology_table = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        counterparty_table = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        df_counts = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        total_volumes_per_year = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

        # Create a mock object for the open function that raises an exception
        with patch('openpyxl.workbook.workbook.save_workbook', side_effect=PermissionError):
            # Call the function with the mock object
            with self.assertRaises(PermissionError):
                export_project_risk_output('', top_projects, bottom_projects, country_table, technology_table, counterparty_table, df_counts, total_volumes_per_year)


if __name__ == '__main__':
    unittest.main()