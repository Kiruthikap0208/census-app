# Import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


@st.cache()
def load_data():
	# Load the Adult Income dataset into DataFrame.

	df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/adult.csv', header=None)
	df.head()

	# Rename the column names in the DataFrame.

	# Create the list
	column_name =['age', 'workclass', 'fnlwgt', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race', 'gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']

	# Rename the columns using 'rename()'
	for i in range(df.shape[1]):
	  df.rename(columns={i:column_name[i]},inplace=True)

	# Print the first five rows of the DataFrame
	df.head()

	# Replace the invalid values ' ?' with 'np.nan'.

	df['native-country'] = df['native-country'].replace(' ?',np.nan)
	df['workclass'] = df['workclass'].replace(' ?',np.nan)
	df['occupation'] = df['occupation'].replace(' ?',np.nan)

	# Delete the rows with invalid values and the column not required

	# Delete the rows with the 'dropna()' function
	df.dropna(inplace=True)

	# Delete the column with the 'drop()' function
	df.drop(columns='fnlwgt',axis=1,inplace=True)

	return df

census_df = load_data()

st.title('Census Data Web app')

if st.sidebar.checkbox("show raw data"):
  st.subheader("Census Data set")
  st.dataframe(census_df)
  st.write("Number of rows are ",census_df.shape[0])
  st.write("Number of columns are ",census_df.shape[1])

st.subheader('Visualisation Selector')

# Add a multiselect in the sidebar with label 'Select the Charts/Plots:'
# Store the current value of this widget in a variable 'plot_list'.
features_list = st.multiselect("Select Features:",('income','gender'))
plot_list = st.sidebar.multiselect('Select the Charts/Plots:', ('Pie chart', 'Box Plot', 'Count Plot'))

# Display pie plot using matplotlib module and 'st.pyplot()'
if 'Pie chart' in plot_list:
  st.subheader('Pie chart')
  pie_income = census_df['income'].value_counts()
  plt.pie(pie_income, labels = pie_income.index, autopct = '%1.2f%%')
  plt.title("Distribution of records for income-groups")
  st.pyplot()
  
  pie_gender = census_df['gender'].value_counts()
  plt.pie(pie_gender, labels = pie_gender.index, autopct = '%1.2f%%')
  plt.title("Distribution of records for gender groups")
  st.pyplot()

# Display box plot using matplotlib module and 'st.pyplot()'
if "Box Plot" in plot_list:
  for feature in features_list:
    st.subheader(f"Box plot between {feature} and hours-per-week")
    plt.figure(figsize = (12, 6))
    sns.boxplot(census_df['hours-per-week'], census_df[feature])
    plt.title(f"distribution of hours per week for different {feature} groups")
    st.pyplot()
	
# Display count plot using seaborn module and 'st.pyplot()' 
if 'Count Plot' in plot_list:
  st.subheader("Count Plot for Distribution of records for unique workclass groups")
  sns.countplot(x = 'workclass', data = census_df)
  st.pyplot()
