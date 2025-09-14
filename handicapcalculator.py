import streamlit as st
import heapq
import statistics
import pandas as pd

# Title
st.markdown("## ⛳️ Golf Handicap Index Calculator")
st.write("Enter your 20 golf scores below to calculate your handicap.")

# Input scores
scores = []
cols = st.columns(5)  # Display inputs in 5 columns for a cleaner look
for i in range(20):
    with cols[i % 5]:
        score = st.number_input(f"Score {i+1}", min_value=18, max_value=200, step=1, key=f"score_{i}")
        scores.append(score)

# Button to calculate
if st.button("Calculate Handicap"):
    top_eight_scores = heapq.nsmallest(8, scores)
    best_score = float(statistics.mean(top_eight_scores))
    handicap = best_score - 72  # assuming par 72

    st.markdown("---")
    st.markdown("### 📊 Results")

    # Display scores in a table
    st.subheader("All Rounds Entered")
    all_scores_df = pd.DataFrame({"Score": scores}, index=[f"Round {i+1}" for i in range(20)])
    st.table(all_scores_df)

    # Display top 8
    st.subheader("Lowest Rounds")
    top8_df = pd.DataFrame({"Score": top_eight_scores}, index=[f"Round {i+1}" for i in range(8)])
    st.table(top8_df)

    # Handicap result
    st.success(f"### Your Handicap Index is: {handicap:.1f}")
