# app/tinylang.py
"""
Модуль интерпретатора языка TinyLang.
TinyLang — минимальный учебный язык, демонстрирующий работу теоремы
о неподвижной точке. Поддерживает одну команду:

    PRINT <строковый литерал Python>

Пример программы на TinyLang:
    PRINT 'Привет, мир!'

Комментарии начинаются с символа '#'.
"""

import ast
from typing import Optional


class TinyLangError(Exception):
    """Исключение при ошибках интерпретации TinyLang."""
    pass


def interpret_tinylang(program_text: str, input_text: Optional[str] = "") -> str:
    """
    Интерпретирует программу TinyLang и возвращает результат.

    :param program_text: текст программы
    :param input_text: вход (не используется, для совместимости)
    :return: результат выполнения программы
    """
    out_lines = []
    lines = program_text.splitlines()

    for ln_no, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        # Поддерживаем только команду PRINT
        if line.upper().startswith("PRINT "):
            literal_part = line[6:].strip()
            try:
                value = ast.literal_eval(literal_part)
            except Exception as e:
                raise TinyLangError(f"Ошибка парсинга литерала в строке {ln_no}: {e!s}")
            out_lines.append(str(value))
            continue

        raise TinyLangError(f"Неизвестная команда в строке {ln_no}: {line!r}")

    return "\n".join(out_lines)
