# MyScan - Modbus Scanner v1.0.2  
**Author:** Mustafa AYDIN  

---

## 1️⃣ Purpose and Scope

**MyScan** is a professional Modbus TCP client application designed for:

- 🏭 Industrial automation engineers  
- 📡 Protocol developers  
- 🛠 Control system integrators  
- 🎓 Educational and diagnostic purposes  

### Key Features:

- Connect to Modbus TCP devices  
- Read and write from/to various Modbus register types (Holding, Input, Coil, Discrete)  
- Stable, continuous periodic data acquisition  
- Decode raw Modbus data into multiple formats (Int, UInt, Float, Double, Hex, Binary, ASCII)  
- **NEW:** Live real-time chart view for selected register  
- **NEW:** Targeted register selection for graphing  
- Modular and scalable structure ready for field deployment  

---

## 2️⃣ System Architecture

### 2.1 High-Level Modules

| Module                | Description                           |
|------------------------|---------------------------------------|
| `main.py`             | User interface (PyQt5 GUI)            |
| `core/modbus_tcp.py`  | Modbus TCP protocol communication     |
| `core/chart_window.py`| Live data chart window (PyQtGraph)    |
| `core/ip_history.py`  | Persistent IP connection memory       |

### 2.2 System Flow

```text
User Inputs (IP, Port, Unit ID, Address, Count, Register Type, Data Type)
        │
        ▼
Establish Modbus TCP Connection
        │
        ▼
Perform Read / Write Operations
        │
        ▼
Decode and Display Data (Table View)
        │
        ▼
[Optional] Periodic Auto-Read via Timer
        │
        ▼
[Optional] Live Chart View for Selected Address
3️⃣ Algorithmic Flow
3.1 main.py — User Interface Layer
PyQt5 Components Used:
QMainWindow, QVBoxLayout, QHBoxLayout

QLineEdit, QLabel, QComboBox, QPushButton, QTableWidget

QSpinBox, QTimer

Primary Functions:
Function	Role
toggle_connection()	Toggle connect/disconnect
connect_to_modbus()	Establish TCP connection
read_data()	Perform read and decode values
start_auto_read()	Enable periodic reading with QTimer
stop_auto_read()	Stop timer-based acquisition
decode_value()	Parse register values based on data type
write_data()	Perform register/coil writing
open_chart_window()	Launch separate chart window for live monitoring

3.2 modbus_tcp.py — Protocol Layer
Core Functions:
Function	Description
read_registers_by_type()	Generic read by register type
write_single_register()	Write to a single holding register
write_single_coil()	Write a coil bit
write_multiple_registers()	Write multiple registers (bulk write)

Example Logic:
python
Copy
Edit
client = ModbusTcpClient(host=ip, port=port)
client.connect()
response = client.read_holding_registers(address=address, count=count, slave=unit_id)
client.close()
4️⃣ Data Parsing and Decoding
4.1 Register Mapping Table
Register Type	Modbus Command Used	Address Offset
Holding	read_holding_registers()	40001
Input	read_input_registers()	30001
Coil	read_coils()	00001
Discrete	read_discrete_inputs()	10001

4.2 Data Format Decoding Logic
Data Type	Decoding Method
Int	16-bit signed integer
UInt	16-bit unsigned integer
Hex	hex(data[index])
Binary	format(data[index], '016b')
ASCII	chr(data[index] & 0xFF)
Float	struct.unpack('<f', struct.pack('<HH', ...))
Double	struct.unpack('>d', struct.pack('>HHHH', ...))

5️⃣ Error Handling & Stability
All Modbus operations are wrapped in try-except blocks

Connection checks are enforced before read/write

Auto-read stops immediately upon connection failure

Disconnection halts all timers and operations safely

User feedback via QMessageBox

6️⃣ Engineering Principles
Modular Design: Core logic separated from GUI

Minimal Dependencies: Only pymodbus, pyqt5, pyqtgraph

UI Scalability: Adaptive table layout

Clean Codebase: Naming conventions and logical functions

Protocol Compliance: Follows Modbus TCP standards

User Focus: Field-usable, minimal configuration

7️⃣ New Features in v1.0.2
✅ Live Chart View using PyQtGraph

✅ Target Register Selection for charting

✅ Chart Start/Stop Control

✅ Improved GUI layout (Chart button integrated to UI)

✅ Smart Register Address Mapping (e.g., 40001 offset)

⚠️ Chart now works only with selected target register (default: 0)

8️⃣ Installation Guide
8.1 Python Dependencies
bash
Copy
Edit
pip install pymodbus pyqt5 pyqtgraph
8.2 Environment
Python 3.8+

Cross-platform: Windows / Linux

9️⃣ Project Directory Structure
css
Copy
Edit
MyScan/
├── main.py
├── core/
│   ├── modbus_tcp.py
│   ├── chart_window.py
│   └── ip_history.py
├── README.md
├── requirements.txt
└── CHANGELOG.md
🔟 Logic Summary
User inputs connection and read parameters

Establish TCP connection to Modbus slave

Perform data read/write

Decode and display results in table

Optionally visualize live chart for selected address

Automatically stops reading on failure

⚠️ Engineering Note
MyScan is built for real-world industrial diagnostics and SCADA testing.
The design and source code are scalable and suitable for use with:

PLCs, RTUs, and field instruments

Simulation environments for protocol training

SCADA development and integration projects