import meshtastic # ***** installare con pip install meshtastic
import meshtastic.serial_interface
import meshtastic.tcp_interface
import sys
import platform
import requests
import json
from datetime import datetime
import pytz # ***** installare con pip install pytz


# CONFIGURAZIONE

# Porta seriale (Windows es: "COM3"), oppure indirizzo TCP "ip:porta" (meshtastic usa la porta 4403/TCP)
port = "COM4"  # oppure "/dev/ttyUSB0" per Linux oppure per network "192.168.1.199:4403" 
is_tcp = False # True per gestire la connessione via rete

# Coordinate geografiche per i dati meteo
latitude  = 44.1234567
longitude = 11.1234567
luogo = "Scrivi qui il nome della città" # per il messaggio, usato per descrivere il luogo delle coordinate

# Quali dati meteo includere: opzioni possibili: temperature_2m, relative_humidity_2m, wind_speed_10m, precipitation, etc.
desired_hourly = ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"]

# Meshtastic: destinazione e canale
destination_node = None # esempio: "!06c7fb0c", per un messaggio broadcast (all'intero canale) indicare None
channel_index    = 1    # nella mia configurazione il canale 1 è la Toscana

# Messaggio base in caso di fallback
fallback_message = "Nessun dato meteo disponibile."

# Recupera dati meteo da Open-Meteo
def get_weather(lat, lon, hourly_vars):
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(hourly_vars),
        "current_weather": True,
        "timezone": "auto"
    }

    try:
        r = requests.get(base_url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data
    except Exception as e:
        print(f"[ERRORE] Chiamata Open-Meteo fallita: {e}")
        return None

# Costruisci messaggio dal JSON meteo
def format_weather_message(data):
    try:
        cw = data.get("current_weather", {})
        # time = cw.get("time") se vuoi usare il generico
        temp = cw.get("temperature")
        wind = cw.get("windspeed")
        
        # Orario corrente in Italia
        tz = pytz.timezone("Europe/Rome")
        now = datetime.now(tz)
        time_str = now.strftime("%d/%m/%Y %H:%M:%S")
        
        msg = f"{luogo}\nMeteo attuale alle {time_str}:\nTemperatura: {temp}°C\nVento: {wind} km/h\n"
        return msg
    except Exception as e:
        print(f"[ERRORE] Formattazione meteo fallita: {e}")
        return fallback_message

# Invio messaggio verso Meshtastic
def send_message(iface, text):
    try:
        if destination_node:
            iface.sendText(text, destinationId=destination_node, channelIndex=channel_index)
            print(f"[INFO] Messaggio inviato a nodo {destination_node}:\n{text}")
        else:
            iface.sendText(text, channelIndex=channel_index)
            print(f"[INFO] Messaggio broadcast inviato:\n{text}")
    except Exception as e:
        print(f"[ERRORE] Invio messaggio fallito: {e}")
    finally:
        print("[INFO] Chiusura connessione Meshtastic...")
        iface.close()

# Connesso, recupera i dati
def on_connected(iface):
    print("[INFO] Connesso al dispositivo Meshtastic. Recupero meteo...")
    weather = get_weather(latitude, longitude, desired_hourly)
    if weather:
        msg = format_weather_message(weather)
    else:
        msg = fallback_message
    send_message(iface, msg)

# AVVIO: connessione Meshtastic
try:
    if is_tcp:
        print(f"[INFO] Connessione via rete a {port}...")
        ip, tcp_port = port.split(":")
        interface = meshtastic.tcp_interface.TCPInterface(ip, int(tcp_port))
    else:
        print(f"[INFO] Connessione seriale su {port}...")
        interface = meshtastic.serial_interface.SerialInterface(port)
except Exception as e:
    print(f"[ERRORE] Impossibile connettersi a Meshtastic: {e}")
    sys.exit(1)

if getattr(interface, "isConnected", False) or getattr(interface, "is_connected", False):
    on_connected(interface)
else:
    interface.onConnected = on_connected
