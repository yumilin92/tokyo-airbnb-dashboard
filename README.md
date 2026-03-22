# 🗼 Tokyo Airbnb Market Dashboard

An interactive business dashboard exploring 11,000+ Airbnb listings 
in Tokyo — built with Plotly Dash and real 2023 data.

---

## 🚀 Live Demo

```bash
git clone https://github.com/yumilin92/tokyo-airbnb-dashboard.git
cd tokyo-airbnb-dashboard
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:8050** in your browser.

---

## 📊 Dashboard Features

**Interactive filters:**
- Room type (Entire home, Private room, Hotel room, Shared room)
- Neighbourhood (all 46 Tokyo neighbourhoods)
- Price range slider (¥0 — ¥100,000/night)

**Real-time KPIs:**
- Total listings count
- Median price per night
- Average rating
- Number of neighbourhoods

**Visualizations:**
- Top 15 neighbourhoods by median price
- Room type distribution (pie chart)
- Price distribution histogram
- Interactive map of all listings with hover details

---

## 🔍 Key Findings

1. **Entire homes dominate (72%)** — Tokyo guests strongly prefer 
   full property rentals over shared spaces
2. **Median price: ¥14,293/night** — with significant variation 
   across neighbourhoods
3. **Shibuya, Minato, Chiyoda** are the most expensive areas — 
   central Tokyo commands a clear price premium
4. **Average rating: 4.67/5** — Tokyo hosts maintain exceptionally 
   high quality standards
5. **Okutama** appears in top 10 despite being rural — 
   luxury nature retreats command premium prices

---

## 📁 Repository Structure

```
tokyo-airbnb-dashboard/
│
├── data/
│   ├── listings.csv               # raw Airbnb listings data
│   └── listings_clean.csv         # cleaned dataset used by dashboard
│
├── visuals/
│   └── eda_overview.png           # price, room type, neighbourhood charts
│
├── 01_eda.ipynb                   # exploratory data analysis
├── app.py                         # Dash dashboard application
├── requirements.txt               # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

- **Python 3.12**
- **Dash 4.0** — interactive web dashboard framework
- **Plotly** — interactive charts and maps
- **Dash Bootstrap Components** — responsive layout
- **pandas / numpy** — data processing
- **matplotlib / seaborn** — static EDA charts

---

## 📦 Dataset

**Source:** [Kaggle — Tokyo Airbnb Open Data 2023](https://www.kaggle.com/datasets/lucamassaron/tokyo-airbnb-open-data-2023)  
**Original source:** Inside Airbnb (insideairbnb.com)  
**Size:** 11,177 listings | 75 features | Scraped December 2021  
**Geography:** All 46 Tokyo neighbourhoods

> Download the dataset from Kaggle and place CSV files in the `data/` folder.

---

## 👤 Author

**Yulia Vovk**  
Economics background + Data Science  
📍 Tokyo, Japan  
🔗 [Kaggle](https://kaggle.com/yuliavovk) | [GitHub](https://github.com/yumilin92)
