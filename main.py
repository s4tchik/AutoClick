import sys
import os
import json
import time 
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QComboBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import QThread, pyqtSignal

# Переводы для интерфейса
TRANSLATIONS = { 
    "en": {
        "language": "Language:" 
        "hotkey": "Hotkey:", 
        "set": "Set", 
        "delay": "Delay (sec):",
        "mouse_button": "Mouse Button:",
        "click_mode": "Click Mode:", 
        "infinite": "Infinite",
        "click_count": "Click Count",
        "duration": "Duration (sec)",
        "enter_click_count": "Enter click count",
        "enter_duration": "Enter duration in seconds",
        "status_disabled": "Status: Disabled",
        "status_enabled": "Status: Enabled",
        "start": "Start",
        "stop": "Stop",
        "invalid_hotkey": "Invalid Hotkey",
        "enter_valid_hotkey": "Enter a valid hotkey",
        "invalid_delay": "Invalid Delay",
        "enter_valid_delay": "Enter a valid delay",
        "invalid_click_count": "Invalid Count",
        "enter_valid_click_count": "Enter a valid click count",
        "invalid_duration": "Invalid Duration",
        "enter_valid_duration": "Enter a valid duration",
    },
    "ru": {
        "language": "Язык:",
        "hotkey": "Горячая клавиша:",
        "set": "Установить",
        "delay": "Задержка (сек):",
        "mouse_button": "Кнопка мыши:",
        "click_mode": "Режим кликов:",
        "infinite": "Бесконечно",
        "click_count": "Количество кликов",
        "duration": "Длительность (сек)",
        "enter_click_count": "Введите количество кликов",
        "enter_duration": "Введите длительность в секундах",
        "status_disabled": "Статус: Отключено",
        "status_enabled": "Статус: Включено",
        "start": "Старт",
        "stop": "Стоп",
        "invalid_hotkey": "Неверная горячая клавиша",
        "enter_valid_hotkey": "Введите корректную горячую клавишу",
        "invalid_delay": "Неверная задержка",
        "enter_valid_delay": "Введите корректную задержку",
        "invalid_click_count": "Неверное количество",
        "enter_valid_click_count": "Введите корректное количество кликов",
        "invalid_duration": "Неверная длительность",
        "enter_valid_duration": "Введите корректную длительность",
    },
    "zh": {
        "language": "语言:",
        "hotkey": "快捷键:",
        "set": "设置",
        "delay": "延迟 (秒):",
        "mouse_button": "鼠标按钮:",
        "click_mode": "点击模式:",
        "infinite": "无限",
        "click_count": "点击次数",
        "duration": "持续时间 (秒)",
        "enter_click_count": "输入点击次数",
        "enter_duration": "输入持续时间（秒）",
        "status_disabled": "状态: 已禁用",
        "status_enabled": "状态: 已启用",
        "start": "开始",
        "stop": "停止",
        "invalid_hotkey": "无效的快捷键",
        "enter_valid_hotkey": "输入有效的快捷键",
        "invalid_delay": "无效的延迟",
        "enter_valid_delay": "输入有效的延迟",
        "invalid_click_count": "无效的点击次数",
        "enter_valid_click_count": "输入有效的点击次数",
        "invalid_duration": "无效的持续时间",
        "enter_valid_duration": "输入有效的持续时间",
    },
    "cs": {
        "language": "Jazyk:",
        "hotkey": "Horká klávesa:",
        "set": "Nastavit",
        "delay": "Zpoždění (sek):",
        "mouse_button": "Tlačítko myši:",
        "click_mode": "Režim kliknutí:",
        "infinite": "Nekonečné",
        "click_count": "Počet kliknutí",
        "duration": "Délka (sek)",
        "enter_click_count": "Zadejte počet kliknutí",
        "enter_duration": "Zadejte délku v sekundách",
        "status_disabled": "Stav: Zakázáno",
        "status_enabled": "Stav: Povolen",
        "start": "Start",
        "stop": "Stop",
        "invalid_hotkey": "Neplatná horká klávesa",
        "enter_valid_hotkey": "Zadejte platnou horkou klávesu",
        "invalid_delay": "Neplatné zpoždění",
        "enter_valid_delay": "Zadejte platné zpoždění",
        "invalid_click_count": "Neplatný počet",
        "enter_valid_click_count": "Zadejte platný počet kliknutí",
        "invalid_duration": "Neplatná délka",
        "enter_valid_duration": "Zadejte platnou délku",
    },
    "kk": {
        "language": "Тіл:",
        "hotkey": "Түймешік:",
        "set": "Орнату",
        "delay": "Кідіріс (сек):",
        "mouse_button": "Тышқан батырмасы:",
        "click_mode": "Басу режимі:",
        "infinite": "Шексіз",
        "click_count": "Басу саны",
        "duration": "Ұзақтығы (сек)",
        "enter_click_count": "Басу санын енгізіңіз",
        "enter_duration": "Ұзақтығын енгізіңіз",
        "status_disabled": "Күйі: Өшірілді",
        "status_enabled": "Күйі: Қосылды",
        "start": "Бастау",
        "stop": "Тоқтату",
        "invalid_hotkey": "Жарамсыз түймешік",
        "enter_valid_hotkey": "Жарамды түймешікті енгізіңіз",
        "invalid_delay": "Жарамсыз кідіріс",
        "enter_valid_delay": "Жарамды кідірісті енгізіңіз",
        "invalid_click_count": "Жарамсыз саны",
        "enter_valid_click_count": "Басу санын енгізіңіз",
        "invalid_duration": "Жарамсыз ұзақтық",
        "enter_valid_duration": "Ұзақтығын енгізіңіз",
    },
    "pl": {
        "language": "Język:",
        "hotkey": "Skrót klawiszowy:",
        "set": "Ustaw",
        "delay": "Opóźnienie (sek):",
        "mouse_button": "Przycisk myszy:",
        "click_mode": "Tryb kliknięcia:",
        "infinite": "Nieskończone",
        "click_count": "Liczba kliknięć",
        "duration": "Czas trwania (sek)",
        "enter_click_count": "Wpisz liczbę kliknięć",
        "enter_duration": "Wpisz czas trwania w sekundach",
        "status_disabled": "Status: Wyłączone",
        "status_enabled": "Status: Włączone",
        "start": "Start",
        "stop": "Stop",
        "invalid_hotkey": "Nieprawidłowy skrót klawiszowy",
        "enter_valid_hotkey": "Wprowadź prawidłowy skrót klawiszowy",
        "invalid_delay": "Nieprawidłowe opóźnienie",
        "enter_valid_delay": "Wprowadź prawidłowe opóźnienie",
        "invalid_click_count": "Nieprawidłowa liczba kliknięć",
        "enter_valid_click_count": "Wprowadź prawidłową liczbę kliknięć",
        "invalid_duration": "Nieprawidłowy czas trwania",
        "enter_valid_duration": "Wprowadź prawidłowy czas trwania",
    },
}

from PyQt5.QtGui import QColor

class ClickerThread(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.clicking = False
        self.delay = 0.01
        self.button = 'left'
        self.click_count = 0
        self.duration = 0
        self.click_mode = 'infinite'

    def run(self):
        start_time = time.time()
        clicks_performed = 0
        while self.clicking:
            if self.click_mode == 'count' and clicks_performed >= self.click_count:
                break
            if self.click_mode == 'duration' and time.time() - start_time >= self.duration:
                break
            # Simulate a mouse click (requires 'mouse' package)
            from mouse import click
            click(button=self.button)
            clicks_performed += 1
            time.sleep(self.delay)
        self.clicking = False
        self.finished.emit()


class AutoClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.lang = 'en'  # Default language
        self.initUI()
        self.clicker_thread = ClickerThread()
        self.clicker_thread.finished.connect(self.on_clicking_finished)
        self.load_config()

    def initUI(self):
        self.setWindowIcon(QIcon("saturn_icon_182816.ico"))
        layout = QVBoxLayout()

        # Language selection
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel(self.tr("language"))
        lang_layout.addWidget(self.lang_label)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Русский", "中文", "Čeština", "Қазақша", "Polski"])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        # Hotkey setup
        hotkey_layout = QHBoxLayout()
        self.hotkey_label = QLabel(self.tr("hotkey"))
        hotkey_layout.addWidget(self.hotkey_label)
        self.hotkey_input = QLineEdit("z")
        hotkey_layout.addWidget(self.hotkey_input)
        self.set_hotkey_button = QPushButton(self.tr("set"))
        self.set_hotkey_button.clicked.connect(self.set_hotkey)
        hotkey_layout.addWidget(self.set_hotkey_button)
        layout.addLayout(hotkey_layout)

        # Delay setup
        delay_layout = QHBoxLayout()
        self.delay_label = QLabel(self.tr("delay"))
        delay_layout.addWidget(self.delay_label)
        self.delay_input = QLineEdit("0.01")
        delay_layout.addWidget(self.delay_input)
        self.set_delay_button = QPushButton(self.tr("set"))
        self.set_delay_button.clicked.connect(self.update_delay)
        delay_layout.addWidget(self.set_delay_button)
        layout.addLayout(delay_layout)

        # Mouse button selection
        mouse_button_layout = QHBoxLayout()
        self.mouse_button_label = QLabel(self.tr("mouse_button"))
        mouse_button_layout.addWidget(self.mouse_button_label)
        self.mouse_button_combo = QComboBox()
        self.mouse_button_combo.addItems(['left', 'right', 'middle'])
        mouse_button_layout.addWidget(self.mouse_button_combo)
        layout.addLayout(mouse_button_layout)

        # Click mode
        click_mode_layout = QVBoxLayout()
        self.click_mode_label = QLabel(self.tr("click_mode"))
        click_mode_layout.addWidget(self.click_mode_label)
        self.click_mode_group = QButtonGroup()
        self.infinite_radio = QRadioButton(self.tr("infinite"))
        self.count_radio = QRadioButton(self.tr("click_count"))
        self.duration_radio = QRadioButton(self.tr("duration"))
        self.click_mode_group.addButton(self.infinite_radio)
        self.click_mode_group.addButton(self.count_radio)
        self.click_mode_group.addButton(self.duration_radio)
        click_mode_layout.addWidget(self.infinite_radio)
        click_mode_layout.addWidget(self.count_radio)
        click_mode_layout.addWidget(self.duration_radio)
        self.click_count_input = QLineEdit()
        self.click_count_input.setPlaceholderText(self.tr("enter_click_count"))
        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText(self.tr("enter_duration"))
        click_mode_layout.addWidget(self.click_count_input)
        click_mode_layout.addWidget(self.duration_input)
        layout.addLayout(click_mode_layout)

        # Status and toggle button
        self.status_label = QLabel(self.tr("status_disabled"))
        layout.addWidget(self.status_label)
        self.toggle_button = QPushButton(self.tr("start"))
        self.toggle_button.clicked.connect(self.toggle_clicker)
        layout.addWidget(self.toggle_button)

        # Apply yellow tones
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF7E0;
                color: #000000;
                font-family: Arial;
                font-size: 14px;
            }
            QLineEdit, QPushButton, QComboBox {
                background-color: #FFD966;
                border: 1px solid #B45F04;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #F1C232;
            }
            QPushButton:pressed {
                background-color: #BF9000;
            }
            QLabel {
                font-weight: bold;
                color: #4A3600;
            }
        """)

        self.retranslateUi()
        self.setLayout(layout)
        self.setWindowTitle("AutoClicker_SAT")
        self.show()

    def tr(self, text):
        return TRANSLATIONS[self.lang].get(text, text)

    def set_hotkey(self):
        hotkey = self.hotkey_input.text().strip()
        if hotkey:
            try:
                from keyboard import add_hotkey
                add_hotkey(hotkey, self.toggle_clicker)
                self.set_hotkey_button.setText(f"{self.tr('set')}: {hotkey}")
                self.save_config()
            except ValueError as e:
                QMessageBox.warning(self, self.tr('invalid_hotkey'), str(e))
        else:
            QMessageBox.warning(self, self.tr('invalid_hotkey'), self.tr('enter_valid_hotkey'))

    def update_delay(self):
        try:
            self.clicker_thread.delay = float(self.delay_input.text())
            self.set_delay_button.setText(self.tr('set'))
        except ValueError:
            QMessageBox.warning(self, self.tr('invalid_delay'), self.tr('enter_valid_delay'))

    def toggle_clicker(self):
        if not self.clicker_thread.clicking:
            self.clicker_thread.button = self.mouse_button_combo.currentText()
            if self.infinite_radio.isChecked():
                self.clicker_thread.click_mode = 'infinite'
            elif self.count_radio.isChecked():
                try:
                    self.clicker_thread.click_count = int(self.click_count_input.text())
                    self.clicker_thread.click_mode = 'count'
                except ValueError:
                    QMessageBox.warning(self, self.tr('invalid_click_count'), self.tr('enter_valid_click_count'))
                    return
            elif self.duration_radio.isChecked():
                try:
                    self.clicker_thread.duration = float(self.duration_input.text())
                    self.clicker_thread.click_mode = 'duration'
                except ValueError:
                    QMessageBox.warning(self, self.tr('invalid_duration'), self.tr('enter_valid_duration'))
                    return
            self.clicker_thread.clicking = True
            self.clicker_thread.start()
            self.status_label.setText(self.tr('status_enabled'))
            self.toggle_button.setText(self.tr('stop'))
        else:
            self.clicker_thread.clicking = False
            self.status_label.setText(self.tr('status_disabled'))
            self.toggle_button.setText(self.tr('start'))

    def on_clicking_finished(self):
        self.status_label.setText(self.tr('status_disabled'))
        self.toggle_button.setText(self.tr('start'))

    def save_config(self):
        temp_dir = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'AutoClicker SAT')
        os.makedirs(temp_dir, exist_ok=True)
        config_file = os.path.join(temp_dir, 'config.json')
        with open(config_file, 'w') as f:
            json.dump({'hotkey': self.hotkey_input.text(), 'lang': self.lang}, f)

    def load_config(self):
        temp_dir = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'AutoClicker SAT')
        config_file = os.path.join(temp_dir, 'config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.hotkey_input.setText(config.get('hotkey', 'z'))
                self.lang = config.get('lang', 'en')
                self.lang_combo.setCurrentIndex(["en", "ru", "zh", "cs", "kk", "pl"].index(self.lang))
        self.set_hotkey()
        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(self.tr("AutoClicker"))
        self.hotkey_label.setText(self.tr('hotkey'))
        self.set_hotkey_button.setText(self.tr('set'))
        self.delay_label.setText(self.tr('delay'))
        self.set_delay_button.setText(self.tr('set'))
        self.mouse_button_label.setText(self.tr('mouse_button'))
        self.click_mode_label.setText(self.tr('click_mode'))
        self.infinite_radio.setText(self.tr('infinite'))
        self.count_radio.setText(self.tr('click_count'))
        self.duration_radio.setText(self.tr('duration'))
        self.click_count_input.setPlaceholderText(self.tr('enter_click_count'))
        self.duration_input.setPlaceholderText(self.tr('enter_duration'))
        self.status_label.setText(self.tr('status_disabled'))
        self.toggle_button.setText(self.tr('start'))
        self.lang_label.setText(self.tr('language'))

    def change_language(self, index):
        self.lang = ["en", "ru", "zh", "cs", "kk", "pl"][index]
        self.retranslateUi()
        self.save_config()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AutoClicker()
    sys.exit(app.exec_())

