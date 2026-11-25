import sys

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graph")

        self.figure = Figure(figsize=(5, 4))
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlim(0, 10)
        self.axes.set_ylim(0, 200)
        self.axes.set_xlabel("Time")
        self.axes.set_ylabel("Temperature")
        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)
        self.graph_canvas = FigureCanvasQTAgg(self.figure)

        self.graph_type_combo = QComboBox()
        self.draw_button = QPushButton("Draw")
        self.clear_button = QPushButton("Clear")
        self.export_button = QPushButton("Export to CSV")
        for control in (
            self.graph_type_combo,
            self.draw_button,
            self.clear_button,
            self.export_button,
        ):
            control.setMinimumSize(160, 44)
            control.setStyleSheet("font-size: 12pt;")

        controls_layout = QVBoxLayout()
        controls_layout.addWidget(self.graph_type_combo)
        controls_layout.addWidget(self.draw_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.export_button)
        controls_layout.addStretch()

        layout = QHBoxLayout(self)
        layout.addWidget(self.graph_canvas, 1)
        layout.addLayout(controls_layout)


def main() -> int:
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
