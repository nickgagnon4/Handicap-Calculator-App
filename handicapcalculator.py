import streamlit as st
import heapq
import statistics
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import requests

# Page setup
st.set_page_config(page_title="Golf Handicap Calculator", layout="wide")

# Title
st.markdown("## ⛳️ Golf Handicap Index Calculator (WHS)")
st.write("Enter your 20 golf rounds below to calculate your handicap. Results update automatically.")

# Input scores in 5-column grid
scores = []
cols = st.columns(5)
for i in range(20):
    with cols[i % 5]:
        score = st.number_input(f"Round {i+1}", min_value=18, max_value=200, step=1, key=f"score_{i}")
        scores.append(score)

# Calculate only if all scores are entered
if all(score is not None for score in scores):
    # Top 8 scores & handicap
    top_eight_scores = heapq.nsmallest(8, scores)
    best_score = float(statistics.mean(top_eight_scores))
    handicap = best_score - 72  # assuming par 72

    st.markdown("---")
    st.markdown("### 📊 Results")

    # Styling functions
    def highlight_top8(val):
        return 'background-color: #b7e4c7; font-weight: bold' if val in top_eight_scores else ''

    def add_trophy(val):
        return f"🏆 {val}" if val in top_eight_scores else str(val)

    # All scores table
    all_scores_df = pd.DataFrame({"Score": [add_trophy(x) for x in scores]}, index=[f"Round {i+1}" for i in range(20)])
    st.subheader("All Scores Entered")
    st.dataframe(all_scores_df.style.applymap(highlight_top8), use_container_width=True)

    # Top 8 rounds table
    top8_df = pd.DataFrame({"Score": [f"🏆 {x}" for x in top_eight_scores]}, index=[f"Round {i+1}" for i in range(8)])
    st.subheader("Best 8 Rounds")
    st.dataframe(top8_df.style.applymap(lambda x: 'background-color: #b7e4c7; font-weight: bold'), use_container_width=True)

    # H
