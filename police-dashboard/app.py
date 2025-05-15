import os
import json

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
from shapely.geometry import shape

# ─── Paths ────────────────────────────────────────────────────────────────────
APP_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR  = os.path.dirname(APP_DIR)
DATA_DIR     = os.path.join(PROJECT_DIR, "police-dashboard", "data")
WARD_GEOJSON = os.path.join(DATA_DIR, "ward_choro.json")
LSOA_GEOJSON = os.path.join(DATA_DIR, "lsoa_choro.json")

# ─── Load GeoJSONs once ───────────────────────────────────────────────────────
with open(WARD_GEOJSON) as f:
    ward_geo = json.load(f)
with open(LSOA_GEOJSON) as f:
    lsoa_geo = json.load(f)

# ─── Build DataFrames ─────────────────────────────────────────────────────────
ward_df = pd.DataFrame([
    {"code": feat["properties"]["code"], "count": feat["properties"]["count"]}
    for feat in ward_geo["features"]
])

lsoa_df = pd.DataFrame([
    {"code": feat["properties"]["code"], "count": feat["properties"]["count"],
     "geometry": shape(feat["geometry"])}
    for feat in lsoa_geo["features"]
])

# ─── Dash App Setup ──────────────────────────────────────────────────────────
app = dash.Dash(__name__)

# CSS styles for sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "300px",
    "padding": "20px",
    "background-color": "#f8f9fa",
    "overflow": "auto",
    "transition": "transform 0.3s ease"
}
SIDEBAR_HIDDEN = {**SIDEBAR_STYLE, "transform": "translateX(-100%)"}
CONTENT_STYLE = {"margin-left": "320px", "margin-right": "20px", "padding": "20px"}

app.layout = html.Div([
    dcc.Store(id="selected-ward", data=None),
    dcc.Store(id="sidebar-open", data=True),

    # Toggle button
    html.Button("☰ Filters", id="btn-toggle", n_clicks=0,
                style={"position": "fixed", "top": "10px", "left": "10px", "zIndex": 1000}),

    # Sidebar
    html.Div(id="sidebar", children=[
        html.H2("Filters", style={"margin-top": "0"}), html.Hr(),
        # Data View
        html.Div([html.Label("Data View"),
            dcc.RadioItems(id="data-mode",
                options=[{"label":"Past Data","value":"past"},
                         {"label":"Predicted Data","value":"pred"}],
                value="past", labelStyle={"display":"block","margin-bottom":"5px"}
            )], style={"margin-bottom":"20px"}),
        # Granularity
        html.Div([html.Label("View Level"),
            dcc.Dropdown(id="level",
                options=[{"label":"Ward","value":"ward"},
                         {"label":"LSOA","value":"lsoa"}],
                value="ward", clearable=False)
        ], style={"margin-bottom":"20px"}),
        # Past controls
        html.Div(id="past-controls", children=[
            html.Label("Select Date Range (Year-Month)"),
            dcc.RangeSlider(id="past-range", min=2018, max=2025, step=1/12,
                marks={year:str(year) for year in range(2018,2026)}, value=[2019,2022])
        ], style={"margin-bottom":"20px"}),
        # Predicted controls
        html.Div(id="pred-controls", children=[
            html.Label("Prediction Horizon (months)"),
            dcc.Dropdown(id="pred-horizon",
                options=[{"label":"1-month ahead","value":1},
                         {"label":"2-months ahead","value":2},
                         {"label":"3-months ahead","value":3}],
                value=1, clearable=False), html.Br(),
            html.Label("Prediction Data Source"),
            dcc.RadioItems(id="pred-data-choice",
                options=[{"label":"Use Last Prediction","value":"last"},
                         {"label":"Upload New Data","value":"upload"}],
                value="last", labelStyle={"display":"block","margin-bottom":"5px"}),
            dcc.Upload(id="upload-pred-data",
                children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                style={"width":"100%","height":"40px","lineHeight":"40px",
                       "borderWidth":"1px","borderStyle":"dashed",
                       "borderRadius":"5px","textAlign":"center"})
        ], style={"display":"none","margin-bottom":"20px"}),
        html.Hr(),
        html.Button("← Back to Wards", id="back-button",
                    style={"display":"none","width":"100%","margin-bottom":"10px"}),
        html.Button("Apply", id="apply-button", n_clicks=0,
                    style={"width":"100%","margin-top":"10px"})
    ], style=SIDEBAR_STYLE),

    # Main Content
    html.Div(children=[html.H1("London Burglary Heatmap"),
                      dcc.Graph(id="map", style={"height":"80vh"})],
             id="page-content", style=CONTENT_STYLE)
])

