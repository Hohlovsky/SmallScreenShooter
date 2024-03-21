import io
import os
import time
import keyboard
import pystray
import requests
from PIL import Image
import pyautogui
import autostart_manager  # Импортируем функции для управления автозагрузкой
# Удалим приветствие: https://stackoverflow.com/questions/51464455/how-to-disable-welcome-message-when-importing-pygame
# Из-за этого получим PEP8 ошибку, поэтому спрячем её.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer  # noqa: E402

class ScreenshotApp:
    def __init__(self):
        """Инициализация приложения"""
        self.tray_icon = None
        self.folder_path = "screenshots"  # Папка для сохранения скриншотов
        os.makedirs(self.folder_path, exist_ok=True)  # Создаем папку, если она не существует
        self.sound_enabled = True  # Флаг для отслеживания состояния звука
        self.autostart_enabled = autostart_manager.is_installed()  # Флаг для отслеживания состояния автозагрузки
        self.start_keyboard_listener()  # Запускаем клавиатурный уловитель
        self.create_tray_icon()  # Создаем иконку в трее

    def take_screenshot(self):
        """Функция для создания скриншота"""
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(self.folder_path, f"screen_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        self.play_sound()

    def play_sound(self):
        """Функция для воспроизведения звука"""
        if self.sound_enabled:
            sound_file = "screenshot.mp3"
            if os.path.exists(sound_file):
                mixer.init()
                mixer.music.load(sound_file)
                mixer.music.play()

    def toggle_sound(self):
        """Функция для переключения состояния звука"""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.tray_icon.notify("Звук включен!")
        else:
            self.tray_icon.notify("Звук выключен!")

    def toggle_autostart(self):
        """Функция для переключения состояния автозагрузки"""
        self.autostart_enabled = not self.autostart_enabled
        if self.autostart_enabled:
            autostart_manager.install_autostart()
            self.tray_icon.notify("Добавлен в автозагрузку!")
        else:
            autostart_manager.uninstall_autostart()
            self.tray_icon.notify("Удален из автозагрузки!")

    # noinspection SpellCheckingInspection
    # В методе create_tray_icon отключим проверки на опечатки
    def create_tray_icon(self):
        """Функция для создания иконки в трее и контекстного меню"""
        try:
            icon = Image.open("icon.png")  # Попытка открыть локальное изображение
        except FileNotFoundError:
            # Загрузка изображения по URL
            response = requests.get("https://icon-icons.com/icons2/1066/PNG/512/Camera_icon-icons.com_76883.png")
            icon = Image.open(io.BytesIO(response.content))

        menu_items = [
            pystray.MenuItem("Открыть папку", ScreenshotApp.open_shots_folder),
            pystray.MenuItem("Hohlovsky 2024", ScreenshotApp.site),
            pystray.MenuItem("Выход", self.exit_app)
        ]

        # Проверяем, существует ли файл screenshot.mp3
        if os.path.exists("screenshot.mp3"):
            menu_items.insert(0, pystray.MenuItem(r"Вкл\выкл звук", self.toggle_sound))

        # Проверяем, существует ли файл SmallScreenShooter.exe
        if os.path.exists("SmallScreenShooter.exe"):
            menu_items.insert(1, pystray.MenuItem(r"Вкл\выкл автозагрузку", self.toggle_autostart))

        menu = pystray.Menu(*menu_items)
        self.tray_icon = pystray.Icon("screenshot_app", icon, "Screen Shooter", menu)
        self.tray_icon.run()

    @staticmethod
    def open_shots_folder():
        """Функция для открытия папки со скриншотами"""
        if os.path.exists("screenshots"):
            os.startfile("screenshots")

    @staticmethod
    def site():
        """Функция для открытия сайта"""
        os.startfile("https://github.com/Hohlovsky")

    def start_keyboard_listener(self):
        """Функция для запуска уловителя клавиш"""
        keyboard.on_press_key("print screen", lambda _: self.take_screenshot())

    def exit_app(self):
        """Функция для выхода из приложения"""
        self.tray_icon.notify("Прощай, друг мой! Мне понравилось делать для тебя скриншоты. "
                              "Благодарю тебя за каждый момент, проведенный рядом. "
                              "Если когда-нибудь захочешь вернуться, знай, я рядом.")
        self.tray_icon.stop()

if __name__ == "__main__":
    app = ScreenshotApp()
