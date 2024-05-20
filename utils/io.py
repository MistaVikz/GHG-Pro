import sys
import os
import pandas as pd
import numpy as np
import datetime
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Border, Side, Alignment, PatternFill

def load_and_process_data(input_choice='excel'):
    """
    Load and process data from Excel file or CSV files.

    Parameters:
    input_choice (str): The format of the input data. Default is 'excel'.

    Returns:
    num_buckets (int): The number of risk buckets.
    num_risk_factors (int): The number of risk factors.
    df_project (pandas.DataFrame): A DataFrame containing project data.
    df_default_rates (pandas.DataFrame): A DataFrame containing default rates data.
    df_recovery_potential (pandas.DataFrame): A DataFrame containing recovery potential data.

    Notes:
    This function assumes that the input Excel file contains three sheets named 'Project Data', 'Default Rates', and 'Recovery Potential'.
    If input_choice is 'csv' or 'tsv', it assumes that there are three separate files named 'GHG_Data.csv', 'Default_Rates.csv', and 'Recovery_Potential.csv' or 'GHG_Data.tsv', 'Default_Rates.tsv', and 'Recovery_Potential.tsv' respectively.
    """
    if input_choice == 'excel':
        # Load Data
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.join(current_dir, '..', 'data')
        file_path = os.path.join(data_dir, 'GHG_Data.xlsx')

        df_project = pd.read_excel(file_path, sheet_name='Project Data')  
        df_default_rates = pd.read_excel(file_path, sheet_name='Default Rates')
        df_recovery_potential = pd.read_excel(file_path, sheet_name='Recovery Potential')

    elif input_choice == 'csv':
        # Load Data
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.join(current_dir, '..', 'data')

        df_project = pd.read_csv(os.path.join(data_dir, 'GHG_Data.csv'))  
        df_default_rates = pd.read_csv(os.path.join(data_dir, 'Default_Rates.csv'))
        df_recovery_potential = pd.read_csv(os.path.join(data_dir, 'Recovery_Potential.csv'))

    elif input_choice == 'tsv':
        # Load Data
        current_dir = os.path.dirname(__file__)
        data_dir = os.path.join(current_dir, '..', 'data')

        df_project = pd.read_csv(os.path.join(data_dir, 'GHG_Data.tsv'), sep='\t')  
        df_default_rates = pd.read_csv(os.path.join(data_dir, 'Default_Rates.tsv'), sep='\t')
        df_recovery_potential = pd.read_csv(os.path.join(data_dir, 'Recovery_Potential.tsv'), sep='\t')

    else:
        raise ValueError("Invalid input choice. Please choose 'excel', 'csv', or 'tsv'.")

    # Set index for default rates and recovery potential dataframes
    df_default_rates = df_default_rates.set_index('Unnamed: 0')
    df_recovery_potential = df_recovery_potential.set_index('Unnamed: 0')

    # Convert Data Types
    df_default_rates.columns = df_default_rates.columns.astype(int)
    df_recovery_potential.columns= df_recovery_potential.columns.astype(int)

    # Replace NaN with 0 in risk bucket factors and weights columns
    risk_columns = [col for col in df_project.columns if 'risk_bucket' in col]
    df_project[risk_columns] = df_project[risk_columns].fillna(0)

    # Convert 'Screening Date' to datetime
    df_project['screening_date'] = pd.to_datetime(df_project['screening_date'])

    # Calculate the number of risk buckets
    num_buckets = max(int(col.split('_')[2]) for col in df_project.columns if 'risk_bucket' in col)

    # Calculate the number of risk factors
    num_risk_factors = len([col for col in df_project.columns if 'factor' in col and f"risk_bucket_1_factor" in col])

    return num_buckets, num_risk_factors, df_project, df_default_rates, df_recovery_potential

def create_output_folder():
    """
    Create a time-stamped folder for the simulation output and summary output
    """
    # Get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")

    # Get the current directory of the script
    current_dir = os.path.dirname(__file__)

    # Construct the path to the output directory
    output_dir = os.path.join(current_dir, '..', 'output')

    # Create a new folder with the timestamp
    folder_name = os.path.join(output_dir, date_time)
    os.makedirs(folder_name, exist_ok=True)

    return folder_name

