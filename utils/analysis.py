import pandas as pd
import numpy as np

def calculate_top_bottom_projects(df_project, num_projects, columns):
    """
    Calculate the top and bottom projects based on their average expected value.

    Parameters:
    df_project (pandas DataFrame): The DataFrame containing the project data.
    num_projects (int): The number of top and bottom projects to return.
    columns (list): A list of columns to include in the top and bottom projects DataFrames.

    Returns:
    top_projects (pandas DataFrame): The top projects based on their average expected value.
    bottom_projects (pandas DataFrame): The bottom projects based on their average expected value.
    """

    if num_projects <= 0:
        raise ValueError('num_projects must be greater than 0')
    
    # Calculate the mean of expected value percentages for each project
    expected_value_columns = [f'project_expected_value_percentage_year_{i}' for i in range(1, 11)]
    average_expected_values = df_project[expected_value_columns].mean(axis=1, skipna=True)

    # Select and sort projects by their average expected value
    top_bottom_projects = df_project[columns].assign(average_expected_value=average_expected_values)
    top_projects = top_bottom_projects.sort_values(by='average_expected_value', ascending=False).head(num_projects).reset_index(drop=True)
    top_projects.insert(0, 'rank', range(1, num_projects + 1))

    bottom_projects = top_bottom_projects.sort_values(by='average_expected_value', ascending=True).head(num_projects).reset_index(drop=True)
    bottom_projects.insert(0, 'rank', range(1, num_projects + 1))

    return top_projects, bottom_projects

def create_group_table(df_project, group_by):
    """
    Creates a table showing the total offered volume, total projects, and percentage of each rating for each group.

    Parameters:
    df_project (pandas DataFrame): A DataFrame containing the project data. It's expected to have columns named 'country', 'technology', 'counterparty', 'offered_volume_year_1' through 'offered_volume_year_10', and 'overall_project_rating'.
    group_by (str): The column to group by. Must be either 'country', 'technology', or 'counterparty'.

    Returns:
    pandas DataFrame: A DataFrame containing the total offered volume, total projects, and percentage of each rating for each group.
    """
    # Check for valid groups
    if group_by not in ['country', 'technology', 'counterparty']:
        raise ValueError("group_by must be 'country', 'technology', or 'counterparty'")

    # Calculate the tables
    total_offered_volume = df_project[[f'offered_volume_year_{i}' for i in range(1, 11)]].sum(axis=1)
    group_table = df_project.assign(total_offered_volume=total_offered_volume).groupby(group_by).agg({
        'total_offered_volume': 'sum',
        'overall_project_rating': 'count'
    }).reset_index()
    group_table = group_table.rename(columns={
        'total_offered_volume': 'Total Offered Volume',
        'overall_project_rating': 'Total Projects'
    })
    group_rating_counts = df_project.groupby([group_by, 'overall_project_rating'], observed=False).size().reset_index(name='counts')
    group_rating_counts = group_rating_counts.pivot(index=group_by, columns='overall_project_rating', values='counts').reset_index()
    group_table = pd.merge(group_table, group_rating_counts, on=group_by).fillna(0)

    # Format the tables
    rating_columns = [col for col in group_table.columns if col not in ['Total Offered Volume', 'Total Projects', group_by]]
    for col in rating_columns:
        group_table[col] = round((group_table[col] / group_table['Total Projects']) * 100, 2)

    group_table = group_table.rename(columns={col: f'{col} (%)' for col in rating_columns})

    return group_table

def calculate_total_volumes_by_year(df_project):
    """
    Calculate the total offered volume and overall project delivery for each calendar year.

    Parameters:
    df_project (pandas DataFrame): A DataFrame containing the project data.

    Returns:
    pandas DataFrame: A DataFrame with the total offered volume and overall project delivery for each calendar year.
    """

    if df_project.empty:
        return pd.DataFrame(columns=['Year', 'Total Offered Volume', 'Overall Project Delivery'])

    end_years = df_project['start_year'] + df_project['contract_duration'] - 1
    
    total_volumes_by_year = pd.DataFrame(index=range(df_project['start_year'].min(), end_years.max() + 1), columns=['Total Offered Volume', 'Overall Project Delivery'])
    total_volumes_by_year[['Total Offered Volume', 'Overall Project Delivery']] = 0.0

    for index, row in df_project.iterrows():
        for i in range(row['contract_duration']):
            year = row['start_year'] + i
            total_volumes_by_year.loc[year, 'Total Offered Volume'] += row[f'offered_volume_year_{i+1}']
            total_volumes_by_year.loc[year, 'Overall Project Delivery'] += row[f'project_delivery_volume_year_{i+1}']

    total_volumes_by_year = total_volumes_by_year.reset_index().rename(columns={'index': 'Year'})

    return total_volumes_by_year