import streamlit as st
import pandas as pd
import time
import json
import os
from modules.analyzer import ProductAnalyzer
from modules.scorer import ProductScorer
from modules.strategist import SalesStrategist
from modules.content_generator import ContentGenerator
from modules.campaign_manager import CampaignManager
from modules.publisher import Publisher
import config

# Page Config
st.set_page_config(page_title="Affiliate Automation Dashboard", page_icon="🚀", layout="wide")

# Custom CSS (Injected from user's design)
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary-color: #21808d; /* Teal 500 */
        --bg-color: #fcfcf9; /* Cream 50 */
        --text-color: #1f2121; /* Charcoal 700 */
    }
    
    /* Global Styles */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
        color: var(--text-color);
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: rgba(59, 130, 246, 0.08);
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: #1f2121;
        font-weight: 700;
    }
    
    /* Cards */
    .stMetric {
        background: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(94, 82, 64, 0.12);
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    
    /* Buttons */
    .stButton button {
        background-color: #21808d;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #1d7480;
    }
    
    /* Alerts */
    .stAlert {
        background-color: rgba(34, 197, 94, 0.08);
        border: 1px solid #21808d;
        color: #1f2121;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>🚀 Affiliate Marketing Automation Dashboard</h1>
    <p>Start Earning Without Any Investment - India & Global Markets</p>
    <span style="background:#21808d; color:white; padding:4px 8px; border-radius:99px; font-size:12px; font-weight:bold;">₹0 INVESTMENT REQUIRED</span>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("⚙️ Configuration")
region = st.sidebar.selectbox("Target Region", list(config.REGIONS.keys()), index=1) # Default to India
niche = st.sidebar.selectbox("Target Niche", config.TARGET_NICHES)

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Autonomous Agent")
if st.sidebar.button("Start Background Runner"):
    st.sidebar.success("Agent started in background! (Simulated)")
    # In a real app, this would trigger a subprocess or service
    
st.sidebar.markdown("---")
st.sidebar.info("Built with Python & Streamlit")

# --- Stats Overview ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Potential Earnings", "₹50k - ₹3L", "Monthly")
col2.metric("Active Programs", "6", "+2 this week")
col3.metric("Total Earnings", "₹12,450", "+15%")
col4.metric("Time to First Earning", "1-7 Days", "Avg")

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Dashboard", "Find Programs", "Content Generator", "Income Projector", "Traffic Guide", "Live Logs"])

# --- Tab 1: Dashboard ---
with tab1:
    st.subheader("🔥 Top Recommended Programs")
    
    # Filter programs by region
    programs = [p for p in config.AFFILIATE_PROGRAMS if region in p['region'] or "Global" in p['region']]
    
    for p in programs[:3]:
        with st.expander(f"{p['name']} ({p['commission']})"):
            st.write(f"**Category:** {p['category']}")
            st.write(f"**Potential:** {p['earning_potential']}")
            st.write(f"[Join Program]({p['url']})")

    st.subheader("✅ Daily Tasks")
    tasks = [
        {"task": "Create 1 social media post", "time": "15 mins", "earn": "₹50-500"},
        {"task": "Share link in 3 communities", "time": "20 mins", "earn": "₹25-200"},
        {"task": "Send 5 personalized emails", "time": "25 mins", "earn": "₹100-500"}
    ]
    for t in tasks:
        st.checkbox(f"{t['task']} ({t['time']}) - Potential: {t['earn']}")

# --- Tab 2: Find Programs ---
with tab2:
    st.subheader("Affiliate Programs - Zero Investment")
    
    # Search/Filter
    search_term = st.text_input("Search Programs", "")
    
    cols = st.columns(3)
    for i, p in enumerate(programs):
        if search_term.lower() in p['name'].lower():
            with cols[i % 3]:
                st.markdown(f"""
                <div style="padding:1rem; border:1px solid #ddd; border-radius:8px; margin-bottom:1rem;">
                    <h4>{p['name']}</h4>
                    <p style="color:#21808d; font-weight:bold;">{p['commission']}</p>
                    <p style="font-size:12px;">{p['earning_potential']}</p>
                    <a href="https://{p['url']}" target="_blank">View Details</a>
                </div>
                """, unsafe_allow_html=True)

# --- Tab 3: Content Generator ---
with tab3:
    st.subheader("Auto-Generated Promotional Content")
    
    selected_program = st.selectbox("Select Program", [p['name'] for p in programs])
    content_type = st.selectbox("Content Type", ["Social Media Post", "Email Template", "Blog Title Ideas"])
    
    if st.button("Generate Content"):
        prog_data = next(p for p in programs if p['name'] == selected_program)
        
        if content_type == "Social Media Post":
            st.text_area("Generated Post", f"🚀 Just discovered {prog_data['name']}! It's a game-changer for {prog_data['category']}.\n\nCheck it out here: [LINK]\n\n#Affiliate #Growth")
        elif content_type == "Email Template":
            st.text_area("Generated Email", f"Subject: You need to see this tool\n\nHi there,\n\nI found a tool that can help you with {prog_data['category']}: {prog_data['name']}.\n\nIt's highly recommended. Let me know if you want more info!\n\nBest,\n[Name]")
        elif content_type == "Blog Title Ideas":
            st.info(f"1. {prog_data['name']} Review: Is it worth it?\n2. Top {prog_data['category']} Tools in 2025\n3. How to use {prog_data['name']} to grow.")

# --- Tab 4: Income Projector ---
with tab4:
    st.subheader("Income Projector & Analytics")
    
    col_calc1, col_calc2 = st.columns(2)
    with col_calc1:
        daily_conversions = st.number_input("Expected Conversions Per Day", value=2, min_value=0)
        avg_commission = st.number_input("Avg Commission (₹)", value=500, min_value=0)
    
    with col_calc2:
        daily_earn = daily_conversions * avg_commission
        monthly_earn = daily_earn * 30
        st.metric("Daily Earnings", f"₹{daily_earn:,}")
        st.metric("Monthly Earnings", f"₹{monthly_earn:,}")
        
    st.success("💡 Pro Tip: Focus on recurring programs for compound earnings!")

# --- Tab 5: Traffic Guide ---
with tab5:
    st.subheader("Free Traffic Methods Guide")
    st.info("All these methods are 100% free. No ads needed.")
    
    methods = [
        {"name": "YouTube", "desc": "Create tutorials/reviews. High effort, high reward."},
        {"name": "Instagram Reels", "desc": "Short clips showcasing products. Viral potential."},
        {"name": "Quora/Reddit", "desc": "Answer questions and link to your landing page."}
    ]
    
    for m in methods:
        st.markdown(f"**{m['name']}**: {m['desc']}")

# --- Tab 6: Live Logs ---
with tab6:
    st.subheader("🤖 Autonomous Agent Activity")
    st.info("This log shows what the background agent is doing in real-time.")
    
    log_file_path = os.path.join(os.path.dirname(__file__), 'output', 'activity.log')
    
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as f:
            lines = f.readlines()
            # Show last 20 lines
            for line in reversed(lines[-20:]):
                st.code(line.strip(), language="text")
    else:
        st.warning("No activity log found yet. Start the background runner first!")
    
    if st.button("Refresh Logs"):
        st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 Autonomous Sales Agent | [View Walkthrough](walkthrough.md)")
