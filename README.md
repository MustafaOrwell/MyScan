MyScan - Modbus Scanner v1.0.1
Author: Mustafa AYDIN

1️⃣ Purpose and Scope
MyScan is a Modbus TCP client application designed for:

Industrial automation engineers

Protocol developers

Control system integration engineers

Educational purposes

It enables users to:

Connect to Modbus TCP devices

Read and write data from/to various Modbus register types

Perform continuous periodic data acquisition with stability

Analyze and decode raw Modbus data into multiple formats

The project is developed as a professional-grade engineering tool with a focus on scalability, modular architecture, and field usability.

2️⃣ System Architecture
2.1 High Level Modules
Module	Description
main.py	User interface (PyQt5 GUI)
modbus_tcp.py	Modbus protocol layer

2.2 System Flow Diagram
pgsql
Copy
Edit
User Inputs (IP, Port, UnitID, Address, Count, Register Type, Data Type)
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
  Optional Periodic Auto-Read via Timer
3️⃣ Algorithmic Flow (Core Logic)
3.1 main.py — User Interface Layer
3.1.1 PyQt5 Components Used
QMainWindow → Application window

QVBoxLayout, QHBoxLayout → Layout design

QLineEdit, QLabel, QComboBox → User inputs

QPushButton → Action triggers

QTableWidget → Data display table

QTimer → Periodic data acquisition

3.1.2 Primary Functions
Function	Role
toggle_connection()	Connect / Disconnect toggle
connect_to_modbus()	Establish Modbus TCP connection
read_data()	Perform single read
start_auto_read()	Start timer-based continuous reading
stop_auto_read()	Stop periodic reading safely
write_data()	Perform write operations (single/multiple)
decode_value()	Decode raw Modbus data to user-selected format

3.2 modbus_tcp.py — Modbus Communication Layer
3.2.1 Core Functions
Function	Description
read_registers_by_type()	Read Holding, Input, Coil, Discrete
write_single_register()	Write single holding register
write_single_coil()	Write single coil (bit output)
write_multiple_registers()	Write multiple holding registers

3.2.2 Communication Logic
python
Copy
Edit
client = ModbusTcpClient(host=ip, port=port)
client.connect()
response = client.read_holding_registers(address=address, count=count, slave=unit_id)
client.close()
4️⃣ Data Parsing and Decoding Logic
4.1 Register Type Mapping
Register Type	Modbus Command Used
Holding	read_holding_registers()
Input	read_input_registers()
Coil	read_coils()
Discrete	read_discrete_inputs()

4.2 Data Type Decoding Logic
DataType	Parsing Algorithm
Int	16-bit signed integer
UInt	16-bit unsigned integer
Hex	Hexadecimal display
Binary	Binary format
ASCII	Single byte ASCII character
Float	2 words (32-bit IEEE 754 float), Little Endian
Double	4 words (64-bit IEEE 754 double), Big Endian

Example (Float Parsing):
python
Copy
Edit
b = struct.pack('<HH', data[index], data[index + 1])
float_value = struct.unpack('<f', b)[0]
Example (Double Parsing):
python
Copy
Edit
b = struct.pack('>HHHH', data[index], data[index+1], data[index+2], data[index+3])
double_value = struct.unpack('>d', b)[0]
5️⃣ Error Handling and Stability
All communication is wrapped with try-except error handling blocks.

Every read/write operation checks connection validity before proceeding.

The auto-read timer is safely stopped upon any connection or protocol failure.

Disconnect operation automatically cancels ongoing read cycles for full stability.

6️⃣ Engineering Design Principles
Modular Architecture: GUI and protocol layers are completely separated.

Minimal Dependency: Only pymodbus and PyQt5 are required.

Stable Runtime: Automatic recovery from communication failures.

Clean Code: Clear function separation and naming.

Protocol Compliance: Strict adherence to Modbus TCP standards.

7️⃣ Future Planned Enhancements (Next Versions)
In upcoming professional versions, following features are targeted to be implemented:

🔧 Connection Management
IP address history: Store previously connected IP addresses.

Dropdown selector for saved connections.

🔧 UI Enhancement
Address & Quantity inputs will allow multi-column read instead of simple list view.

More advanced visualization of bit-level data:

When reading Coils → display per-bit states directly.

When selecting Binary → display entire register as individual bits.

🔧 Execution Mode
Full packaging into a standalone Windows/Linux executable (.exe/.app) via PyInstaller.

🔧 Professional Grade Features
Logging system for communication monitoring.

Export/Import of read data (CSV, JSON support).

Word Swap / Endian toggle selection directly from GUI.

Real-time live data chart visualization.

Goal:
MyScan will gradually evolve into a full-featured, professional-grade, field-usable Modbus diagnostic and testing tool suitable for real-world industrial deployment.

8️⃣ Installation
8.1 Python Dependencies
bash
Copy
Edit
pip install pymodbus pyqt5
8.2 Environment
Python 3.8 or above

Fully cross-platform (Windows / Linux supported)

9️⃣ Project Directory Structure
bash
Copy
Edit
my_scan_project/
│
├── main.py           # User interface and application logic
├── core/
│   └── modbus_tcp.py # Communication protocol layer
└── README.md         # This technical documentation
10️⃣ Summary Logic Flow
User provides input parameters.

Modbus TCP connection is established.

Read/Write operations are executed via modbus_tcp.py.

Data is decoded into appropriate formats.

Results are displayed in real-time table view.

System maintains full runtime safety on connection loss or protocol exceptions.

⚠ Engineering Note
This project is intentionally designed as an educational and scalable industrial communication client platform.
The codebase, architecture, and algorithms are directly applicable to real-world SCADA, PLC, and automation test systems.

