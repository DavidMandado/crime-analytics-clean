import os
import json

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ─── Paths ────────────────────────────────────────────────────────────────────
APP_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR  = os.path.dirname(APP_DIR)
DATA_DIR     = os.path.join(PROJECT_DIR, "police-dashboard", "data")
WARD_GEOJSON = os.path.join(DATA_DIR, "ward_choro.json")
LSOA_GEOJSON = os.path.join(DATA_DIR, "lsoa_choro.json")

# ─── Load pre‐baked GeoJSONs once ─────────────────────────────────────────────
with open(WARD_GEOJSON) as f:
    ward_geo = json.load(f)
with open(LSOA_GEOJSON) as f:
    lsoa_geo = json.load(f)

# ─── Build DataFrames from the GeoJSONs ──────────────────────────────────────
ward_df = pd.DataFrame([
    {"code": feat["properties"]["code"], "count": feat["properties"]["count"]}
    for feat in ward_geo["features"]
])
lsoa_df = pd.DataFrame([
    {
        "code": feat["properties"]["code"],
        "count": feat["properties"]["count"],
        # make sure your LSOA GeoJSON has a 'ward' property to filter on
        "ward": feat["properties"].get("ward")
    }
    for feat in lsoa_geo["features"]
])

# ─── Dash App Setup ──────────────────────────────────────────────────────────
app = dash.Dash(__name__)

app.layout = html.Div([
    # hidden store for the clicked ward code
    dcc.Store(id="selected-ward", data=None),

    html.H1("London Burglary Heatmap"),

    dcc.Dropdown(
        id="level",
        options=[
            {"label": "Ward", "value": "ward"},
            {"label": "LSOA", "value": "lsoa"}
        ],
        value="ward",
        clearable=False
    ),

    dcc.Graph(id="map", style={"height": "80vh"})
])

# ─── Callback #1: capture clicks on a ward ──────────────────────────────────
@app.callback(
    Output("selected-ward", "data"),
    Input("map", "clickData"),
    prevent_initial_call=True
)
def store_ward(clickData):
    # clickData['points'][0]['location'] is the ward code
    return clickData["points"][0]["location"]

# ─── Callback #2: redraw map at ward or LSOA (and filter if ward clicked) ───
@app.callback(
    Output("map", "figure"),
    [
        Input("level", "value"),
        Input("selected-ward", "data")
    ]
)
def update_map(level, selected_ward):
    if level == "ward":
        df, geo = ward_df.copy(), ward_geo
    else:
        # if a ward has been clicked, filter LSOAs down to that ward
        if selected_ward:
            df = lsoa_df[lsoa_df["ward"] == selected_ward].copy()
            feats = [
                f for f in lsoa_geo["features"]
                if f["properties"].get("ward") == selected_ward
            ]
            geo = {"type": "FeatureCollection", "features": feats}
        else:
            df, geo = lsoa_df.copy(), lsoa_geo

    # ensure codes are strings
    df["code"] = df["code"].astype(str)

    # make the choropleth mapbox
    fig = px.choropleth_mapbox(
        df,
        geojson=geo,
        featureidkey="properties.code",
        locations="code",
        color="count",
        color_continuous_scale="YlOrRd",
        mapbox_style="open-street-map",   # works without a token
        center={"lat": 51.5074, "lon": -0.1278},
        zoom=10,
        opacity=0.7,
        labels={"count": "Burglary Count"}
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

if __name__ == "__main__":
    # Dash 3.x now uses `app.run(...)` instead of `run_server`
    app.run(debug=True)
