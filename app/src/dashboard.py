import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from analytics.aqicn import get_latest_air_kpis
from config.settings import DASH_HOST, DASH_PORT, DASH_DEBUG

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    title="GoodAir – Qualité de l'air",
    suppress_callback_exceptions=True,
)

server = app.server

app.layout = dbc.Container(
    [
        # Title
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("🌿 GoodAir Dashboard", className="text-success mt-3"),
                        html.P(
                            "Surveillance de la qualité de l'air en France",
                            className="text-muted",
                        ),
                    ]
                )
            ]
        ),
        # AQI by cities
        dbc.Row(id="kpi-cards", className="mb-3"),
        # Auto refresh
        dcc.Interval(id="auto-refresh", interval=5 * 60 * 1000, n_intervals=0),
    ],
    fluid=True,
)


def get_aqi_gradient_color(aqi):
    if aqi == "N/A":
        return "white"

    aqi = min(max(aqi, 0), 200)

    if aqi <= 50:
        ratio = aqi / 50
        r = int(255 * ratio)
        g = 255
        b = 0
        return f"rgb({r}, {g}, {b})"
    elif aqi <= 100:
        ratio = (aqi - 50) / 50
        r = 255
        g = int(255 * (1 - ratio))
        b = 0
        return f"rgb({r}, {g}, {b})"
    else:
        ratio = (aqi - 100) / 100
        r = 255
        g = int(165 * (1 - ratio))
        b = 0
        return f"rgb({r}, {g}, {b})"


@app.callback(
    Output("kpi-cards", "children"),
    Input("auto-refresh", "n_intervals"),
)
def update_kpi_cards(n_intervals):
    try:
        reponse = get_latest_air_kpis()

        if not reponse["success"]:
            return [
                dbc.Col(
                    dbc.Alert(
                        "Pas de données disponibles. Attendez le prochain cycle de collecte.",
                        color="info",
                    ),
                    width=12,
                )
            ]

        cards = []
        for row in reponse["data"]:
            aqi = row["aqi"] if row["aqi"] else "N/A"
            color = get_aqi_gradient_color(aqi)

            cards.append(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(row["city"], className="fw-bold"),
                            dbc.CardBody(
                                [
                                    html.H3(
                                        f"AQI {aqi}",
                                        className="mb-3",
                                        style={"color": color},
                                    ),
                                    html.Small(
                                        "0 (Good) — 200 (Hazardous)",
                                        className="text-muted",
                                    ),
                                ]
                            ),
                        ],
                        color="dark",
                        outline=True,
                    ),
                    width=3,
                    className="mb-3",
                )
            )

        return cards

    except Exception as e:
        import traceback

        error_msg = f"Erreur: {str(e)}"
        print(traceback.format_exc())
        return [dbc.Col(dbc.Alert(error_msg, color="danger"), width=12)]


def run_dashboard():
    app.run(host=DASH_HOST, port=DASH_PORT, debug=DASH_DEBUG)
