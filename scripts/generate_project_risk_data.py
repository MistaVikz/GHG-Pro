import pandas as pd
import numpy as np
import random
import os
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)

NUM_YEARS = 10

if __name__ == "__main__":
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--projects', type=int, default=100, help='Number of projects')
        parser.add_argument('-b', '--buckets', type=int, default=5, help='Number of risk buckets')
        parser.add_argument('-f', '--factors', type=int, default=5, help='Number of factors')
        parser.add_argument('-o', '--output', choices=['excel', 'csv'], default='excel', help='Output file format')
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
            'contract_duration': np.random.randint(1, NUM_YEARS + 1, num_projects),
            'country': [random.choice(country_list) for _ in range(num_projects)],
            'technology': [random.choice(technology_list) for _ in range(num_projects)],
            'counterparty': [random.choice(counterparty_list) for _ in range(num_projects)],
            'start_year': np.random.randint(2000, 2015, num_projects),
            'screening_date': ['2024-05-11'] * num_projects
        }

        for i in range(1, NUM_YEARS + 1):
            data[f'offered_volume_year_{i}'] = np.random.randint(100000, 950001, num_projects)

        for i in range(1, num_buckets + 1):
            weights = np.random.dirichlet(np.ones(num_factors) * 10, size=num_projects)
            for j in range(1, num_factors + 1):
                data[f'risk_bucket_{i}_factor_{j}'] = np.random.randint(0, 11, num_projects)
                data[f'risk_bucket_{i}_weight_{j}'] = weights[:, j-1]

        # Create a DataFrame
        df = pd.DataFrame(data)

        if args.output == 'csv':
            # Write the DataFrame to a CSV file
            df.to_csv(os.path.join('..', 'data', 'GHG_Data.csv'), index=False)
        
            default_rates = {
                "Investment": {i: 0.14 * i for i in range(1, NUM_YEARS + 1)},
                "Speculative": {i: 4.49 * i for i in range(1, NUM_YEARS + 1)},
                "C": {i: 27.58 * i for i in range(1, NUM_YEARS + 1)}
            }

            recovery_potential = {
                "Investment": {i: 0 * i for i in range(1, NUM_YEARS + 1)},
                "Speculative": {i: 0 * i for i in range(1, NUM_YEARS + 1)},
                "C": {i: 0 * i for i in range(1, NUM_YEARS + 1)}
            }

            # Convert dictionaries to DataFrames
            df_default_rates = pd.DataFrame(default_rates).T
            df_recovery_potential = pd.DataFrame(recovery_potential).T

            # Save DataFrames to csv files
            df_default_rates.to_csv(os.path.join('..', 'data', 'Default_Rates.csv'))
            df_recovery_potential.to_csv(os.path.join('..', 'data', 'Recovery_Potential.csv'))
        else:
            # Write the DataFrame to an Excel file
            with pd.ExcelWriter(os.path.join('..', 'data', 'GHG_Data.xlsx')) as writer:
                df.to_excel(writer, sheet_name='Project Data', index=False)

                # Write Default Rates and Recovery Potential To the same excel file

                default_rates = {
                    "Investment": {i: 0.14 * i for i in range(1, NUM_YEARS + 1)},
                    "Speculative": {i: 4.49 * i for i in range(1, NUM_YEARS + 1)},
                    "C": {i: 27.58 * i for i in range(1, NUM_YEARS + 1)}
                }

                recovery_potential = {
                    "Investment": {i: 0 * i for i in range(1, NUM_YEARS + 1)},
                    "Speculative": {i: 0 * i for i in range(1, NUM_YEARS + 1)},
                    "C": {i: 0 * i for i in range(1, NUM_YEARS + 1)}
                }

                # Convert dictionaries to DataFrames
                df_default_rates = pd.DataFrame(default_rates).T
                df_recovery_potential = pd.DataFrame(recovery_potential).T

                # Save DataFrames to Excel worksheets
                df_default_rates.to_excel(writer, sheet_name='Default Rates')
                df_recovery_potential.to_excel(writer, sheet_name='Recovery Potential')

        print(f"Generated {num_projects} projects with {num_buckets} risk buckets and {num_factors} factors and saved to GHG_Data.{args.output}")

    except IOError as e:
        logging.error(f"An error occurred while writing to the {args.output.upper()} file: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise