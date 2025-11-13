# app/quine_core.py

from pathlib import Path
import sys

def read_own_source(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def make_tiny_program_printing(f_text: str, user_input: str | None = None) -> str:
    """
    Возвращает TinyLang-программу, которая печатает результат применения f() к своему коду.
    Это и есть реализация логики неподвижной точки.
    """
    escaped = repr(f_text)

    lines = []
    # программа печатает текст, содержащий саму себя
    lines.append(f"PRINT {escaped}")
    return "\n".join(lines)

def interpret_tinylang(program_text: str) -> str:
    output_lines = []
    for line in program_text.splitlines():
        line = line.strip()
        if line.startswith("PRINT"):
            try:
                literal = line[len("PRINT"):].strip()
                text = eval(literal)
                output_lines.append(str(text))
            except Exception as e:
                output_lines.append(f"[Ошибка: {e}]")
    return "\n".join(output_lines)

def run_tiny_on_source(source_path: str, user_input: str | None = None) -> tuple[int, str]:
    """
    Читает собственный исходник, строит f(source) и выполняет как TinyLang.
    """
    source_code = read_own_source(source_path)

    # функция f: добавляем строку о вводе, если есть
    f_of_source = f"# Программа с фиксированной точкой\n{source_code}"
    if user_input:
        f_of_source += f"\n# Пользователь ввёл: {user_input}"

    tiny_program = make_tiny_program_printing(f_of_source, user_input)
    result = interpret_tinylang(tiny_program)
    return 0, result

def run_self_as_quine(user_input: str | None = None) -> str:
    current_file = Path(__file__).resolve()
    exit_code, result = run_tiny_on_source(str(current_file), user_input)
    return result if exit_code == 0 else f"[Ошибка TinyLang, код {exit_code}]"

