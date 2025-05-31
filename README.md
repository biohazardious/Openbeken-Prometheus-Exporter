# 🔌 OpenBeken Prometheus Exporter

This project is a lightweight Prometheus exporter that collects real-time metrics from **OpenBeken-based smart plugs** and exposes them in Prometheus-compatible format for monitoring and visualization via Grafana or similar tools.
Metrics data is compatible with Gizex's Tuya dashboard. (https://grafana.com/grafana/dashboards/23018-power/)

---

## 📈 Metrics Exported

| Metric Name                     | Description                                         |
|--------------------------------|-----------------------------------------------------|
| `tuya_smartplug_power`         | Instantaneous power usage in watts (W)             |
| `tuya_smartplug_voltage`       | Voltage in volts (V)                                |
| `tuya_smartplug_current`       | Current in milliamps (mA)                           |
| `tuya_smartplug_switch_on`     | Device state (1 = ON, 0 = OFF)                      |
| `tuya_smartplug_power_kwh_day` | Estimated energy usage per day in kilowatt-hours    |

---

## ⚙️ Configuration

Edit the `config.yaml` file to define your smart plugs:

```yaml
devices:
  - name: plug_livingroom
    ip: 192.168.1.10
  - name: plug_kitchen
    ip: 192.168.1.11

🚀 Quick Start with Docker Compose
1. Clone the Repository

git clone https://github.com/biohazardious/Openbeken-Prometheus-Exporter.git
cd Openbeken-Prometheus-Exporter

2. Run with Docker Compose

docker compose up --build -d

The exporter will be accessible at:

http://localhost:9345/metrics

📡 Prometheus Integration

Add the following job to your prometheus.yml:

scrape_configs:
  - job_name: 'openbeken_smartplugs'
    static_configs:
      - targets: ['host.docker.internal:9345']

Or if Prometheus is running in the same Docker network:

      - targets: ['openbeken-exporter:9345']

🐳 Dockerfile

The project includes a minimal Dockerfile using Python 3.11 slim:

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "exporter.py"]

📦 Requirements

    Python 3.11+

    Prometheus

    Docker + Docker Compose

🔄 CI/CD

You can configure GitHub Actions to build and push Docker images to Docker Hub automatically using GitOps workflows and a Personal Access Token (PAT).
🧑‍💻 Author

Created with ❤️ by @biohazardious
