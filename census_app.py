# Import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title='Census Visualisation Web App',
                   page_icon='random',
                   layout='centered',
                   initial_sidebar_state='auto')

# Configure your home page.
# Set the title to the home page contents.
st.title('Census Visualisation Web App')
# Provide a brief description for the web app.
st.subheader('This web app allows a user to explore ans visualise the census data')

st.title("View Data")
with st.beta_expander("View Dataset"):
  st.table(census_df)

# Create three beta_columns.
st.subheader("Columns Description")
beta_col1,beta_col2,beta_col3 = st.beta_columns(3)
# Add a checkbox in the first column. Display the column names of 'census_df' on the click of checkbox.
with beta_col1:
  if st.checkbox("Show all columns names"):
    st.table(census_df.columns)
# Add a checkbox in the second column. Display the column data-types of 'census_df' on the click of checkbox.
with beta_col2:
  if st.checkbox("View column data-type"):
    st.table(census_df.dtype)
# Add a checkbox in the third column followed by a selectbox which accepts the column name whose data needs to be displayed.
with beta_col3:
  if st.checkbox("View column data"):
    column_data = st.selectbox("Select Column",tuple(census_df.columns))
  st.write(census_df[column_data])
# Display summary of the dataset on the click of checkbox.
if st.checkbox("Show Summary"):
  st.table(census_df.describe())
  
@st.cache_data()
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

# Add a multiselect widget to allow the user to select multiple visualisations.
# Add a subheader in the sidebar with the label "Visualisation Selector"
st.sidebar.subheader("Visualisation Selector")
# Add a multiselect in the sidebar with label 'Select the Charts/Plots:'
# Store the current value of this widget in a variable 'plot_list'.
plot_list = st.sidebar.multiselect("Select the Charts/Plots: ",("pie plot","box plot","count plot"))
# Display pie plot using matplotlib module and 'st.pyplot()'
if 'Pie Chart' in plot_list:
  st.subheader('Pie Chart')
  pie_data = census_df['income'].value_counts()
  plt.figure(figsize=(3,6))
  plt.title("Distribution of records for different income-group")
  plt.pie(pie_data,labels=pie_data.index,autopct='%1.2f%%',startangle=30,)
  st.pyplot()
  
  pie_data = census_df['gender'].value_counts()
  plt.figure(figsize=(3,6))
  plt.title("Distribution of records for different Gender")
  plt.pie(pie_data,labels=pie_data.index,autopct='%1.2f%%',startangle=30)
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
if "Count Plot" in plot_list:
  st.subheader('Count Plot')
  plt.title(' count plot for distribution of records for unique workclass groups for different income groups')
  sns.countplot(x='workclass',hue = 'income',data=census_df)
  st.pyplot()

