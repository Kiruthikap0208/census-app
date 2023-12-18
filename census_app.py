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
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Census Data Web app')

if st.sidebar.checkbox("show raw data"):
  st.subheader("Census Data set")
  st.dataframe(census_df)
  st.write("Number of rows are ",census_df.shape[0])
  st.write("Number of columns are ",census_df.shape[1])

st.subheader('Visualisation Selector')

# Add a multiselect in the sidebar with label 'Select the Charts/Plots:'
# Store the current value of this widget in a variable 'plot_list'.
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
if 'Box Plot' in plot_list :
  st.subheader('Box Plot')
  plt.figure(figsize=(8,4))
  plt.title('Box plot for the hours worked per week for different income groups')
  sns.boxplot(x=census_df['hours-per-week'],y=census_df['income'])
  st.pyplot()
  
  plt.figure(figsize=(8,4))
  plt.title('Box plot for the hours worked per week  for different gender groups')
  sns.boxplot(x=census_df['hours-per-week'],y=census_df['gender'])
  st.pyplot() 
	
# Display count plot using seaborn module and 'st.pyplot()' 
if 'Count Plot' in plot_list:
  st.subheader("Count Plot for Distribution of records for unique workclass groups")
  sns.countplot(x = 'workclass', data = census_df)
  st.pyplot()

st.set_page_config(page_title = 'Census Visualisation Web App',
                   page_icon = None,
                   layout = 'centered',
                   initial_sidebar_state = 'auto')

# Set the title to the home page contents.
st.subheader('Census Visualisation Web App')
# Provide a brief description for the web app.
st.title('This web app allows a user to explore and visualise the census data')

# View Dataset Configuration
st.header('View Data')
# Add an expander and display the dataset as a static table within the expander.
with st.beta_expander('View Dataset') :
  st.table(census_df)

# Create three beta_columns.
beta_col1, beta_col2, beta_col3 = st.beta_columns(3)
# Add a checkbox in the first column. Display the column names of 'census_df' on the click of checkbox.
with beta_col1 :
  if st.checkbox('Show all column names') :
    st.table(list(census_df.columns))

# Add a checkbox in the second column. Display the column data-types of 'census_df' on the click of checkbox.
with beta_col2 :
  if st.checkbox('View column data type') :
    st.table(census_df.dtypes)

# Add a checkbox in the third column followed by a selectbox which accepts the column name whose data needs to be displayed.
with beta_col3 :
  if st.checkbox('View column data') :
    column_data = st.selectbox('Select column', tuple(census_df.columns))
    st.table(census_df[column_data])

# Display summary of the dataset on the click of checkbox.
if st.checkbox('Show summary') :
  st.table(census_df.describe())
