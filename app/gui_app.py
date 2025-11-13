# app/gui_app.py
"""
Графический интерфейс программы на PySide6.
Демонстрирует работу программы с неподвижной точкой (Fixed Point Logic).
Позволяет:
 - выполнить программу локально;
 - запустить в Docker;
 - запустить тесты;
 - записывать результаты в базу данных SQLite.
"""

import sys
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QLabel, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt

from .quine_core import run_tiny_on_source
from .log_db import init_db, add_log


class QuineGUI(QWidget):
    """Класс графического интерфейса программы."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Программа с неподвижной точкой (Fixed Point Logic)")
        self.resize(900, 600)

        # Инициализация базы данных логов
        init_db()

        # Основной вертикальный макет
        self.layout = QVBoxLayout()

        # Поле ввода
        self.label = QLabel("Введите входные данные (будут включены в результат):")
        self.layout.addWidget(self.label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("например: Привет, мир!")
        self.layout.addWidget(self.input_field)

        # Кнопки действий
        self.run_button = QPushButton("Выполнить программу локально")
        self.run_button.clicked.connect(self.run_local)
        self.layout.addWidget(self.run_button)

        '''
        self.docker_button = QPushButton("Запустить в Docker")
        self.docker_button.clicked.connect(self.run_in_docker)
        self.layout.addWidget(self.docker_button)
        '''

        self.test_button = QPushButton("Запустить тесты (pytest)")
        self.test_button.clicked.connect(self.run_tests)
        self.layout.addWidget(self.test_button)

        # Поле вывода
        self.output_label = QLabel("Результат выполнения:")
        self.layout.addWidget(self.output_label)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setLineWrapMode(QTextEdit.NoWrap)
        self.layout.addWidget(self.output_area)

        # Устанавливаем основной макет
        self.setLayout(self.layout)

    # ============================================================
    # === Методы кнопок ===
    # ============================================================

    def run_local(self):
        """Запуск программы локально."""
        user_input = self.input_field.text().strip()
        code, result = run_tiny_on_source(str(Path(__file__).resolve()), user_input)

        # Отображаем результат
        self.output_area.setPlainText(result)
        add_log("Запуск локальный", result)

        if code != 0:
            QMessageBox.warning(self, "Ошибка", f"Код завершения: {code}")
        
    def run_in_docker(self):
        """Сборка и запуск программы в Docker."""
        try:
            subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE)
        except Exception:
            QMessageBox.critical(self, "Ошибка", "Docker не установлен или не запущен.")
            return

        project_root = Path(__file__).parent.parent.resolve()
        dockerfile = project_root / "Dockerfile"

        if not dockerfile.exists():
            QMessageBox.critical(self, "Ошибка", "Файл Dockerfile не найден.")
            return

        try:
            # Сборка Docker-образа
            build_cmd = ["docker", "build", "-t", "fixed_quine_app", str(project_root)]
            self.output_area.setPlainText("Сборка Docker-образа...\n")
            subprocess.run(build_cmd, check=True, text=True, encoding="utf-8", errors="ignore")

            # Запуск контейнера
            run_cmd = ["docker", "run", "--rm", "-it", "-v", "fixed_quine_app"]
            self.output_area.append("Запуск контейнера...\n")
            result = subprocess.run(
                run_cmd, check=True, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore"
            )
            output = result.stdout

            self.output_area.append("=== РЕЗУЛЬТАТ ===\n")
            self.output_area.append(output)
            add_log("Запуск Docker", output)

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Ошибка Docker", f"Не удалось запустить контейнер:\n{e}")
        

    def run_tests(self):
        """Запуск тестов с помощью pytest."""
        try:
            self.output_area.setPlainText("Запуск тестов pytest...\n")
            result = subprocess.run(
                ["python", "-m", "pytest", "-v"],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )
            output = result.stdout
            self.output_area.append(output)
            add_log("Запуск тестов", output)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить тесты:\n{e}")


def main():
    """Точка входа GUI-приложения."""
    app = QApplication(sys.argv)
    gui = QuineGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
