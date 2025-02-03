import pandas as pd

# -----------------------
# 1. Create Sample Data
# -----------------------

# Community table data
df_community = pd.DataFrame({
    "community_id": [1, 2],
    "name": ["Greenfield", "Rivertown"],
    "region": ["North", "South"],
    "population": [15000, 22000]
})

# Demographic table data
df_demographic = pd.DataFrame({
    "demographic_id": [1, 2, 3, 4],
    "age_group": ["0-18", "19-35", "36-60", "60+"],
    "gender": ["All", "All", "All", "All"]
})

# Vaccination_Type table data
df_vaccine = pd.DataFrame({
    "vaccine_id": [1, 2],
    "vaccine_name": ["Vaccine A", "Vaccine B"],
    "manufacturer": ["PharmaCorp", "HealthMeds"]
})

# Vaccination_Record table data
df_record = pd.DataFrame({
    "record_id": [1, 2, 3, 4, 5],
    "community_id": [1, 1, 1, 2, 2],
    "demographic_id": [1, 2, 1, 3, 4],
    "vaccine_id": [1, 1, 2, 1, 2],
    "date_administered": pd.to_datetime(["2024-01-15", "2024-01-15", "2024-02-15", "2024-01-20", "2024-03-10"]),
    "doses_administered": [500, 700, 300, 600, 200]
})

# Merge community info into the Vaccination_Record to include community name and population
df_record = df_record.merge(df_community, on="community_id", how="left")

# ------------------------------------
# 2. Create Aggregated (Pivot-like) Data
# ------------------------------------

# Pivot: Total doses per community along with vaccination percentage
pivot_community = df_record.groupby(["name", "population"])["doses_administered"].sum().reset_index()
pivot_community.rename(columns={"doses_administered": "total_doses"}, inplace=True)
pivot_community["vaccination_rate(%)"] = pivot_community["total_doses"] / pivot_community["population"] * 100

# Pivot: Vaccination trends by month
df_record["month"] = df_record["date_administered"].dt.to_period("M").astype(str)
pivot_trends = df_record.groupby("month")["doses_administered"].sum().reset_index()
pivot_trends.rename(columns={"doses_administered": "total_doses"}, inplace=True)

# ------------------------------------
# 3. Write to an Excel File using XlsxWriter
# ------------------------------------

excel_file = "SDG_Data_Analysis.xlsx"
with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
    # Write raw data sheets
    df_community.to_excel(writer, sheet_name="Community", index=False)
    df_demographic.to_excel(writer, sheet_name="Demographic", index=False)
    df_vaccine.to_excel(writer, sheet_name="Vaccination_Type", index=False)
    df_record.to_excel(writer, sheet_name="Vaccination_Record", index=False)
    
    # Write aggregated (pivot-like) sheets
    pivot_community.to_excel(writer, sheet_name="Pivot_Community", index=False)
    pivot_trends.to_excel(writer, sheet_name="Pivot_Trends", index=False)
    
    # Create a Calculations sheet demonstrating an Excel formula for vaccination percentage
    worksheet_calc = writer.book.add_worksheet("Calculations")
    # Write headers
    worksheet_calc.write_row('A1', ["Community", "Total Doses", "Population", "Vaccination Rate (%)"])
    # Write data rows from the pivot_community DataFrame
    for row_num, row in enumerate(pivot_community.values, start=1):
        worksheet_calc.write_row(row_num, 0, row.tolist())
    # Insert an Excel formula in cell D2 (assuming row 2 corresponds to the first community)
    worksheet_calc.write_formula('D2', '=B2/C2*100')
    
    # -------------------------
    # 4. Create Charts
    # -------------------------
    
    # Create a new worksheet for charts
    worksheet_chart = writer.book.add_worksheet("Charts")
    
    # Bar Chart: Total doses per community (from Pivot_Community)
    chart1 = writer.book.add_chart({'type': 'column'})
    chart1.add_series({
        'name':       'Total Doses per Community',
        'categories': ['Pivot_Community', 1, 0, len(pivot_community), 0],  # Community names
        'values':     ['Pivot_Community', 1, 2, len(pivot_community), 2],  # Total doses (column index 2)
    })
    chart1.set_title({'name': 'Total Doses per Community'})
    chart1.set_x_axis({'name': 'Community'})
    chart1.set_y_axis({'name': 'Total Doses'})
    # Insert the chart in the Charts sheet
    worksheet_chart.insert_chart('B2', chart1)
    
    # Line Chart: Vaccination trends by month (from Pivot_Trends)
    chart2 = writer.book.add_chart({'type': 'line'})
    chart2.add_series({
        'name':       'Doses Administered',
        'categories': ['Pivot_Trends', 1, 0, len(pivot_trends), 0],  # Month labels
        'values':     ['Pivot_Trends', 1, 1, len(pivot_trends), 1],  # Total doses (column index 1)
    })
    chart2.set_title({'name': 'Vaccination Trends by Month'})
    chart2.set_x_axis({'name': 'Month'})
    chart2.set_y_axis({'name': 'Total Doses'})
    # Insert the chart in the Charts sheet
    worksheet_chart.insert_chart('B20', chart2)

print("Excel file created:", excel_file)
