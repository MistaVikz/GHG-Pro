# GHG Risk Evaluation

### Introduction

The GHG Risk Evaluation project is a data-driven tool designed to estimate the potential greenhouse gas (GHG) reductions of various projects, taking into account the risks associated with their implementation. By leveraging risk screening data, this project provides a more realistic assessment of a project's likely impact on reducing GHG emissions, helping stakeholders make more informed decisions and prioritize initiatives that are most likely to succeed.

### Overview

The GHG Risk Evaluation project is a data-driven tool designed to estimate the potential greenhouse gas (GHG) reductions of various projects. The project takes into account the risks associated with project implementation, providing a more realistic assessment of a project's likely impact on reducing GHG emissions.

#### Key Features

* Supports five customizable risk categories, such as Country Risk and Technology Risk
* Accepts data inputs from CSV and XLSX files for easy integration with existing workflows
* Utilizes Monte Carlo simulations to estimate the percentage of GHG reductions achieved each year of project operation

#### Benefits

* Provides a more accurate estimate of GHG reductions by accounting for project-specific risks
* Allows users to easily input and analyze data from various sources
* Offers a robust and reliable method for estimating GHG reductions through Monte Carlo simulations

### Requirements

To run the GHG Risk Evaluation project, you'll need to install the required dependencies listed in the `requirements.txt` file. You can do this by running the following command in your terminal:
pip install -r requirements.txt

This will install all the necessary dependencies, including [list some of the key dependencies, e.g., pandas, numpy, etc.].

Note: Make sure you have Python [3.0] or higher installed on your system.

### Usage

To run the GHG Risk Evaluation project, navigate to the main directory and execute the `project_risk.py` file using Python:
python project_risk.py

This will read in the data and perform the analysis.

Here is the updated section of your README.md:

If you want to generate sample data for testing purposes, you can use the `generate_project_risk_data.py` script located in the scripts directory. To generate sample data, run the following command:
`python scripts/generate_project_risk_data.py`

By default, this script will generate 100 test projects with 5 risk buckets. You can specify the number of test projects and risk buckets to generate by passing optional command line arguments, like this:
`python scripts/generate_project_risk_data.py -p 10 -b 3`

Replace 10 with the desired number of test projects and 3 with the desired number of risk buckets. The number of test projects must be an integer between 1 and 1000, and the number of risk buckets must be an integer between 1 and 10.

Note: Make sure you have the required dependencies installed (see the Requirements section above) before running the project.

### Methodology

The `project_risk.py` file performs the following steps to analyze the project risk data:

1. `calculate_risk_bucket_scores(df_project, num_buckets=5, num_factors=5):` This function calculates risk bucket scores for a given DataFrame. It takes in a DataFrame with risk factors and weights, and outputs the same DataFrame with additional columns containing the calculated risk bucket scores. The function assumes a specific naming convention for the input DataFrame's columns. It calculates the risk bucket scores by multiplying corresponding factors and weights, summing these products, and assigning the sums to new 'risk_bucket_X_score' columns in the DataFrame.
2. `score_to_rating_vectorized(scores):` This function takes in a pandas Series of scores and outputs a corresponding Series of project ratings. The function first checks that all scores are between 0 and 10, raising an error if not. It then uses the pandas cut function to assign a rating to each score based on the following bins: scores less than or equal to 3.5 are rated 'C', scores between 3.5 and 7.5 are rated 'Speculative', and scores greater than 7.5 are rated 'Investment'.
3. `calculate_yearly_exposure(df_project, df_default_rates, df_recovery_potential, risk_bucket_count):` This function calculates the exposure for each year and risk bucket in a project. It takes in three DataFrames: one with project data, one with default rates, and one with recovery potentials. It also takes in the number of risk buckets. The function then calculates the exposure for each year (1-10) and risk bucket by looking up the default rate and recovery potential for the project's rating and contract duration, and applying the formula (default rate * (1 - recovery potential)) / 100. If the year is beyond the project's contract duration, the exposure is set to NaN. The calculated exposures are then added as new columns to the project DataFrame, which is returned by the function.
4. `calculate_yearly_expected_value(df_project, num_risk_buckets=5, num_years=10):` This function calculates the yearly expected value for each risk bucket and year in a project. It takes in a DataFrame with project data, as well as the number of risk buckets and years. The function calculates the expected value for each year and risk bucket by multiplying the offered volume for that year by (1 - exposure for that year and risk bucket). The calculated expected values are then added as new columns to the project DataFrame, which is returned by the function.
5. `calculate_yearly_standard_deviation(df_project, num_risk_buckets=5, num_years=10):` This function calculates the yearly standard deviation for each risk bucket and year in a project. It takes in a DataFrame with project data, as well as the number of risk buckets and years. The function calculates the standard deviation for each year and risk bucket by multiplying 0.5 by the difference between the offered volume for that year and the expected value for that year and risk bucket. The calculated standard deviations are stored in a new DataFrame, which is then concatenated with the original DataFrame. The updated DataFrame is returned by the function. 
6. `run_simulation(df_project, num_buckets, num_samples=10000)`: This function runs a simulation to calculate the projected delivery volume and its standard deviation for each year in a project. It takes in a DataFrame with expected values and standard deviations for each risk bucket, the number of risk buckets, as well as the number of random samples to generate (default is 10000). The function generates random samples for each risk bucket using a normal distribution with the expected value and standard deviation for that bucket. It then calculates the projected delivery volume for each set of input samples by summing the samples across all risk buckets. The function calculates the standard deviation of the projected delivery volume for each year, as well as the project delivery volume (defined as the offered volume minus twice the standard deviation) and the project expected value percentage (defined as the project delivery volume divided by the offered volume). The results are stored in new columns in the input DataFrame, including 'project_standard_deviation_year_i', 'project_delivery_volume_year_i', and 'project_expected_value_percentage_year_i' for i in range(1,11), which is returned by the function.
7. Then the average expected value percentage is calculated for all years of each project. This is used by the `score_to_rating_vectorized(scores):` to assign an overall rating for the project. Then the number of "Investment", "Speculative", and "C" projects are group into a new dataframe.
8. `calculate_top_bottom_projects(df_project, num_projects, columns):` This function calculates the top and bottom projects based on their average expected value. It takes in a DataFrame with project data, the number of top and bottom projects to return, and a list of columns to include in the output DataFrames. The function calculates the mean of the expected value percentages for each project across all years. It then selects and sorts the projects by their average expected value, and returns two DataFrames: one with the top projects (those with the highest average expected values) and one with the bottom projects (those with the lowest average expected values). The output DataFrames include the specified columns from the input DataFrame, as well as a new column with the average expected value and a 'rank' column indicating the project's ranking.
9. `create_group_table(df_project, group_by):` This function creates a table showing the total offered volume, total projects, and percentage of each rating for each group in a project DataFrame. The group can be by country, technology, or counterparty. The function first checks if the group_by parameter is valid. Then it calculates the total offered volume for each project by summing up the offered volumes across all years. It then groups the projects by the specified group and calculates the total offered volume and total projects for each group. Next, it counts the number of projects with each rating for each group and pivots the result to create a table with the counts of each rating for each group. This table is then merged with the previous table. Finally, the function formats the table by calculating the percentage of each rating for each group and renaming the columns. The resulting table is returned by the function.
10. `calculate_total_volumes_by_year(df_project):` This function calculates the total offered volume and overall project delivery for each calendar year in the project DataFrame. 
The function first calculates the end years for each project by adding the contract duration to the start year. It then creates a new DataFrame with the total offered volume and overall project delivery for each year, initializing these values to 0. The function then iterates over each project and each year of the project's contract duration. For each year, it adds the offered volume and overall project delivery for that year to the corresponding values in the total volumes by year DataFrame. Finally, the function resets the index of the total volumes by year DataFrame and renames the index column to 'Year'. The resulting DataFrame is returned by the function.

### Data and Inputs

This project requires a single input file, GHG_Data.xlsx, located in the data directory. The file should be in Excel (.xlsx) format and contain the following sheets:

#### Project Data

This sheet should contain the following columns:
- project_id: Unique identifier for each project
- project_name: Name of each project
- contract_duration: Contract duration for each project
- country: Country where each project is located
- technology: Technology used for each project
- counterparty: Counterparty for each project
- start_year: Start year for each project
- screening_date: Screening date for each project
- offered_volume_year_1 to offered_volume_year_10: Offered volume for each project over 10 years
- risk_bucket_1_factor_1 to risk_bucket_1_factor_5: Factors for Risk Bucket 1
- risk_bucket_1_weight_1 to risk_bucket_1_weight_5: Weights for Risk Bucket 1
...
- risk_bucket_5_factor_1 to risk_bucket_5_factor_5: Factors for Risk Bucket 5
- risk_bucket_5_weight_1 to risk_bucket_5_weight_5: Weights for Risk Bucket 5

