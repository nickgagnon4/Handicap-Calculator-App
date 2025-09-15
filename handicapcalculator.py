import streamlit as st
import heapq
import statistics
import pandas as pd

# page setup
st.set_page_config(page_title="Golf Handicap Calculator by Nick Gagnon", layout="wide")

# title
st.markdown("## ⛳️ Golf Handicap Index Calculator")
st.write("Enter your 20 golf rounds below to calculate your handicap. Results update automatically.")

# input scores in 5-column grid
scores = []
cols = st.columns(5)
for i in range(20):
    with cols[i % 5]:
        score = st.number_input(f"Round {i+1}", min_value=18, max_value=200, step=1, key=f"score_{i}")
        scores.append(score)

# calculate only if all scores are entered
if all(score is not None for score in scores):
    # top 8 scores and handicap
    top_eight_scores = heapq.nsmallest(8, scores)
    best_score = float(statistics.mean(top_eight_scores))
    handicap = best_score - 72  # assuming par 72

    st.markdown("---")
    st.markdown("### 📊 Results")

    # styling
    def highlight_top8(val):
        return 'background-color: #b7e4c7; font-weight: bold' if val in top_eight_scores else ''

    def add_trophy(val):
        return f"🏆 {val}" if val in top_eight_scores else str(val)

    # all scores table
    all_scores_df = pd.DataFrame({"Score": [add_trophy(x) for x in scores]}, index=[f"Round {i+1}" for i in range(20)])
    st.subheader("All Scores Entered")
    st.dataframe(all_scores_df.style.applymap(highlight_top8), use_container_width=True)

    # top 8 rounds table
    top8_df = pd.DataFrame({"Score": [f"🏆 {x}" for x in top_eight_scores]}, index=[f"Round {i+1}" for i in range(8)])
    st.subheader("Best 8 Rounds")
    st.dataframe(top8_df.style.applymap(lambda x: 'background-color: #b7e4c7; font-weight: bold'), use_container_width=True)

    # handicap display
    st.success(f"### Your Handicap Index is: {handicap:.1f}")

    # csv
    st.markdown("### 💾 Download CSV")
    max_len = max(len(scores), len(top_eight_scores))
    csv_df = pd.DataFrame({
        "All Scores": scores + [None]*(max_len - len(scores)),
        "Top 8 Rounds": top_eight_scores + [None]*(max_len - len(top_eight_scores))
    })
    csv_df.loc[max_len] = [None, None]
    csv_df.loc[max_len, "All Scores"] = "Handicap Index"
    csv_df.loc[max_len, "Top 8 Rounds"] = handicap
    csv_bytes = csv_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv_bytes, file_name="handicap_report.csv", mime="text/csv")