def export_ghg_data(output_folder,df_project, df_default_rates, df_recovery_potential):
    """
    Export GHG data to an Excel file.

    Parameters:
    df_project (pandas.DataFrame): A DataFrame containing project data.
    df_default_rates (pandas.DataFrame): A DataFrame containing default rates data.
    df_recovery_potential (pandas.DataFrame): A DataFrame containing recovery potential data.

    Notes:
    This function exports the input DataFrames to three separate worksheets in the 'GHG_Data.xlsx' file.
    The 'Default Rates' and 'Recovery Potential' worksheets include "Investment", "Speculative", and "C" next to the values.
    """
    # Create a new workbook for GHG_Data.xlsx
    wb = Workbook()
    ws = wb.active
    ws.title = 'Project Data'

    # Write df_project to the worksheet
    for row in dataframe_to_rows(df_project, index=False):
        ws.append(row)

    # Adjust column widths
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 25
    ws.column_dimensions['B'].width = 35

    # Add row color switching
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            if cell.row % 2 == 0:
                cell.fill = PatternFill(start_color='C5C5C5', fill_type='solid')

    # Bold/Underline headers
    for cell in ws["1:1"]:
        cell.font = Font(bold=True, underline='single')

    # Write df_default_rates to the Default Rates worksheet
    wb.create_sheet('Default Rates')
    ws = wb['Default Rates']
    ws.append([""] + list(df_default_rates.columns))
    ws.append(["Investment"] + list(df_default_rates.loc["Investment"]))
    ws.append(["Speculative"] + list(df_default_rates.loc["Speculative"]))
    ws.append(["C"] + list(df_default_rates.loc["C"]))

    # Adjust column widths
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 15
    
    # Add row color switching
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            if cell.row % 2 == 0:
                cell.fill = PatternFill(start_color='C5C5C5', fill_type='solid')

    # Bold/Underline headers
    for cell in ws["1:1"]:
        cell.font = Font(bold=True, underline='single')

    # Write df_recovery_potential to the Recovery Potential worksheet
    wb.create_sheet('Recovery Potential')
    ws = wb['Recovery Potential']
    ws.append([""] + list(df_recovery_potential.columns))
    ws.append(["Investment"] + list(df_recovery_potential.loc["Investment"]))
    ws.append(["Speculative"] + list(df_recovery_potential.loc["Speculative"]))
    ws.append(["C"] + list(df_recovery_potential.loc["C"]))

    # Adjust column widths
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 15
    
    # Add row color switching
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            if cell.row % 2 == 0:
                cell.fill = PatternFill(start_color='C5C5C5', fill_type='solid')

    # Bold/Underline headers
    for cell in ws["1:1"]:
        cell.font = Font(bold=True, underline='single')

    # Save simulation output
    now = datetime.datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")
    wb.save(f"{output_folder}/GHG_Data_Simulation_{date_time}.xlsx")

