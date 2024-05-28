# GHG_Pro

### Introduction

The GHG_Pro project is a data-driven tool designed to estimate the potential greenhouse gas (GHG) reductions of various projects, taking into account the risks associated with their implementation. By leveraging risk screening data, this project provides a more realistic assessment of a project's likely impact on reducing GHG emissions, helping stakeholders make more informed decisions and prioritize initiatives that are most likely to succeed.

### Overview

The GHG_Pro project is a data-driven tool designed to estimate the potential greenhouse gas (GHG) reductions of various projects. The project takes into account the risks associated with project implementation, providing a more realistic assessment of a project's likely impact on reducing GHG emissions.

#### Key Features

* Supports five customizable risk categories, such as Country Risk and Technology Risk
* Accepts data inputs from CSV and XLSX files for easy integration with existing workflows
* Utilizes Monte Carlo simulations to estimate the percentage of GHG reductions achieved each year of project operation

#### Benefits

* Provides a more accurate estimate of GHG reductions by accounting for project-specific risks
* Allows users to easily input and analyze data from various sources
* Offers a robust and reliable method for estimating GHG reductions through Monte Carlo simulations

### Requirements

To run the GHG_Pro project, you'll need to install the required dependencies listed in the `requirements.txt` file. You can do this by running the following command in your terminal:
pip install -r requirements.txt

This will install all the necessary dependencies, including [list some of the key dependencies, e.g., pandas, numpy, etc.].

Note: Make sure you have Python [3.0] or higher installed on your system.

### Usage

To run the GHG_Pro project, navigate to the main directory and execute the project_risk.py file using Python:
python project_risk.py

This will read in the data and perform the analysis. By default, it will look for an Excel file named GHG_Data.xlsx in the data directory. However, you can specify the input file format as either 'excel', 'csv', or 'tsv' by passing an optional command line argument, like this:
python project_risk.py -i csv

If you choose 'csv', the script will instead look for three separate CSV files named GHG_Data.csv, Default_Rates.csv, and Recovery_Potential.csv in the data directory. If you choose 'tsv', the script will look for three separate TSV files named GHG_Data.tsv, Default_Rates.tsv, and Recovery_Potential.tsv in the data directory.

You can also control whether the console output is displayed or not by using the -d option. To display the console output, use -d on:
python project_risk.py -d on

To hide the console output, use -d off:
python project_risk.py -d off

By default, the console output is displayed.

If you want to generate sample data for testing purposes, you can use the generate_project_risk_data.py script located in the scripts directory. To generate sample data, run the following command:
python scripts/generate_project_risk_data.py

By default, this script will generate 100 test projects with 5 risk buckets and 5 risk factors and save them to an Excel file named GHG_Data.xlsx. You can specify the number of test projects, risk buckets, and risk factors to generate by passing optional command line arguments, like this:
python scripts/generate_project_risk_data.py -p 10 -b 3 -f 4

Replace 10 with the desired number of test projects, 3 with the desired number of risk buckets, and 4 with the desired number of risk factors. The number of test projects must be an integer between 0 and 1000, the number of risk buckets must be an integer between 1 and 10, and the number of risk factors must be an integer between 1 and 10. You can also specify the output file format as either 'excel', 'csv', or 'tsv' by adding the -o option, like this:
python scripts/generate_project_risk_data.py -p 10 -b 3 -f 4 -o csv

Note: Make sure you have the required dependencies installed (see the Requirements section above) before running the project.

### Methodology

The `project_risk.py` file performs the following steps to analyze the project risk data:

