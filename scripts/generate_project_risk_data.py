import pandas as pd
import numpy as np
import random
import os
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--projects', type=int, default=100, help='Number of projects')
        parser.add_argument('-b', '--buckets', type=int, default=5, help='Number of risk buckets')
        parser.add_argument('-f', '--factors', type=int, default=5, help='Number of factors')
        args = parser.parse_args()

        if not 0 <= args.projects <= 1000:
            raise ValueError("Number of projects must be an integer between 0 and 1000")
        if not 1 <= args.buckets <= 10:
            raise ValueError("Number of risk buckets must be an integer between 1 and 10")
        if not 1 <= args.factors <= 10:
            raise ValueError("Number of factors must be an integer between 1 and 10")

        num_projects = args.projects
        num_buckets = args.buckets
        num_factors = args.factors

        # Define the columns
        columns = [
            'project_id', 'project_name', 'contract_duration', 'country', 'technology', 'counterparty', 'start_year', 'screening_date'
        ]

        for i in range(1, num_buckets + 1):
            for j in range(1, num_factors + 1):
                columns.append(f'risk_bucket_{i}_factor_{j}')
                columns.append(f'risk_bucket_{i}_weight_{j}')

        environment_names = ["Wind", "Hydro", "Solar", "Geothermal", "Biofuel", "Green", "Recycling", "Eco-Friendly", "Sustainable", "Conservation"]
        site_names = ["East", "West", "North", "South", "Site A", "Site B", "Site C", "Site D", "Park", "Reserve"]
        company_names = ["GreenTech Inc.", "EcoEnergy Corp.", "Renewable Solutions", "Sustainable Futures", "Clean Power Co.", "ClimateCare Ltd.", "EarthFirst Energy", "Nature's Way", "Pure Planet", "BioEnergy Systems"]
        country_list = ['Italy', 'Spain', 'Brazil', 'USA', 'Netherlands', 'France', 'Germany', 'India', 'China', 'Japan', 'South Africa', 'Australia', 'Canada', 'Mexico', 'Russia', 'South Korea', 'Indonesia', 'Turkey', 'Poland', 'Sweden']
        technology_list = ['Renewable Energy', 'Carbon Capture', 'Energy Efficiency', 'Waste Management', 'Water Conservation', 'Sustainable Agriculture', 'Forestry Management', 'Air Pollution Reduction', 'Waste-to-Energy', 'Green Building Practices']
        counterparty_list = ['Non-Profit Organization', 'Government Agency', 'Community Group', 'Private Company', 'NGO']

        data = {
            'project_id': range(1, num_projects + 1),
            'project_name': [' '.join(random.sample([random.choice(company_names), random.choice(environment_names), random.choice(site_names)], 3)) for _ in range(num_projects)],
            'contract_duration': np.random.randint(1, 11, num_projects),
            'country': [random.choice(country_list) for _ in range(num_projects)],
            'technology': [random.choice(technology_list) for _ in range(num_projects)],
            'counterparty': [random.choice(counterparty_list) for _ in range(num_projects)],
            'start_year': np.random.randint(2000, 2015, num_projects),
            'screening_date': ['2024-05-11'] * num_projects
        }

        for i in range(1, 11):
            data[f'offered_volume_year_{i}'] = np.random.randint(100000, 950001, num_projects)

        for i in range(1, num_buckets + 1):
            weights = np.random.dirichlet(np.ones(num_factors), size=num_projects)
            for j in range(1, num_factors + 1):
                data[f'risk_bucket_{i}_factor_{j}'] = np.random.randint(0, 11, num_projects)
                data[f'risk_bucket_{i}_weight_{j}'] = weights[:, j-1]

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Write the DataFrame to an Excel file
        with pd.ExcelWriter(os.path.join('..', 'data', 'GHG_Data.xlsx')) as writer:
            df.to_excel(writer, sheet_name='Project Data', index=False)

            # Write Default Rates and Recovery Potential To the same excel file

            default_rates = {
                "Investment": {1: 0.14, 2: 0.37, 3: 0.64, 4: 0.98, 5: 1.34, 6: 1.71, 7: 2.06, 8: 2.41, 9: 2.74,10: 3.08},
                "Speculative": {1: 4.49, 2: 8.91, 3: 12.81, 4: 15.95, 5: 18.47, 6: 20.6, 7: 22.37, 8: 23.88, 9: 25.23,10: 26.46},
                "C": {1: 27.58, 2: 38.13, 3: 44.28, 4: 48.19, 5: 51.09, 6: 52.43, 7: 53.59, 8: 54.47, 9: 55.66,10: 56.51}
            }

            recovery_potential = {
                "Investment": {1: 0, 2: 0.5, 3: 0.67, 4: 0.75, 5: 0.8, 6: 0.83, 7: 0.86, 8: 0.88, 9: 0.89, 10: 0.9},
                "Speculative": {1: 0, 2: 0, 3: 0.03, 4: 0.5, 5: 0.6, 6: 0.67, 7: 0.71, 8: 0.75, 9: 0.78, 10: 0.8},
                "C": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0.08, 6: 0.24, 7: 0.34, 8: 0.43, 9: 0.49, 10: 0.54}
            }

            # Convert dictionaries to DataFrames
            df_default_rates = pd.DataFrame(default_rates).T
            df_recovery_potential = pd.DataFrame(recovery_potential).T

            # Save DataFrames to Excel worksheets
            df_default_rates.to_excel(writer, sheet_name='Default Rates')
            df_recovery_potential.to_excel(writer, sheet_name='Recovery Potential')

        print(f"Generated {num_projects} projects with {num_buckets} risk buckets and {num_factors} factors and saved to GHG_Data.xlsx")

    except IOError as e:
        logging.error(f"An error occurred while writing to the Excel file: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise