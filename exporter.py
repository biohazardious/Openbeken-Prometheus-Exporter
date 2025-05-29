from flask import Flask, Response
import requests, yaml
from prometheus_client import Gauge, generate_latest
from threading import Lock

app = Flask(__name__)
lock = Lock()

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Prometheus Gauges, one per metric, distinguished by plug name
g_power = Gauge('tuya_power', 'Current power consumption in W', ['plug'])
g_voltage = Gauge('tuya_voltage', 'Voltage in V', ['plug'])
g_current = Gauge('tuya_current', 'Current in A', ['plug'])
g_energy = Gauge('tuya_energy_total', 'Total energy consumption in kWh', ['plug'])

@app.route('/metrics')
def metrics():
    with lock:
        for dev in config.get("devices", []):
            name = dev.get("name")
            ip = dev.get("ip")
            try:
                url = f"http://{ip}/cm?cmnd=Status%208"
                res = requests.get(url, timeout=2)
                data = res.json().get("StatusSNS", {})

                g_power.labels(plug=name).set(float(data.get("Power", 0)))
                g_voltage.labels(plug=name).set(float(data.get("Voltage", 0)))
                g_current.labels(plug=name).set(float(data.get("Current", 0)))
                g_energy.labels(plug=name).set(float(data.get("EnergyTotal", 0)))

            except Exception as e:
                print(f"Failed to fetch from {name} ({ip}): {e}")

        return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9345)
