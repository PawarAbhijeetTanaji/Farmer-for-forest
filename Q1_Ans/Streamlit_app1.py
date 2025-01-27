import pandas as pd
import gspread
import streamlit as st
from datetime import datetime
import warnings
warnings.filterwarnings(action="ignore")
## required python pakages
## gspread, stramlit, datetime, pandas, plotly
## Need to make account on google cloud console
## Automate google sheet and get .config key
## Give share google sheet and give permission to edit with new generated email on google console
try:
    gc = gspread.service_account(filename="f4fautomation-22a0bffaa650.json") # Give path of your key json file
# this key is between d/ to /edit url of google sheet
    worksheet = gc.open_by_key("14lTPdRqUJn-E9GJ0yDohJ8N9K6IuSHL1fF130o_vICA")
    current_sheet = worksheet.worksheet('trial')
    data = current_sheet.get_all_records()
    df = pd.DataFrame(data)

except Exception as e:
    st.error(f"Error loading data from Google Sheets: {e}")

st.set_page_config(page_title="Forest For Farmers Dashboard",
                   page_icon=":deciduous_tree:",
                   layout="wide")
st.image("Farmer-For-Forests.png", use_container_width= True)
st.sidebar.header("Please filter Here:")
farmer_name = st.sidebar.selectbox(
    "Select the Farmer: ",
    options= df["farmer_name"].unique(),
)
df_selection = df.query("farmer_name == @farmer_name")

st.title(":deciduous_tree: Farmer For Forest Dashboard")
st.markdown(f"<h2 style='color: green; font-family: Arial; text-align: left;'>{farmer_name}</h2>", unsafe_allow_html=True)
st.markdown("##")
# --------- KPI -------------------------------
if not df_selection.empty:
    total_area = int(df_selection["area_f4f_acre"].values[0])
    water_availability = str(df_selection["water_available"].values[0])
    electricity_availability = str(df_selection["electricity_available"].values[0])

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.header("Total area for F4F:")
        st.subheader(f"Available {total_area} acre land")

    with middle_column:
        st.header("Water Availability:")
        if water_availability.lower() in ["yes", "no"]:
            st.subheader(f"{water_availability.upper()}")
        else:
            st.subheader(f"Wrong input: {water_availability.upper()}")

    with right_column:
        st.header("Electricity Availability:")
        if electricity_availability.lower() in ["yes", "no"]:
            st.subheader(f"{electricity_availability.upper()}")
        else:
            st.subheader(f"Wrong input: {electricity_availability.upper()}")

else:
    st.warning("No data available for the selected farmer.")

st.markdown("##")

if not df_selection.empty:
    tree_planted = int(df_selection["trees_planted"].values[0])
    date_format = "%d-%b-%y"
    contract_date_str = df_selection["contract_date"].values[0]
    plantation_date_str = df_selection["plantation_date"].values[0]

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.header("Trees Planted:")
        if 350 <= tree_planted <= 450:
            st.subheader(f"Available: {tree_planted} trees")
        else:
            st.subheader(f"WARNING! {tree_planted} trees")

    with middle_column:
        st.header("Plantation and Contract Date:")
        st.subheader(f"Plantation Date: {plantation_date_str}")
        st.subheader(f"Contract Date: {contract_date_str}")

    with right_column:
        st.header("Status:")

        if plantation_date_str != "NA":
            plantation_date = datetime.strptime(plantation_date_str, date_format)
        else:
            plantation_date = None

        if contract_date_str != "NA":
            contract_date = datetime.strptime(contract_date_str, date_format)
        else:
            contract_date = None

        if plantation_date and contract_date:
            if plantation_date > contract_date:
                st.subheader("Done")
            else:
                st.subheader("WARNING! Plantation is done before contract.")
        else:
            st.subheader("WARNING! Dates are not available.")
else:
    st.warning("No data available for the selected farmer.")

st.dataframe(df_selection)

