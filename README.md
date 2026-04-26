# 🏏 IPL Data Analysis Dashboard (2008–2024)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-green?logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple?logo=pandas)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

> An interactive, end-to-end IPL cricket analytics dashboard built with Python, Streamlit, and Plotly — covering 16 seasons of match and delivery data (2008–2024).

🔗 **Live Demo:** [ipl-analysis-gavcwtjchgy7ryqjqzdxlc.streamlit.app](https://ipl-analysis-gavcwtjchgy7ryqjqzdxlc.streamlit.app/)

---

## 📸 Screenshots
<img width="1897" height="846" alt="Screenshot 2026-04-26 171527" src="https://github.com/user-attachments/assets/aa8dd56c-1bc3-413c-94e9-5e10484124e8" />
<img width="1905" height="858" alt="Screenshot 2026-04-26 171549" src="https://github.com/user-attachments/assets/e71fb1b1-311e-4c11-b735-d5787b8d1113" />
<img width="1884" height="831" alt="Screenshot 2026-04-26 171615" src="https://github.com/user-attachments/assets/a31612fa-a9b1-4b60-8254-561c47e5db16" />
<img width="1904" height="836" alt="Screenshot 2026-04-26 171633" src="https://github.com/user-attachments/assets/b6e80ad0-ec65-4ffe-996f-c5c254eefa26" />
<img width="1870" height="827" alt="Screenshot 2026-04-26 171740" src="https://github.com/user-attachments/assets/74f94c2c-0cd8-4e73-8c4c-4b92a587e773" />



---

## 📌 Problem Statement

The Indian Premier League generates enormous volumes of match and ball-by-ball data every season, but this data is typically scattered across raw CSV files with no easy way to explore it interactively. Cricket fans, analysts, and enthusiasts have no convenient single-page tool to:

- Filter matches by team and season at a glance
- Compare team win records historically and within a season
- Identify top run-scorers and wicket-takers across seasons
- Understand venue-level patterns — which stadiums favour which teams
- Explore all of the above through interactive, zoomable visualizations without writing any code

---

## ✅ Solution

This dashboard aggregates `matches.csv` and `deliveries.csv` from the publicly available [IPL Dataset on Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020) and presents them as a clean, filterable, interactive web application using:

- **Pandas** for data cleaning, merging, and aggregation
- **Streamlit** for the sidebar controls and multi-page layout
- **Plotly** for all interactive charts (hoverable, zoomable, downloadable)

### Key Features

| Feature | Description |
|---|---|
| 🔍 **Filtered Match Insights** | Table of matches filtered by team & season — Match ID, Date, Teams, Venue, Winner |
| 📊 **IPL Team Wins Chart** | Horizontal bar chart of all-time wins per team, colour-coded by franchise |
| 🍩 **Season Win Distribution** | Donut chart showing each team's share of wins in the selected season |
| 🏆 **Top Run Scorers** | Bar chart of top 10 batters (all time or filtered by season) |
| 🎯 **Top Wicket Takers** | Bar chart of top 10 bowlers with colour-coded wicket scale |
| 🏟️ **Venue Insights** | Venues ranked by matches hosted; win rate by team at each ground |
| 🎛️ **Sidebar Controls** | Team dropdown + season slider — all charts update reactively |
| 📈 **Toss Factor Metric** | KPI card showing % of matches won by the toss winner |

---

## 🗂️ Project Structure

```
ipl-dashboard/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md
│
├── data/
│   ├── matches.csv         # Match-level data (2008–2024)
│   └── deliveries.csv      # Ball-by-ball delivery data
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9+ |
| UI Framework | Streamlit |
| Visualizations | Plotly Express & Plotly Graph Objects |
| Data Processing | Pandas, NumPy |
| Deployment | Streamlit Community Cloud |

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ipl-dashboard.git
cd ipl-dashboard
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the datasets

Download `matches.csv` and `deliveries.csv` from [Kaggle](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020) and place them in the `data/` folder.

### 4. Run the app

```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

---

## 📦 requirements.txt

```
streamlit
pandas
plotly
numpy
```

---

## 📊 Data Sources

| File | Description | Source |
|---|---|---|
| `matches.csv` | One row per match — teams, toss, winner, venue, date | [Kaggle IPL Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020) |
| `deliveries.csv` | Ball-by-ball records — runs, wickets, bowler, batter | [Kaggle IPL Dataset](https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020) |

Seasons covered: **2008 – 2024** (16 seasons, 1000+ matches)

---

## 🔮 Future Enhancements

| Priority | Enhancement |
|---|---|
| 🔴 High | **Head-to-head analysis** — win/loss breakdown between any two selected teams |
| 🔴 High | **Player profile pages** — career stats, season-by-season trends, strike rate & economy charts |
| 🟡 Medium | **Predictive win probability** — ML model (Logistic Regression / XGBoost) trained on toss, venue, and team form |
| 🟡 Medium | **Phase-wise batting analysis** — Powerplay vs Middle Overs vs Death Overs run rates per team |
| 🟡 Medium | **Geo map of venues** — Plotly Mapbox choropleth showing stadium locations across India |
| 🟢 Low | **Dark/light theme toggle** — user-selectable Streamlit theme |
| 🟢 Low | **CSV export** — download filtered match table as CSV directly from the dashboard |
| 🟢 Low | **Season-over-season comparison** — line chart showing a team's win percentage across all 16 seasons |
| 🟢 Low | **Mobile responsiveness** — optimised layout for smaller screen sizes |
| ⚪ Stretch | **Real-time data pipeline** — auto-update with live IPL 2025 scores via CricAPI |
| ⚪ Stretch | **Fantasy points estimator** — compute Dream11-style fantasy scores from deliveries data |

---





---

## 👤 Author

Built with ❤️ using Python, Streamlit, and Plotly.

If you found this useful, consider ⭐ starring the repo!
