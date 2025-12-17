from serial.tools import list_ports
import serial

for p in list_ports.comports():
    status = ""
    try:
        s = serial.Serial(p.device, timeout=0.5)
        s.close()
        status = "OK"
    except Exception as e:
        status = f"ERR: {e}"
    print(f"{p.device}\t{p.description}\t{status}")
