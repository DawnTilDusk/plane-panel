# Plane Panel 监控系统

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.10-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Plane Panel 监控系统** 是一个专为嵌入式工业应用设计的轻量级实时环境监控与视频流系统。它通过 Modbus RTU 采集传感器数据，并通过 Web 界面提供实时视频流。

## 🚀 功能特性

- **实时环境监测**：
  - 通过 RS485/串口采集 Modbus 传感器数据。
  - 监测指标：温度、湿度、VOC、PM2.5、PM10。
- **实时视频流**：
  - 使用 OpenCV 和 Motion JPEG (MJPEG) 实现低延迟视频传输。
  - 支持多个摄像头索引切换。
- **Web 仪表盘**：
  - 内置 Flask Web 服务器用于数据可视化。
  - 提供 REST API 接口以便数据集成。
- **历史数据**：
  - 维护最近传感器读数的滚动缓冲区，用于趋势分析。

## 📂 项目结构

```
Plane_Panel/
├── web_monitor/          # 核心应用源码
│   ├── app.py            # Flask 应用入口与逻辑
│   ├── requirements.txt  # Python 依赖列表
│   └── static/           # 前端资源 (HTML/CSS/JS)
├── configs/              # 配置文件
│   └── custom_frame_example.json
├── list_ports.py         # 列出可用 COM 端口的工具脚本
├── test.py               # Modbus 连接测试脚本
└── *.pdf                 # 硬件规格书与文档
```

## 🛠️ 安装与部署

### 环境要求
- **操作系统**: Windows (已测试) 或 Linux。
- **Python**: 版本 3.8 或更高。
- **硬件**:
  - Modbus RTU 传感器 (通过 USB-RS485 转接器连接)。
  - USB 摄像头或网络摄像头。

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/DawnTilDusk/plane-panel.git
   cd plane-panel
   ```

2. **安装依赖**
   ```bash
   pip install -r web_monitor/requirements.txt
   ```

## 🖥️ 使用说明

1. **检查 COM 端口**
   运行工具脚本以查找传感器的 COM 端口：
   ```bash
   python list_ports.py
   ```

2. **配置端口 (可选)**
   默认情况下，程序使用 `COM12`。如果您的设备连接在其他端口，请修改 `web_monitor/app.py`：
   ```python
   # 第 132 行
   kwargs={"port": "YOUR_COM_PORT", ...}
   ```

3. **启动服务器**
   ```bash
   python web_monitor/app.py
   ```
   服务器将启动在 `http://0.0.0.0:5000`。

4. **访问仪表盘**
   打开浏览器并访问 `http://localhost:5000`。

## 🔌 API 接口

- **`GET /`**: 主仪表盘页面。
- **`GET /video_feed?index=<id>`**: MJPEG 视频流 (默认 index=2)。
- **`GET /api/readings`**: 返回最新的传感器数据 (JSON)。
- **`GET /api/history`**: 返回最近 100 个数据点 (JSON)。

## 🤝 参与贡献

欢迎提交贡献！请遵循以下步骤：
1. Fork 本仓库。
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 开启一个 Pull Request。

## 📄 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
