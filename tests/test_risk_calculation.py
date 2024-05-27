import unittest
from utils.risk_calculation import *
import pandas as pd
import numpy as np
import time

class TestRunSimulation(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'contract_duration': [10, 5],
            'risk_bucket_1_expected_value_year_1': [100000, 200000],
            'risk_bucket_1_standard_deviation_year_1': [10000, 20000],
            'risk_bucket_2_expected_value_year_1': [100000, 200000],
            'risk_bucket_2_standard_deviation_year_1': [10000, 20000],
            'risk_bucket_3_expected_value_year_1': [100000, 200000],
            'risk_bucket_3_standard_deviation_year_1': [10000, 20000],
            'risk_bucket_4_expected_value_year_1': [100000, 200000],
            'risk_bucket_4_standard_deviation_year_1': [10000, 20000],
            'risk_bucket_5_expected_value_year_1': [100000, 200000],
            'risk_bucket_5_standard_deviation_year_1': [10000, 20000],
            'offered_volume_year_1': [1000000, 2000000],

            'risk_bucket_1_expected_value_year_2': [110000, 210000],
            'risk_bucket_1_standard_deviation_year_2': [11000, 21000],
            'risk_bucket_2_expected_value_year_2': [110000, 210000],
            'risk_bucket_2_standard_deviation_year_2': [11000, 21000],
            'risk_bucket_3_expected_value_year_2': [110000, 210000],
            'risk_bucket_3_standard_deviation_year_2': [11000, 21000],
            'risk_bucket_4_expected_value_year_2': [110000, 210000],
            'risk_bucket_4_standard_deviation_year_2': [11000, 21000],
            'risk_bucket_5_expected_value_year_2': [110000, 210000],
            'risk_bucket_5_standard_deviation_year_2': [11000, 21000],
            'offered_volume_year_2': [1100000, 2100000],

            'risk_bucket_1_expected_value_year_3': [120000, 220000],
            'risk_bucket_1_standard_deviation_year_3': [12000, 22000],
            'risk_bucket_2_expected_value_year_3': [120000, 220000],
            'risk_bucket_2_standard_deviation_year_3': [12000, 22000],
            'risk_bucket_3_expected_value_year_3': [120000, 220000],
            'risk_bucket_3_standard_deviation_year_3': [12000, 22000],
            'risk_bucket_4_expected_value_year_3': [120000, 220000],
            'risk_bucket_4_standard_deviation_year_3': [12000, 22000],
            'risk_bucket_5_expected_value_year_3': [120000, 220000],
            'risk_bucket_5_standard_deviation_year_3': [12000, 22000],
            'offered_volume_year_3': [1200000, 2200000],

            'risk_bucket_1_expected_value_year_4': [130000, 230000],
            'risk_bucket_1_standard_deviation_year_4': [13000, 23000],
            'risk_bucket_2_expected_value_year_4': [130000, 230000],
            'risk_bucket_2_standard_deviation_year_4': [13000, 23000],
            'risk_bucket_3_expected_value_year_4': [130000, 230000],
            'risk_bucket_3_standard_deviation_year_4': [13000, 23000],
            'risk_bucket_4_expected_value_year_4': [130000, 230000],
            'risk_bucket_4_standard_deviation_year_4': [13000, 23000],
            'risk_bucket_5_expected_value_year_4': [130000, 230000],
            'risk_bucket_5_standard_deviation_year_4': [13000, 23000],
            'offered_volume_year_4': [1300000, 2300000],

            'risk_bucket_1_expected_value_year_5': [140000, 240000],
            'risk_bucket_1_standard_deviation_year_5': [14000, 24000],
            'risk_bucket_2_expected_value_year_5': [140000, 240000],
            'risk_bucket_2_standard_deviation_year_5': [14000, 24000],
            'risk_bucket_3_expected_value_year_5': [140000, 240000],
            'risk_bucket_3_standard_deviation_year_5': [14000, 24000],
            'risk_bucket_4_expected_value_year_5': [140000, 240000],
            'risk_bucket_4_standard_deviation_year_5': [14000, 24000],
            'risk_bucket_5_expected_value_year_5': [140000, 240000],
            'risk_bucket_5_standard_deviation_year_5': [14000, 24000],
            'offered_volume_year_5': [1400000, 2400000],

            'risk_bucket_1_expected_value_year_6': [150000, np.nan],
            'risk_bucket_1_standard_deviation_year_6': [15000, np.nan],
            'risk_bucket_2_expected_value_year_6': [150000, np.nan],
            'risk_bucket_2_standard_deviation_year_6': [15000, np.nan],
            'risk_bucket_3_expected_value_year_6': [150000, np.nan],
            'risk_bucket_3_standard_deviation_year_6': [15000, np.nan],
            'risk_bucket_4_expected_value_year_6': [150000, np.nan],
            'risk_bucket_4_standard_deviation_year_6': [15000, np.nan],
            'risk_bucket_5_expected_value_year_6': [150000, np.nan],
            'risk_bucket_5_standard_deviation_year_6': [15000, np.nan],
            'offered_volume_year_6': [1500000, np.nan],

            'risk_bucket_1_expected_value_year_7': [160000, np.nan],
            'risk_bucket_1_standard_deviation_year_7': [16000, np.nan],
            'risk_bucket_2_expected_value_year_7': [160000, np.nan],
            'risk_bucket_2_standard_deviation_year_7': [16000, np.nan],
            'risk_bucket_3_expected_value_year_7': [160000, np.nan],
            'risk_bucket_3_standard_deviation_year_7': [16000, np.nan],
            'risk_bucket_4_expected_value_year_7': [160000, np.nan],
            'risk_bucket_4_standard_deviation_year_7': [16000, np.nan],
            'risk_bucket_5_expected_value_year_7': [160000, np.nan],
            'risk_bucket_5_standard_deviation_year_7': [16000, np.nan],
            'offered_volume_year_7': [1600000, np.nan],

            'risk_bucket_1_expected_value_year_8': [170000, np.nan],
            'risk_bucket_1_standard_deviation_year_8': [17000, np.nan],
            'risk_bucket_2_expected_value_year_8': [170000, np.nan],
            'risk_bucket_2_standard_deviation_year_8': [17000, np.nan],
            'risk_bucket_3_expected_value_year_8': [170000, np.nan],
            'risk_bucket_3_standard_deviation_year_8': [17000, np.nan],
            'risk_bucket_4_expected_value_year_8': [170000, np.nan],
            'risk_bucket_4_standard_deviation_year_8': [17000, np.nan],
            'risk_bucket_5_expected_value_year_8': [170000, np.nan],
            'risk_bucket_5_standard_deviation_year_8': [17000, np.nan],
            'offered_volume_year_8': [1700000, np.nan],

            'risk_bucket_1_expected_value_year_9': [180000, np.nan],
            'risk_bucket_1_standard_deviation_year_9': [18000, np.nan],
            'risk_bucket_2_expected_value_year_9': [180000, np.nan],
            'risk_bucket_2_standard_deviation_year_9': [18000, np.nan],
            'risk_bucket_3_expected_value_year_9': [180000, np.nan],
            'risk_bucket_3_standard_deviation_year_9': [18000, np.nan],
            'risk_bucket_4_expected_value_year_9': [180000, np.nan],
            'risk_bucket_4_standard_deviation_year_9': [18000, np.nan],
            'risk_bucket_5_expected_value_year_9': [180000, np.nan],
            'risk_bucket_5_standard_deviation_year_9': [18000, np.nan],
            'offered_volume_year_9': [1800000, np.nan],

            'risk_bucket_1_expected_value_year_10': [190000, np.nan],
            'risk_bucket_1_standard_deviation_year_10': [19000, np.nan],
            'risk_bucket_2_expected_value_year_10': [190000, np.nan],
            'risk_bucket_2_standard_deviation_year_10': [19000, np.nan],
            'risk_bucket_3_expected_value_year_10': [190000, np.nan],
            'risk_bucket_3_standard_deviation_year_10': [19000, np.nan],
            'risk_bucket_4_expected_value_year_10': [190000, np.nan],
            'risk_bucket_4_standard_deviation_year_10': [19000, np.nan],
            'risk_bucket_5_expected_value_year_10': [190000, np.nan],
            'risk_bucket_5_standard_deviation_year_10': [19000, np.nan],
            'offered_volume_year_10': [1900000, np.nan]
        })
    
    def test_run_simulation(self):
        df_result = run_simulation(self.df_project, 5)
        
        # Check that the values in the result are reasonable
        for i in range(1, 11):
            self.assertGreater(df_result[f'project_standard_deviation_year_{i}'].values[0], 0)
            self.assertGreater(df_result[f'project_delivery_volume_year_{i}'].values[0], 0)
            self.assertGreater(df_result[f'project_expected_value_percentage_year_{i}'].values[0], 0)

        # Check that the values for years 6-10 are NaN for the second project
        for i in range(6, 11):
            self.assertTrue(np.isnan(df_result[f'project_standard_deviation_year_{i}'].values[1]))
            self.assertTrue(np.isnan(df_result[f'project_delivery_volume_year_{i}'].values[1]))
            self.assertTrue(np.isnan(df_result[f'project_expected_value_percentage_year_{i}'].values[1]))

    def test_run_simulation_invalid_input(self):
        # Drop a required column from the DataFrame
        df_project = self.df_project.drop('risk_bucket_1_standard_deviation_year_1', axis=1)

        # Run the simulation and check that it raises a KeyError
        with self.assertRaises(KeyError):
            run_simulation(df_project, 5)

    def test_zero_standard_deviation(self):
        # Set the standard deviations to zero
        self.df_project['risk_bucket_1_standard_deviation_year_1'] = 0
        self.df_project['risk_bucket_2_standard_deviation_year_1'] = 0
        self.df_project['risk_bucket_3_standard_deviation_year_1'] = 0
        self.df_project['risk_bucket_4_standard_deviation_year_1'] = 0
        self.df_project['risk_bucket_5_standard_deviation_year_1'] = 0

        # Run the simulation
        result_df = run_simulation(self.df_project, 5)

        # Check that the results are as expected
        self.assertTrue((result_df['project_standard_deviation_year_1'] == 0).all())
        self.assertTrue((result_df['project_delivery_volume_year_1'] == result_df['offered_volume_year_1']).all())
        self.assertTrue((result_df['project_expected_value_percentage_year_1'] == 1).all())
    
    def test_large_dataframe_performance(self):
        # Create a large DataFrame
        large_df = pd.concat([self.df_project] * 250, ignore_index=True)

        # Measure the time it takes to run the simulation
        start_time = time.time()
        result_df = run_simulation(large_df, 5)
        end_time = time.time()
    
        # Check that the simulation completed within a reasonable amount of time
        self.assertLess(end_time - start_time, 10)
    
    def test_large_number_of_samples_performance(self):
        # Set the number of samples to a large value
        num_samples = 1000000

        # Measure the time it takes to run the simulation
        start_time = time.time()
        result_df = run_simulation(self.df_project, 5, num_samples)
        end_time = time.time()

        # Check that the simulation completed within a reasonable amount of time
        self.assertLess(end_time - start_time, 5)

