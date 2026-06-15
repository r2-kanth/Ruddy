# 🍛 RUDDY — Restaurant Recommendation System

A content-based recommendation system with a custom "order ticket" themed UI.
Users enter a food craving + city (+ optional locality) and get restaurants
ranked by cuisine match , rating, and popularity.

## Files
- `recommend.py` — data loading, location filtering, recommendation logic
- `app.py` — Streamlit app with custom "Tiffin Trail" theme
- `.streamlit/config.toml` — forces light theme (prevents dark mode bleed-through)
- `sample_dataset.csv` — small sample dataset for testing
- `dataset.csv` — place your full Kaggle dataset here

## Setup
```bash
pip install pandas scikit-learn streamlit
```

## Run
```bash
streamlit run app.py
```

## Inputs
- Craving (required) — e.g. "Biryani"
- City (required) — e.g. "Bangalore"
- Locality (optional) — e.g. "Koramangala"
- Number of recommendations (slider, 3-15)

## Design
- Color palette: cream (#FBF5E9), ink (#2E2A24), saffron (#E2A33B), terracotta (#C1542D), curry green (#5B6E49)
- Fonts: Fraunces (headings), Inter (body), JetBrains Mono (scores)
- Each restaurant result is shown as a "ticket": details on the left,
  a dashed perforation, and a stamped match-percentage circle on the right.

  ________________________________________________________________________________________________________________________________________