# ─── Callbacks ───────────────────────────────────────────────────────────────
@app.callback(
    Output("sidebar", "style"), Output("page-content", "style"),
    Input("btn-toggle", "n_clicks"), State("sidebar-open", "data")
)
def toggle_sidebar(n, open_):
    if n:
        return (SIDEBAR_HIDDEN, {**CONTENT_STYLE, "margin-left":"20px"}) if open_ else (SIDEBAR_STYLE, CONTENT_STYLE)
    return SIDEBAR_STYLE, CONTENT_STYLE

@app.callback(Output("sidebar-open","data"), Input("sidebar","style"))
def store_sidebar(style): return style.get("transform")!="translateX(-100%)"

@app.callback(Output("past-controls","style"), Output("pred-controls","style"),
              Input("data-mode","value"))
def toggle_mode(mode):
    return ({"margin-bottom":"20px"}, {"display":"none"}) if mode=="past" else ({"display":"none"},{"margin-bottom":"20px"})

@app.callback(Output("selected-ward","data"), Output("back-button","style"),
              Input("map","clickData"), Input("back-button","n_clicks"))
def handle_selection(clickData, n_clicks):
    ctx=dash.callback_context
    if not ctx.triggered: raise PreventUpdate
    trig=ctx.triggered[0]["prop_id"].split('.')[0]
    if trig=="map" and clickData:
        return clickData["points"][0]["location"], {"display":"block","width":"100%"}
    if trig=="back-button": return None, {"display":"none"}
    raise PreventUpdate

@app.callback(
    Output("map","figure"),
    Input("apply-button","n_clicks"),
    Input("selected-ward","data"),
    State("level","value"),
    State("data-mode","value"),
    State("past-range","value"),
    State("pred-horizon","value"),
    State("pred-data-choice","value")
)
def update_map(n_clicks, selected_ward, level, mode, past_range, pred_horizon, pred_source):
    # Render drilldown if ward selected
    if selected_ward:
        ward_feat=next((f for f in ward_geo["features"] if f["properties"]["code"]==selected_ward),None)
        if ward_feat:
            ward_poly=shape(ward_feat["geometry"])
            feats=[f for f in lsoa_geo["features"] if ward_poly.contains(shape(f["geometry"]).centroid)]
            geo={"type":"FeatureCollection","features":feats}
            codes={f["properties"]["code"] for f in feats}
            df=lsoa_df[lsoa_df["code"].isin(codes)].drop(columns="geometry")
            minx,miny,maxx,maxy=ward_poly.bounds
            center={"lat":(miny+maxy)/2,"lon":(minx+maxx)/2}; zoom=12
        else:
            df,geo,center,zoom=ward_df,ward_geo,{"lat":51.5074,"lon":-0.1278},10
    else:
        # No ward: respect dropdown level
        if level=="ward": df,geo,center,zoom=ward_df,ward_geo,{"lat":51.5074,"lon":-0.1278},10
        else: df,geo,center,zoom=lsoa_df.drop(columns="geometry"),lsoa_geo,{"lat":51.5074,"lon":-0.1278},10
    df=df.astype({"code":str,"count":int})
    fig=px.choropleth_map(df,geojson=geo,featureidkey="properties.code",
        locations="code",color="count",color_continuous_scale="YlOrRd",
        map_style="open-street-map",center=center,zoom=zoom,opacity=0.7,
        labels={"count":"Burglary Count"})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__=="__main__": app.run(debug=True)
