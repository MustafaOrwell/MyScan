# chart_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph import PlotWidget
from collections import deque

class ChartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Chart")
        self.setGeometry(200, 200, 600, 400)

        self.graph_data = deque(maxlen=100)
        self.target_address = 0  # ✅ Varsayılan hedef adres
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.plot_widget = PlotWidget()
        self.graph_curve = self.plot_widget.plot()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

    def set_target_address(self, address):  # ✅ main.py'de kullanılan fonksiyon
        self.target_address = address

    def update_chart(self, value):  # ✅ Veri güncelleme fonksiyonu
        self.graph_data.append(value)
        self.graph_curve.setData(list(self.graph_data))
