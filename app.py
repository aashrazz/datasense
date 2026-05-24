import streamlit as st
import pandas as pd
from utils.pdf_generator import generate_pdf

# Import your master engine
from analyzer.scorer import generate_scorecard

# 1. Page Configuration (must be the first Streamlit command)
st.set_page_config(page_title="DataSense", page_icon="📊", layout="wide")

# 2. Header Section
st.title("DataSense: Data Quality Scorecard Generator")
st.subheader("Upload any CSV. Get a quality score in seconds.")

# 3. File Uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV only)", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded file into Pandas
    df = pd.read_csv(uploaded_file)
    
    # Show a quick preview of the data
    st.markdown("### Dataset Preview")
    st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
    st.dataframe(df.head()) # Shows the first 5 rows in a clean table

    # 4. The Analyze Button
    if st.button("Run Data Quality Analysis", type="primary"):
        
        # Show a loading spinner while the engine runs
        with st.spinner("Analyzing completeness, consistency, uniqueness, validity, and accuracy..."):
            report = generate_scorecard(df)
            
        st.success("Analysis Complete!")

        # Generate the PDF
        pdf_file = generate_pdf(report)
        
        # Show a download button
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="DataSense_Report.pdf",
            mime="application/pdf"
        )
        
        # 5. The Scorecard Dashboard
        st.markdown("---")
        
        # Create two columns for the header layout
        header_left, header_right = st.columns([1, 2])
        
        with header_left:
            st.metric(label="Final Score", value=f"{report['total_score']} / 100")
            
        with header_right:
            st.markdown(f"### Grade: {report['grade']}")
            st.markdown(f"**Verdict:** {report['verdict']}")
            
        st.markdown("---")
        st.markdown("### Dimension Breakdown")
        
        # Create 5 columns across the screen for the 5 dimension scores
        cols = st.columns(5)
        dimensions = list(report['dimensions'].keys())
        
        for i in range(5):
            dim_name = dimensions[i]
            score = report['dimensions'][dim_name]['score']
            with cols[i]:
                st.metric(label=dim_name, value=f"{score}/20")