class TestCalculateRiskBucketScores(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'risk_bucket_1_factor_1': [0.1, 0.2, 0.3],
            'risk_bucket_1_weight_1': [0.4, 0.5, 0.6],
            'risk_bucket_1_factor_2': [0.7, 0.8, 0.9],
            'risk_bucket_1_weight_2': [0.1, 0.2, 0.3],
            'risk_bucket_2_factor_1': [0.4, 0.5, 0.6],
            'risk_bucket_2_weight_1': [0.7, 0.8, 0.9],
            'risk_bucket_2_factor_2': [0.1, 0.2, 0.3],
            'risk_bucket_2_weight_2': [0.4, 0.5, 0.6]
        })

    def test_calculate_risk_bucket_scores(self):
        result = calculate_risk_bucket_scores(self.df_project, num_buckets=2, num_factors=2)
        self.assertIn('risk_bucket_1_score', result.columns)
        self.assertIn('risk_bucket_2_score', result.columns)

    def test_invalid_input(self):
        with self.assertRaises(KeyError):
            calculate_risk_bucket_scores(self.df_project, num_buckets=3, num_factors=2)

    def test_default_values(self):
        result = calculate_risk_bucket_scores(self.df_project, num_buckets=2, num_factors=2)
        self.assertEqual(len(result.columns), len(self.df_project.columns))  # Two new columns added

class TestScoreToRatingVectorized(unittest.TestCase):
    def test_valid_scores(self):
        scores = pd.Series([0, 3.5, 7.5, 10])
        ratings = score_to_rating_vectorized(scores)
        self.assertEqual(ratings.tolist(), ['C', 'C', 'Speculative', 'Investment'])

    def test_invalid_scores(self):
        scores = pd.Series([-1, 11])
        with self.assertRaises(ValueError):
            score_to_rating_vectorized(scores)

    def test_boundary_values(self):
        scores = pd.Series([3.5, 3.6, 7.5, 7.6])
        ratings = score_to_rating_vectorized(scores)
        self.assertEqual(ratings.tolist(), ['C', 'Speculative', 'Speculative', 'Investment'])

    def test_empty_series(self):
        scores = pd.Series([])
        ratings = score_to_rating_vectorized(scores)
        self.assertEqual(len(ratings), 0)

class TestCalculateYearlyShortfall(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'contract_duration': [5, 10, 7],
            'risk_bucket_1_rating': ['Investment', 'Speculative', 'Investment'],
            'risk_bucket_2_rating': ['Speculative', 'Investment', 'Speculative']
        })
        self.df_default_rates = pd.DataFrame(index=['Investment', 'Speculative'], columns=range(1, 11), data=0.05)
        self.df_recovery_potential = pd.DataFrame(index=['Investment', 'Speculative'], columns=range(1, 11), data=0.1)
        self.risk_bucket_count = 2
        self.num_years = 10

    def test_calculate_yearly_shortfall(self):
        result = calculate_yearly_shortfall(self.df_project, self.df_default_rates, self.df_recovery_potential, self.risk_bucket_count, self.num_years)
        self.assertEqual(result.shape[1], self.df_project.shape[1] + self.risk_bucket_count * self.num_years)

    def test_calculate_yearly_shortfall_with_nan_values(self):
        self.df_project.loc[0, 'contract_duration'] = np.nan
        result = calculate_yearly_shortfall(self.df_project, self.df_default_rates, self.df_recovery_potential, self.risk_bucket_count, self.num_years)
        self.assertTrue(result.iloc[:, -self.risk_bucket_count * self.num_years:].isna().any().any())

    def test_calculate_yearly_shortfall_with_invalid_rating(self):
        self.df_project.loc[0, 'risk_bucket_1_rating'] = 'Invalid'
        with self.assertRaises(KeyError):
            calculate_yearly_shortfall(self.df_project, self.df_default_rates, self.df_recovery_potential, self.risk_bucket_count, self.num_years)

class TestCalculateYearlyExpectedValue(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'offered_volume_year_1': [100, 200, 300],
            'offered_volume_year_2': [150, 250, 350],
            'risk_bucket_1_shortfall_year_1': [0.1, 0.2, 0.3],
            'risk_bucket_1_shortfall_year_2': [0.15, 0.25, 0.35],
            'risk_bucket_2_shortfall_year_1': [0.05, 0.1, 0.15],
            'risk_bucket_2_shortfall_year_2': [0.1, 0.2, 0.3]
        })
        self.num_risk_buckets = 2
        self.num_years = 2

    def test_calculate_yearly_expected_value(self):
        result = calculate_yearly_expected_value(self.df_project, self.num_risk_buckets, self.num_years)
        expected_columns = ['offered_volume_year_1', 'offered_volume_year_2',
                        'risk_bucket_1_shortfall_year_1', 'risk_bucket_1_shortfall_year_2',
                        'risk_bucket_2_shortfall_year_1', 'risk_bucket_2_shortfall_year_2',
                        'risk_bucket_1_expected_value_year_1',
                        'risk_bucket_1_expected_value_year_2',
                        'risk_bucket_2_expected_value_year_1',
                        'risk_bucket_2_expected_value_year_2']
        self.assertEqual(list(result.columns), expected_columns)

    def test_calculate_yearly_expected_value_with_nan_values(self):
        self.df_project.loc[0, 'offered_volume_year_1'] = np.nan
        result = calculate_yearly_expected_value(self.df_project, self.num_risk_buckets, self.num_years)
        self.assertTrue(result.iloc[:, -self.num_risk_buckets * self.num_years:].isna().any().any())

    def test_calculate_yearly_expected_value_with_missing_columns(self):
        self.df_project.drop(columns=['risk_bucket_1_shortfall_year_1'], inplace=True)
        with self.assertRaises(KeyError):
            calculate_yearly_expected_value(self.df_project, self.num_risk_buckets, self.num_years)

class TestCalculateYearlyStandardDeviation(unittest.TestCase):
    def setUp(self):
        self.df_project = pd.DataFrame({
            'offered_volume_year_1': [100, 200],
            'risk_bucket_1_expected_value_year_1': [50, 100]
        })

    def test_valid_input(self):
        result = calculate_yearly_standard_deviation(self.df_project, num_risk_buckets=1, num_years=1)
        self.assertIn('risk_bucket_1_standard_deviation_year_1', result.columns)

    def test_invalid_column_names(self):
        df_project = pd.DataFrame({
            'invalid_column_name': [100, 200],
            'risk_bucket_1_expected_value_year_1': [50, 100]
        })
        with self.assertRaises(KeyError):
            calculate_yearly_standard_deviation(df_project, num_risk_buckets=1, num_years=1)

    def test_non_numeric_values(self):
        df_project = pd.DataFrame({
            'offered_volume_year_1': ['a', 'b'],
            'risk_bucket_1_expected_value_year_1': [50, 100]
        })
        with self.assertRaises(TypeError):
            calculate_yearly_standard_deviation(df_project, num_risk_buckets=1, num_years=1)

if __name__ == '__main__':
    unittest.main()
