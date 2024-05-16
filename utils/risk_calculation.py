import pandas as pd
import numpy as np

def run_simulation(df_project, num_samples=10000):
    """
    Run a simulation to calculate the projected delivery volume and its standard deviation.

    Parameters:
    df_project (pandas.DataFrame): A DataFrame containing the expected values and standard deviations for each risk bucket.
    num_samples (int): The number of random samples to generate. Default is 10000.

    Returns:
    df_project (pandas.DataFrame): The input DataFrame with additional columns: 'project_standard_deviation_year_i' for i in range(1,11).
    """

    # Initialize the results arrays to NaN
    std_dev = np.full((len(df_project), 10), np.nan)
    overall_project_delivery = np.full((len(df_project), 10), np.nan)
    expected_value_percentage = np.full((len(df_project), 10), np.nan)

    # Iterate over each row in the DataFrame
    for index, row in df_project.iterrows():
        contract_duration = int(row['contract_duration'])

        # Run the simulation for each year up to the contract duration
        for year in range(contract_duration):
            risk_bucket_1_exp_val = row[f'risk_bucket_1_expected_value_year_{year+1}']
            risk_bucket_1_std = row[f'risk_bucket_1_standard_deviation_year_{year+1}']
            risk_bucket_2_exp_val = row[f'risk_bucket_2_expected_value_year_{year+1}']
            risk_bucket_2_std = row[f'risk_bucket_2_standard_deviation_year_{year+1}']
            risk_bucket_3_exp_val = row[f'risk_bucket_3_expected_value_year_{year+1}']
            risk_bucket_3_std = row[f'risk_bucket_3_standard_deviation_year_{year+1}']
            risk_bucket_4_exp_val = row[f'risk_bucket_4_expected_value_year_{year+1}']
            risk_bucket_4_std = row[f'risk_bucket_4_standard_deviation_year_{year+1}']
            risk_bucket_5_exp_val = row[f'risk_bucket_5_expected_value_year_{year+1}']
            risk_bucket_5_std = row[f'risk_bucket_5_standard_deviation_year_{year+1}']

            # Generate random samples for each input (10000 samples)
            risk_bucket_1_samples = np.random.normal(loc=risk_bucket_1_exp_val, scale=risk_bucket_1_std, size=num_samples)
            risk_bucket_2_samples = np.random.normal(loc=risk_bucket_2_exp_val, scale=risk_bucket_2_std, size=num_samples)
            risk_bucket_3_samples = np.random.normal(loc=risk_bucket_3_exp_val, scale=risk_bucket_3_std, size=num_samples)
            risk_bucket_4_samples = np.random.normal(loc=risk_bucket_4_exp_val, scale=risk_bucket_4_std, size=num_samples)
            risk_bucket_5_samples = np.random.normal(loc=risk_bucket_5_exp_val, scale=risk_bucket_5_std, size=num_samples)

            # Calculate the projected delivery volume for each set of input samples
            projected_delivery_volume_samples = risk_bucket_1_samples + risk_bucket_2_samples + risk_bucket_3_samples + risk_bucket_4_samples + risk_bucket_5_samples

            # Calculate statistics
            std_dev[index, year] = np.std(projected_delivery_volume_samples)
            overall_project_delivery[index, year] = row[f'offered_volume_year_{year+1}'] - (2 * std_dev[index, year])
            expected_value_percentage[index, year] = overall_project_delivery[index, year] / row[f'offered_volume_year_{year+1}']

    # Store the results in the DataFrame
    for year in range(1, 11):
        df_project[f'project_standard_deviation_year_{year}'] = std_dev[:, year-1]
        df_project[f'overall_project_delivery_year_{year}'] = overall_project_delivery[:, year-1]
        df_project[f'expected_value_percentage_year_{year}'] = expected_value_percentage[:, year-1]

    return df_project


