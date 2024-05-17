# project_risk.py
# Author: Mark Vickers
# Date Created: 2024-05-11
# Description: Calculates project risk scores and generates output tables

from utils.io import *
from utils.risk_calculation import *
from utils.analysis import *
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        risk_bucket_count, df_project, df_default_rates, df_recovery_potential = load_and_process_data()
        
        if valid_project_data(df_project,risk_bucket_count) and check_df_format(df_default_rates, df_recovery_potential):        
            
            # Calculate Risk Bucket Risk Scores and Ratings for each risk bucket 
            df_project = calculate_risk_bucket_scores(df_project,risk_bucket_count)        
            for i in range(1, risk_bucket_count + 1):
                df_project[f'risk_bucket_{i}_rating'] = score_to_rating_vectorized(df_project[f'risk_bucket_{i}_score'])
            
            # Prepare for the simulation
            df_project = calculate_yearly_exposure(df_project, df_default_rates, df_recovery_potential, risk_bucket_count)
            df_project = calculate_yearly_expected_value(df_project, risk_bucket_count)
            df_project = calculate_yearly_standard_deviation(df_project,risk_bucket_count)
        
            # Run the yearly simulations for all projects
            df_project = run_simulation(df_project, risk_bucket_count)
            overall_expected_value_percentage = df_project[[f'project_expected_value_percentage_year_{year}' for year in range(1, 11)]].mean(axis=1, skipna=True) * 10
            df_project['overall_project_rating'] = score_to_rating_vectorized(overall_expected_value_percentage)

            # Calculate Project Output Tables
            df_counts = pd.DataFrame(df_project['overall_project_rating'].value_counts()).reset_index()
            df_counts.columns = ['overall_project_rating', 'counts']
            top_projects, bottom_projects = calculate_top_bottom_projects(df_project, 10, ['project_id', 'project_name', 'country', 'technology', 'counterparty', 'start_year'])            
            country_table = create_group_table(df_project, 'country')
            technology_table = create_group_table(df_project, 'technology')
            counterparty_table = create_group_table(df_project, 'counterparty')
            total_volumes_per_year = calculate_total_volumes_by_year(df_project)
            
            # Display and Export Data
            display_project_risk_output(df_counts, top_projects, bottom_projects, country_table, technology_table, counterparty_table, total_volumes_per_year)
            output_folder = create_output_folder()
            export_project_risk_output(output_folder, top_projects, bottom_projects, country_table, technology_table, counterparty_table, df_counts, total_volumes_per_year)
            export_ghg_data(output_folder, df_project,df_default_rates,df_recovery_potential)
        else:
            print("Data not loaded properly from GHG_Data.xlsx")

    except FileNotFoundError as e:
        logging.error(f"File not found: {str(e)}")
    except pd.errors.EmptyDataError as e:
        logging.error(f"Empty data error: {str(e)}")
    except TypeError as e:
        logging.error(f"Type error occurred: {str(e)}")
    except ValueError as e:
        logging.error(f"Value error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise