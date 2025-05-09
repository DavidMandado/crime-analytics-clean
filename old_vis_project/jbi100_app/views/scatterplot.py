# scatterplot.py
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output
from jbi100_app.data import load_filtered_data

def layout():
    """ Return the Dash layout with two graphs and maybe a dropdown. """
    df = load_filtered_data()
    states_list = sorted(df["State"].dropna().unique())

    return html.Div([
        html.H2("Shark Incidents Analysis"),
        dcc.Dropdown(
            id="state-dropdown",
            options=[{"label": s, "value": s} for s in states_list],
            value=states_list[0],
            clearable=False
        ),
        dcc.Graph(id="line-chart"),
        dcc.Graph(id="bar-chart"),
    ])

def register_callbacks(app):
    """ Register callbacks for the line and bar charts. """
    @app.callback(
        [Output("line-chart", "figure"),
         Output("bar-chart", "figure")],
        [Input("state-dropdown", "value")]
    )
    def update_charts(selected_state):
        df = load_filtered_data()
        df_state = df[df["State"] == selected_state]

        # Example line chart: Incidents over years
        line_data = (
            df_state.groupby("Incident.year")["Incident.month"]
            .count()
            .reset_index(name="incident_count")
        )
        fig_line = px.line(
            line_data,
            x="Incident.year",
            y="incident_count",
            title=f"Incidents Over Time in {selected_state}"
        )

        # Example bar chart: Provoked vs. Unprovoked
        bar_data = (
            df_state.groupby("Provoked/unprovoked")["Incident.month"]
            .count()
            .reset_index(name="count")
        )
        fig_bar = px.bar(
            bar_data,
            x="Provoked/unprovoked",
            y="count",
            title=f"Types of Incidents in {selected_state}"
        )

        return fig_line, fig_bar