1. `calculate_risk_bucket_scores(df_project, num_buckets=5, num_factors=5):` This function calculates risk bucket scores for a given DataFrame. It takes in a DataFrame with risk factors and weights, and outputs the same DataFrame with additional columns containing the calculated risk bucket scores. The function assumes a specific naming convention for the input DataFrame's columns. It calculates the risk bucket scores by multiplying corresponding factors and weights, summing these products, and assigning the sums to new 'risk_bucket_X_score' columns in the DataFrame.
2. `score_to_rating_vectorized(scores):` This function takes in a pandas Series of scores and outputs a corresponding Series of project ratings. The function first checks that all scores are between 0 and 10, raising an error if not. It then uses the pandas cut function to assign a rating to each score based on the following bins: scores less than or equal to 3.5 are rated 'C', scores between 3.5 and 7.5 are rated 'Speculative', and scores greater than 7.5 are rated 'Investment'.
3. `calculate_yearly_shortfall(df_project, df_default_rates, df_recovery_potential, risk_bucket_count):` This function calculates the shortfall for each year and risk bucket in a project. It takes in three DataFrames: one with project data, one with default rates, and one with recovery potentials. It also takes in the number of risk buckets. The function then calculates the shortfall for each year (1-10) and risk bucket by looking up the default rate and recovery potential for the project's rating and contract duration, and applying the formula (default rate * (1 - recovery potential)) / 100. If the year is beyond the project's contract duration, the shortfall is set to NaN. The calculated shortfalls are then added as new columns to the project DataFrame, which is returned by the function.
4. `calculate_yearly_expected_value(df_project, num_risk_buckets=5, num_years=10):` This function calculates the yearly expected value for each risk bucket and year in a project. It takes in a DataFrame with project data, as well as the number of risk buckets and years. The function calculates the expected value for each year and risk bucket by multiplying the offered volume for that year by (1 - shortfall for that year and risk bucket). The calculated expected values are then added as new columns to the project DataFrame, which is returned by the function.
5. `calculate_yearly_standard_deviation(df_project, num_risk_buckets=5, num_years=10):` This function calculates the yearly standard deviation for each risk bucket and year in a project. It takes in a DataFrame with project data, as well as the number of risk buckets and years. The function calculates the standard deviation for each year and risk bucket by multiplying 0.5 by the difference between the offered volume for that year and the expected value for that year and risk bucket. The calculated standard deviations are stored in a new DataFrame, which is then concatenated with the original DataFrame. The updated DataFrame is returned by the function. 
6. `run_simulation(df_project, num_buckets, num_samples=10000)`: This function runs a simulation to calculate the projected delivery volume and its standard deviation for each year in a project. It takes in a DataFrame with expected values and standard deviations for each risk bucket, the number of risk buckets, as well as the number of random samples to generate (default is 10000). The function generates random samples for each risk bucket using a normal distribution with the expected value and standard deviation for that bucket. It then calculates the projected delivery volume for each set of input samples by summing the samples across all risk buckets. The function calculates the standard deviation of the projected delivery volume for each year, as well as the project delivery volume (defined as the offered volume minus twice the standard deviation) and the project expected value percentage (defined as the project delivery volume divided by the offered volume). The results are stored in new columns in the input DataFrame, including 'project_standard_deviation_year_i', 'project_delivery_volume_year_i', and 'project_expected_value_percentage_year_i' for i in range(1,11), which is returned by the function.
7. Then the average expected value percentage is calculated for all years of each project. This is used by the `score_to_rating_vectorized(scores):` to assign an overall rating for the project. Then the number of "Investment", "Speculative", and "C" projects are group into a new dataframe.
8. `calculate_top_bottom_projects(df_project, num_projects, columns):` This function calculates the top and bottom projects based on their average expected value. It takes in a DataFrame with project data, the number of top and bottom projects to return, and a list of columns to include in the output DataFrames. The function calculates the mean of the expected value percentages for each project across all years. It then selects and sorts the projects by their average expected value, and returns two DataFrames: one with the top projects (those with the highest average expected values) and one with the bottom projects (those with the lowest average expected values). The output DataFrames include the specified columns from the input DataFrame, as well as a new column with the average expected value and a 'rank' column indicating the project's ranking.
9. `create_group_table(df_project, group_by):` This function creates a table showing the total offered volume, total projects, and percentage of each rating for each group in a project DataFrame. The group can be by country, technology, or counterparty. The function first checks if the group_by parameter is valid. Then it calculates the total offered volume for each project by summing up the offered volumes across all years. It then groups the projects by the specified group and calculates the total offered volume and total projects for each group. Next, it counts the number of projects with each rating for each group and pivots the result to create a table with the counts of each rating for each group. This table is then merged with the previous table. Finally, the function formats the table by calculating the percentage of each rating for each group and renaming the columns. The resulting table is returned by the function.
10. `calculate_total_volumes_by_year(df_project):` This function calculates the total offered volume and overall project delivery for each calendar year in the project DataFrame. 
The function first calculates the end years for each project by adding the contract duration to the start year. It then creates a new DataFrame with the total offered volume and overall project delivery for each year, initializing these values to 0. The function then iterates over each project and each year of the project's contract duration. For each year, it adds the offered volume and overall project delivery for that year to the corresponding values in the total volumes by year DataFrame. Finally, the function resets the index of the total volumes by year DataFrame and renames the index column to 'Year'. The resulting DataFrame is returned by the function.

