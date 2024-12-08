import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QRadioButton,
    QButtonGroup
)
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

# Переводы для интерфейса
TRANSLATIONS = {
    "en": {
        "Language": "Language:",
        "Hotkey": "Hotkey:",
        "Set": "Set",
        "Delay": "Delay (sec):",
        "Mouse Button": "Mouse Button:",
        "Click Mode": "Click Mode:",
        "Infinite": "Infinite",
        "Click Count": "Click Count",
        "Duration": "Duration (sec)",
        "Enter click count": "Enter click count",
        "Enter duration in seconds": "Enter duration in seconds",
        "Status Disabled": "Status: Disabled",
        "Status Enabled": "Status: Enabled",
        "Start": "Start",
        "Stop": "Stop",
        "Invalid Hotkey": "Invalid Hotkey",
        "Enter a valid hotkey": "Enter a valid hotkey",
        "Invalid Delay": "Invalid Delay",
        "Enter a valid delay": "Enter a valid delay",
        "Invalid Count": "Invalid Count",
        "Enter a valid click count": "Enter a valid click count",
        "Invalid Duration": "Invalid Duration",
        "Enter a valid duration": "Enter a valid duration"
    },
    "ru": {
        "Language": "Язык:",
        "Hotkey": "Горячая клавиша:",
        "Set": "Установить",
        "Delay": "Задержка (сек):",
        "Mouse Button": "Кнопка мыши:",
        "Click Mode": "Режим кликов:",
        "Infinite": "Бесконечно",
        "Click Count": "Количество кликов",
        "Duration": "Длительность (сек)",
        "Enter click count": "Введите количество кликов",
        "Enter duration in seconds": "Введите длительность в секундах",
        "Status Disabled": "Статус: Отключено",
        "Status Enabled": "Статус: Включено",
        "Start": "Старт",
        "Stop": "Стоп",
        "Invalid Hotkey": "Неверная горячая клавиша",
        "Enter a valid hotkey": "Введите корректную горячую клавишу",
        "Invalid Delay": "Неверная задержка",
        "Enter a valid delay": "Введите корректную задержку",
        "Invalid Count": "Неверное количество",
        "Enter a valid click count": "Введите корректное количество кликов",
        "Invalid Duration": "Неверная длительность",
        "Enter a valid duration": "Введите корректную длительность"
    }
}


class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = 'en'  # Default language
        self.initUI()
        self.load_config()

    def initUI(self):
        layout = QVBoxLayout()

        # Language selection
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel(TRANSLATIONS[self.lang]["Language"])
        lang_layout.addWidget(self.lang_label)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['English', 'Русский'])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # Hotkey setup
        hotkey_layout = QHBoxLayout()
        self.hotkey_label = QLabel(TRANSLATIONS[self.lang]["Hotkey"])
        hotkey_layout.addWidget(self.hotkey_label)
        self.hotkey_input = QLineEdit("W+S")
        hotkey_layout.addWidget(self.hotkey_input)
        self.set_hotkey_button = QPushButton(TRANSLATIONS[self.lang]["Set"])
        hotkey_layout.addWidget(self.set_hotkey_button)
        layout.addLayout(hotkey_layout)

        # Delay setup
        delay_layout = QHBoxLayout()
        self.delay_label = QLabel(TRANSLATIONS[self.lang]["Delay"])
        delay_layout.addWidget(self.delay_label)
        self.delay_input = QLineEdit("0.01")
        delay_layout.addWidget(self.delay_input)
        self.set_delay_button = QPushButton(TRANSLATIONS[self.lang]["Set"])
        delay_layout.addWidget(self.set_delay_button)
        layout.addLayout(delay_layout)

        # Mouse button setup
        mouse_button_layout = QHBoxLayout()
        self.mouse_button_label = QLabel(TRANSLATIONS[self.lang]["Mouse Button"])
        mouse_button_layout.addWidget(self.mouse_button_label)
        self.mouse_button_combo = QComboBox()
        self.mouse_button_combo.addItems(['left', 'right', 'middle'])
        mouse_button_layout.addWidget(self.mouse_button_combo)
        layout.addLayout(mouse_button_layout)

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF8DC;  /* Светлый жёлтый фон */
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit, QPushButton, QComboBox {
                background-color: #FFD700;
                border: 1px solid #DAA520;
                border-radius: 5px;
                padding: 5px;
                box-shadow: 2px 2px 6px #A0522D;
            }
            QPushButton:hover {
                background-color: #FFC107;
                box-shadow: 0 0 12px #FFA500;
            }
            QPushButton:pressed {
                background-color: #FFA500;
                box-shadow: inset 2px 2px 4px #8B4513;
            }
            QLabel {
                color: #8B4513;
                font-weight: bold;
                text-shadow: 1px 1px 2px #A0522D;
            }
        """)

        self.setLayout(layout)
        self.setWindowTitle("AutoClicker")

    def change_language(self, index):
        self.lang = 'en' if index == 0 else 'ru'
        self.retranslateUi()
        self.save_config()

    def retranslateUi(self):
        self.lang_label.setText(TRANSLATIONS[self.lang]["Language"])
        self.hotkey_label.setText(TRANSLATIONS[self.lang]["Hotkey"])
        self.set_hotkey_button.setText(TRANSLATIONS[self.lang]["Set"])
        self.delay_label.setText(TRANSLATIONS[self.lang]["Delay"])
        self.set_delay_button.setText(TRANSLATIONS[self.lang]["Set"])
        self.mouse_button_label.setText(TRANSLATIONS[self.lang]["Mouse Button"])

    def save_config(self):
        config = {"lang": self.lang}
        with open("config.json", "w") as f:
            json.dump(config, f)

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                self.lang = config.get("lang", "en")
                self.lang_combo.setCurrentIndex(0 if self.lang == 'en' else 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoClicker()
    ex.show()
    sys.exit(app.exec_())
