import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# names and paths of the different currencies
CONFIGURATION = {
    "btc": ("Bitcoin", "data/btc.csv"),
    "ltc": ("Litecoin", "data/ltc.csv"),
    "eth": ("Ethereum", "data/eth.csv")
}

# we get bootstrap css from the CDN
BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"

app = dash.Dash(external_stylesheets=[BS])
app.title = "Currency Graph"

# content for first column
col1_content = dbc.Card(
    [
        dbc.CardTitle("What am I looking at?"),
        dbc.CardText(
            "This page lets you explore the value of currencies over time"
        ),
        dbc.FormGroup(
            [
                dbc.Label("Select currency"),
                dcc.Dropdown(
                    id="dash-input-dropdown",
                    options=[
                        {"label": label, "value": key}
                        for key, (label, _) in CONFIGURATION.items()
                    ],
                    value="btc",
                ),
                dbc.FormText("Choose the currency you would like to plot"),
            ]
        ),
        dbc.CardText(
            [
                "Included are ",
                html.Span("cryptocurrencies", id="cryptocurrency"),
                " and regular currencies.",
            ]
        ),
        dbc.Tooltip(
            "A cryptocurrency is a digital asset that uses strong "
            "cryptography to secure financial transactions",
            target="cryptocurrency",
            placement="right",
        ),
    ],
    body=True,
    color="primary",
    outline=True,
)

col2_content = dcc.Graph(
    id="dash-output-graph", config={"displayModeBar": False}
)

app.layout = dbc.Container(
    [
        # we can manually apply bootstrap css classes such as text-primary
        html.H1("Currency Graph", className="text-primary"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    col1_content,
                    # default order this second and let width 100%
                    width={"order": 2, "size": 12},
                    # on medium screens and larger order first and width 33%
                    md={"order": 1, "size": 4},
                    align="center",
                ),
                dbc.Col(
                    col2_content,
                    # default order this first and let width 100%
                    width={"order": 1, "size": 12},
                    # on medium screens and larger order second and width 66%
                    md={"order": 2, "size": 8},
                    className="mb-5",
                ),
            ]
        ),
    ],
    className="mb-5",
)


@app.callback(
    Output("dash-output-graph", "figure"),
    [Input("dash-input-dropdown", "value")]
)
def _on_dropdown_change(value):
    _, data_path = CONFIGURATION[value]
    df = pd.read_csv(data_path)
    figure = {
        "data": [go.Scatter({"x": df.day, "y": df.price_close})]
    }
    return figure


if __name__ == "__main__":
    app.run_server(port=8888, debug=True)
