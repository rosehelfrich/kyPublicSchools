import os.path
import pandas as pd
import numpy as np

header = pd.read_csv('/Users/rosehelfrich/Repos/School_Imports/df_header.csv').loc[:,['District Code', 'District', 'School', 'School Code', 'Level']]

def folder_imports(folder_path): 
    files = os.listdir(folder_path)
    dict = {}
    for file in files:
        new_df = pd.read_csv(os.path.join(folder_path, file))
        dict[file] = new_df
    return dict

# Rounding data to integer by columns
def to_int(df, columns):
  for column in columns:
    df[column] = pd.to_numeric(df[column]).round(0).astype('Int64')

# Rename columns, replace end year, and standardize with df_header 
def format_school_data(df, year):
    df.columns = ['End Year', 'School Code', 'Reported Spending per student',
                  'Student Count', 'Educator Count', 'Years of experience']
    df['End Year'] = year
    new_df = header.merge(df, on=['School Code'], how='inner').dropna(thresh=7).reset_index(drop=True)
    return new_df


# Import School data by year. 
school_spending = folder_imports('/Users/rosehelfrich/Repos/School_Imports/spending')

envir_2012 = school_spending['raw_2012.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 'MEMBERSHIP_TOTAL','FULLTIME_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2012 = format_school_data(envir_2012, 2012)

envir_2013 = school_spending['raw_2013.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 'ENROLLMENT_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2013 = format_school_data(envir_2013, 2013)

envir_2014 = school_spending['raw_2014.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 'MEMBERSHIP_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2014 = format_school_data(envir_2014, 2014)

envir_2015 = school_spending['raw_2015.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 'MEMBERSHIP_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2015 = format_school_data(envir_2015, 2015)

envir_2016 = school_spending['raw_2016.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 'MEMBERSHIP_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2016 = format_school_data(envir_2016, 2016)

envir_2017 = school_spending['raw_2017.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'SPENDING_PER_STDNT', 'MEMBERSHIP_TOTAL', 'FTE_TCH_TOTAL', 'AVG_YRS_TCH_EXP']]
envir_2017 = format_school_data(envir_2017, 2017)


# Load and format columns for 2018 - 2019 data. To retrieve the same data as above years, three files had to be imported per year.
def format_2018_2019_data(spending, students, teacher):
  df_spending = spending.loc[:, ['SCH_YEAR', 'DIST_NUMBER', 'SCH_NUMBER', 'TOTAL_PER_STU_ALLFUNDS']]
  df_spending['School Code'] = (df_spending['DIST_NUMBER'] * 1000 + df_spending['SCH_NUMBER'])
  df_students = students.loc[:,['DIST_NUMBER', 'SCH_NUMBER', 'MEMBERSHIP_TOTAL']]
  df_students['School Code'] = (df_students['DIST_NUMBER'] * 1000 + df_students['SCH_NUMBER'])
  spending_and_students = df_spending.merge(df_students, how='left', on='School Code')
  df_teacher = teacher.loc[:,['SCH_CD','Teacher Count','AVGEXPERIENCEYEARS']]
  new_df = spending_and_students.merge(df_teacher, left_on='School Code', right_on='SCH_CD', how='left').loc[:, ['SCH_YEAR', 'School Code', 'TOTAL_PER_STU_ALLFUNDS', 'MEMBERSHIP_TOTAL', 'Teacher Count', 'AVGEXPERIENCEYEARS']]
  return new_df

envir_2018 = format_2018_2019_data(school_spending['spending_2018.csv'], school_spending['stu_2018.csv'], school_spending['raw_2018.csv'])
envir_2018 = format_school_data(envir_2018, 2018)

envir_2019 = format_2018_2019_data(school_spending['spending_2019.csv'], school_spending['stu_2019.csv'], school_spending['raw_2019.csv'])
envir_2019 = format_school_data(envir_2019, 2019)


# Format changed for 2020+ years
spending_and_students_2020 = school_spending['spending_2020.csv'].loc[:,['SCHOOL YEAR', 'SCHOOL CODE', 'Total Spending per Student - All Fund Sources', 'MEMBERSHIP']]
teacher_2020 = school_spending['raw_2020.csv'].loc[:,['SCHOOL CODE', 'EDUCATOR COUNT', 'AVERAGE YEARS OF EXPERIENCE']]
envir_2020 = spending_and_students_2020.merge(teacher_2020, left_on='SCHOOL CODE', right_on='SCHOOL CODE', how='left')
envir_2020 = format_school_data(envir_2020, 2020)

spending_and_students_2021 = school_spending['spending_2021.csv'].loc[:,['SCHOOL YEAR', 'SCHOOL CODE', 'Total Spending per Student - All Fund Sources', 'MEMBERSHIP']]
teacher_2021 = school_spending['raw_2021.csv'].loc[:,['SCHOOL CODE','EDUCATOR COUNT', 'AVERAGE YEARS OF EXPERIENCE']]
envir_2021 = spending_and_students_2021.merge(teacher_2021, on='SCHOOL CODE', how='left')
envir_2021 = format_school_data(envir_2021, 2021)

spending_and_students_2022 = school_spending['spending_2022.csv'].loc[:,['SCHOOL YEAR', 'SCHOOL CODE', 'Total Spending per Student - All Fund Sources', 'MEMBERSHIP']]
teacher_2022 = school_spending['raw_2022.csv'].loc[:,['SCHOOL CODE', 'EDUCATOR COUNT', 'AVERAGE YEARS OF EXPERIENCE']]
envir_2022 = spending_and_students_2022.merge(teacher_2022, how='left', on='SCHOOL CODE')
envir_2022 = format_school_data(envir_2022, 2022)


# 2023 spending data is not available yet - Jan 26 2024.
#.loc[:,['SCHOOL YEAR', 'SCHOOL CODE', 'Total Spending per Student - All Fund Sources', 'MEMBERSHIP']]
teacher_2023 = school_spending['raw_2023.csv'].loc[:,['SCHOOL CODE', 'EDUCATOR COUNT', 'AVERAGE YEARS OF EXPERIENCE']]

## Compile school data into one df
school_envir = pd.concat([envir_2012, envir_2013, envir_2014, envir_2015, envir_2016,
                       envir_2017, envir_2018, envir_2019, envir_2020, envir_2021, envir_2022],
                       axis=0, ignore_index=True)


to_int(school_envir, ['Reported Spending per student', 'Student Count', 'Educator Count', 'Years of experience'])

school_envir.to_csv('school_df.csv', index = False)
print("File1 Finished; school_df.csv updated")