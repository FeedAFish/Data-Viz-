import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path
import os
from datetime import datetime

from analytics.aqicn import get_latest_air_kpis
from analytics.meteo import get_latest_meteo_kpis
from config.settings import DASH_HOST, DASH_PORT, DASH_DEBUG

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
    return app.server.send_from_directory(assets_dir, path)


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
                "Surveillance de la qualité de l'air et météo en France",
                className="text-muted",
            )
        ),
        # Unified cards for all cities
        dbc.Row(id="kpi-unified-cards", className="mb-3"),
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


def get_aqi_status(aqi):
    """Get AQI status label based on AQI value"""
    if aqi == "N/A" or aqi is None:
        return "N/A"

    aqi = float(aqi)
    if aqi <= 50:
        return "GOOD"
    elif aqi <= 100:
        return "MODERATE"
    elif aqi <= 150:
        return "UNHEALTHY FOR SENSITIVE GROUPS"
    elif aqi <= 200:
        return "UNHEALTHY"
    else:
        return "VERY UNHEALTHY"


def get_wind_direction(degrees):
    """Convert wind degrees to cardinal direction"""
    if degrees is None:
        return "N/A"

    degrees = float(degrees) % 360
    directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    index = round(degrees / 22.5) % 16
    return directions[index]


def format_timestamp(ts):
    """Format timestamp for display"""
    if not ts:
        return "N/A"
    try:
        if isinstance(ts, str):
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = ts
        return dt.strftime("%a, %B %d, %Y | %I:%M %p")
    except:
        return "N/A"


