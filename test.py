import time,serial

def crc16(d):
    c=0xFFFF
    for b in d:
        c^=b
        for _ in range(8):
            c=(c>>1)^0xA001 if c&1 else c>>1
    return c

s=serial.Serial('COM12',9600,timeout=1,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)

while True:
    time.sleep(1)
    req=bytes.fromhex('01 04 00 00 00 07 B1 C8')
    s.write(req); s.flush()
    r=s.read(64)
    if len(r)>=19 and r[0]==1 and r[1]==0x04 and r[2]==14:
        recv_crc=r[-2]|(r[-1]<<8)
        if recv_crc==crc16(r[:-2]):
            vals=[(r[i]<<8)|r[i+1] for i in range(3,17,2)]
            temp=vals[0]/10.0
            humi=vals[1]/10.0
            voc=vals[2]
            pm25=vals[5]
            pm10=vals[6]
            print(f"TEMP={temp}℃ HUMI={humi}% VOC={voc} PM2.5={pm25}ug/m3 PM10={pm10}ug/m3")
        else:
            print("crc_err",r.hex())
    else:
        print(r.hex())
