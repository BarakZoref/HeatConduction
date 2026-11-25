import sys

from Body import Body
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Heat Transfer")

        self.body1_temp_history = []
        self.body2_temp_history = []
        self.time_history = [0]
        self.current_time = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_method)

        self.left_body = None
        self.right_body = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(0)

        self.left_slider = QSlider(Qt.Orientation.Vertical)
        self.left_slider.setMinimumHeight(140)
        self.left_slider.setRange(0,255)
        self.left_slider.valueChanged.connect(self.left_temperature_changed)

        self.left_box = QLabel()
        self.left_box.setFixedSize(120, 120)
        self.left_box.setStyleSheet("border: 2px solid #333; background-color: rgb(0,0,0);")

        self.connection = QLabel()
        self.connection.setFixedSize(200, 32)
        self.connection.setStyleSheet("border: 2px solid #333; background-color: lightgray;")

        self.right_box = QLabel()
        self.right_box.setFixedSize(120, 120)
        self.right_box.setStyleSheet("border: 2px solid #333; background-color:rgb(0,0,0);")

        self.right_slider = QSlider(Qt.Orientation.Vertical)
        self.right_slider.setMinimumHeight(140)
        self.right_slider.setRange(0,255)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)
        left_top_layout = QHBoxLayout()
        left_top_layout.setSpacing(0)
        left_top_layout.addWidget(self.left_slider)
        left_top_layout.addSpacing(12)
        left_top_layout.addWidget(self.left_box)
        left_layout.addLayout(left_top_layout)

        self.left_temperature = QDoubleSpinBox()
        self.left_temperature.setRange(0,200)
        self.left_mass = QDoubleSpinBox()
        self.left_mass.setRange(1,100)
        self.left_mass.setValue(100)
        self.left_heat_capacity = QDoubleSpinBox()
        self.left_heat_capacity.setRange(0.1,999)
        self.left_heat_capacity.setValue(2)
        self.left_temperature_label = QLabel("Temp.")
        self.left_mass_label = QLabel("Mass.")
        self.left_heat_capacity_label = QLabel("H. Cap.")

        for label in (
            self.left_temperature_label,
            self.left_mass_label,
            self.left_heat_capacity_label,
        ):
            label.setFixedWidth(48)
            label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        for spin_box in (self.left_temperature, self.left_mass, self.left_heat_capacity):
            spin_box.setFixedWidth(90)

        left_temperature_row = QHBoxLayout()
        left_temperature_row.setSpacing(4)
        left_temperature_row.addWidget(self.left_temperature_label)
        left_temperature_row.addWidget(self.left_temperature)
        left_layout.addLayout(left_temperature_row)

        left_mass_row = QHBoxLayout()
        left_mass_row.setSpacing(4)
        left_mass_row.addWidget(self.left_mass_label)
        left_mass_row.addWidget(self.left_mass)
        left_layout.addLayout(left_mass_row)

        left_heat_capacity_row = QHBoxLayout()
        left_heat_capacity_row.setSpacing(4)
        left_heat_capacity_row.addWidget(self.left_heat_capacity_label)
        left_heat_capacity_row.addWidget(self.left_heat_capacity)
        left_layout.addLayout(left_heat_capacity_row)

        center_layout = QVBoxLayout()
        center_layout.setSpacing(0)
        self.conductivity_label = QLabel("Conductivity")
        self.conductivity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conductivity = QDoubleSpinBox()
        self.conductivity.setRange(1,100)
        self.conductivity.setSuffix(" J/s\u00b0C")
        self.conductivity.setFixedWidth(90)
        center_layout.addWidget(
            self.conductivity_label, 0, Qt.AlignmentFlag.AlignHCenter
        )
        center_layout.addSpacing(4)
        center_layout.addWidget(self.conductivity, 0, Qt.AlignmentFlag.AlignHCenter)
        center_layout.addSpacing(12)
        center_layout.addWidget(self.connection, 0, Qt.AlignmentFlag.AlignHCenter)

        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)
        self.start_button.toggled.connect(self.start_stop_button_method)

        self.graphs_button = QPushButton("Graphs")
        self.about_button = QPushButton("About")
        for button in (self.start_button, self.graphs_button, self.about_button):
            button.setFixedSize(90, self.left_temperature.sizeHint().height())

        center_layout.addSpacing(73)
        center_layout.addWidget(self.start_button, 0, Qt.AlignmentFlag.AlignHCenter)
        center_layout.addSpacing(8)
        center_layout.addWidget(self.graphs_button, 0, Qt.AlignmentFlag.AlignHCenter)
        center_layout.addSpacing(8)
        center_layout.addWidget(self.about_button, 0, Qt.AlignmentFlag.AlignHCenter)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(8)
        right_top_layout = QHBoxLayout()
        right_top_layout.setSpacing(0)
        right_top_layout.addWidget(self.right_box)
        right_top_layout.addSpacing(12)
        right_top_layout.addWidget(self.right_slider)
        right_layout.addLayout(right_top_layout)

        self.right_temperature = QDoubleSpinBox()
        self.right_temperature.setRange(0,200)
        self.right_mass = QDoubleSpinBox()
        self.right_mass.setRange(1,100)
        self.right_mass.setValue(100)
        self.right_heat_capacity = QDoubleSpinBox()
        self.right_heat_capacity.setRange(0.1,999)
        self.right_heat_capacity.setValue(2)

        self.left_mass.setSuffix(" kg")
        self.left_heat_capacity.setSuffix(" J/Kg\u00b0C")
        self.right_mass.setSuffix(" kg")
        self.right_heat_capacity.setSuffix(" J/Kg\u00b0C")
        for spin_box in (
            self.left_temperature,
            self.left_mass,
            self.left_heat_capacity,
            self.right_temperature,
            self.right_mass,
            self.right_heat_capacity,
            self.conductivity,
        ):
            spin_box.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        for temperature_spin_box in (self.left_temperature, self.right_temperature):
            temperature_spin_box.setReadOnly(True)
            temperature_spin_box.setSuffix(" \u00b0C")
            temperature_spin_box.setStyleSheet("background-color: lightgray;")

        self.right_temperature_label = QLabel("Temp.")
        self.right_mass_label = QLabel("Mass.")
        self.right_heat_capacity_label = QLabel("H. Cap.")

        for label in (
            self.right_temperature_label,
            self.right_mass_label,
            self.right_heat_capacity_label,
        ):
            label.setFixedWidth(48)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        for spin_box in (self.right_temperature, self.right_mass, self.right_heat_capacity):
            spin_box.setFixedWidth(90)

        right_temperature_row = QHBoxLayout()
        right_temperature_row.setSpacing(4)
        right_temperature_row.addWidget(self.right_temperature)
        right_temperature_row.addWidget(self.right_temperature_label)
        right_layout.addLayout(right_temperature_row)

        right_mass_row = QHBoxLayout()
        right_mass_row.setSpacing(4)
        right_mass_row.addWidget(self.right_mass)
        right_mass_row.addWidget(self.right_mass_label)
        right_layout.addLayout(right_mass_row)

        right_heat_capacity_row = QHBoxLayout()
        right_heat_capacity_row.setSpacing(4)
        right_heat_capacity_row.addWidget(self.right_heat_capacity)
        right_heat_capacity_row.addWidget(self.right_heat_capacity_label)
        right_layout.addLayout(right_heat_capacity_row)

        layout.addLayout(left_layout)
        layout.addLayout(center_layout)
        layout.setAlignment(center_layout, Qt.AlignmentFlag.AlignTop)
        layout.addLayout(right_layout)

        self.left_slider.setValue(255)

    def left_temperature_changed(self):
        value = self.left_slider.value()
        self.left_temperature.setValue(self.slider_value_to_celsius(value))
        self.left_box.setStyleSheet(f'background-color:rgb({value},0,0)')

    def right_temperature_changed(self):
        value = self.right_slider.value()
        self.right_temperature.setValue(self.slider_value_to_celsius(value))
        self.right_box.setStyleSheet(f'background-color:rgb({value},0,0)')

    def slider_value_to_celsius(self, value: int) -> float:
        return value * 200 / 255

    def celsius_to_slider_value(self, temperature: float) -> int:
        return round(temperature * 255 / 200)

    def start_stop_button_method(self, checked: bool):
        self.start_button.setText("Stop" if checked else "Start")
        if checked:
            self.left_body = Body(self.left_mass.value(), self.left_heat_capacity.value(), self.left_temperature.value())
            self.right_body = Body(self.right_mass.value(), self.right_heat_capacity.value(), self.right_temperature.value())

            self.body1_temp_history.append(self.left_body.temperature)
            self.body2_temp_history.append(self.right_body.temperature)
            
            self.timer.start(1000)
        else:
            self.reboot_values()
            self.timer.stop()

    def timer_method(self):

        i1 = self.conductivity.value()*(self.right_body.temperature-self.left_body.temperature)
        i2 = i1*(-1)
        self.left_body.add_heat(i1)
        self.right_body.add_heat(i2)
        
        self.left_slider.setValue(self.celsius_to_slider_value(self.left_body.temperature))
        self.right_slider.setValue(self.celsius_to_slider_value(self.right_body.temperature))
        self.left_temperature.setValue(self.left_body.temperature)
        self.right_temperature.setValue(self.right_body.temperature)

        self.body1_temp_history.append(self.left_body.temperature)
        self.body2_temp_history.append(self.right_body.temperature)

        self.current_time+=1
        self.time_history.append(self.current_time)

        if self.current_time == 10:
            self.timer.stop()
            self.start_button.setChecked(False)
            self.reboot_values()


        print(self.body1_temp_history)
        print(self.body2_temp_history)
        print(self.time_history)

        print("---------------------")
        
    def reboot_values(self):
        self.body1_temp_history = []
        self.body2_temp_history = []
        self.current_time = 0
        self.time_history = [0]
      




def main() -> int:
    app = QApplication(sys.argv)
    window = HeatTransfer()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

