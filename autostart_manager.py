# autostart_manager.py
import os
from win32com.client import Dispatch

# Путь к папке автозагрузки
AUTOSTART_FOLDER = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
# Имя ярлыка в папке автозагрузки
SHORTCUT_NAME = "SmallScreenShooter.lnk"


def is_installed():
    """Проверяет, установлено ли приложение в автозагрузке."""
    return os.path.exists(os.path.join(AUTOSTART_FOLDER, SHORTCUT_NAME))


def install_autostart():
    """Устанавливает приложение в автозагрузку."""
    if not is_installed():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        create_shortcut(os.path.join(current_directory, 'SmallScreenShooter.exe'),
                        os.path.join(AUTOSTART_FOLDER, SHORTCUT_NAME), current_directory)


def uninstall_autostart():
    """Удаляет приложение из автозагрузки."""
    if is_installed():
        os.remove(os.path.join(AUTOSTART_FOLDER, SHORTCUT_NAME))


def create_shortcut(target, shortcut_path, current_directory):
    """Создает ярлык."""
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = current_directory
    shortcut.save()
