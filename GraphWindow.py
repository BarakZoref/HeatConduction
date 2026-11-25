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
    def __init__(self, main_window = None):
        super().__init__()

        self.main_window = main_window
        self.drawn_bodies = set()

        self.setWindowTitle("Graph")

        self.figure = Figure(figsize=(5, 4))
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlim(0, 11)
        self.axes.set_ylim(0, 200)
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Temperature (\u00b0C)")
        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)
        self.body1_line, = self.axes.plot([], [], label="Body1")
        self.body2_line, = self.axes.plot([], [], label="Body2")
        self.graph_canvas = FigureCanvasQTAgg(self.figure)

        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems(["Body1", "Body2"])
        self.draw_button = QPushButton("Draw")
        self.draw_button.clicked.connect(self.plot_selected_graph)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_graph)
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

    def plot_selected_graph(self):
        if self.graph_type_combo.currentText() == "Body1":
            self.plot_left_body_graph()
        elif self.graph_type_combo.currentText() == "Body2":
            self.plot_right_body_graph()

    def clear_graph(self):
        self.drawn_bodies.clear()
        self.body1_line.set_data([], [])
        self.body2_line.set_data([], [])
        self.graph_canvas.draw_idle()

    def update_graph(self):
        if "Body1" in self.drawn_bodies:
            self._set_body_line(
                self.body1_line,
                self.main_window.body1_temp_history,
            )
        if "Body2" in self.drawn_bodies:
            self._set_body_line(
                self.body2_line,
                self.main_window.body2_temp_history,
            )
        self.graph_canvas.draw_idle()

    def _set_body_line(self, line, temperature_history):
        line.set_data(self.main_window.time_history, temperature_history)

    def plot_left_body_graph(self):
        self.drawn_bodies.add("Body1")
        self._set_body_line(self.body1_line, self.main_window.body1_temp_history)
        self.graph_canvas.draw_idle()

    def plot_right_body_graph(self):
        self.drawn_bodies.add("Body2")
        self._set_body_line(self.body2_line, self.main_window.body2_temp_history)
        self.graph_canvas.draw_idle()


def main() -> int:
    app = QApplication(sys.argv)
    window = GraphWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
