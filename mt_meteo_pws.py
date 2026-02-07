import meshtastic
import meshtastic.serial_interface
import meshtastic.tcp_interface
import sys
import requests
import json
from datetime import datetime
import pytz

# -------------------------------------------------
# CONFIGURAZIONE MESHTASTIC
# -------------------------------------------------

port   = "COM4"          # es. "COM3" o "/dev/ttyUSB0" o "192.168.1.199:4403"
is_tcp = False           # True se usiamo TCP

destination_node = None
channel_index    = 0

fallback_message = "Nessun dato meteo disponibile."

# -------------------------------------------------
# CONFIGURAZIONE WEATHER UNDERGROUND
# -------------------------------------------------

WEATHER_API_KEY = "APIKEY"
STATION_ID      = "IDSTAZIONE"
UNITS           = "m"

WEATHER_URL = "https://api.weather.com/v2/pws/observations/current"

LOCATION_NAME = "Scrivi qui il nome della stazione meteo"

JSON_FIELDS = {
    "temperature": ("metric", "temp"),
    "humidity": "humidity",
    "wind_speed": ("metric", "windSpeed"),
    "precip_rate": ("metric", "precipRate"),
    "precip_total": ("metric", "precipTotal"),
    "pressure": ("metric", "pressure")
}

# -------------------------------------------------
# FUNZIONI WEATHER UNDERGROUND
# -------------------------------------------------

def get_weather_data():
    params = {
        "stationId": STATION_ID,
        "format": "json",
        "units": UNITS,
        "apiKey": WEATHER_API_KEY
    }

    try:
        r = requests.get(WEATHER_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[ERRORE] Chiamata Weather Underground fallita: {e}")
        return None


def extract_field(obs, field):
    if isinstance(field, tuple):
        return obs.get(field[0], {}).get(field[1])
    return obs.get(field)


def format_weather_message(weather_json):
    try:
        obs = weather_json["observations"][0]

        temp = extract_field(obs, JSON_FIELDS["temperature"])
        hum  = extract_field(obs, JSON_FIELDS["humidity"])
        wind = extract_field(obs, JSON_FIELDS["wind_speed"])
        rain = extract_field(obs, JSON_FIELDS["precip_rate"])
        rtot = extract_field(obs, JSON_FIELDS["precip_total"])
        pres = extract_field(obs, JSON_FIELDS["pressure"])

        tz = pytz.timezone("Europe/Rome")
        now = datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")

        # Icone meteo 
        ICON_STATION = "🏠"
        ICON_TEMP    = "🌡️"
        ICON_HUM     = "💧"
        ICON_WIND    = "💨"
        ICON_RAIN    = "🌧️"
        ICON_TOTAL   = "☔"
        ICON_PRES    = "📈"
        ICON_TIME    = "🕒"

        msg = (
            f"{LOCATION_NAME} {ICON_STATION}Stazione Meteo: {STATION_ID}\n"
            f"{ICON_TIME} Meteo alle {now}\n"
            f"{ICON_TEMP} Temp: {temp} °C\n"
            f"{ICON_HUM} Umidità: {hum} %\n"
            f"{ICON_WIND} Vento: {wind} km/h\n"
            f"{ICON_RAIN} Pioggia: {rain} mm\n"
            f"{ICON_TOTAL} Da mezzanotte: {rtot} mm\n"
            f"{ICON_PRES} Pressione: {pres} hPa"
        )

        return msg

    except Exception as e:
        print(f"[ERRORE] Formattazione meteo fallita: {e}")
        return fallback_message

# -------------------------------------------------
# MESHTASTIC
# -------------------------------------------------

def send_message(iface, text):
    try:
        if destination_node:
            iface.sendText(text, destinationId=destination_node, channelIndex=channel_index)
            print(f"[INFO] Messaggio inviato a nodo {destination_node}:\n{text}")
        else:
            iface.sendText(text, channelIndex=channel_index)
            print(f"[INFO] Messaggio broadcast sul canale {channel_index} inviato:\n{text}")
    except Exception as e:
        print(f"[ERRORE] Invio messaggio fallito: {e}")
    finally:
        iface.close()


def on_connected(iface):
    print("[INFO] Connesso al dispositivo Meshtastic. Recupero meteo da WEATHER UNDERGROUND...")
    weather = get_weather_data()
    if weather:
        msg = format_weather_message(weather)
    else:
        msg = fallback_message
    send_message(iface, msg)

# -------------------------------------------------
# AVVIO
# -------------------------------------------------

try:
    if is_tcp:
        print(f"[INFO] Connessione TCP a {port}...")
        ip, tcp_port = port.split(":")
        interface = meshtastic.tcp_interface.TCPInterface(ip, int(tcp_port))
    else:
        print(f"[INFO] Connessione seriale su {port}...")
        interface = meshtastic.serial_interface.SerialInterface(port)
except Exception as e:
    print(f"[ERRORE] Connessione Meshtastic fallita: {e}")
    sys.exit(1)

if getattr(interface, "isConnected", False) or getattr(interface, "is_connected", False):
    on_connected(interface)
else:
    interface.onConnected = on_connected
