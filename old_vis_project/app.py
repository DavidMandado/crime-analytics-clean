import dash
from dash import html
import os

app = dash.Dash(__name__)

file_path = os.path.join("jbi100_app", "assets", "index.html")
with open(file_path, "r", encoding="utf-8") as f:
    app.index_string = f.read()

app.layout = html.Div([])
if __name__ == "__main__":
    app.run_server(
    debug=True,
    dev_tools_ui=False  
)
# to do in the html, add division lines for filters, make filters look clean as well as the show filter button, 
# make filter options more centered and ordered looking