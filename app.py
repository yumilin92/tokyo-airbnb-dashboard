import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# =====================
# 1. LOAD DATA
# =====================
df = pd.read_csv('data/listings_clean.csv')

# =====================
# 2. APP SETUP
# =====================
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# =====================
# 3. LAYOUT
# =====================
app.layout = dbc.Container([

    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🗼 Tokyo Airbnb Dashboard",
                    className="text-center my-4"),
            html.P("Explore Tokyo Airbnb listings — prices, neighbourhoods, and room types",
                   className="text-center text-muted mb-4")
        ])
    ]),

    # Filters row
    dbc.Row([
        dbc.Col([
            html.Label("Room Type"),
            dcc.Dropdown(
                id='room-type-filter',
                options=[{'label': rt, 'value': rt} 
                         for rt in sorted(df['room_type'].unique())],
                value=None,
                placeholder="All room types",
                clearable=True
            )
        ], width=3),

        dbc.Col([
            html.Label("Neighbourhood"),
            dcc.Dropdown(
                id='neighbourhood-filter',
                options=[{'label': n, 'value': n} 
                         for n in sorted(df['neighbourhood_cleansed'].unique())],
                value=None,
                placeholder="All neighbourhoods",
                clearable=True
            )
        ], width=3),

        dbc.Col([
            html.Label("Price Range (¥/night)"),
            dcc.RangeSlider(
                id='price-slider',
                min=0,
                max=100000,
                step=1000,
                value=[0, 100000],
                marks={0: '¥0', 25000: '¥25K', 
                       50000: '¥50K', 75000: '¥75K', 
                       100000: '¥100K'}
            )
        ], width=6)
    ], className="mb-4"),

    # KPI cards
    dbc.Row([
    dbc.Col(dbc.Card([
        dbc.CardBody([
            html.H4(id='kpi-listings', className="card-title text-center text-primary"),
            html.P("Total Listings", className="text-center text-muted")
        ])
    ], color="light", outline=True), width=3),

    dbc.Col(dbc.Card([
        dbc.CardBody([
            html.H4(id='kpi-price', className="card-title text-center text-success"),
            html.P("Median Price/night", className="text-center text-muted")
        ])
    ], color="light", outline=True), width=3),

    dbc.Col(dbc.Card([
        dbc.CardBody([
            html.H4(id='kpi-rating', className="card-title text-center text-warning"),
            html.P("Avg Rating", className="text-center text-muted")
        ])
    ], color="light", outline=True), width=3),

    dbc.Col(dbc.Card([
        dbc.CardBody([
            html.H4(id='kpi-neighbourhoods', className="card-title text-center text-info"),
            html.P("Neighbourhoods", className="text-center text-muted")
        ])
    ], color="light", outline=True), width=3),
], className="mb-4"),

    # Charts row 1
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='price-by-neighbourhood')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='room-type-pie')
        ], width=6)
    ], className="mb-4"),

    # Charts row 2
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='price-distribution')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='map')
        ], width=6)
    ])

], fluid=True)

# =====================
# 4. CALLBACKS
# =====================
@app.callback(
    Output('kpi-listings', 'children'),
    Output('kpi-price', 'children'),
    Output('kpi-rating', 'children'),
    Output('kpi-neighbourhoods', 'children'),
    Output('price-by-neighbourhood', 'figure'),
    Output('room-type-pie', 'figure'),
    Output('price-distribution', 'figure'),
    Output('map', 'figure'),
    Input('room-type-filter', 'value'),
    Input('neighbourhood-filter', 'value'),
    Input('price-slider', 'value')
)
def update_dashboard(room_type, neighbourhood, price_range):
    filtered = df.copy()
    filtered = filtered[
        (filtered['price'] >= price_range[0]) &
        (filtered['price'] <= price_range[1])
    ]
    if room_type:
        filtered = filtered[filtered['room_type'] == room_type]
    if neighbourhood:
        filtered = filtered[
            filtered['neighbourhood_cleansed'] == neighbourhood]

    # KPIs
    kpi_listings = f"{len(filtered):,}"
    kpi_price = f"¥{filtered['price'].median():,.0f}"
    kpi_rating = f"{filtered['review_scores_rating'].mean():.2f} ⭐"
    kpi_neighbourhoods = f"{filtered['neighbourhood_cleansed'].nunique()}"

    # Chart 1: Price by neighbourhood (top 15)
    top_neigh = (filtered.groupby('neighbourhood_cleansed')['price']
                 .median()
                 .sort_values(ascending=False)
                 .head(15)
                 .reset_index())
    fig_neigh = px.bar(top_neigh, 
                       x='price', 
                       y='neighbourhood_cleansed',
                       orientation='h',
                       title='Top 15 Neighbourhoods by Median Price',
                       labels={'price': 'Median Price (¥)', 
                               'neighbourhood_cleansed': ''},
                       color='price',
                       color_continuous_scale='Blues')
    fig_neigh.update_layout(showlegend=False, coloraxis_showscale=False)

    # Chart 2: Room type pie
    room_counts = filtered['room_type'].value_counts().reset_index()
    fig_pie = px.pie(room_counts, 
                     values='count', 
                     names='room_type',
                     title='Room Type Distribution',
                     color_discrete_sequence=px.colors.sequential.Blues_r)

    # Chart 3: Price distribution
    fig_dist = px.histogram(filtered, 
                            x='price', 
                            nbins=50,
                            title='Price Distribution (¥/night)',
                            labels={'price': 'Price (¥)', 'count': 'Listings'},
                            color_discrete_sequence=['#2a6496'])

    # Chart 4: Map
    fig_map = px.scatter_mapbox(
        filtered.sample(min(2000, len(filtered))),
        lat='latitude',
        lon='longitude',
        color='price',
        size='accommodates',
        hover_name='name',
        hover_data={
            'latitude': False,
            'longitude': False,
            'price': ':,.0f',
            'room_type': True,
            'neighbourhood_cleansed': True,
            'accommodates': True
    },
    labels={
        'price': 'Price (¥)',
        'room_type': 'Room type',
        'neighbourhood_cleansed': 'Neighbourhood',
        'accommodates': 'Guests'
    },
        color_continuous_scale='Reds',
        title='Listings Map',
        mapbox_style='carto-positron',
        zoom=10,
        center={'lat': 35.6762, 'lon': 139.6503}
    )
    fig_map.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

    return (kpi_listings, kpi_price, kpi_rating, kpi_neighbourhoods,
            fig_neigh, fig_pie, fig_dist, fig_map)

# =====================
# 5. RUN
# =====================
if __name__ == '__main__':
    app.run(debug=True)
