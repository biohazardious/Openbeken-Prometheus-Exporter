# OpenBeken Prometheus Exporter

This project provides a lightweight Prometheus exporter for [OpenBeken](https://github.com/openshwprojects/OpenBK7231T_App) smart devices that emulate Tuya smart plug metrics.

Metrics are exported in the format compatible with [`tuya-smartplug-exporter`](https://github.com/rkfg/tuya-smartplug-exporter), allowing easy integration with existing Prometheus setups and Grafana dashboards.

---

## 🔧 Features

- 🧠 Exposes power, voltage, current, and energy metrics per plug.
- 📁 YAML config for multiple devices.
- 🐳 Docker and Docker Compose support.
- 🔌 Tuya-style metrics like `tuya_power`, `tuya_voltage`, etc.

---

## 📦 Example Metrics

tuya_power{plug="plug_livingroom"} 18.5 tuya_voltage{plug="plug_livingroom"} 231.3 tuya_current{plug="plug_livingroom"} 0.08 tuya_energy_total{plug="plug_livingroom"} 12.8

---

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/biohazardious/Openbeken-Prometheus-Exporter.git
cd Openbeken-Prometheus-Exporter

2. Edit config.yaml

devices:
  - name: plug_livingroom
    ip: 192.168.1.100
  - name: plug_bedroom
    ip: 192.168.1.101

3. Start with Docker Compose

docker compose up -d --build

The metrics endpoint will be available at:

http://localhost:9345/metrics


---

📈 Prometheus Scrape Config

scrape_configs:
  - job_name: 'openbeken'
    static_configs:
      - targets: ['your-host-ip:9345']


---

🔧 Advanced

Add more devices

Just edit config.yaml, then restart the container:

docker compose restart
