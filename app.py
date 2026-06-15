
import streamlit as st
import pandas as pd
from recommend import load_data, filter_by_location, recommend_restaurants

st.set_page_config(page_title="Ruddy", page_icon="🍛", layout="centered")

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500&family=JetBrains+Mono:wght@500&display=swap');

html {
    scroll-behavior: smooth;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        linear-gradient(
            rgba(0,0,0,0.55),
            rgba(0,0,0,0.55)
        ),
        url("https://images.unsplash.com/photo-1504674900247-0877df9cc836");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}



.main .block-container {
    animation: fadeInPage .8s ease;
    max-width: 1100px;
}

@keyframes fadeInPage {

    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}


.tt-header {
    text-align: center;
    padding: 1.5rem 0 1rem 0;
}

@keyframes floatTitle {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

.tt-title {

    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 3rem;
    color: white;
    animation: floatTitle 4s ease-in-out infinite;
    text-shadow:
        0px 4px 15px rgba(0,0,0,.4);
}

.tt-tagline {

    color: #F5E6CF;
    font-size: 1rem;
}
            .stSlider [data-baseweb="slider"] {
    padding-top: 10px;
}

/* Active progress track */
.stSlider [data-baseweb="slider"] > div > div > div:nth-child(1) {
    background: linear-gradient(
        90deg,
        #FF6B35,
        #FF9F1C,
        #FFD166
    ) !important;

    height: 8px !important;
    border-radius: 999px !important;

    box-shadow:
        0 0 10px rgba(255,107,53,.7),
        0 0 20px rgba(255,159,28,.5);
}
            

.stSlider [data-baseweb="slider"] > div > div > div:nth-child(2) {
    background: rgba(255,255,255,.15) !important;
    height: 8px !important;
    border-radius: 999px !important;
    backdrop-filter: blur(10px);
}

.stSlider [role="slider"] {

    width: 24px !important;
    height: 24px !important;
    background: white !important;
    border: 4px solid #FF9F1C !important;
    border-radius: 50% !important;

    box-shadow:
        0 0 10px rgba(255,159,28,.8),
        0 0 20px rgba(255,159,28,.6),
        0 0 35px rgba(255,159,28,.3);

    transition: all .25s ease !important;
}

.stSlider [role="slider"]:hover {

    transform: scale(1.3);

    box-shadow:
        0 0 15px rgba(255,159,28,1),
        0 0 30px rgba(255,159,28,.8),
        0 0 50px rgba(255,159,28,.5);
}


.food-float {

    text-align:center;
    font-size:32px;
    margin-bottom:20px;
    animation: floatFood 4s ease-in-out infinite;
}

@keyframes floatFood {

    0% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-8px);
    }
    100% {
        transform: translateY(0px);
    }
}



div[data-testid="stForm"] {

    background:
        rgba(255,255,255,0.12);
    backdrop-filter:
        blur(18px);
    border:
        1px solid rgba(255,255,255,0.15);
    border-radius: 18px;
    padding: 1.5rem;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.25);
}

.tt-section-label {

    font-family: 'JetBrains Mono', monospace;
    font-size: .75rem;
    color: #F5D7A7;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin: 1.5rem 0 .6rem 0;
}

.stTextInput input,
.stTextInput > div > div > input {

    background-color:
        rgba(255,255,255,.95) !important;

    border:
        1px solid #E5DBC8 !important;
    border-radius: 10px !important;
    color: #2E2A24 !important;
    transition:
        all .3s ease;
}

.stTextInput input:focus {
    transform: scale(1.02);
    border:
        1px solid #FF9F1C !important;
    box-shadow:
        0 0 15px rgba(255,159,28,.3);
}

.stTextInput input::placeholder {
    color: #A89B85 !important;
}

.stTextInput label,
.stSlider label {
    color: #FFF4E4 !important;
    text-transform: uppercase;
    font-size: .75rem !important;
}

.stSlider [role="slider"] {

    background-color:
        #FF9F1C !important;
    border-color:
        #FF9F1C !important;
    transition:
        all .2s ease;
}

.stSlider [role="slider"]:hover {
    transform: scale(1.2);
    box-shadow:
        0 0 15px rgba(255,159,28,.5);
}

.stButton button,
.stFormSubmitButton button {

    background:
        linear-gradient(
            135deg,
            #FF6B35,
            #FF9F1C
        ) !important;

    color: white !important;
    border: none !important;
     border-radius: 12px !important;
    font-weight: 600 !important;
    transition:
        all .2s ease !important;
    cursor: pointer !important;

    width: 100%;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    transform:
        translateY(-4px);
    box-shadow:
        0 12px 30px rgba(255,107,53,.45);
}

.stButton button:active,
.stFormSubmitButton button:active {
    transform:
        scale(.92);
    box-shadow:
        0 3px 8px rgba(0,0,0,.25);
}

