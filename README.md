# Plane Panel Monitor

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Plane Panel Monitor** is a lightweight, real-time environmental monitoring and video streaming system designed for embedded industrial applications. It collects sensor data via Modbus RTU and streams video feeds via a web interface.

## 🚀 Features

- **Real-time Environmental Monitoring**:
  - Collects data from Modbus sensors via RS485/Serial.
  - Metrics: Temperature, Humidity, VOC, PM2.5, PM10.
- **Live Video Streaming**:
  - Low-latency video feed using OpenCV and Motion JPEG (MJPEG).
  - Supports multiple camera indices.
- **Web Dashboard**:
  - Built-in Flask web server for visualization.
  - REST API endpoints for data integration.
- **Data History**:
  - Maintains a rolling buffer of recent sensor readings for trend analysis.

## 📂 Project Structure

```
Plane_Panel/
├── web_monitor/          # Main application source code
│   ├── app.py            # Flask application entry point & logic
│   ├── requirements.txt  # Python dependencies
│   └── static/           # Frontend assets (HTML/CSS/JS)
├── configs/              # Configuration files
│   └── custom_frame_example.json
├── list_ports.py         # Utility to list available COM ports
├── test.py               # Standalone script for testing Modbus connection
└── *.pdf                 # Hardware specifications and documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- **OS**: Windows (tested) or Linux.
- **Python**: Version 3.8 or higher.
- **Hardware**:
  - Modbus RTU Sensor (connected via USB-RS485 adapter).
  - USB Camera or Web Camera.

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/DawnTilDusk/plane-panel.git
   cd plane-panel
   ```

2. **Install Dependencies**
   ```bash
   pip install -r web_monitor/requirements.txt
   ```

## 🖥️ Usage

1. **Check COM Ports**
   Run the utility script to find your sensor's COM port:
   ```bash
   python list_ports.py
   ```

2. **Configure Port (Optional)**
   By default, the application uses `COM12`. If your device is on a different port, modify `web_monitor/app.py`:
   ```python
   # Line 132
   kwargs={"port": "YOUR_COM_PORT", ...}
   ```

3. **Start the Server**
   ```bash
   python web_monitor/app.py
   ```
   The server will start at `http://0.0.0.0:5000`.

4. **Access Dashboard**
   Open your browser and navigate to `http://localhost:5000`.

## 🔌 API Endpoints

- **`GET /`**: Main dashboard.
- **`GET /video_feed?index=<id>`**: MJPEG video stream (default index=2).
- **`GET /api/readings`**: Returns the latest sensor data (JSON).
- **`GET /api/history`**: Returns the last 100 data points (JSON).

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
