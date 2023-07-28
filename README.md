#HEALTHCARE


if submitted:
    # Show a spinner while the AI model is processing the data
    with st.spinner('Processing...'):
        insights = agent.run(template)

    # Prepare the data for CSV file
    csv_data = {
        "Primary_Impacted_LOB": insights["Primary_Impacted_LOB"],
        "Issue_Severity": insights["Issue_Severity"]
    }
    csv_df = pd.DataFrame(csv_data)

    # Create and download CSV file
    csv_file_path = "issue_severity_tabular_data.csv"
    csv_df.to_csv(csv_file_path, index=False)

    st.download_button(
        label="Download Tabular Data CSV",
        data=csv_file_path,
        file_name="issue_severity_tabular_data.csv",
        mime="text/csv"
    )
