import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path
import os

from analytics.aqicn import get_latest_air_kpis
from analytics.meteo import get_latest_meteo_kpis
from config.settings import DASH_HOST, DASH_PORT, DASH_DEBUG

# Get the static directory path (relative to the app)
static_dir = os.path.join(os.path.dirname(__file__), "static")
assets_dir = os.path.join(os.path.dirname(__file__), "static")

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    title="GoodAir – Qualité de l'air",
    suppress_callback_exceptions=True,
    assets_folder=assets_dir,
)


# Configure Flask to serve static files
@app.server.route("/static/<path:path>")
def serve_static(path):
    return app.server.send_from_directory(static_dir, path)


server = app.server

app.layout = dbc.Container(
    [
        # Title
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("🌿 GoodAir Dashboard", className="text-success mt-3"),
                    ]
                )
            ]
        ),
        dbc.Row(
            html.P(
                "Surveillance de la qualité de l'air en France",
                className="text-muted",
            )
        ),
        # AQI by cities
        dbc.Row(id="kpi-aqi-cards", className="mb-3"),
        dbc.Row(
            html.P(
                "Surveillance de la météo en France",
                className="text-muted",
            )
        ),
        # Weather by cities
        dbc.Row(id="kpi-weather-cards", className="mb-3"),
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
    Output("kpi-aqi-cards", "children"),
    Input("auto-refresh", "n_intervals"),
)
def update_kpi_aqi__cards(n_intervals):
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


def get_temp_gradient_color(temp):
    if temp == "N/A":
        return "white"

    temp = min(max(temp, -20), 40)

    # Cold: Blue (< 0°C)
    if temp < 0:
        ratio = max(temp / -20, 0)
        r = int(100 * ratio)
        g = int(150 * ratio)
        b = 255
        return f"rgb({r}, {g}, {b})"
    # Fresh/Cool: Cyan (0-15°C)
    elif temp <= 15:
        ratio = temp / 15
        r = 0
        g = int(200 + 55 * ratio)
        b = 255
        return f"rgb({r}, {g}, {b})"
    # Warm: Yellow-green (15-25°C)
    elif temp <= 25:
        ratio = (temp - 15) / 10
        r = int(255 * ratio)
        g = 255
        b = int(255 * (1 - ratio))
        return f"rgb({r}, {g}, {b})"
    # Hot: Red (> 25°C)
    else:
        ratio = min((temp - 25) / 15, 1)
        r = 255
        g = int(255 * (1 - ratio))
        b = 0
        return f"rgb({r}, {g}, {b})"


@app.callback(
    Output("kpi-weather-cards", "children"),
    Input("auto-refresh", "n_intervals"),
)
def update_kpi_meteo_cards(n_intervals):
    try:
        reponse = get_latest_meteo_kpis()

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
            temperature = row["temp"] if row["temp"] else "N/A"
            color = get_temp_gradient_color(temperature)
            icon_code = row.get("icon_weather", "01d")
            weather_desc = row.get("weather_description", "N/A")

            cards.append(
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(row["city"], className="fw-bold"),
                            dbc.CardBody(
                                [
                                    html.Div(
                                        html.Img(
                                            src=f"/static/weather_icons/{icon_code}@2x.png",
                                            style={
                                                "width": "80px",
                                                "height": "80px",
                                                "margin": "10px auto",
                                            },
                                        ),
                                        style={"text-align": "center"},
                                    ),
                                    html.H3(
                                        f"Temp {temperature} °C",
                                        className="mb-3",
                                        style={"color": color, "text-align": "center"},
                                    ),
                                    html.P(
                                        (
                                            weather_desc.capitalize()
                                            if weather_desc != "N/A"
                                            else weather_desc
                                        ),
                                        className="text-muted text-center",
                                        style={"font-size": "0.9rem"},
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