def export_project_risk_output(output_folder, top_projects, bottom_projects, country_table, technology_table, counterparty_table, df_counts, total_volumes_per_year):
    """
    Exports project risk output to an Excel file.

    Parameters:
    top_projects (DataFrame): Top performing projects.
    bottom_projects (DataFrame): Bottom performing projects.
    country_table (DataFrame): Country table.
    technology_table (DataFrame): Technology table.
    counterparty_table (DataFrame): Counterparty table.
    df_counts (DataFrame): Project rating distribution counts.
    total_volumes_per_year (DataFrame): Total volumes per year data.

    Returns:
    None

    Notes:
    This function creates an Excel file named 'project_risk_output.xlsx' and writes the input DataFrames to separate worksheets in the file. The worksheets are ordered as follows: Project Rating Distribution, Highest Performing Projects, Lowest Performing Projects, Annual Project Volumes, Overall Project Rating Distribution by Country, Overall Project Rating Distribution by Technology, Overall Project Rating Distribution by Counterparty.
    """
    
    # Create the workbook
    wb = Workbook()
    ws_df_counts = wb.active
    ws_df_counts.title = "Rating Distribution"
    ws_top_projects = wb.create_sheet("Highest Performing")
    ws_bottom_projects = wb.create_sheet("Lowest Performing")
    ws_total_volumes_per_year = wb.create_sheet("Annual Volumes")
    ws_country_table = wb.create_sheet("Country Distribution")
    ws_technology_table = wb.create_sheet("Technology Distribution")
    ws_counterparty_table = wb.create_sheet("Counterparty Distribution")

    # Reorder worksheets
    wb._sheets = [ws_df_counts, ws_top_projects, ws_bottom_projects, ws_total_volumes_per_year, ws_country_table, ws_technology_table, ws_counterparty_table]

    # Write titles to worksheets
    ws_df_counts['A1'] = "Project Rating Distribution"
    ws_df_counts['A1'].font = Font(bold=True, size=16)
    ws_top_projects['A1'] = "Highest Performing Projects"
    ws_top_projects['A1'].font = Font(bold=True, size=16)
    ws_bottom_projects['A1'] = "Lowest Performing Projects"
    ws_bottom_projects['A1'].font = Font(bold=True, size=16)
    ws_total_volumes_per_year['A1'] = "Annual Project Volumes"
    ws_total_volumes_per_year['A1'].font = Font(bold=True, size=16)
    ws_country_table['A1'] = "Overall Project Rating Distribution by Country"
    ws_country_table['A1'].font = Font(bold=True, size=16)
    ws_technology_table['A1'] = "Overall Project Rating Distribution by Technology"
    ws_technology_table['A1'].font = Font(bold=True, size=16)
    ws_counterparty_table['A1'] = "Overall Project Rating Distribution by Counterparty"
    ws_counterparty_table['A1'].font = Font(bold=True, size=16)

    # Write data to worksheets
    for row in dataframe_to_rows(df_counts, index=False, header=True):
        ws_df_counts.append(row)
    for row in dataframe_to_rows(top_projects, index=False, header=True):
        ws_top_projects.append(row)
    for row in dataframe_to_rows(bottom_projects, index=False, header=True):
        ws_bottom_projects.append(row)
    for row in dataframe_to_rows(total_volumes_per_year, index=False, header=True):
        ws_total_volumes_per_year.append(row)

    rows = dataframe_to_rows(country_table, index=False, header=True)
    header = next(rows)
    ws_country_table.append(header)
    for row in rows:
        if row != [''] * len(row):
            ws_country_table.append(row)

    rows = dataframe_to_rows(technology_table, index=False, header=True)
    header = next(rows)
    ws_technology_table.append(header)
    for row in rows:
        if row != [''] * len(row):
            ws_technology_table.append(row)

    rows = dataframe_to_rows(counterparty_table, index=False, header=True)
    header = next(rows)
    ws_counterparty_table.append(header)
    for row in rows:
        if row != [''] * len(row):
            ws_counterparty_table.append(row)

    # Set column widths
    for ws in [ws_top_projects, ws_bottom_projects, ws_country_table, ws_technology_table, ws_counterparty_table, ws_df_counts, ws_total_volumes_per_year]:
        for col in ws.columns:
            ws.column_dimensions[col[0].column_letter].width = 20
    ws_top_projects.column_dimensions['C'].width = 35
    ws_bottom_projects.column_dimensions['C'].width = 35
    ws_top_projects.column_dimensions['H'].width = 26
    ws_bottom_projects.column_dimensions['H'].width = 26
    ws_total_volumes_per_year.column_dimensions['C'].width = 25
    ws_df_counts.column_dimensions['A'].width = 26

    # Add borders
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
    for ws in [ws_top_projects, ws_bottom_projects, ws_country_table, ws_technology_table, ws_counterparty_table, ws_df_counts, ws_total_volumes_per_year]:
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.border = thin_border

    # Alternate row colors
    for ws in [ws_top_projects, ws_bottom_projects, ws_country_table, ws_technology_table, ws_counterparty_table, ws_df_counts, ws_total_volumes_per_year]:
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                if cell.row % 2 == 0:
                    cell.fill = PatternFill(start_color='C5C5C5', fill_type='solid')

    # Bold and underline headers
    for ws in [ws_top_projects, ws_bottom_projects, ws_country_table, ws_technology_table, ws_counterparty_table, ws_df_counts, ws_total_volumes_per_year]:
        for cell in ws["2:2"]:
            cell.font = Font(bold=True, underline='single')

    # Get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%Y%m%d_%H%M%S")
    wb.save(f"{output_folder}/Project_Risk_Summary_Data_{date_time}.xlsx")

