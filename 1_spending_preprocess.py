import os.path
import pandas as pd
import numpy as np

import os
from dotenv import load_dotenv
load_dotenv()
pathImport=os.getenv('pathImport')

header = pd.read_csv(pathImport+'df_header.csv').loc[:,['District Code', 'District', 'School', 'School Code', 'Level']]

# Import folder path and return dfs for easy retrieval  
def folder_imports(folder_path):
    files = os.listdir(folder_path)
    dfs = {} 
    for file in files:
        new_df = pd.read_csv(os.path.join(folder_path, file))
        dfs[file] = new_df
    return dfs

# Convert to float, then Round 
def round_to_int(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').round(0)

# Rename columns, replace end year, and standardize with df_header 
def format_spending(df, year):
    df.columns = ['End Year', 'School Code', 'Reported Spending per student',
                  'Student Count', 'Educator Count', 'Years of experience']
    df['End Year'] = year
    new_df = header.merge(df, on=['School Code'], how='inner').dropna(thresh=7).reset_index(drop=True)
    return new_df


# Import School data by year. 
dfsSpending = folder_imports(pathImport+'spending')

envir_2012 = dfsSpending['raw_2012.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 
                                                'MEMBERSHIP_TOTAL','FULLTIME_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2012 = format_spending(envir_2012, 2012)

envir_2013 = dfsSpending['raw_2013.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 
                                                'ENROLLMENT_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2013 = format_spending(envir_2013, 2013)

envir_2014 = dfsSpending['raw_2014.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 
                                                'MEMBERSHIP_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2014 = format_spending(envir_2014, 2014)

envir_2015 = dfsSpending['raw_2015.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 
                                                'MEMBERSHIP_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2015 = format_spending(envir_2015, 2015)

envir_2016 = dfsSpending['raw_2016.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 
                                                'MEMBERSHIP_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2016 = format_spending(envir_2016, 2016)

envir_2017 = dfsSpending['raw_2017.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 
                                                'MEMBERSHIP_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2017 = format_spending(envir_2017, 2017)


# Load and format columns for 2018 - 2019 data. To retrieve the same data as above years, three files had to be imported per year.
def format_2018_19(spending, students, teacher):
  df_spending = spending.loc[:, ['SCH_YEAR', 'DIST_NUMBER', 'SCH_NUMBER', 'TOTAL_PER_STU_ALLFUNDS']]
  df_spending['School Code'] = (df_spending['DIST_NUMBER'] * 1000 + df_spending['SCH_NUMBER'])
  df_students = students.loc[:,['DIST_NUMBER', 'SCH_NUMBER', 'MEMBERSHIP_TOTAL']]
  df_students['School Code'] = (df_students['DIST_NUMBER'] * 1000 + df_students['SCH_NUMBER'])
  spending_and_students = df_spending.merge(df_students, how='left', on='School Code')
  df_teacher = teacher.loc[:,['SCH_CD','Teacher Count','AVGEXPERIENCEYEARS']]
  new_df = spending_and_students.merge(df_teacher, left_on='School Code', right_on='SCH_CD', how='left').loc[:, ['SCH_YEAR', 'School Code', 'TOTAL_PER_STU_ALLFUNDS', 'MEMBERSHIP_TOTAL', 'Teacher Count', 'AVGEXPERIENCEYEARS']]
  return new_df

envir_2018 = format_2018_19(dfsSpending['spending_2018.csv'], dfsSpending['stu_2018.csv'], dfsSpending['raw_2018.csv'])
envir_2018 = format_spending(envir_2018, 2018)

envir_2019 = format_2018_19(dfsSpending['spending_2019.csv'], dfsSpending['stu_2019.csv'], dfsSpending['raw_2019.csv'])
envir_2019 = format_spending(envir_2019, 2019)


# Format changed for 2020+ years
students_2020 = dfsSpending['spending_2020.csv'].loc[:,['SCHOOL YEAR', 'SCHOOL CODE', 'Total Spending per Student - All Fund Sources', 'MEMBERSHIP']]
teacher_2020 = dfsSpending['raw_2020.csv'].loc[:,['SCHOOL CODE', 'EDUCATOR COUNT', 'AVERAGE YEARS OF EXPERIENCE']]
envir_2020 = students_2020.merge(teacher_2020, left_on='SCHOOL CODE', right_on='SCHOOL CODE', how='left')
envir_2020 = format_spending(envir_2020, 2020)

students_2021 = dfsSpending['spending_2021.csv'].loc[:,['SCHOOL YEAR', 'SCHOOL CODE', 'Total Spending per Student - All Fund Sources', 'MEMBERSHIP']]
teacher_2021 = dfsSpending['raw_2021.csv'].loc[:,['SCHOOL CODE','EDUCATOR COUNT', 'AVERAGE YEARS OF EXPERIENCE']]
envir_2021 = students_2021.merge(teacher_2021, on='SCHOOL CODE', how='left')
envir_2021 = format_spending(envir_2021, 2021)

students_2022 = dfsSpending['spending_2022.csv'].loc[:,['SCHOOL YEAR', 'SCHOOL CODE', 'Total Spending per Student - All Fund Sources', 'MEMBERSHIP']]
teacher_2022 = dfsSpending['raw_2022.csv'].loc[:,['SCHOOL CODE', 'EDUCATOR COUNT', 'AVERAGE YEARS OF EXPERIENCE']]
envir_2022 = students_2022.merge(teacher_2022, how='left', on='SCHOOL CODE')
envir_2022 = format_spending(envir_2022, 2022)


# 2023 spending data is not available yet - Jan 26 2024.
#.loc[:,['SCHOOL YEAR', 'SCHOOL CODE', 'Total Spending per Student - All Fund Sources', 'MEMBERSHIP']]
teacher_2023 = dfsSpending['raw_2023.csv'].loc[:,['SCHOOL CODE', 'EDUCATOR COUNT', 'AVERAGE YEARS OF EXPERIENCE']]

## Compile school data into one df
spending_df = pd.concat([envir_2012, envir_2013, envir_2014, envir_2015, envir_2016,
                       envir_2017, envir_2018, envir_2019, envir_2020, envir_2021, envir_2022],
                       axis=0, ignore_index=True)


round_to_int(spending_df, ['Reported Spending per student', 'Student Count', 'Educator Count', 'Years of experience'])

spending_df.to_csv('spending_df.csv', index = False)
print("File 1 Finished and updated")