### GHG_Pro.xlsx
The GHG_Pro.xlsx is a comprehensive Excel-based application designed to streamline the project screening process. The tool consists of three main components: Model Configuration, Project Screening, and Project Analysis.

#### Configuring a Model
The GHG_Pro.xlsx allows users to configure a model by entering the necessary information in the Model Config worksheet. This includes:

Model ID and name
- Maximum number of risk buckets
- Maximum number of risk factors for each bucket
- Names of each risk bucket
- Names and descriptions of each risk factor, along with their scoring rules and weights (which must add up to 1 for each risk bucket)

Once the model configuration is defined, users can save, edit, or delete different models as needed. To begin screening projects, the model configuration must be applied.
The `ApplyModelConfig` subroutine is responsible for applying the model configuration to the Project Screening worksheet. It does this by:

- Clearing any existing input values
- Generating headers for the project data
- Copying the model name, number of risk buckets, and number of risk factors from the Model Config worksheet to the Project Screening worksheet
- Copying the names of each risk bucket, risk factor, and scoring rules from the Model Config worksheet to the Project Screening worksheet
- This ensures that the Project Screening worksheet is properly configured and ready for use with the defined model configuration.

#### Screening Projects
GHG_Pro.xlsx allows users to screen projects by entering the necessary information in the Project Screening worksheet. This includes:

- Project ID and name
- Technology, country, and counterparty
- Start year and contract duration
- Offered volume for each year of the contract duration
- Scores for each risk factor (between 0 and 10)

Once the project information is entered, it must be saved to the Project Data worksheet. The `SaveProjectData` subroutine is responsible for validating the input data and saving it to the Project Data worksheet. It performs the following tasks:

- Checks if a model has been applied before saving the project data
- Validates the input data, including the project ID, name, contract duration, country, technology, counterparty, start year, and offered volumes
- Validates the risk factors
- Saves the project data to the Project Data worksheet, including the project ID, name, contract duration, country, technology, counterparty, start year, screening date, and offered volumes
- Saves the risk bucket factors to the Project Data worksheet
- Clears the input values in the Project Screening worksheet after saving the project data

Projects can also be updated and deleted after they are saved.

#### Analyzing Projects
After screening all projects, the saved projects in the Project Data worksheet can be analyzed by GHG_Pro.py. The Analyze Model button in the Model Config worksheet prepares the saved projects for analysis.

The AnalyzeModel subroutine is responsible for preparing the saved projects for analysis. It does this by:

Creating a new workbook named "GHG_Data.xlsx" in the "/data" directory
Copying the Project Data worksheet to the new workbook
Copying the Default Rates and Recovery Potential ranges from the Model Config worksheet to the new workbook
Copying the Model Config data to the new workbook
Saving the new workbook
Before creating the new workbook, the subroutine checks if a file named "GHG_Data.xlsx" already exists in the "/data" directory. If it does, it warns the user and asks for confirmation before proceeding.

Once the new workbook is created, it is ready to be analyzed by the GHG_Pro.py. GHG_Pro.py is called to analyze the projects in GHG_Data.xls. This Python script uses xlwings to interact with the Excel file and perform the analysis. The results of the analysis are then saved to the output directory

### Data and Inputs
This project either requires a single excel input file, GHG_Data.xlsx, located in the data directory, or 4 csv/tsv files (ex: GHG_Data.csv, Default_Rates.csv, Recovery_Potential.csv, Model_Config.csv). The file(s) need to have the following organization:

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

Columns: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Rows: Investment, Speculative, C
Cell values: Default rates for each category and year
For example:
1	2	3	4	5	6	7	8	9	10
Investment	0.14	0.37	0.64	0.98	1.34	1.71	2.06	2.41	2.74	3.08
Speculative	4.49	8.91	12.81	15.95	18.47	20.6	22.37	23.88	25.23	26.46
C	27.58	38.13	44.28	48.19	51.09	52.43	53.59	54.47	55.66	56.51

#### Recovery Potential
This sheet should contain recovery potentials for "Investment", "Speculative", and "C" over 10 years, with the following format:

Columns: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Rows: Investment, Speculative, C
Cell values: Recovery potentials for each category and year
For example:
1	2	3	4	5	6	7	8	9	10
Investment	0	0.5	0.67	0.75	0.8	0.83	0.86	0.88	0.89	0.9
Speculative	0	0	0.03	0.5	0.6	0.67	0.71	0.75	0.78	0.8
C	0	0	0	0	0.08	0.24	0.34	0.43	0.49	0.54

