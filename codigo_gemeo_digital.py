# Estrutura de Código para Projeto de Gêmeo Digital com ESP32 + SCADA + Python

# Diretório do Projeto:
# projeto_gemeo_digital/
# ├── arduino/
# │   ├── esp32_sensores.ino
# ├── python_gateway/
# │   ├── main_gateway.py
# │   └── modbus_client.py
# ├── web/
# │   └── app_flask.py
# ├── scadaBR/
# │   └── configuracao_datasource.txt
# └── README.md

# === arduino/esp32_sensores.ino ===
/* ESP32 com sensores DS18B20, KY-038 e MPU-6050 */
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <MPU6050.h>

#define ONE_WIRE_BUS 5
#define KY038_PIN 4

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  sensors.begin();
  Wire.begin();
  mpu.initialize();
}

void loop() {
  sensors.requestTemperatures();
  float temp = sensors.getTempCByIndex(0);

  int sound = analogRead(KY038_PIN);

  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  Serial.print("TEMP:"); Serial.print(temp);
  Serial.print(",SOUND:"); Serial.print(sound);
  Serial.print(",AX:"); Serial.print(ax);
  Serial.print(",AY:"); Serial.print(ay);
  Serial.print(",AZ:"); Serial.println(az);

  delay(1000);
}

# === python_gateway/main_gateway.py ===
import time
from modbus_client import ModbusGateway

gateway = ModbusGateway()

while True:
    data = gateway.read_data()
    gateway.store_to_db(data)
    time.sleep(5)

# === python_gateway/modbus_client.py ===
from pymodbus.client.sync import ModbusSerialClient
import psycopg2

class ModbusGateway:
    def __init__(self):
        self.client = ModbusSerialClient(port='/dev/ttyUSB0', baudrate=9600, method='rtu', timeout=1)
        self.conn = psycopg2.connect("dbname=gemeo user=admin password=admin")

    def read_data(self):
        result = self.client.read_input_registers(0, 6, unit=1)
        return result.registers if result.isError() is False else []

    def store_to_db(self, data):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO dados_modbus (reg1, reg2, reg3, reg4, reg5, reg6) VALUES (%s,%s,%s,%s,%s,%s)", tuple(data))
            self.conn.commit()

# === web/app_flask.py ===
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    conn = psycopg2.connect("dbname=gemeo user=admin password=admin")
    cur = conn.cursor()
    cur.execute("SELECT * FROM dados_modbus ORDER BY id DESC LIMIT 10")
    data = cur.fetchall()
    return str(data)

if __name__ == '__main__':
    app.run(debug=True)

# === scadaBR/configuracao_datasource.txt ===
"""
- Data Source: Modbus Serial
- Baudrate: 9600
- Timeout: 2.5s
- Endereço do dispositivo: 1
- Data Points:
  - Temperatura Motor: Registro 0
  - Nível de Ruído: Registro 1
  - Vibração X: Registro 2
  - Vibração Y: Registro 3
  - Vibração Z: Registro 4
- Alarmes:
  - Temperatura > 75ºC
  - Som > 85 dB
  - Vibração X,Y > 2.5 m/s²
"""

# === README.md ===
"""
# Projeto de Gêmeo Digital para Monitoramento de Motores Elétricos
Este projeto integra sensores com ESP32, comunicação via Modbus, armazenamento PostgreSQL/TimescaleDB e visualização com Grafana.

## Componentes
- ESP32
- Sensores: DS18B20, KY-038, MPU-6050
- Inversor de Frequência WEG CFW-08
- Python com Flask e Pymodbus
- SCADA: ScadaBR
- Banco de Dados: PostgreSQL + TimescaleDB
"""
