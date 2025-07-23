import streamlit as st
from ai_agent import AIAgent
from game_logic import simulate_game

st.title("🐦 Flappy AI Simulator")
st.markdown("This AI tries to play a simplified Flappy Bird using rule-based logic.")

threshold = st.slider("Flap Threshold", min_value=0.0, max_value=100.0, value=40.0, step=5.0)

if st.button("Run Simulation"):
    agent = AIAgent(flap_threshold=threshold)
    score = simulate_game(agent)
    st.success(f"AI Score: {score}")
    st.markdown(f"Flap threshold: `{threshold}`")
