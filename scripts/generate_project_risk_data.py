import pandas as pd
import numpy as np
import random
import os
import logging
import argparse
from datetime import date, datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

NUM_YEARS = 10

default_rates = {
    "Investment": [0.14, 0.37, 0.64, 0.98, 1.34, 1.71, 2.06, 2.41, 2.74, 3.08],
    "Speculative": [4.49, 8.91, 12.81, 15.95, 18.47, 20.6, 22.37, 23.88, 25.23, 26.46],
    "C": [27.58, 38.13, 44.28, 48.19, 51.09, 52.43, 53.59, 54.47, 55.66, 56.51]
}

recovery_potential = {
    "Investment": [0, 0.5, 0.67, 0.75, 0.8, 0.83, 0.86, 0.88, 0.89, 0.9],
    "Speculative": [0, 0, 0.03, 0.5, 0.6, 0.67, 0.71, 0.75, 0.78, 0.8],
    "C": [0, 0, 0, 0, 0.08, 0.24, 0.34, 0.43, 0.49, 0.54]
}

def parse_args():
    """
    Parse command line arguments.

    Returns:
        args: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--projects', type=int, default=100, help='Number of projects')
    parser.add_argument('-b', '--buckets', type=int, default=5, help='Number of risk buckets')
    parser.add_argument('-f', '--factors', type=int, default=5, help='Number of factors')
    return parser.parse_args()

def generate_data(num_projects, num_buckets, num_factors):
    """
    Generate data for GHG projects.

    Args:
        num_projects (int): Number of projects to generate.
        num_buckets (int): Number of risk buckets.
        num_factors (int): Number of factors.

    Returns:
        df: DataFrame containing generated data.
    """
    # Column names
    columns = [
        'project_id', 'project_name', 'contract_duration', 'country', 'technology', 'counterparty', 'start_year', 'screening_date'
    ]

    for i in range(1, num_buckets + 1):
        for j in range(1, num_factors + 1):
            columns.append(f'risk_bucket_{i}_factor_{j}')
            columns.append(f'risk_bucket_{i}_weight_{j}')

    # Lists of names
    environment_names = ["Wind", "Hydro", "Solar", "Geothermal", "Biofuel", "Green", "Recycling", "Eco-Friendly", "Sustainable", "Conservation"]
    site_names = ["East", "West", "North", "South", "Site A", "Site B", "Site C", "Site D", "Park", "Reserve"]
    company_names = ["GreenTech Inc.", "EcoEnergy Corp.", "Renewable Solutions", "Sustainable Futures", "Clean Power Co.", "ClimateCare Ltd.", "EarthFirst Energy", "Nature's Way", "Pure Planet", "BioEnergy Systems"]
    country_list = ['Italy', 'Spain', 'Brazil', 'USA', 'Netherlands', 'France', 'Germany', 'India', 'China', 'Japan', 'South Africa', 'Australia', 'Canada', 'Mexico', 'Russia', 'South Korea', 'Indonesia', 'Turkey', 'Poland', 'Sweden']
    technology_list = ['Renewable Energy', 'Carbon Capture', 'Energy Efficiency', 'Waste Management', 'Water Conservation', 'Sustainable Agriculture', 'Forestry Management', 'Air Pollution Reduction', 'Waste-to-Energy', 'Green Building Practices']
    counterparty_list = ['Non-Profit Organization', 'Government Agency', 'Community Group', 'Private Company', 'NGO']

    # Data
    data = {
        'project_id': range(1, num_projects + 1),
        'project_name': [' '.join(random.sample([random.choice(company_names), random.choice(environment_names), random.choice(site_names)], 3)) for _ in range(num_projects)],
        'contract_duration': np.random.randint(1, NUM_YEARS + 1, num_projects),
        'country': [random.choice(country_list) for _ in range(num_projects)],
        'technology': [random.choice(technology_list) for _ in range(num_projects)],
        'counterparty': [random.choice(counterparty_list) for _ in range(num_projects)],
        'start_year': np.random.randint(2000, 2015, num_projects),
        'screening_date': [date.today().strftime("%Y-%m-%d")] * num_projects
    }

    # Offered volumes
    for i in range(1, NUM_YEARS + 1):
        data[f'offered_volume_year_{i}'] = np.where(i <= data['contract_duration'], np.random.randint(100000, 950001, num_projects), np.nan)

    # Risk factors and weights
    weights = np.random.dirichlet(np.ones(num_factors) * 10, size=1)[0]  # Generate weights once
    for i in range(1, num_buckets + 1):
        for j in range(1, num_factors + 1):
            data[f'risk_bucket_{i}_factor_{j}'] = np.random.randint(0, 11, num_projects)
            data[f'risk_bucket_{i}_weight_{j}'] = [weights[j-1]] * num_projects  # Use the same weights for each project

    # Create a DataFrame
    df = pd.DataFrame(data)
    return df

def generate_model(num_buckets, num_factors):
    """
    Generate a model.

    Args:
        num_buckets (int): Number of risk buckets.
        num_factors (int): Number of factors.

    Returns:
        df: DataFrame containing the generated model.
    """
    model_id = random.randint(1, 1000)
    model_name = f"Model{model_id}"
    model_last_saved = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        'model_id': [model_id],
        'model_name': [model_name],
        'num_buckets': [num_buckets],
        'num_factors': [num_factors],
        'last_saved': [model_last_saved]
    }

    # Add risk bucket names
    for i in range(1, num_buckets + 1):
        data[f'risk_bucket_{i}_name'] = [f'Risk Bucket {i}']

    # Add factor names and rules for each risk bucket
    for i in range(1, num_buckets + 1):
        for j in range(1, num_factors + 1):
            data[f'risk_bucket_{i}_factor_{j}_name'] = [f'Factor {j}']
            data[f'risk_bucket_{i}_factor_{j}_rules'] = [f'Rules for Factor {j}']

    df = pd.DataFrame(data)
    return df

def write_to_file(df, default_rates, recovery_potential, model_df):
    """
    Write data to file.

    Args:
        df (DataFrame): DataFrame containing data to write.
        default_rates (dict): Dictionary containing default rates.
        recovery_potential (dict): Dictionary containing recovery potential.
        model_df (DataFrame): DataFrame containing the model configuration.
    """

    # Convert dictionaries to DataFrames with specific column names
    df_default_rates = pd.DataFrame(list(default_rates.values()), index=['Investment', 'Speculative', 'C'], columns=range(1, 11))
    df_recovery_potential = pd.DataFrame(list(recovery_potential.values()), index=['Investment', 'Speculative', 'C'], columns=range(1, 11))

    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(os.path.join('..', 'data', 'GHG_Data.xlsx')) as writer:
        df.to_excel(writer, sheet_name='Project Data', index=False)

        # Save DataFrames to Excel worksheets
        df_default_rates.to_excel(writer, sheet_name='Default Rates')
        df_recovery_potential.to_excel(writer, sheet_name='Recovery Potential')
        model_df.to_excel(writer, sheet_name='Model Config', index=False)

if __name__ == "__main__":
    try:
        args = parse_args()

        if not 0 <= args.projects <= 1000:
            raise ValueError("Number of projects must be an integer between 0 and 1000")
        if not 1 <= args.buckets <= 10:
            raise ValueError("Number of risk buckets must be an integer between 1 and 10")
        if not 1 <= args.factors <= 10:
            raise ValueError("Number of factors must be an integer between 1 and 10")

        num_projects = args.projects
        num_buckets = args.buckets
        num_factors = args.factors

        df = generate_data(num_projects, num_buckets, num_factors)
        model_df = generate_model(num_buckets, num_factors)
        write_to_file(df, default_rates, recovery_potential, model_df)

        print(f"Generated {num_projects} projects with {num_buckets} risk buckets and {num_factors} factors and saved to GHG_Data.xlsx in the '../data' directory.")

    except IOError as e:
        logging.error(f"An error occurred while writing to the GHG_Data.xlsx file: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise