# main.py
from core.modbus_tcp import read_holding_registers
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
import sys

class ModScanApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ModScan Clone - v0.1")
        self.setGeometry(200, 200, 400, 250)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter IP Address:")
        self.ip_input = QLineEdit()
        self.connect_button = QPushButton("Connect (TCP)")

        layout.addWidget(self.label)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.connect_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.connect_button.clicked.connect(self.handle_connect)
    def handle_connect(self):
        ip = self.ip_input.text()
        port = 502          # Default Modbus TCP port
        unit_id = 1         # Slave ID
        address = 0         # Starting address (40001 için 0 yazılır)
        count = 5           # 5 register oku
    
        result = read_holding_registers(ip, port, unit_id, address, count)
        self.label.setText(f"Result: {result}")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModScanApp()
    window.show()
    sys.exit(app.exec_())