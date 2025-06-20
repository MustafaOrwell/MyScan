# MyScan v1.0.2 - Custom Build
# Developed by Mustafa AYDIN for SAVRONIK

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt5.QtCore import QTimer
from pymodbus.client import ModbusTcpClient
import sys
import math
import struct
from core.ip_history import load_ip_history, save_ip_history
from core.modbus_tcp import (
    read_registers_by_type,
    write_single_register,
    write_single_coil,
    write_multiple_registers
)

class MyScan(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyScan - Modbus Scanner | Savronik")
        self.setGeometry(300, 150, 800, 550)
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_data)
        self.client = None
        self.initUI()
        self.statusBar().showMessage("by Mustafa AYDIN")

    def initUI(self):
        ip_label = QLabel("IP:")
        self.ip_combo = QComboBox()
        self.ip_combo.setEditable(True)
        self.ip_combo.addItems(load_ip_history())
        self.ip_combo.setCurrentText("127.0.0.1")
        port_label = QLabel("Port:")
        self.port_input = QLineEdit("502")
        unit_label = QLabel("Unit ID:")
        self.unit_input = QLineEdit("1")
        self.connect_button = QPushButton("Connect")
        self.connect_button.setObjectName("connect_button")
        self.connect_button.clicked.connect(self.toggle_connection)
        self.connect_button.setToolTip("Developed by Mustafa AYDIN - Savronik")

        ip_port_layout = QVBoxLayout()
        ip_port_layout.addWidget(ip_label)
        ip_port_layout.addWidget(self.ip_combo)
        ip_port_layout.addWidget(port_label)
        ip_port_layout.addWidget(self.port_input)
        ip_port_layout.addWidget(unit_label)
        ip_port_layout.addWidget(self.unit_input)
        ip_port_layout.addWidget(self.connect_button)

        address_label = QLabel("Start Address:")
        self.address_input = QLineEdit("0")
        count_label = QLabel("Quantity:")
        self.count_input = QLineEdit("10")

        address_layout = QVBoxLayout()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input)
        address_layout.addWidget(count_label)
        address_layout.addWidget(self.count_input)

        regtype_label = QLabel("Register Type:")
        self.regtype_combo = QComboBox()
        self.regtype_combo.addItems(["Holding", "Input", "Coil", "Discrete"])

        datatype_label = QLabel("Data Type:")
        self.datatype_combo = QComboBox()
        self.datatype_combo.addItems(["Int", "UInt", "Float", "Double", "Hex", "Binary", "ASCII"])

        options_layout = QVBoxLayout()
        options_layout.addWidget(regtype_label)
        options_layout.addWidget(self.regtype_combo)
        options_layout.addWidget(datatype_label)
        options_layout.addWidget(self.datatype_combo)

        top_layout = QHBoxLayout()
        top_layout.addLayout(address_layout)
        top_layout.addStretch()
        top_layout.addLayout(options_layout)
        top_layout.addStretch()
        top_layout.addLayout(ip_port_layout)

        self.read_button = QPushButton("Start Read")
        self.read_button.setObjectName("read_button")
        self.read_button.clicked.connect(self.start_auto_read)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stop_button")
        self.stop_button.clicked.connect(self.stop_auto_read)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.read_button)
        button_layout.addWidget(self.stop_button)

        self.table = QTableWidget()
       
        self.write_label = QLabel("Write Address:")
        self.write_address = QLineEdit()
        self.value_label = QLabel("Write Value(s):")
        self.write_value = QLineEdit()
        self.write_type_label = QLabel("Write Type:")
        self.write_type_combo = QComboBox()
        self.write_type_combo.addItems(["Register", "Coil", "Multiple Register"])
        self.write_button = QPushButton("Write")
        self.write_button.setObjectName("write_button")
        self.write_button.clicked.connect(self.write_data)

        write_layout = QHBoxLayout()
        write_layout.addWidget(self.write_label)
        write_layout.addWidget(self.write_address)
        write_layout.addWidget(self.value_label)
        write_layout.addWidget(self.write_value)
        write_layout.addWidget(self.write_type_label)
        write_layout.addWidget(self.write_type_combo)
        write_layout.addWidget(self.write_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(write_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""
            QMainWindow { background-color: #f0f2f5; }
            QLabel { font-weight: bold; }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QPushButton {
                padding: 6px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton#connect_button { background-color: #4CAF50; color: white; }
            QPushButton#stop_button { background-color: #e74c3c; color: white; }
            QPushButton#read_button { background-color: #3498db; color: white; }
            QPushButton#write_button { background-color: #f39c12; color: white; }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f2f2f2;
                gridline-color: #dcdcdc;
            }
            QHeaderView::section {
                background-color: #dfe4ea;
                font-weight: bold;
                border: 1px solid #cfd8dc;
                padding: 4px;
            }
        """)

    def toggle_connection(self):
        if self.client and self.client.connected:
            self.client.close()
            self.client = None
            self.connect_button.setText("Connect")
            QMessageBox.information(self, "Disconnected", "Connection closed.")
            self.stop_auto_read()
        else:
            self.connect_to_modbus()

    def connect_to_modbus(self):
        ip = self.ip_combo.currentText()
        save_ip_history(ip)
        port = int(self.port_input.text())
        try:
            self.client = ModbusTcpClient(host=ip, port=port)
            if self.client.connect():
                QMessageBox.information(self, "Connection", f"Connected to {ip}:{port}")
                self.connect_button.setText("Disconnect")
            else:
                QMessageBox.critical(self, "Connection Failed", f"Could not connect to {ip}:{port}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def start_auto_read(self):
        if not self.client or not self.client.connect():
            QMessageBox.warning(self, "Connection Error", "Modbus connection could not be established.")
            return
        self.read_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.timer.start(3000)

    def stop_auto_read(self):
        if self.timer.isActive():
            self.timer.stop()
        self.read_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    def read_data(self):
        try:
            ip = self.ip_combo.currentText()
            port = int(self.port_input.text())
            unit_id = int(self.unit_input.text())
            address = int(self.address_input.text())
            count = int(self.count_input.text())
            datatype = self.datatype_combo.currentText()
            register_type = self.regtype_combo.currentText()
    
            result = read_registers_by_type(ip, port, unit_id, address, count, register_type)
            self.table.setRowCount(0)
    
            # Register tipi bazlı Modbus offset başlangıcı
            if register_type == "Holding":
                base_offset = 40001
            elif register_type == "Input":
                base_offset = 30001
            elif register_type == "Coil":
                base_offset = 1
            elif register_type == "Discrete":
                base_offset = 10001
            else:
                base_offset = 0
    
            if isinstance(result, list):
                # --- BINARY GÖRÜNÜM ---
                if datatype == "Binary":
                    self.table.setColumnCount(17)
                    headers = ["Address"] + [f"Bit {15 - i}" for i in range(16)]
                    self.table.setHorizontalHeaderLabels(headers)
                    self.table.setRowCount(len(result))
    
                    for row, val in enumerate(result):
                        modbus_address = base_offset + address + row
                        self.table.setItem(row, 0, QTableWidgetItem(str(modbus_address)))
                        bit_str = format(val, '016b')
                        for col, bit in enumerate(bit_str):
                            self.table.setItem(row, col + 1, QTableWidgetItem(bit))
                else:
                    # --- STANDART VERİ TİPLERİ ---
                    pair_per_row = 3
                    row_count = math.ceil(len(result) / pair_per_row)
                    self.table.setColumnCount(pair_per_row * 2)
                    self.table.setRowCount(row_count)
    
                    headers = []
                    for i in range(pair_per_row):
                        headers.append(f"Address {i+1}")
                        headers.append(f"Value {i+1}")
                    self.table.setHorizontalHeaderLabels(headers)
    
                    for idx, val in enumerate(result):
                        row = idx // pair_per_row
                        col = (idx % pair_per_row) * 2
    
                        modbus_address = base_offset + address + idx
                        value_str = self.decode_value(result, idx, datatype)
    
                        self.table.setItem(row, col, QTableWidgetItem(str(modbus_address)))
                        self.table.setItem(row, col + 1, QTableWidgetItem(str(value_str)))
            else:
                QMessageBox.warning(self, "Read Failed", str(result))
                self.stop_auto_read()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
            self.stop_auto_read()

    def decode_value(self, data, index, datatype):
        try:
            if datatype == "Int":
                return data[index]
            elif datatype == "UInt":
                return data[index] & 0xFFFF
            elif datatype == "Hex":
                return hex(data[index])
            elif datatype == "Binary":
                return bin(data[index])
            elif datatype == "ASCII":
                return chr(data[index] & 0xFF)
            elif datatype == "Float" and index + 1 < len(data):
                b = struct.pack('<HH', data[index], data[index + 1])
                return struct.unpack('<f', b)[0]
            elif datatype == "Double" and index + 3 < len(data):
                b = struct.pack('>HHHH', data[index], data[index+1], data[index+2], data[index+3])
                return struct.unpack('>d', b)[0]
            else:
                return data[index]
        except Exception as e:
            return f"ERR ({str(e)})"

    def write_data(self):
        ip = self.ip_combo.currentText()
        port = int(self.port_input.text())
        unit_id = int(self.unit_input.text())
        address = int(self.write_address.text())
        write_type = self.write_type_combo.currentText()
        value_input = self.write_value.text()

        if not ip or not value_input:
            QMessageBox.warning(self, "Input Error", "Please enter IP and value to write.")
            return

        if write_type == "Register":
            try:
                value = int(value_input)
                result = write_single_register(ip, port, unit_id, address, value)
            except ValueError:
                QMessageBox.warning(self, "Value Error", "Value must be an integer.")
                return

        elif write_type == "Coil":
            if value_input.lower() in ["true", "1"]:
                value = True
            elif value_input.lower() in ["false", "0"]:
                value = False
            else:
                QMessageBox.warning(self, "Value Error", "Coil value must be True/False or 1/0.")
                return
            result = write_single_coil(ip, port, unit_id, address, value)

        elif write_type == "Multiple Register":
            try:
                values = [int(v.strip()) for v in value_input.split(",")]
                result = write_multiple_registers(ip, port, unit_id, address, values)
            except ValueError:
                QMessageBox.warning(self, "Value Error", "Enter comma-separated integers (e.g., 100,200).")
                return
        else:
            QMessageBox.warning(self, "Type Error", "Invalid write type selected.")
            return

        if result == "Success":
            QMessageBox.information(self, "Success", f"Write successful.")
        else:
            QMessageBox.warning(self, "Write Error", f"Write failed: {result}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyScan()
    win.show()
    sys.exit(app.exec_())