@keyframes fadeUp {

    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.tt-card {
    background:
        rgba(255,255,255,.97);
    border:
        1px solid #E5DBC8;
    border-radius: 14px;
    display: flex;
    overflow: hidden;
    margin-bottom: 1rem;
    animation:
        fadeUp .6s ease;
    transition:
        all .3s ease;
    cursor:pointer;
}

.tt-card:hover {
    transform:
        translateY(-6px);
    box-shadow:
        0 15px 35px rgba(0,0,0,.18);
}

.tt-card:active {
    transform:
        scale(.98);
}

.tt-card-body {
    flex: 1;
    padding: 16px 18px;
}

.tt-card-name {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.1rem;
    color: #2E2A24;
}

.tt-tag {
    font-size: .72rem;
    padding: 4px 10px;
    border-radius: 20px;
    background-color: #EEF1E7;
    color: #5B6E49;
    margin-right: 4px;
    display: inline-block;
}

.tt-meta {
    color: #8A7E6B;
    margin-top: 8px;
}

.tt-stamp-col {
    width: 100px;
    border-left:
        1.5px dashed #E5DBC8;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    gap:8px;
}

@keyframes pulse {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
    100% {
        transform: scale(1);
    }
}

.tt-stamp {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    border: 3px solid #C1542D;
    display:flex;
    justify-content:center;
    align-items:center;
    font-family:'JetBrains Mono', monospace;
    font-weight:600;
    color:#C1542D;
    animation:
        pulse 2s infinite;
}
            
.tt-rating {
    color:#8A7E6B;
    font-size:.78rem;
}

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #2E2A24;
}

::-webkit-scrollbar-thumb {
        background:
        linear-gradient(
            #FF6B35,
            #FF9F1C
        );
        border-radius: 20px;
}

.ruddy-logo{
    display:flex;
    justify-content:center;
    margin-top:10px;
    margin-bottom:10px;
}

.ruddy-logo img{
    width:260px; 
    opacity:0.45; 
    mix-blend-mode:screen;
    filter:
        drop-shadow(0px 0px 15px rgba(255,170,0,.15))
        drop-shadow(0px 5px 15px rgba(0,0,0,.35));

    animation:logoFloat 6s ease-in-out infinite;
}

@keyframes logoFloat{
    0%{
        transform:translateY(0px);
    }
    50%{
        transform:translateY(-8px);
    }
    100%{
        transform:translateY(0px);
    }
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data("dataset.csv")

try:
    df = get_data()
except FileNotFoundError:
    st.error("'dataset.csv' not found. Place the dataset file in the same folder as app.py.")
    st.stop()

import base64

with open("assets/fooditem.png", "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

st.markdown(
    f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{encoded}" class="ruddy-logo">
    </div>
    """,
    unsafe_allow_html=True
)

with st.form("search_form"):
    col1, col2 = st.columns(2)
    with col1:
        food_item = st.text_input("Craving", placeholder="E.g. Biryani, Pizza, Dosa")
    with col2:
        city = st.text_input("City", placeholder="E.g. Bangalore")
    locality = st.text_input("Locality (optional)", placeholder="E.g. Koramangala")
    top_n = st.slider("Number of recommendations", min_value=1, max_value=20, value=5)
    submitted = st.form_submit_button("Find restaurants")
    

if submitted:
    if not food_item.strip():
        st.warning("Enter a food item to search for.")
    elif not city.strip():
        st.warning("Enter a city.")
    else:
        filtered_df, match_level = filter_by_location(df, city=city, locality=locality)

        if match_level == "locality":
            label = f"Top matches near {locality.title()}, {city.title()}"
        elif match_level == "city":
            label = f"No exact locality match — showing results across {city.title()}"
        else:
            label = "Right now no location detected.We are working on it to add more restaurants  — Showing the results from another cities "

        results = recommend_restaurants(food_item, filtered_df, top_n=top_n)
        st.markdown(f'<div class="tt-section-label">{label}</div>', unsafe_allow_html=True)

        if results.empty:
            st.error("No matching restaurants found. Try a different food item or location.")
        else:
            
            for _, row in results.iterrows():
                match_pct = int(round(row["similarity"] * 100))
                cuisines = [c.strip().title() for c in row["Cuisines"].split(",")][:2]
                tags_html = "".join(f'<span class="tt-tag">{c}</span>' for c in cuisines)

                card_html = f"""
                <div class="tt-card">
                    <div class="tt-card-body">
                        <div class="tt-card-name">{row['Restaurant Name']}</div>
                        <div>{tags_html}</div>
                        <div class="tt-meta">
                            {row['Locality'].title()}, {row['City'].title()} &middot;
                            {int(row['Votes'])} votes
                        </div>
                    </div>
                    <div class="tt-stamp-col">
                        <div class="tt-stamp">{match_pct}%</div>
                        <div class="tt-rating">&#9733; {row['Rating']:.1f}</div>
                    </div>
                </div>         
                
                """
                st.markdown(card_html, unsafe_allow_html=True)
