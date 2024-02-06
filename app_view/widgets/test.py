from PyQt6.QtWidgets import *


app = QApplication([])

def connect():
    print(f'Connected\nPrinter:{printers_line.text()}\nLaptop:{laptop_line.text()}')
    # powershell script

window = QWidget()

layout = QVBoxLayout()

layout.addStretch()

laptop_row = QHBoxLayout()
layout.addLayout(laptop_row)

laptop_label = QLabel('Laptop')
laptop_row.addWidget(laptop_label)
laptop_line = QLineEdit()
laptop_row.addWidget(laptop_line)

printer_row = QHBoxLayout()
layout.addLayout(printer_row)

printers_label = QLabel('Printers')
printer_row.addWidget(printers_label)
printers_line = QLineEdit()
printer_row.addWidget(printers_line)

connect_button = QPushButton('Connect')
connect_button.clicked.connect(connect)
layout.addWidget(connect_button)

layout.addStretch()

window.setLayout(layout)
window.show()
app.exec()