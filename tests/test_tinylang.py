"""
Модуль автоматического тестирования программы с неподвижной точкой.
Используется pytest. Проверяются:
 - интерпретатор TinyLang,
 - функции ядра (quine_core),
 - работа базы данных логов,
 - консольный интерфейс (CLI),
 - сборка и запуск Docker (если установлен).
"""

import subprocess
import sys
import os
import sqlite3
from pathlib import Path
import pytest

# Импорт модулей приложения
from app.tinylang import interpret_tinylang
from app.quine_core import (
    make_tiny_program_printing,
    run_tiny_on_source,
    read_own_source,
)
from app.log_db import init_db, add_log, DB_PATH

# ==========================================================
# === ТЕСТЫ МОДУЛЯ TINYLANG ===
# ==========================================================

def test_tinylang_basic():
    """Проверка базовой работы интерпретатора TinyLang."""
    program = "PRINT 'Привет'\nPRINT 'Мир'"
    result = interpret_tinylang(program)
    assert "Привет" in result
    assert "Мир" in result


def test_tinylang_invalid_literal():
    """Проверка реакции на некорректный литерал."""
    bad_program = "PRINT привет"
    with pytest.raises(Exception):
        interpret_tinylang(bad_program)


# ==========================================================
# === ТЕСТЫ МОДУЛЯ QUINE_CORE ===
# ==========================================================

def test_make_tiny_program():
    """Проверка генерации программы TinyLang из строки."""
    code = make_tiny_program_printing("ABC")
    assert code.startswith("PRINT")
    assert "ABC" in code


def test_quine_fixed_point(tmp_path):
    """Проверяет, что программа реализует логику неподвижной точки."""
    src = tmp_path / "sample_program.py"
    content = "print('demo')"
    src.write_text(content, encoding="utf-8")

    code, result = run_tiny_on_source(str(src))
    assert code == 0
    assert content in result  # исходный код должен быть в выводе


def test_read_own_source(tmp_path):
    """Проверка чтения исходного файла."""
    f = tmp_path / "source.txt"
    f.write_text("data", encoding="utf-8")
    assert read_own_source(str(f)) == "data"


# ==========================================================
# === ТЕСТЫ БАЗЫ ДАННЫХ LOG_DB ===
# ==========================================================

def test_database_creation_and_logging(tmp_path):
    """Проверка инициализации базы данных и записи логов."""
    test_db = tmp_path / "test_logs.db"

    # Переопределяем путь к БД
    from app import log_db
    log_db.DB_PATH = test_db

    # Инициализация и запись
    init_db()
    add_log("Test", "Успешно")

    conn = sqlite3.connect(test_db)
    cur = conn.cursor()
    cur.execute("SELECT action, result FROM logs")
    rows = cur.fetchall()
    conn.close()

    assert len(rows) >= 1
    assert rows[0][0] == "Test"
    assert "Успешно" in rows[0][1]


# ==========================================================
# === ТЕСТЫ CLI-ВЕРСИИ ===
# ==========================================================

@pytest.mark.parametrize("args", [[], ["Hello_World"]])
def test_cli_execution(args):
    """Проверка CLI: выполнение без и с аргументами."""
    result = subprocess.run(
        [sys.executable, "-m", "app.cli", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8", errors="ignore",

    )
    assert result.returncode == 0
    assert "python" in result.stdout or "import" in result.stdout

