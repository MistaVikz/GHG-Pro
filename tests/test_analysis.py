from utils.analysis import *
import unittest
import pandas as pd

class TestCalculateTopBottomProjects(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'project_id': [1, 2, 3, 4, 5],
            'project_name': ['Project 1', 'Project 2', 'Project 3', 'Project 4', 'Project 5'],
            'project_expected_value_percentage_year_1': [10, 20, 30, 40, 50],
            'project_expected_value_percentage_year_2': [20, 30, 40, 50, 60],
            'project_expected_value_percentage_year_3': [30, 40, 50, 60, 70],
            'project_expected_value_percentage_year_4': [40, 50, 60, 70, 80],
            'project_expected_value_percentage_year_5': [50, 60, 70, 80, 90],
            'project_expected_value_percentage_year_6': [60, 70, 80, 90, 100],
            'project_expected_value_percentage_year_7': [70, 80, 90, 100, 110],
            'project_expected_value_percentage_year_8': [80, 90, 100, 110, 120],
            'project_expected_value_percentage_year_9': [90, 100, 110, 120, 130],
            'project_expected_value_percentage_year_10': [100, 110, 120, 130, 140]
        })
        self.num_projects = 2
        self.columns = ['project_id', 'project_name']

    def test_calculate_top_bottom_projects(self):
        top_projects, bottom_projects = calculate_top_bottom_projects(self.df_project, self.num_projects, self.columns)
        self.assertEqual(top_projects.shape[0], self.num_projects)
        self.assertEqual(bottom_projects.shape[0], self.num_projects)

        self.assertIn('rank', top_projects.columns)
        self.assertIn('rank', bottom_projects.columns)

        self.assertEqual(top_projects['rank'].tolist(), [1, 2])
        self.assertEqual(bottom_projects['rank'].tolist(), [1, 2])

    def test_calculate_top_bottom_projects_invalid_num_projects(self):
        with self.assertRaises(ValueError):
            calculate_top_bottom_projects(self.df_project, 0, self.columns)

    def test_calculate_top_bottom_projects_invalid_columns(self):
        with self.assertRaises(KeyError):
            calculate_top_bottom_projects(self.df_project, self.num_projects, ['invalid_column'])

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

    def test_empty_dataframe(self):
        df_project = pd.DataFrame()
        result = calculate_total_volumes_by_year(df_project)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)

    def test_single_project(self):
        data = {
            'start_year': [2020],
            'contract_duration': [3],
            'offered_volume_year_1': [100],
            'project_delivery_volume_year_1': [80],
            'offered_volume_year_2': [120],
            'project_delivery_volume_year_2': [90],
            'offered_volume_year_3': [110],
            'project_delivery_volume_year_3': [70]
        }
        df_project = pd.DataFrame(data)
        result = calculate_total_volumes_by_year(df_project)
        self.assertEqual(len(result), 3)
        self.assertEqual(result.loc[0, 'Year'], 2020)
        self.assertEqual(result.loc[0, 'Total Offered Volume'], 100)
        self.assertEqual(result.loc[0, 'Overall Project Delivery'], 80)
        self.assertEqual(result.loc[1, 'Year'], 2021)
        self.assertEqual(result.loc[1, 'Total Offered Volume'], 120)
        self.assertEqual(result.loc[1, 'Overall Project Delivery'], 90)
        self.assertEqual(result.loc[2, 'Year'], 2022)
        self.assertEqual(result.loc[2, 'Total Offered Volume'], 110)
        self.assertEqual(result.loc[2, 'Overall Project Delivery'], 70)

    def test_multiple_projects(self):
        data = {
            'start_year': [2020, 2021],
            'contract_duration': [2, 2],
            'offered_volume_year_1': [100, 120],
            'project_delivery_volume_year_1': [80, 90],
            'offered_volume_year_2': [110, 130],
            'project_delivery_volume_year_2': [70, 60]
        }
        df_project = pd.DataFrame(data)
        result = calculate_total_volumes_by_year(df_project)
        self.assertEqual(len(result), 3)
        self.assertEqual(result.loc[0, 'Year'], 2020)
        self.assertEqual(result.loc[0, 'Total Offered Volume'], 100)
        self.assertEqual(result.loc[0, 'Overall Project Delivery'], 80)
        self.assertEqual(result.loc[1, 'Year'], 2021)
        self.assertEqual(result.loc[1, 'Total Offered Volume'], 230)  # 110 + 120
        self.assertEqual(result.loc[1, 'Overall Project Delivery'], 160)  # 70 + 90
        self.assertEqual(result.loc[2, 'Year'], 2022)
        self.assertEqual(result.loc[2, 'Total Offered Volume'], 130)
        self.assertEqual(result.loc[2, 'Overall Project Delivery'], 60)

if __name__ == '__main__':
    unittest.main()