@app.callback(
    Output("kpi-unified-cards", "children"),
    Input("auto-refresh", "n_intervals"),
)
def update_kpi_unified_cards(n_intervals):
    """Create unified cards with combined weather and AQI data"""
    try:
        # Get both air and meteo data
        air_response = get_latest_air_kpis()
        meteo_response = get_latest_meteo_kpis()

        if not meteo_response["success"]:
            return [
                dbc.Col(
                    dbc.Alert(
                        "Pas de données disponibles. Attendez le prochain cycle de collecte.",
                        color="info",
                    ),
                    width=12,
                )
            ]

        # Create a mapping of AQI data by city
        aqi_map = {}
        if air_response["success"]:
            for aqi_row in air_response["data"]:
                aqi_map[aqi_row["city"]] = aqi_row

        cards = []
        for weather_row in meteo_response["data"]:
            city_name = weather_row["city"]
            aqi_data = aqi_map.get(city_name, {})

            # Extract weather data
            temperature = weather_row.get("temp", "N/A")
            weather_desc = weather_row.get("weather_description", "N/A")
            icon_code = weather_row.get("icon_weather", "01d")
            wind_speed = weather_row.get("wind_speed", "N/A")
            wind_deg = weather_row.get("wind_deg", None)
            humidity = weather_row.get("humidity", "N/A")
            recorded_at = weather_row.get("weather_time", "N/A")

            # Extract AQI data
            aqi = aqi_data.get("aqi", "N/A")
            pm25 = aqi_data.get("pm25", "N/A")

            # Get derived data
            aqi_status = get_aqi_status(aqi)
            wind_dir = get_wind_direction(wind_deg)
            temp_color = get_temp_gradient_color(temperature)
            aqi_color = get_aqi_gradient_color(aqi)

            # Build card
            card = dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        # Left section: Weather icon and temperature
                                        dbc.Col(
                                            [   
                                                html.H4(
                                                    city_name.upper(),
                                                    className="fw-bold mb-0",
                                                ), # City name
                                                html.Div(
                                                    [
                                                        html.Img(
                                                            src=f"/static/weather_icons/{icon_code}@2x.png",
                                                            style={
                                                                "width": "100px",
                                                                "height": "100px",
                                                            },
                                                        ),
                                                    ],
                                                    style={"text-align": "center"},
                                                ),
                                                html.H2(
                                                    (
                                                        f"{temperature}°C"
                                                        if temperature != "N/A"
                                                        else "N/A"
                                                    ),
                                                    style={
                                                        "color": temp_color,
                                                        "text-align": "center",
                                                        "margin": "10px 0",
                                                    },
                                                    className="fw-bold",
                                                ),
                                                html.P(
                                                    (
                                                        weather_desc.capitalize()
                                                        if weather_desc != "N/A"
                                                        else "N/A"
                                                    ),
                                                    style={"text-align": "center"},
                                                    className="text-muted",
                                                ),
                                            ],
                                        ),
                                        # Right section: AQI
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    [
                                                        html.P(
                                                            "AIR QUALITY",
                                                            className="text-muted",
                                                            style={
                                                                "font-size": "0.9rem"
                                                            },
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        html.Div(
                                                                            style={
                                                                                "width": "100px",
                                                                                "height": "100px",
                                                                                "borderRadius": "50%",
                                                                                "border": f"8px solid {aqi_color}",
                                                                                "boxSizing": "border-box",
                                                                            }
                                                                        ),
                                                                        html.Div(
                                                                            (
                                                                                aqi
                                                                                if aqi
                                                                                != "N/A"
                                                                                else "N/A"
                                                                            ),
                                                                            style={
                                                                                "position": "absolute",
                                                                                "left": "50%",
                                                                                "top": "50%",
                                                                                "transform": "translate(-50%,-50%)",
                                                                                "fontSize": "22px",
                                                                                "fontWeight": "700",
                                                                            },
                                                                        ),
                                                                    ],
                                                                    style={
                                                                        "position": "relative",
                                                                        "width": "100px",
                                                                        "height": "100px",
                                                                        "margin": "10px auto",
                                                                    },
                                                                ),
                                                                html.P(
                                                                    aqi_status,
                                                                    style={
                                                                        "text-align": "center",
                                                                        "color": aqi_color,
                                                                        "margin": "5px 0",
                                                                    },
                                                                    className="fw-bold",
                                                                ),
                                                                html.P(
                                                                    (
                                                                        f"PM2.5: {pm25} µg/m³"
                                                                        if pm25 != "N/A"
                                                                        else "PM2.5: N/A"
                                                                    ),
                                                                    style={
                                                                        "text-align": "center",
                                                                        "font-size": "0.9rem",
                                                                    },
                                                                    className="text-muted",
                                                                ),
                                                            ],
                                                            style={
                                                                "text-align": "center"
                                                            },
                                                        ),
                                                    ],
                                                    style={"text-align": "center"},
                                                ),
                                                html.Hr(style={"margin": "5px 0"}),
                                                html.P(
                                                    [
                                                        html.Span(
                                                            "💨 ",
                                                            style={
                                                                "font-size": "1.2em"
                                                            },
                                                        ),
                                                        (
                                                            f"{wind_speed} km/h ({wind_dir})"
                                                            if wind_speed != "N/A"
                                                            else "N/A"
                                                        ),
                                                    ],
                                                    className="mb-2",
                                                ),
                                                html.P(
                                                    [
                                                        html.Span(
                                                            "💧 ",
                                                            style={
                                                                "font-size": "1.2em"
                                                            },
                                                        ),
                                                        (
                                                            f"{humidity}%"
                                                            if humidity != "N/A"
                                                            else "N/A"
                                                        ),
                                                    ],
                                                    className="mb-0",
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                            ],
                            className="p-4",
                        )
                    ],
                    style={
                        "background": "linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)"
                    },
                    class_name="border-0",
                ),
                width=3,
                className="mb-4",
            )

            cards.append(card)

        return (
            cards
            if cards
            else [
                dbc.Col(
                    dbc.Alert("Pas de données disponibles.", color="info"), width=12
                )
            ]
        )

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


def run_dashboard():
    app.run(host=DASH_HOST, port=DASH_PORT, debug=DASH_DEBUG)
