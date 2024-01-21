# Project Overview 

The Kentucky Department of Education (KDE) website provides public access to public school and district data. Although the data is legitimately public, access is not enough for the public to understand and interpret the data.  This project aimed to resolve these issues and focus on the popular topics of school test scores, COVID impact, school testing trends, and school spending.  

Schools are mandated to report their spending based on the average teacher salary within a district.  It would be more accurate to view a school budget based on average teacher salary per school.  For each Kentucky school with available data, this project estimated the school budget, and compared the estimated school spending with the previous school test scores.


## File 1: Spending Data
* Imports over 30 files from the Kentucky Department of Education (KDE) website, including data directly received from a KDE representative.
* Data cleaning and preprocessing.
* Produced _preprocessed_df_ encompassing data for over 1500 Kentucky public schools' test scores spanning eleven years. In the primary file, data from two years (2020 and 2021) and about 300 schools are excluded due to the absence of associated test scores.

  <details><summary>Variable Information</summary>
    
  ### Imported Variables from the data:
  * **End Year**: The academic year concluding in that spring/summer, e.g., 2012 indicates the year starting in 2011.
  * **District**: The administrative region the school belongs to.
  * **School**: The official name of the educational institution.
  * **Level**: Specifies if the school is a high school, middle school, or elementary school.
  * **Reported Spending per Student**: The amount the school officially reports as expenditure per student.
  * **Student Count**: The total number of students.
  * **Educator Count**: The total number of teachers.
  * **Years of Experience**: The average teaching experience at the school, calculated annually.
  * **District Teacher Salary Average**: Reflects the standard salary claim for each teacher by the school, though this figure often varies from actuals.
  * **Teacher Salary Based on Experience**: The salary for a Rank II KY teacher in the district, adjusted for the average years of experience at the school.
  ### Calculated Variables for improved estimates:
  * **Money Difference per School**: The variance between the district's average teacher salary and the salary based on years of experience, multiplied by the number of educators.
  * **Money Difference per Student**: This figure redistributes the Money Difference across all students in the school.
  * **Estimated Spending per Student**: A refined estimate of spending per student, calculated using 'Teacher Salary Based on Experience' instead of the district average. This figure more accurately reflects actual expenditure compared to the reported spending.
  
  </details>



## File 2:  Test scores per school
* Combines the test scores per school per year. 
* Outputs _df_scores_ that contains data for 1200+ Ky public school test scores across nine years.

## File 3: Predict Classification and Rating
* This is the primary file that predicts missing classifications and ratings for schools.
* Results in the _predict_df_. 


## Original Files 

The original data was retrieved from the Kentucky Department of Education (KDE) website or directly from a KDE representative.  

  <details><summary>Links to KDE</summary>
  
  ### School Report Cards
  
  These are the primary links for detailed information about each individual school, encompassing data on per-student spending, teacher and student counts, average teacher experience in years, and overall school test performance:
  * [2020 & Onward data](<https://www.kyschoolreportcard.com/datasets?year=2022>)
  * [Pre-2020 data](<https://openhouse.education.ky.gov/Home/SRCData>)
  
  _As of January 2024, financial data for the 2022-2023 school year remains unavailable._
  
  
  ### District Financial Reporting
  
  * For details on teacher salaries per district, refer to the _**certified**_ salary schedule [here](<https://education.ky.gov/districts/FinRept/Pages/School%20District%20Personnel%20Information.aspx>).
  * Each year, the KDE releases salary schedules categorized by rank. To access historical records, one must contact the [KDE representative](<https://education.ky.gov/districts/FinRept/Pages/School%20District%20Personnel%20Information.aspx>). When I made such a request, I received the necessary information in less than 24 hours.
  
  
  </details>
