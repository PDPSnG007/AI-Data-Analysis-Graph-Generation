from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import logging
import plotly.express as px
import plotly.figure_factory as ff
import base64
from agent import agent
from schemas import Insight
from dotenv import load_dotenv
import json
import numpy as np
import io

def convert_numpy(obj):
    """Recursively convert NumPy types in dict/list to native Python types"""
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    else:
        return obj

# Load environment variables
load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="InsightPilot API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

def plot_to_base64(fig):
    """Convert Plotly figure to base64 PNG safely"""
    try:
        img_bytes = fig.to_image(format="png")
        return base64.b64encode(img_bytes).decode()
    except Exception as e:
        logging.warning(f"Chart export failed: {e}")
        return ""  # Return empty string if chart fails

@app.post("/analyze")
async def analyze(file: UploadFile) -> Insight:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    try:
        # Load CSV
        contents = await file.read()

        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        df = pd.read_csv(io.BytesIO(contents))

        # Generate stats summary
        stats = df.describe(include="all").transpose()
        stats_text = stats.fillna("").to_string()

        # Generate AI prompt requesting structured JSON output
        prompt = f"""
Dataset Summary Statistics:
{stats_text}

You are a business data analyst.
Provide the output in the following JSON format exactly:

{{
  "summary": "<one paragraph summary of the dataset>",
  "key_trends": ["trend1", "trend2"],
  "risks": ["risk1", "risk2"],
  "recommendations": ["rec1", "rec2"]
}}

Be factual and concise. Avoid speculation.
"""
        result = await agent.run(prompt)

        # Step 3: Process AI output safely
        try:
            insights_json = json.loads(result.output)
        except Exception:
            insights_json = {
                "summary": getattr(result, "output", str(result)),
                "key_trends": [],
                "risks": [],
                "recommendations": []
                }

# Convert NumPy types to native Python
        insights_json = convert_numpy(insights_json)

        # Step 4: Generate charts
        charts = {}
        numeric_cols = df.select_dtypes(include="number").columns
        categorical_cols = df.select_dtypes(include="object").columns

        # Numeric visualizations
        for col in numeric_cols:
            try:
                fig_hist = px.histogram(df, x=col, nbins=30, title=f"{col} Distribution")
                charts[f"{col}_hist"] = plot_to_base64(fig_hist)

                fig_line = px.line(df, y=col, title=f"{col} Trend")
                charts[f"{col}_trend"] = plot_to_base64(fig_line)

                fig_box = px.box(df, y=col, title=f"{col} Outliers")
                charts[f"{col}_box"] = plot_to_base64(fig_box)
            except Exception as e:
                logging.warning(f"Failed to generate numeric chart for {col}: {e}")

        # Correlation heatmap
        if len(numeric_cols) > 1:
            try:
                corr = df[numeric_cols].corr()
                fig_corr = ff.create_annotated_heatmap(
                    z=corr.values,
                    x=list(corr.columns),
                    y=list(corr.index),
                    colorscale='Viridis'
                )
                charts["correlation_heatmap"] = plot_to_base64(fig_corr)
            except Exception as e:
                logging.warning(f"Failed to generate correlation heatmap: {e}")

        # Categorical charts
        for col in categorical_cols:
            try:
                counts = df[col].value_counts()
                top10 = counts.head(10)
                other_count = counts.iloc[10:].sum()
                top10 = top10.copy()
                top10["Other"] = other_count

                top10 = top10.reset_index()
                top10.columns = [col, "count"]
                fig_cat = px.bar(top10, x=col, y="count", title=f"Top 10 {col} + Other")
                charts[f"{col}_top"] = plot_to_base64(fig_cat)
            except Exception as e:
                logging.warning(f"Failed to generate categorical chart for {col}: {e}")

        # Step 5: Prepare interactive drill-down data
        interactive_data = {}

        # Numeric drill-down: top/bottom 10%
        for col in numeric_cols:
            top10 = df.nlargest(max(1, len(df)//10), col).to_dict(orient="records")
            bottom10 = df.nsmallest(max(1, len(df)//10), col).to_dict(orient="records")
            interactive_data[col] = {
                "top_10_percent": top10,
                "bottom_10_percent": bottom10
            }

        # Compare two categories for numeric columns
        for col in categorical_cols:
            categories = df[col].unique()
            if len(categories) >= 2:
                cat1, cat2 = categories[:2]
                compare_df = df[df[col].isin([cat1, cat2])]
                interactive_data[f"{col}_compare"] = convert_numpy(compare_df.to_dict(orient="records"))

        # Step 6: Return everything
        return Insight(
            **insights_json,
            charts=charts,
            interactive=interactive_data
        )

    except Exception as e:
        logging.exception("Analysis failed")
        raise HTTPException(status_code=500, detail=str(e))
