import pandas as pd
import gspread_dataframe
import gspread
import streamlit as st
import plotly.express as px
import warnings
from datetime import datetime

warnings.filterwarnings(action="ignore")
## required python pakages
## gspread, stramlit, datetime, pandas, plotly
## Need to make account on google cloud console
## Automate google sheet and get .config key
## Give share google sheet and give permission to edit with new generated email on google console

# ------------------ Google sheet connection -------------------------------------
try:
    gc = gspread.service_account(filename="f4fautomation-22a0bffaa650.json") # Give path of your key json file
    worksheet = gc.open_by_key("14lTPdRqUJn-E9GJ0yDohJ8N9K6IuSHL1fF130o_vICA")
    current_sheet = worksheet.worksheet('trial')
    # current_sheet.update_cell(2, 3, "2023")
    data = current_sheet.get_all_records()
    # print(worksheet.worksheets())
    # print(current_sheet)
    df = pd.DataFrame(data)
    # print(df.head(10))
except Exception as e:
    st.error(f"Error loading data from Google Sheets: {e}")

st.set_page_config(page_title="Forest For Farmers Dashboard",
                   page_icon=":deciduous_tree:",
                   layout="wide")

# st.image("Farmer-For-Forests.png", use_container_width= True) ### Needed Image Farmer-For-Forests.png in folder
st.title(":deciduous_tree: Farmer For Forest Dashboard")

#---------------------------FILTER---------------------------------------

st.sidebar.header("Please filter Here: ")
farmer_name = st.sidebar.multiselect(
    "Select the Farmer: ",
    options= df["farmer_name"].unique(),
    default = df["farmer_name"][0]
)
farmer_id = st.sidebar.multiselect(
    "Select the uid: ",
    options= df["uid"].unique(),
    default = df["uid"][0]
)

year = st.sidebar.multiselect(
    "Select the year: ",
    options= df["program_year"].unique()
)

district = st.sidebar.multiselect(
    "Select the district: ",
    options= df["District"].unique()
)
df_selection = df.query(
    "farmer_name == @farmer_name | uid == @farmer_id | program_year == @year & District == @district"
)

st.dataframe(df_selection)

# -------------- pie chart -----------------------------
total_plantation = df_selection.groupby(by='program_year')['trees_planted'].sum().reset_index()

fig_total_plantation = px.pie(
    total_plantation,
    names='program_year',
    values='trees_planted',
    title='Total Trees Planted by Program Year'
)

st.plotly_chart(fig_total_plantation)

# ---------------- Bar chart -------------------------------------------------------

selected_columns = df_selection.iloc[:, 26:]
selected_columns = selected_columns.apply(pd.to_numeric)
column_sums = selected_columns.sum()
result_df = pd.DataFrame({
    'column_name': column_sums.index,
    'values': column_sums.values
})
result_df = result_df.sort_values(by="values",ascending=False)
plant_category = px.bar(
    result_df,
    x='column_name',
    y='values',
    title='Quantity of Plants per variety',
    labels={'column_name': 'Column Name', 'values': 'Sum of Values'},
    color='values',
    color_continuous_scale=px.colors.sequential.Viridis
)
st.plotly_chart(plant_category)