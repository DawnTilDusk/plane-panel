import threading, time, json
from typing import Dict
from flask import Flask, Response, jsonify, request, send_from_directory
import serial
from collections import deque
import cv2

app = Flask(__name__, static_folder="static", static_url_path="/static")

latest: Dict[str, float] = {
    "temp": None,
    "humi": None,
    "voc": None,
    "pm25": None,
    "pm10": None,
    "ok": False,
    "msg": "init",
}
history = deque(maxlen=100)

def crc16(d: bytes) -> int:
    c = 0xFFFF
    for b in d:
        c ^= b
        for _ in range(8):
            c = (c >> 1) ^ 0xA001 if c & 1 else c >> 1
    return c & 0xFFFF

def modbus_poll(port: str = "COM12", baud: int = 9600, interval: float = 1.0):
    ser = None
    while True:
        try:
            if ser is None or not ser.is_open:
                ser = serial.Serial(port, baudrate=baud, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
                latest.update({"msg": f"serial opened {port}", "ok": True})
            pdu = bytes([1, 0x04, 0x00, 0x00, 0x00, 0x07])
            c = crc16(pdu)
            req = pdu + bytes([c & 0xFF, (c >> 8) & 0xFF])
            ser.reset_input_buffer()
            ser.write(req)
            ser.flush()
            time.sleep(0.05)
            r = ser.read(64)
            if len(r) >= 19 and r[0] == 1 and r[1] == 0x04 and r[2] == 14:
                rc = r[-2] | (r[-1] << 8)
                if rc == crc16(r[:-2]):
                    vals = [(r[i] << 8) | r[i + 1] for i in range(3, 17, 2)]
                    latest.update({
                        "temp": vals[0] / 10.0,
                        "humi": vals[1] / 10.0,
                        "voc": vals[2],
                        "pm25": vals[5],
                        "pm10": vals[6],
                        "ok": True,
                        "msg": "ok",
                    })
                    history.append({
                        "ts": time.time(),
                        "temp": latest["temp"],
                        "humi": latest["humi"],
                        "voc": latest["voc"],
                        "pm25": latest["pm25"],
                        "pm10": latest["pm10"],
                    })
                else:
                    latest.update({"ok": False, "msg": "crc_err"})
            else:
                latest.update({"ok": False, "msg": "no_reply"})
        except Exception as e:
            latest.update({"ok": False, "msg": str(e)})
            try:
                if ser:
                    ser.close()
            except Exception:
                pass
            ser = None
            time.sleep(1)
        time.sleep(interval)

def gen_frames(index: int = 0):
    cap = None
    last_err = None
    while cap is None:
        try:
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if not cap.isOpened():
                cap.release()
                cap = None
                index += 1
                if index > 5:
                    index = 0
                time.sleep(0.5)
        except Exception as e:
            last_err = e
            time.sleep(0.5)
    while True:
        ok, frame = cap.read()
        if not ok:
            cap.release()
            cap = None
            return Response(status=503)
        _, buf = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/video_feed")
def video_feed():
    idx = int(request.args.get("index", "2"))
    return Response(gen_frames(idx), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/api/readings")
def api_readings():
    return jsonify(latest)

@app.route("/api/history")
def api_history():
    ts = [x["ts"] for x in history]
    return jsonify({
        "ts": ts,
        "temp": [x["temp"] for x in history],
        "humi": [x["humi"] for x in history],
        "voc": [x["voc"] for x in history],
        "pm25": [x["pm25"] for x in history],
        "pm10": [x["pm10"] for x in history],
    })

def start_threads():
    t = threading.Thread(target=modbus_poll, kwargs={"port": "COM12", "baud": 9600, "interval": 1.0}, daemon=True)
    t.start()

if __name__ == "__main__":
    start_threads()
    app.run(host="0.0.0.0", port=5000, debug=False)
