from utils.analysis import *
import unittest
import pandas as pd

class TestCalculateTopBottomProjects(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'expected_value_percentage_year_1': [0.1, 0.2, 0.3],
            'expected_value_percentage_year_2': [0.4, 0.5, 0.6],
            'expected_value_percentage_year_3': [0.7, 0.8, 0.9],
            'expected_value_percentage_year_4': [0.1, 0.2, 0.3],
            'expected_value_percentage_year_5': [0.4, 0.5, 0.6],
            'expected_value_percentage_year_6': [0.7, 0.8, 0.9],
            'expected_value_percentage_year_7': [0.1, 0.2, 0.3],
            'expected_value_percentage_year_8': [0.4, 0.5, 0.6],
            'expected_value_percentage_year_9': [0.7, 0.8, 0.9],
            'expected_value_percentage_year_10': [0.1, 0.2, 0.3],
            'project_name': ['Project A', 'Project B', 'Project C']
        })

    def test_valid_input(self):
        top_projects, bottom_projects = calculate_top_bottom_projects(self.df_project, num_projects=2, columns=['project_name'])
        self.assertEqual(len(top_projects), 2)
        self.assertEqual(len(bottom_projects), 2)

    def test_invalid_column_names(self):
        with self.assertRaises(KeyError):
            calculate_top_bottom_projects(self.df_project, num_projects=2, columns=['invalid_column_name'])

    def test_non_numeric_values(self):
        df_project = pd.DataFrame({
            'expected_value_percentage_year_1': ['a', 'b', 'c'],
            'expected_value_percentage_year_2': [0.4, 0.5, 0.6],
            'expected_value_percentage_year_3': [0.7, 0.8, 0.9],
            'expected_value_percentage_year_4': [0.1, 0.2, 0.3],
            'expected_value_percentage_year_5': [0.4, 0.5, 0.6],
            'expected_value_percentage_year_6': [0.7, 0.8, 0.9],
            'expected_value_percentage_year_7': [0.1, 0.2, 0.3],
            'expected_value_percentage_year_8': [0.4, 0.5, 0.6],
            'expected_value_percentage_year_9': [0.7, 0.8, 0.9],
            'expected_value_percentage_year_10': [0.1, 0.2, 0.3],
            'project_name': ['Project A', 'Project B', 'Project C']
        })
        with self.assertRaises(TypeError):
            calculate_top_bottom_projects(df_project, num_projects=2, columns=['project_name'])

class TestCreateGroupTable(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'country': ['USA', 'Canada', 'USA', 'Canada'],
            'technology': ['Tech1', 'Tech2', 'Tech1', 'Tech2'],
            'counterparty': ['Counterparty1', 'Counterparty2', 'Counterparty1', 'Counterparty2'],
            'offered_volume_year_1': [100, 200, 300, 400],
            'offered_volume_year_2': [500, 600, 700, 800],
            'offered_volume_year_3': [900, 1000, 1100, 1200],
            'offered_volume_year_4': [1300, 1400, 1500, 1600],
            'offered_volume_year_5': [1700, 1800, 1900, 2000],
            'offered_volume_year_6': [2100, 2200, 2300, 2400],
            'offered_volume_year_7': [2500, 2600, 2700, 2800],
            'offered_volume_year_8': [2900, 3000, 3100, 3200],
            'offered_volume_year_9': [3300, 3400, 3500, 3600],
            'offered_volume_year_10': [3700, 3800, 3900, 4000],
            'overall_project_rating': ['High', 'Low', 'High', 'Low']
        })

    def test_create_group_table_country(self):
        group_table = create_group_table(self.df_project, 'country')
        self.assertIn('Total Offered Volume', group_table.columns)
        self.assertIn('Total Projects', group_table.columns)
        self.assertIn('High (%)', group_table.columns)
        self.assertIn('Low (%)', group_table.columns)

    def test_create_group_table_technology(self):
        group_table = create_group_table(self.df_project, 'technology')
        self.assertIn('Total Offered Volume', group_table.columns)
        self.assertIn('Total Projects', group_table.columns)
        self.assertIn('High (%)', group_table.columns)
        self.assertIn('Low (%)', group_table.columns)

    def test_create_group_table_counterparty(self):
        group_table = create_group_table(self.df_project, 'counterparty')
        self.assertIn('Total Offered Volume', group_table.columns)
        self.assertIn('Total Projects', group_table.columns)
        self.assertIn('High (%)', group_table.columns)
        self.assertIn('Low (%)', group_table.columns)

    def test_create_group_table_invalid_group_by(self):
        with self.assertRaises(ValueError):
            create_group_table(self.df_project, 'invalid_group')

class TestCalculateTotalVolumesByYear(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'start_year': [2020, 2021],
            'contract_duration': [2, 3],
            'offered_volume_year_1': [100, 200],
            'offered_volume_year_2': [300, 400],
            'offered_volume_year_3': [0, 500],
            'overall_project_delivery_year_1': [10, 20],
            'overall_project_delivery_year_2': [30, 40],
            'overall_project_delivery_year_3': [0, 50]
        })

    def test_calculate_total_volumes_by_year(self):
        total_volumes_by_year = calculate_total_volumes_by_year(self.df_project)
        self.assertIn('Year', total_volumes_by_year.columns)
        self.assertIn('Total Offered Volume', total_volumes_by_year.columns)
        self.assertIn('Overall Project Delivery', total_volumes_by_year.columns)
        self.assertEqual(total_volumes_by_year.shape[0], 4)  # Total years from 2020 to 2023

    def test_calculate_total_volumes_by_year_values(self):
        total_volumes_by_year = calculate_total_volumes_by_year(self.df_project)
        self.assertEqual(total_volumes_by_year.loc[0, 'Total Offered Volume'], 100)  # Year 2020
        self.assertEqual(total_volumes_by_year.loc[1, 'Total Offered Volume'], 500)  # Year 2021
        self.assertEqual(total_volumes_by_year.loc[2, 'Total Offered Volume'], 400)  # Year 2022
        self.assertEqual(total_volumes_by_year.loc[3, 'Total Offered Volume'], 500)  # Year 2023
        self.assertEqual(total_volumes_by_year.loc[0, 'Overall Project Delivery'], 10)  # Year 2020
        self.assertEqual(total_volumes_by_year.loc[1, 'Overall Project Delivery'], 50)  # Year 2021
        self.assertEqual(total_volumes_by_year.loc[2, 'Overall Project Delivery'], 40)  # Year 2022
        self.assertEqual(total_volumes_by_year.loc[3, 'Overall Project Delivery'], 50)  # Year 2023

if __name__ == '__main__':
    unittest.main()