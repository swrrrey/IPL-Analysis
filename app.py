import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(
    page_title="🏏 IPL Data Analysis Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3d425a;
    }
    h1, h2, h3 {
        color: #ff4b4b;
    }
    .stTable {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Function to load data
@st.cache_data
def load_data():
    matches_path = "data/matches.csv"
    deliveries_path = "data/deliveries.csv"
    
    if not os.path.exists(matches_path) or not os.path.exists(deliveries_path):
        return None, None
        
    matches = pd.read_csv(matches_path)
    deliveries = pd.read_csv(deliveries_path)
    
    # Preprocessing
    matches['date'] = pd.to_datetime(matches['date'])
    matches['season'] = matches['season'].astype(int)
    
    return matches, deliveries

matches_df, deliveries_df = load_data()

# Title
st.title("🏏 IPL Data Analysis Dashboard (2008 - 2024)")
st.markdown("---")

if matches_df is None:
    st.error("Data files not found. Please run `generate_data.py` first.")
    st.stop()

# --- Sidebar Controls ---
st.sidebar.header("Dashboard Controls")

# Team selection
all_teams = sorted(list(set(matches_df['team1'].unique()) | set(matches_df['team2'].unique())))
selected_team = st.sidebar.selectbox("Select Team", ["All Teams"] + all_teams)

# Season selection
all_seasons = sorted(matches_df['season'].unique())
selected_season = st.sidebar.select_slider("Select Season", options=all_seasons, value=max(all_seasons))

# Filtering Logic
filtered_df = matches_df[matches_df['season'] == selected_season]
if selected_team != "All Teams":
    filtered_df = filtered_df[(filtered_df['team1'] == selected_team) | (filtered_df['team2'] == selected_team)]

# --- Main Layout ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Matches", len(filtered_df))
with col2:
    if selected_team != "All Teams":
        wins = len(filtered_df[filtered_df['winner'] == selected_team])
        st.metric(f"{selected_team} Wins", wins)
    else:
        st.metric("Total Venues", len(filtered_df['venue'].unique()))
with col3:
    st.metric("Unique Cities", len(filtered_df['city'].unique()))
with col4:
    st.metric("Toss Factor", f"{round((len(filtered_df[filtered_df['toss_winner'] == filtered_df['winner']]) / len(filtered_df)) * 100, 1)}% Win rate")

# --- Section 1: Filtered Match Insights ---
st.header("📊 Filtered Match Insights")
match_display = filtered_df[['id', 'date', 'team1', 'team2', 'venue', 'winner']].rename(
    columns={'id': 'Match ID', 'date': 'Date', 'team1': 'Team 1', 'team2': 'Team 2', 'venue': 'Venue', 'winner': 'Winner'}
)
st.write(match_display.head(20).to_html(classes='table table-striped', index=False), unsafe_allow_html=True)

# --- Section 2: Interactive Visualizations ---
st.markdown("---")
st.header("📈 Performance Trends")

c1, c2 = st.columns(2)

with c1:
    st.subheader("IPL Team Wins (All Time)")
    all_time_wins = matches_df['winner'].value_counts().reset_index()
    all_time_wins.columns = ['Team', 'Wins']
    
    fig_wins = px.bar(
        all_time_wins, 
        x='Wins', 
        y='Team', 
        orientation='h',
        color='Wins',
        color_continuous_scale='Reds',
        template='plotly_dark'
    )
    st.plotly_chart(fig_wins, use_container_width=True)

with c2:
    st.subheader(f"Wins Distribution in {selected_season}")
    season_wins = filtered_df['winner'].value_counts().reset_index()
    season_wins.columns = ['Team', 'Wins']
    
    fig_pie = px.pie(
        season_wins, 
        values='Wins', 
        names='Team',
        hole=0.4,
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- Section 3: Top Players & Trends ---
st.markdown("---")
st.header("🌟 Top Players & Trends")

# For player stats, we need deliveries data
season_match_ids = filtered_df['id'].unique()
season_deliveries = deliveries_df[deliveries_df['match_id'].isin(season_match_ids)]

p1, p2 = st.columns(2)

with p1:
    st.subheader("Top 10 Run Scorers")
    top_scorers = season_deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig_scorers = px.bar(
        top_scorers,
        x='batsman_runs',
        y='batter',
        orientation='h',
        labels={'batsman_runs': 'Total Runs', 'batter': 'Player'},
        color='batsman_runs',
        color_continuous_scale='Viridis',
        template='plotly_dark'
    )
    st.plotly_chart(fig_scorers, use_container_width=True)

with p2:
    st.subheader("Top 10 Wicket Takers")
    # Simple wicket count (excluding run outs for bowler stats usually, but keeping it simple here)
    wickets = season_deliveries[season_deliveries['is_wicket'] == 1]
    top_bowlers = wickets.groupby('bowler')['is_wicket'].count().sort_values(ascending=False).head(10).reset_index()
    
    fig_bowlers = px.bar(
        top_bowlers,
        x='is_wicket',
        y='bowler',
        orientation='h',
        labels={'is_wicket': 'Wickets', 'bowler': 'Player'},
        color='is_wicket',
        color_continuous_scale='Magma',
        template='plotly_dark'
    )
    st.plotly_chart(fig_bowlers, use_container_width=True)

# --- Section 4: Venue-Based Insights ---
st.markdown("---")
st.header("🏟️ Venue-Based Insights")

v1, v2 = st.columns(2)

with v1:
    st.subheader("Top Venues by Match Count")
    venue_counts = filtered_df['venue'].value_counts().reset_index()
    venue_counts.columns = ['Venue', 'Matches']
    
    fig_venue = px.bar(
        venue_counts.head(10),
        x='Matches',
        y='Venue',
        orientation='h',
        template='plotly_dark',
        color='Matches'
    )
    st.plotly_chart(fig_venue, use_container_width=True)

with v2:
    st.subheader("Toss Decision Trend")
    toss_decision = filtered_df['toss_decision'].value_counts().reset_index()
    toss_decision.columns = ['Decision', 'Count']
    
    fig_toss = px.pie(
        toss_decision,
        values='Count',
        names='Decision',
        template='plotly_dark'
    )
    st.plotly_chart(fig_toss, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Dashboard created with Python, Streamlit and Plotly.")