def calculate_risk_bucket_scores(df_project, num_buckets=5, num_factors=5):
    """
    Calculate risk bucket scores for a given DataFrame.

    Parameters:
    df_project (DataFrame): The DataFrame containing the risk bucket factors and weights.
    num_buckets (int, optional): The number of risk buckets. Defaults to 5.
    num_factors (int, optional): The number of factors in each risk bucket. Defaults to 5.

    Returns:
    DataFrame: The input DataFrame with additional columns for each risk bucket score.

    Notes:
    This function assumes that the input DataFrame has columns named 'risk_bucket_X_factor_Y' and 'risk_bucket_X_weight_Y',
    where X is the risk bucket number and Y is the factor number.
    """
    for bucket in range(1, num_buckets+1):
        factors = [f'risk_bucket_{bucket}_factor_{i}' for i in range(1, num_factors+1)]
        weights = [f'risk_bucket_{bucket}_weight_{i}' for i in range(1, num_factors+1)]
        df_project[f'risk_bucket_{bucket}_score'] = sum(df_project[factor] * df_project[weight] for factor, weight in zip(factors, weights))
    return df_project

def score_to_rating_vectorized(scores):
    """
    Determine the project rating based on the score.

    Parameters:
    scores (pandas.Series): A series of scores.

    Returns:
    pandas.Series: A series of project ratings, which can be 'Investment', 'Speculative', or 'C'.
    """
    if not ((scores >= 0) & (scores <= 10)).all():
        raise ValueError("All scores must be between 0 and 10")

    ratings = pd.cut(scores, bins=[-1, 3.5, 7.5, 10], labels=['C', 'Speculative', 'Investment'], include_lowest=True)
    return ratings
    
def calculate_yearly_exposure(df_project, df_default_rates, df_recovery_potential, risk_bucket_count):
    """
    Calculate the exposure for each year and risk bucket.

    Parameters:
    df_project (DataFrame): The DataFrame containing the project data.
    df_default_rates (DataFrame): The DataFrame containing the default rates.
    df_recovery_potential (DataFrame): The DataFrame containing the recovery potentials.
    risk_bucket_count: The number of risk buckets.

    Returns:
    The DataFrame with the calculated exposures.
    """
    exposures = pd.DataFrame(index=df_project.index)
    
    for j in range(1, risk_bucket_count + 1):
        for i in range(1, 11):
            # Calculate the exposure for this year and risk bucket
            exposures[f'risk_bucket_{j}_exposure_year_{i}'] = df_project.apply(lambda row: (df_default_rates.loc[row[f'risk_bucket_{j}_rating'], min(i, row['contract_duration'])] * (1 - df_recovery_potential.loc[row[f'risk_bucket_{j}_rating'], min(i, row['contract_duration'])])) / 100 if i <= row['contract_duration'] else np.nan, axis=1)
    
    df_project = pd.concat([df_project, exposures], axis=1)
    
    return df_project

def calculate_yearly_expected_value(df_project, num_risk_buckets=5, num_years=10):
    """
    Calculate the yearly expected value for each risk bucket and year.

    Parameters:
    df_project (DataFrame): The input DataFrame containing the project data.
    num_risk_buckets (int, optional): The number of risk buckets. Defaults to 5.
    num_years (int, optional): The number of years. Defaults to 10.

    Returns:
    DataFrame: The updated DataFrame with the calculated yearly expected values.
    """
    # Calculate the yearly expected value for each year and risk bucket
    for j in range(1, num_risk_buckets + 1):
        for i in range(1, num_years + 1):
            df_project[f'risk_bucket_{j}_expected_value_year_{i}'] = df_project[f'offered_volume_year_{i}'] * (1 - df_project[f'risk_bucket_{j}_exposure_year_{i}'])
    
    return df_project

def calculate_yearly_standard_deviation(df_project, num_risk_buckets=5, num_years=10):
    """
    Calculate the yearly standard deviation for each risk bucket and year.

    Parameters:
    df_project (DataFrame): The input DataFrame containing the project data.
    num_risk_buckets (int, optional): The number of risk buckets. Defaults to 5.
    num_years (int, optional): The number of years. Defaults to 10.

    Returns:
    DataFrame: The updated DataFrame with the calculated yearly standard deviations.
    """
    # Create a new DataFrame for the standard deviations
    std_dev = pd.DataFrame(index=df_project.index)
    
    # Calculate the yearly standard deviation for each year and risk bucket
    for j in range(1, num_risk_buckets + 1):
        for i in range(1, num_years + 1):
            std_dev[f'risk_bucket_{j}_standard_deviation_year_{i}'] = 0.5 * (df_project[f'offered_volume_year_{i}'] - df_project[f'risk_bucket_{j}_expected_value_year_{i}'])
    
    # Concatenate the new DataFrame with the original DataFrame
    df_project = pd.concat([df_project, std_dev], axis=1)
    
    return df_project


