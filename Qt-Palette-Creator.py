import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QCheckBox, QRadioButton, 
                             QComboBox, QSpinBox, QSlider, QProgressBar, QTabWidget, 
                             QDial, QFrame, QColorDialog, QDialog, QMessageBox, QStyleFactory)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
import pyqtgraph as pg

class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Qt Widgets Demo')
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create a scroll area
        scroll_area = QFrame(self)
        scroll_layout = QVBoxLayout(scroll_area)
        scroll_area.setLayout(scroll_layout)

        # Labels and Buttons
        label_button_layout = QHBoxLayout()
        label_button_layout.addWidget(QLabel('Label: Hello, Qt!'))
        button = QPushButton('Button')
        button.clicked.connect(self.show_message)
        label_button_layout.addWidget(button)
        scroll_layout.addLayout(label_button_layout)

        # Text Input
        text_input_layout = QHBoxLayout()
        text_input_layout.addWidget(QLabel('Line Edit:'))
        text_input_layout.addWidget(QLineEdit())
        scroll_layout.addLayout(text_input_layout)

        text_edit_layout = QHBoxLayout()
        text_edit_layout.addWidget(QLabel('Text Edit:'))
        text_edit_layout.addWidget(QTextEdit())
        scroll_layout.addLayout(text_edit_layout)

        # Checkboxes and Radio Buttons
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(QLabel('Checkbox:'))
        checkbox_layout.addWidget(QCheckBox('Check me'))
        scroll_layout.addLayout(checkbox_layout)

        radio_button_layout = QHBoxLayout()
        radio_button_layout.addWidget(QLabel('Radio Button:'))
        radio_button_layout.addWidget(QRadioButton('Select me'))
        scroll_layout.addLayout(radio_button_layout)

        # Combo Box (Drop-down menu)
        combo_box_layout = QHBoxLayout()
        combo_box_layout.addWidget(QLabel('Combo Box:'))
        combo_box = QComboBox()
        combo_box.addItems(['Option 1', 'Option 2', 'Option 3'])
        combo_box_layout.addWidget(combo_box)
        scroll_layout.addLayout(combo_box_layout)

        # Spin Box (Numeric input)
        spin_box_layout = QHBoxLayout()
        spin_box_layout.addWidget(QLabel('Spin Box:'))
        spin_box_layout.addWidget(QSpinBox())
        scroll_layout.addLayout(spin_box_layout)

        # Slider and Progress Bar
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel('Slider:'))
        slider = QSlider(Qt.Horizontal)
        slider_layout.addWidget(slider)
        scroll_layout.addLayout(slider_layout)

        progress_bar_layout = QHBoxLayout()
        progress_bar_layout.addWidget(QLabel('Progress Bar:'))
        progress_bar = QProgressBar()
        progress_bar_layout.addWidget(progress_bar)
        scroll_layout.addLayout(progress_bar_layout)

        # Knob (QDial)
        knob_layout = QHBoxLayout()
        knob_layout.addWidget(QLabel('Knob (QDial):'))
        knob = QDial()
        knob.setNotchesVisible(True)
        knob_layout.addWidget(knob)
        scroll_layout.addLayout(knob_layout)

        # Plot Widget (from pyqtgraph)
        plot_layout = QVBoxLayout()
        plot_label = QLabel('Plot Widget:')
        plot_label.setFont(QFont('Arial', 14))
        plot_layout.addWidget(plot_label)
        plot_widget = pg.PlotWidget()
        plot_layout.addWidget(plot_widget)
        scroll_layout.addLayout(plot_layout)

        # Tab Widget
        tab_widget_layout = QVBoxLayout()
        tab_label = QLabel('Tab Widget:')
        tab_label.setFont(QFont('Arial', 14))
        tab_widget_layout.addWidget(tab_label)
        tab_widget = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.addWidget(QLabel('Tab 1 Content'))
        tab1.setLayout(tab1_layout)
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel('Tab 2 Content'))
        tab2.setLayout(tab2_layout)
        tab_widget.addTab(tab1, 'Tab 1')
        tab_widget.addTab(tab2, 'Tab 2')
        tab_widget_layout.addWidget(tab_widget)
        scroll_layout.addLayout(tab_widget_layout)

        # Add a button to open the palette editor
        palette_button = QPushButton('Edit Palette')
        palette_button.clicked.connect(self.open_palette_editor)
        scroll_layout.addWidget(palette_button)

        # Add the scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Responsive resizing
        self.setLayout(main_layout)
        scroll_area.setFrameShape(QFrame.StyledPanel)

    def show_message(self):
        QMessageBox.information(self, 'Message', 'Button clicked!')

    def open_palette_editor(self):
        self.palette_editor = PaletteEditor(self)
        self.palette_editor.show()