### Model Config
This sheet should contain the model configuration data with the following columns:

- model_id: Unique identifier for the model
- model_name: Name of the model
- num_buckets: Number of risk buckets in the model
- num_factors: Number of risk factors in the model
- last_saved: Date the model was last saved
- risk_bucket_1_name: Name of the first risk bucket
- risk_bucket_1_factor_1_name: Name of the first factor in the first risk bucket
- risk_bucket_1_factor_1_rules: Rules for the first factor in the first risk bucket
- risk_bucket_1_factor_2_name: Name of the second factor in the first risk bucket
- risk_bucket_1_factor_2_rules: Rules for the second factor in the first risk bucket
...
- risk_bucket_2_name: Name of the second risk bucket
- risk_bucket_2_factor_1_name: Name of the first factor in the second risk bucket
- risk_bucket_2_factor_1_rules: Rules for the first factor in the second risk bucket
- risk_bucket_2_factor_2_name: Name of the second factor in the second risk bucket
- risk_bucket_2_factor_2_rules: Rules for the second factor in the second risk bucket
...
...
- risk_bucket_num_buckets_name: Name of the last risk bucket
- risk_bucket_num_buckets_factor_1_name: Name of the first factor in the last risk bucket
- risk_bucket_num_buckets_factor_1_rules: Rules for the first factor in the last risk bucket
- risk_bucket_num_buckets_factor_num_factors_name: Name of the last factor in the last risk bucket
- risk_bucket_num_buckets_factor_num_factors_rules: Rules for the last factor in the last risk bucket

Note: The actual column names will depend on the number of risk buckets and factors in the model. The above list is just an example.

#### Data Processing and Validation
The data from the 4 sheets is loaded and processed by the `load_and_process_data` function, which:

- Loads the data from either an Excel file (default) or CSV files into four separate DataFrames: df_project, df_default_rates, df_recovery_potential, and df_model. The input file format can be specified as 'excel' or 'csv' using a command line argument.
- Sets the index for the df_default_rates and df_recovery_potential DataFrames.
- Converts the column names of df_default_rates and df_recovery_potential to integers.
- Replaces NaN values with 0 in the risk bucket factors and weights columns of df_project.
- Converts the 'Screening Date' column of df_project to datetime format.

Please ensure that the input file adheres to this column structure and formatting to ensure proper functioning of the project. If using CSV files, please ensure that there are four separate files named 'GHG_Data.csv', 'Default_Rates.csv', 'Recovery_Potential.csv', and 'Model_Config.csv'.

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

The `valid_model` function checks if df_model contains a valid model configuration. It checks the following conditions:

- There is a model id, model name, number of risk buckets, number of risk factors and last saved column.
- There are risk bucket names, risk bucket factor names, and risk bucket factor rules for the correct number of risk buckets and factors
- There is only one configuration in the data frame.

If any of these conditions are not me, the function returns False. Otherwise, it returns True.

### Output
After running the GHG_Pro project, three output files will be generated:

- GHG_Data_Simulation.xlsx: This file contains the detailed analysis output for every project that was screened.
- Project_Risk_Summary_Data.xlsx: This file summarizes the simulation results by country, counterparty, technology, and by year.
- Model_Config.xlsx: This file contains the model configuration data used for the simulation.

Both output files will be saved to a timestamped subfolder in the /output directory. The subfolder name will reflect the date and time when the analysis was run, allowing you to easily keep track of different runs and compare results.

### License and Credits
This GHG_Pro project is released under the Creative Commons Attribution 4.0 International License. This project would not be possible without the following sources:

- The process of converting risk scores to ratings was made possible by the European Bank for Reconstruction and Development (EBRD).
- The default rate table is public information sourced from Moody's.
- The recovery potential table is public information sourced from Standard & Poors.
- The definition of Overall Project Shortfall as 2 Standard Deviations (i.e. 95% confidence band) and Expected Value as the mean was originally proposed by Advisors Grant Thornton and M. Margolick Economist.
- The risk analysis process was originally developed by Paul Vickers M.ENG.
We acknowledge the essential contributions of these organizations and individuals to the development of this project.

### Conclusion

The GHG_Pro project is a powerful tool for estimating the potential greenhouse gas reductions of various projects. By taking into account the risks associated with project implementation, this project provides a more realistic assessment of a project's likely impact on reducing GHG emissions. We hope that this project will be useful for stakeholders seeking to make informed decisions about investments in GHG reduction projects.

Thank you for considering the GHG_Pro project.
