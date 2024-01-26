import os.path
import pandas as pd
import numpy as np

df = pd.read_csv('/Users/rosehelfrich/Repos/School_Imports/df_header.csv')
df_header = df.loc[:,['District Code', 'District', 'School Code', 'School', 'Level']]
school_code = df_header['School Code']

# Import all files from folder into a dictionary
def folder_imports(folder_path): 
    files = os.listdir(folder_path)
    dict = {}
    for file in files:
        new_df = pd.read_csv(os.path.join(folder_path, file))
        dict[file] = new_df
    return dict

# Rename columns and use school_code to filter out any schools that are not in the df_header
def rename_five_cols(df, end_year):
  df.columns = ['End Year', 'School Code', 'Proficiency Score', 'Classification', 'Level']
  df['End Year'] = end_year
  new_df = df[df['School Code'].isin(school_code)]
  return new_df.reset_index(drop=True)

def rename_four_cols(df, end_year):
  df.columns = ['End Year', 'School Code', 'Proficiency Score', 'Level']
  df['End Year'] = end_year
  new_df = df[df['School Code'].isin(school_code)]
  return new_df.reset_index(drop=True)


# # Import test score data
score_dict = folder_imports('/Users/rosehelfrich/Repos/School_Imports/score')

score_2012 = score_dict['profile_2012.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'OVERALL_SCORE', 'CLASSIFICATION', 'CONTENT_LEVEL']] # total points available
score_2013 = score_dict['profile_2013.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'OVERALL_SCORE', 'CLASSIFICATION', 'CONTENT_LEVEL']] # total points available
score_2014 = score_dict['profile_2014.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'OVERALL_SCORE', 'CLASSIFICATION', 'CONTENT_LEVEL']]
score_2015 = score_dict['profile_2015.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'OVERALL_SCORE', 'CLASSIFICATION', 'CONTENT_LEVEL']]
score_2016 = score_dict['profile_2016.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'OVERALL_SCORE', 'CLASSIFICATION', 'CONTENT_LEVEL']]
score_2012 = rename_five_cols(score_2012, 2012)
score_2013 = rename_five_cols(score_2013, 2013)
score_2014 = rename_five_cols(score_2014, 2014)
score_2015 = rename_five_cols(score_2015, 2015)
score_2016 = rename_five_cols(score_2016, 2016)

score_2017 = score_dict['summary_2017.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'ACHIEVEMENT_POINTS', 'CONTENT_LEVEL']]
score_2018 = score_dict['summary_2018.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'PROFICIENCY_RATE', 'LEVEL']] # All Null values for Proficiency Rating
score_2017 = rename_four_cols(score_2017, 2017)
score_2018 = rename_four_cols(score_2018, 2018)

score_2019 = score_dict['profile_2019.csv'].loc[:,['SCH_YEAR', 'SCH_CD', 'PROFICIENCY_RATE', 'PROFICIENCY_RATING', 'LEVEL']] # PROFICIENCY rate available

score_2022 = score_dict['profile_2022.csv'].loc[:,['SCHOOL YEAR','SCHOOL CODE', 'OVERALL INDICATOR RATE', 'OVERALL INDICATOR RATING', 'LEVEL']]  # PROFICIENCY scores NOT available
score_2023 = score_dict['profile_2023.csv'].loc[:,['SCHOOL YEAR','SCHOOL CODE', 'OVERALL COMBINED INDICATOR RATE', 'OVERALL INDICATOR RATING', 'LEVEL']]

score_2019 = rename_five_cols(score_2019, 2019)
score_2022 = rename_five_cols(score_2022, 2022)
score_2023 = rename_five_cols(score_2023, 2023)


# # Concat and standardize values
all_scores = pd.concat([score_2012, score_2013, score_2014, score_2015, score_2016,
                        score_2017, score_2018, score_2019, score_2022, score_2023,
                        ], axis =0).reset_index(drop=True)

# Clean up Classification values
all_scores['Level'].replace(['Elementary School', 'Middle School', 'High School'], ['ES', 'MS', 'HS'], inplace=True)
all_scores['Classification'].replace([1,2,3,4,5], [0,1,2,3,4], inplace=True)
all_scores['Classification'].replace(['Needs Improvement/Progressing', 'Proficient/Progressing', 'Distinguished/Progressing'],
                                     ['Needs Improvement', 'Proficient', 'Distinguished'], inplace=True)
all_scores['Classification'].replace(['Very Low', 'Low', 'Medium', 'High', 'Very High'],
                     [0,1,2,3,4], inplace=True)

# Create a new column 'Rating' in df_scores
all_scores['Rating Code'] = all_scores['Classification']
all_scores['Rating Code'].replace(['Needs Improvement', 'Proficient', 'Distinguished'], np.NaN, inplace=True)
all_scores['Classification'].replace([0,1,2,3,4], np.NaN, inplace=True)

# Create columns with the codes
all_scores['Classification Code'] = all_scores['Classification'].replace(['Needs Improvement', 'Proficient', 'Distinguished'], [0, 1, 2])
all_scores['Rating'] = all_scores['Rating Code'].replace([0,1,2,3,4], ['Very Low', 'Low', 'Medium', 'High', 'Very High'])

# # Merge with header
df_scores = pd.merge(df_header, all_scores, on=['School Code', 'Level'], how='inner')
df_scores.sort_values(by=['End Year', 'District', 'School'], ascending=True, inplace=True)
df_scores['End Year Code'] = df_scores['End Year'] - 2012
df_scores['Level Code'] = df_scores['Level'].replace(['ES', 'MS', 'HS'], [0, 1, 2])
df_scores.reset_index(drop=True, inplace=True)

# Reorder columns
reordered_columns = ['End Year', 'End Year Code',
                     'District', 'District Code',
                     'School', 'School Code',
                     'Level', 'Level Code',
                     'Proficiency Score',
                     'Classification', 'Classification Code',
                     'Rating', 'Rating Code']
df_scores = df_scores[reordered_columns]

# Round and convert to an integer
df_scores['Proficiency Score'] = df_scores['Proficiency Score'].round(0).astype('Int64')

df_scores.to_csv('df_scores.csv', index = False)
df_scores.info()
print("File3 Finished; df_scores.csv updated")