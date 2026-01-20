import streamlit as st
import requests
import base64
import pandas as pd
import plotly.express as px

# -----------------------------
# CONFIG (ADDED – REQUIRED)
# -----------------------------
BACKEND_URL = "ai-data-analysis-graph-generation-production.up.railway.app"

st.set_page_config(
    page_title="InsightPilot",
    layout="wide"
)

st.title("InsightPilot: AI Data Insights & Interactive Exploration")

# -----------------------------
# Step 1: Upload CSV
# -----------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Step 2: AI Insights (UPDATED SAFELY)
    # -----------------------------
    st.info("Generating AI insights, please wait...")

    try:
        with st.spinner("Analyzing dataset with AI..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "text/csv"
                )
            }
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                files=files,
                timeout=120
            )
            response.raise_for_status()
            data = response.json()

        # ---- Original AI summary & charts ----
        st.subheader("AI Summary Insights")
        st.write(data.get("summary", "No summary returned"))

        st.subheader("Key Trends")
        for trend in data.get("key_trends", []):
            st.write("- " + trend)

        st.subheader("Risks")
        for risk in data.get("risks", []):
            st.write("- " + risk)

        st.subheader("Recommendations")
        for rec in data.get("recommendations", []):
            st.write("- " + rec)

        st.subheader("Charts from AI Analysis")
        for name, b64_img in data.get("charts", {}).items():
            if b64_img:
                st.image(
                    base64.b64decode(b64_img),
                    caption=name,
                    width=800  # set a fixed width, e.g., 800px
        )


    except Exception as e:
        st.error(f"AI analysis failed: {e}")
        st.stop()

    # -----------------------------
    # Step 3: Interactive Exploration (UNCHANGED)
    # -----------------------------
    st.sidebar.subheader("Interactive Drill-Down (Optional)")

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    # --- Numeric column exploration ---
    if numeric_cols:
        st.sidebar.markdown("### Numeric Column Drill-Down")
        num_col = st.sidebar.selectbox(
            "Select Numeric Column",
            numeric_cols
        )
        perc = st.sidebar.slider(
            "Percentage of rows to show (Top/Bottom)",
            1, 100, 10
        )

        top_n = max(1, int(len(df) * perc / 100))
        top_df = df.nlargest(top_n, num_col)
        bottom_df = df.nsmallest(top_n, num_col)

        st.subheader(f"Top {perc}% rows for '{num_col}'")
        st.dataframe(top_df)

        st.subheader(f"Bottom {perc}% rows for '{num_col}'")
        st.dataframe(bottom_df)

        # Interactive charts
        st.subheader(f"{num_col} Distribution - Top {perc}%")
        fig_top = px.histogram(top_df, x=num_col, nbins=30)
        st.plotly_chart(fig_top, use_container_width=True)

        st.subheader(f"{num_col} Distribution - Bottom {perc}%")
        fig_bottom = px.histogram(bottom_df, x=num_col, nbins=30)
        st.plotly_chart(fig_bottom, use_container_width=True)

        st.subheader(f"{num_col} Trend Over Index")
        fig_line = px.line(df, y=num_col)
        st.plotly_chart(fig_line, use_container_width=True)

    # --- Categorical column exploration ---
    if categorical_cols:
        st.sidebar.markdown("### Categorical Column Drill-Down")
        cat_col = st.sidebar.selectbox(
            "Select Categorical Column",
            categorical_cols
        )

        st.subheader(f"Top 10 Most Frequent Values for '{cat_col}'")
        top_counts = (
            df[cat_col]
            .value_counts()
            .head(10)
            .reset_index()
        )
        top_counts.columns = [cat_col, "count"]

        fig_cat = px.bar(
            top_counts,
            x=cat_col,
            y="count"
        )
        st.plotly_chart(fig_cat, use_container_width=True)

        # --- Compare & Contrast two categories ---
        st.sidebar.markdown("### Compare Two Categories")
        categories = df[cat_col].unique().tolist()

        if len(categories) >= 2:
            cat1 = st.sidebar.selectbox(
                "Category 1",
                categories,
                index=0
            )
            cat2 = st.sidebar.selectbox(
                "Category 2",
                categories,
                index=1
            )

            st.subheader(
                f"Comparison between '{cat1}' and '{cat2}'"
            )

            compare_df = df[df[cat_col].isin([cat1, cat2])]

            for n_col in numeric_cols:
                fig_cmp = px.box(
                    compare_df,
                    x=cat_col,
                    y=n_col,
                    title=f"{n_col} distribution by {cat_col}"
                )
                st.plotly_chart(
                    fig_cmp,
                    use_container_width=True
                )