#### Default Rates

This sheet should contain default rates for "Investment", "Speculative", and "C" over 10 years, with the following format:
- Columns: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
- Rows: Investment, Speculative, C
- Cell values: Default rates for each category and year
For example:

|  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Investment | 0.14 | 0.37 | 0.64 | 0.98 | 1.34 | 1.71 | 2.06 | 2.41 | 2.74 | 3.08 |
| Speculative | 4.49 | 8.91 | 12.81 | 15.95 | 18.47 | 20.6 | 22.37 | 23.88 | 25.23 | 26.46 |
| C | 27.58 | 38.13 | 44.28 | 48.19 | 51.09 | 52.43 | 53.59 | 54.47 | 55.66 | 56.51 |

#### Recovery Potential

This sheet should contain recovery potentials for "Investment", "Speculative", and "C" over 10 years, with the following format:
- Columns: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
- Rows: Investment, Speculative, C
- Cell values: Recovery potentials for each category and year
For example:

|  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Investment | 0 | 0.5 | 0.67 | 0.75 | 0.8 | 0.83 | 0.86 | 0.88 | 0.89 | 0.9 |
| Speculative | 0 | 0 | 0.03 | 0.5 | 0.6 | 0.67 | 0.71 | 0.75 | 0.78 | 0.8 |
| C | 0 | 0 | 0 | 0 | 0.08 | 0.24 | 0.34 | 0.43 | 0.49 | 0.54 |

#### Data Processing and Validation

The data from the 3 sheets is loaded and processed by the `load_and_process_data` function, which:
- Loads the data from the Excel file into three separate DataFrames: df_project, df_default_rates, and df_recovery_potential.
- Sets the index for the df_default_rates and df_recovery_potential DataFrames.
- Converts the column names of df_default_rates and df_recovery_potential to integers.
- Replaces NaN values with 0 in the risk bucket factors and weights columns of df_project.
- Converts the 'Screening Date' column of df_project to datetime format.
- Please ensure that the input file adheres to this column structure and formatting to ensure proper functioning of the project.

The `valid_project_data` function validates the data in the df_project DataFrame by checking the following conditions:
- All required columns are present.
- Project ID is not null and unique.
- Contract Duration is an integer between 1 and 10.
- Start Year is an integer greater or equal to 2000.
- Offered Volume is an integer greater than 0.
- Screening Date is a date.
- Project Name, Technology, Country, and Counterparty are strings.
- The sum of the weights for each risk bucket equals 1.

If any of these conditions are not met, the function prints an error message and returns False. Otherwise, it returns True.

The `check_df_format` function checks if two dataframes, df_default_rates and df_recovery_potential, are formatted correctly by checking the following conditions:

- Both dataframes have the same shape (i.e., same number of rows and columns).
- Both dataframes have the correct row names ("Investment", "Speculative", and "C").
- Both dataframes have the correct column names (integers from 1 to 10).
- All values in both dataframes are numbers greater or equal to zero.

If any of these conditions are not met, the function returns False. Otherwise, it returns True.

### Output

After running the GHG Risk Evaluation project, two output files will be generated:

1. `GHG_Data_Simulation.xlsx`: This file contains the detailed analysis output for every project that was screened.
2. `Project_Risk_Summary_Data.xlsx`: This file summarizes the simulation results by country, counterparty, technology, and by year.

Both output files will be saved to a timestamped subfolder in the `/output` directory. The subfolder name will reflect the date and time when the analysis was run, allowing you to easily keep track of different runs and compare results.

### License and Credits

This GHG Risk Evaluation project is released under the Creative Commons Attribution 4.0 International License. This project was inspired by the following sources:

* The process of converting risk scores to ratings was inspired by the European Bank for Reconstruction and Development (EBRD).
* The default rate table is sourced from Moody's.
* The recovery potential table is sourced from Standard & Poors.

We acknowledge the contributions of these organizations to the development of this project.

### Conclusion

The GHG Risk Evaluation project is a powerful tool for estimating the potential greenhouse gas reductions of various projects. By taking into account the risks associated with project implementation, this project provides a more realistic assessment of a project's likely impact on reducing GHG emissions. We hope that this project will be useful for stakeholders seeking to make informed decisions about investments in GHG reduction projects.

Thank you for considering the GHG Risk Evaluation project.
