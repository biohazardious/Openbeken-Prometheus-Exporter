from flask import Flask, Response
import requests
import yaml
import time
from prometheus_client import Gauge, generate_latest
from threading import Lock

app = Flask(__name__)
lock = Lock()

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Prometheus Metrics
g_power = Gauge("tuya_smartplug_power", "Total power used, in Watts", ["device"])
g_voltage = Gauge("tuya_smartplug_voltage", "Electrical voltage, in Volts", ["device"])
g_current = Gauge("tuya_smartplug_current", "Current in milliamps", ["device"])
g_switch = Gauge("tuya_smartplug_switch_on", "Switch state (1=on, 0=off)", ["device"])
g_kwh_day = Gauge("tuya_smartplug_power_kwh_day", "Projected power consumption in kWh per day", ["device"])

@app.route("/metrics")
def metrics():
    with lock:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting metrics scrape...")

        for dev in config.get("devices", []):
            name = dev.get("name")
            ip = dev.get("ip")

            print(f"→ Querying device: {name} @ {ip}")
            try:
                status_url = f"http://{ip}/cm?cmnd=Status%208"
                power_url = f"http://{ip}/cm?cmnd=Power"

                # Status 8 for sensor data
                res = requests.get(status_url, timeout=5)
                res.raise_for_status()
                sensor_data = res.json().get("StatusSNS", {}).get("ENERGY", {})

                power_w = float(sensor_data.get("Power", 0))
                voltage = float(sensor_data.get("Voltage", 0))
                current_a = float(sensor_data.get("Current", 0))
                total_kwh = float(sensor_data.get("EnergyTotal", 0))

                # Assume daily kWh = total_kwh * 24 / uptime hours
                # Alternative simple estimation
                kwh_day = round((power_w * 24.0) / 1000.0, 4) if power_w else 0

                # Power state
                power_res = requests.get(power_url, timeout=3)
                power_res.raise_for_status()
                state_data = power_res.json().get("POWER", "").upper()
                state = 1 if state_data == "ON" else 0

                # Set Prometheus metrics
                g_power.labels(device=name).set(power_w)
                g_voltage.labels(device=name).set(voltage)
                g_current.labels(device=name).set(current_a * 1000)  # amps to milliamps
                g_switch.labels(device=name).set(state)
                g_kwh_day.labels(device=name).set(kwh_day)

                print(f"  ✓ {name}: {power_w}W, {voltage}V, {current_a}A, State={'ON' if state else 'OFF'}, Day Est={kwh_day}kWh")

            except Exception as e:
                print(f"  ✗ Error reading {name}: {e}")

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scrape finished.\n")
        return Response(generate_latest(), mimetype="text/plain")

if __name__ == "__main__":
    print("🔌 OpenBeken Prometheus Exporter starting on port 9345...")
    app.run(host="0.0.0.0", port=9345)
