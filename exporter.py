from flask import Flask, Response
import requests
import yaml
import time
from prometheus_client import Gauge, generate_latest
from threading import Lock

app = Flask(__name__)
lock = Lock()

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Prometheus Gauges, labeled by plug name
g_power = Gauge('tuya_power', 'Current power consumption in W', ['plug'])
g_voltage = Gauge('tuya_voltage', 'Voltage in V', ['plug'])
g_current = Gauge('tuya_current', 'Current in A', ['plug'])
g_energy = Gauge('tuya_energy_total', 'Total energy consumption in kWh', ['plug'])

@app.route('/metrics')
def metrics():
    with lock:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting metrics collection...")
        for dev in config.get("devices", []):
            name = dev.get("name")
            ip = dev.get("ip")

            print(f"→ Querying device: {name} @ {ip}")
            try:
                url = f"http://{ip}/cm?cmnd=Status%208"
                res = requests.get(url, timeout=3)
                res.raise_for_status()

                data = res.json().get("StatusSNS", {})

                power = float(data.get("Power", 0))
                voltage = float(data.get("Voltage", 0))
                current = float(data.get("Current", 0))
                energy = float(data.get("EnergyTotal", 0))

                g_power.labels(plug=name).set(power)
                g_voltage.labels(plug=name).set(voltage)
                g_current.labels(plug=name).set(current)
                g_energy.labels(plug=name).set(energy)

                print(f"  ✓ Success: Power={power}W, Voltage={voltage}V, Current={current}A, Energy={energy}kWh")

            except Exception as e:
                print(f"  ✗ Error querying {name} ({ip}): {e}")

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Metrics collection finished.\n")
        return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    print("🔌 OpenBeken Exporter starting up...")
    app.run(host='0.0.0.0', port=9345)
