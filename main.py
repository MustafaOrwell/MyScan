from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from pymodbus.client import ModbusTcpClient
import sys
import struct
from core.modbus_tcp import read_holding_registers

class MyScan(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyScan - Modbus Scanner")
        self.setGeometry(300, 150, 800, 500)
        self.initUI()

    def initUI(self):
        # IP, Port ve Unit ID
        ip_label = QLabel("IP:")
        self.ip_input = QLineEdit("127.0.0.1")
        port_label = QLabel("Port:")
        self.port_input = QLineEdit("502")
        unit_label = QLabel("Unit ID:")
        self.unit_input = QLineEdit("1")
        self.connect_button = QPushButton("Connect")
        self.connect_button.setObjectName("connect_button")
        self.connect_button.clicked.connect(self.connect_to_modbus)

        ip_port_layout = QVBoxLayout()
        ip_port_layout.addWidget(ip_label)
        ip_port_layout.addWidget(self.ip_input)
        ip_port_layout.addWidget(port_label)
        ip_port_layout.addWidget(self.port_input)
        ip_port_layout.addWidget(unit_label)
        ip_port_layout.addWidget(self.unit_input)
        ip_port_layout.addWidget(self.connect_button)

        # Adres ve Quantity
        address_label = QLabel("Start Address:")
        self.address_input = QLineEdit("0")
        count_label = QLabel("Quantity:")
        self.count_input = QLineEdit("10")

        address_layout = QVBoxLayout()
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input)
        address_layout.addWidget(count_label)
        address_layout.addWidget(self.count_input)

        # Register ve Data Tipi
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

        # Üst kısım birleşimi
        top_layout = QHBoxLayout()
        top_layout.addLayout(address_layout)
        top_layout.addStretch()
        top_layout.addLayout(options_layout)
        top_layout.addStretch()
        top_layout.addLayout(ip_port_layout)

        # Okuma/Durdurma
        self.read_button = QPushButton("Start Read")
        self.read_button.setObjectName("read_button")
        self.read_button.clicked.connect(self.read_data)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setObjectName("stop_button")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.read_button)
        button_layout.addWidget(self.stop_button)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Address", "Value"])

        # Ana yerleşim
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Stil
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QLabel {
                font-weight: bold;
            }
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
            QPushButton#connect_button {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#stop_button {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton#read_button {
                background-color: #3498db;
                color: white;
            }
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

    def connect_to_modbus(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        try:
            self.client = ModbusTcpClient(host=ip, port=port)
            if self.client.connect():
                QMessageBox.information(self, "Connection", f"Connected to {ip}:{port}")
                self.connect_button.setEnabled(False)
                self.connect_button.setText("Connected")
            else:
                QMessageBox.critical(self, "Connection Failed", f"Could not connect to {ip}:{port}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def read_data(self):
        ip = self.ip_input.text()
        port = int(self.port_input.text())
        unit_id = int(self.unit_input.text())
        address = int(self.address_input.text())
        count = int(self.count_input.text())
        datatype = self.datatype_combo.currentText()

        result = read_holding_registers(ip, port, unit_id, address, count)
        self.table.setRowCount(0)

        if isinstance(result, list):
            for i, val in enumerate(result):
                value_str = self.decode_value(result, i, datatype)
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(str(address + i)))
                self.table.setItem(i, 1, QTableWidgetItem(str(value_str)))
        else:
            QMessageBox.warning(self, "Read Failed", str(result))

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
                b = struct.pack('>HH', data[index], data[index + 1])
                return struct.unpack('>f', b)[0]
            elif datatype == "Double" and index + 3 < len(data):
                b = struct.pack('>HHHH', data[index], data[index+1], data[index+2], data[index+3])
                return struct.unpack('>d', b)[0]
            else:
                return data[index]
        except:
            return "ERR"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyScan()
    win.show()
    sys.exit(app.exec_())