def valid_project_data(df: pd.DataFrame, num_buckets: int, num_factors: int) -> bool:
    """
    Validates the data in the project DataFrame.

    Parameters:
        df (pd.DataFrame): The project DataFrame to validate.
        num_buckets (int): The number of risk buckets.
        num_factors (int): The number of risk factors.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    # Check if all required columns exist
    required_columns = ['project_id', 'project_name', 'contract_duration', 'country', 'technology', 'counterparty', 'start_year', 'screening_date']
    for year in range(1, 11):
        required_columns.append(f'offered_volume_year_{year}')
    for bucket in range(1, num_buckets + 1):
        for factor in range(1, num_factors + 1):
            required_columns.append(f'risk_bucket_{bucket}_factor_{factor}')
            required_columns.append(f'risk_bucket_{bucket}_weight_{factor}')

    if not all(column in df.columns for column in required_columns):
        print("Error: Not all required columns are present.")
        return False
    
    # Check if Project ID is not null and unique
    if df['project_id'].isnull().any() or df['project_id'].duplicated().any():
        print("Error: Project ID column contains null or duplicate values.")
        return False
    
    # Check if Contract Duration is an integer between 1 and 10
    if df['contract_duration'].dtype != 'int64' or (df['contract_duration'] < 1).any() or (df['contract_duration'] > 10).any():
        print("Error: Contract Duration column contains invalid values. Values must be integers between 1 and 10.")
        return False
    
    # Check if Start Year is an integer greater or equal to 2000
    if df['start_year'].dtype != 'int64' or (df['start_year'] < 2000).any():
        print("Error: Start Year column contains invalid values. Values must be integers greater or equal to 2000.")
        return False
        
    # Check if Screening Date is a date
    if df['screening_date'].dtype != 'datetime64[ns]':
        print("Error: Screening Date column contains invalid values. Values must be dates.")
        return False
    
    # Check if Project Name, Technology, Country, and Counterparty are strings
    for column in ['project_name', 'technology', 'country', 'counterparty']:
        if df[column].dtype != 'object':
            print(f"Error: {column} column contains invalid values. Values must be strings.")
            return False

    for bucket in range(1, num_buckets + 1):
        weight_columns = [f'risk_bucket_{bucket}_weight_{factor}' for factor in range(1, num_factors + 1)]
        if not np.all(np.round(df[weight_columns].sum(axis=1), 6) == 1):
            print(f"Error: Weights for risk bucket {bucket} must sum to 1.")
            return False
    
    return True

def display_project_risk_output(df_counts, top_projects, bottom_projects, country_table, technology_table, counterparty_table, total_volumes_per_year):
    """
    Prints project risk output dataframes in markdown format.

    Parameters:
    df_counts (pd.DataFrame): Project rating distribution dataframe.
    top_projects (pd.DataFrame): Top projects dataframe.
    bottom_projects (pd.DataFrame): Bottom projects dataframe.
    country_table (pd.DataFrame): Country table dataframe.
    technology_table (pd.DataFrame): Technology table dataframe.
    counterparty_table (pd.DataFrame): Counterparty table dataframe.
    total_volumes_per_year (pd.DataFrame): Total volumes per year dataframe.
    """
    
    # Don't print if cmd line argument is set
    if len(sys.argv) > 1 and sys.argv[1] == '--noprint':
        return
    
    print("Project Rating Distribution")
    print(df_counts.to_markdown(index=False))
    print("\nHighest Performing Projects")
    print(top_projects.to_markdown(index=False))
    print("\nLowest Performing Projects")
    print(bottom_projects.to_markdown(index=False))
    print("\nOverall Project Rating Distribution by Country")
    print(country_table.to_markdown(index=False))
    print("\nOverall Project Rating Distribution by Technology")
    print(technology_table.to_markdown(index=False))
    print("\nOverall Project Rating Distribution by Counterparty")
    print(counterparty_table.to_markdown(index=False))
    print("\nAnnual Project Volumes")
    print(total_volumes_per_year.to_markdown(index=False))

def check_df_format(df_default_rates, df_recovery_potential):
    """
    This function checks if two dataframes, df_default_rates and df_recovery_potential, are formatted correctly.
    
    "Formatted correctly" means that the dataframes should have the same shape (i.e., same number of rows and columns), 
    the same column names, the same index values, and the correct row names.

    Parameters:
    df_default_rates (pandas.DataFrame): The first dataframe to compare.
    df_recovery_potential (pandas.DataFrame): The second dataframe to compare.

    Returns:
    bool: True if the dataframes are formatted correctly, False otherwise.
    """

    # Check if both dataframes have the same shape
    if df_default_rates.shape != df_recovery_potential.shape:
        return False

    # Check if both dataframes have the correct row names
    if list(df_default_rates.index) != ['Investment', 'Speculative', 'C'] or list(df_recovery_potential.index) != ['Investment', 'Speculative', 'C']:
        return False

    # Check if both dataframes have the correct column names
    if list(df_default_rates.columns) != list(range(1, 11)) or list(df_recovery_potential.columns) != list(range(1, 11)):
        return False

    # Check if all values in both dataframes are numbers greater or equal to zero
    if not ((df_default_rates.apply(lambda x: x >= 0) & df_default_rates.apply(lambda x: pd.to_numeric(x, errors='coerce')).notnull()).all().all() and
            (df_recovery_potential.apply(lambda x: x >= 0) & df_recovery_potential.apply(lambda x: pd.to_numeric(x, errors='coerce')).notnull()).all().all()):
        return False

    return True