class PaletteEditor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Palette Editor')
        self.setGeometry(150, 150, 500, 400)

        self.layout = QVBoxLayout()
        self.color_labels = {}

        # Style Selector
        style_layout = QHBoxLayout()
        style_label = QLabel("Select Style:")
        self.style_combo = QComboBox()
        self.style_combo.addItems(QStyleFactory.keys())
        self.style_combo.currentIndexChanged.connect(self.change_style)
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combo)
        self.layout.addLayout(style_layout)

        # Create buttons to change palette colors
        self.create_palette_button('Window')
        self.create_palette_button('WindowText')
        self.create_palette_button('Base')
        self.create_palette_button('AlternateBase')
        self.create_palette_button('ToolTipBase')
        self.create_palette_button('ToolTipText')
        self.create_palette_button('Text')
        self.create_palette_button('Button')
        self.create_palette_button('ButtonText')
        self.create_palette_button('BrightText')
        self.create_palette_button('Highlight')
        self.create_palette_button('HighlightedText')

        # Text box to display the current palette
        self.palette_text = QTextEdit()
        self.palette_text.setReadOnly(True)
        self.update_palette_text()

        self.layout.addWidget(self.palette_text)
        self.setLayout(self.layout)

    def create_palette_button(self, color_role):
        hbox = QHBoxLayout()
        button = QPushButton(f'Change {color_role} Color')
        button.clicked.connect(lambda: self.change_color(color_role))
        hbox.addWidget(button)

        color_label = QLabel()
        color_label.setFixedSize(50, 20)
        color_label.setAutoFillBackground(True)
        hbox.addWidget(color_label)
        
        self.color_labels[color_role] = color_label
        self.update_color_label(color_role)

        self.layout.addLayout(hbox)

    def change_color(self, color_role):
        color = QColorDialog.getColor()

        if color.isValid():
            role = getattr(QPalette, color_role)
            palette = self.parent().palette()
            palette.setColor(role, color)
            self.parent().setPalette(palette)
            self.update_color_label(color_role)
            self.update_palette_text()

    def update_color_label(self, color_role):
        palette = self.parent().palette()
        role = getattr(QPalette, color_role)
        color = palette.color(role)

        color_label = self.color_labels[color_role]
        color_label.setStyleSheet(f'background-color: {color.name()}')

    def update_palette_text(self):
        palette = self.parent().palette()
        roles = [
            'Window', 'WindowText', 'Base', 'AlternateBase', 'ToolTipBase',
            'ToolTipText', 'Text', 'Button', 'ButtonText', 'BrightText',
            'Highlight', 'HighlightedText'
        ]
        palette_text = "palette = QPalette()\n"
        for role in roles:
            color = palette.color(getattr(QPalette, role))
            color_name = color.name()
            if color_name.startswith('#'):  # Use QColor's name if it starts with '#'
                palette_text += f'palette.setColor(QPalette.{role}, QColor("{color_name}"))\n'
            else:  # Otherwise, assume it's a named color (like Qt.white)
                palette_text += f'palette.setColor(QPalette.{role}, Qt.{color_name})\n'
        self.palette_text.setText(palette_text)

    def change_style(self):
        style_name = self.style_combo.currentText()
        QApplication.setStyle(style_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DemoWindow()
    demo.show()
    sys.exit(app.exec_())
