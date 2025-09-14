import streamlit as st
import heapq
import statistics

st.title("⛳️ Handicap Index Calculator ⛳️")

st.write("Enter your 20 golf rounds below:")

# Create 20 number inputs dynamically
scores = []
for i in range(20):
    score = st.number_input(f"Score {i+1}/20", min_value=18, max_value=200, step=1, key=f"score_{i}")
    scores.append(score)

if st.button("Calculate Handicap"):
    top_eight_scores = heapq.nsmallest(8, scores)  # lowest 8 scores
    best_score = float(statistics.mean(top_eight_scores))
    handicap = best_score - 72  # assuming par 72

    st.write("Handicap Test Results")
    st.write(f"Scores Entered: {scores}")
    st.write(f"Best 8 Rounds: {top_eight_scores}")
    st.success(f"Your Handicap Index is: {handicap:.1f}")
