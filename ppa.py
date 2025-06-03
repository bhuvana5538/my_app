# app.py
import streamlit as st
import requests

st.set_page_config(page_title="LeetCode & Kaggle Reviewer", layout="centered")
st.title("🧠 LeetCode & Kaggle Profile Reviewer")

backend_url = "http://localhost:8000"  # Make sure FastAPI runs here

leetcode_username = st.text_input("Enter your LeetCode username")
kaggle_username = st.text_input("Enter your Kaggle username")

# ----- LeetCode -----
if leetcode_username:
    st.subheader("🔍 LeetCode Review")
    try:
        leet_response = requests.get(f"{backend_url}/leetcode/{leetcode_username}")
        leet_data = leet_response.json()
        if "error" not in leet_data:
            st.markdown(f"**Name**: {leet_data['realName'] or 'N/A'}")
            st.markdown(f"**Username**: {leet_data['username']}")
            st.markdown(f"**Ranking**: {leet_data['ranking']}")
            st.markdown(f"**Problems Solved**: {leet_data['totalSolved']}")
        else:
            st.error(leet_data["error"])
    except:
        st.error("🚨 Backend API not reachable. Is FastAPI running?")

# ----- Kaggle -----
if kaggle_username:
    st.subheader("🔍 Kaggle Review")
    try:
        kaggle_response = requests.get(f"{backend_url}/kaggle/{kaggle_username}")
        kaggle_data = kaggle_response.json()
        if "error" not in kaggle_data:
            st.markdown(f"**Username**: {kaggle_data['username']}")
            st.markdown(f"[📊 View Datasets]({kaggle_data['datasetLink']})")
            st.markdown(f"[📓 View Notebooks]({kaggle_data['notebookLink']})")
            st.markdown(f"[💬 View Discussions]({kaggle_data['discussionLink']})")
        else:
            st.error(kaggle_data["error"])
    except:
        st.error("🚨 Backend API not reachable. Is FastAPI running?")
