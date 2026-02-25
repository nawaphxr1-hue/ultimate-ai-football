import streamlit as st
import numpy as np

def simulate(home, away, sims=20000):
    h=d=a=0
    for _ in range(sims):
        hg=np.random.poisson(home)
        ag=np.random.poisson(away)
        if hg>ag: h+=1
        elif hg==ag: d+=1
        else: a+=1
    return h/sims*100, d/sims*100, a/sims*100

st.title("Ultimate AI Football Predictor")

home_xg = st.number_input("Home xG",1.5)
away_xg = st.number_input("Away xG",1.0)

if st.button("Predict"):
    home_p, draw_p, away_p = simulate(home_xg,away_xg)
    st.write("Home Win %:",round(home_p,2))
    st.write("Draw %:",round(draw_p,2))
    st.write("Away Win %:",round(away_p,2))
