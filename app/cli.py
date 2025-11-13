# app/cli.py
"""
CLI-версия программы (консольный интерфейс).
Используется для запуска внутри Docker или вручную через терминал.
"""

import sys
from .quine_core import run_tiny_on_source
from .log_db import init_db, add_log


def main(argv=None) -> int:
    """Основная точка входа CLI-приложения."""
    if argv is None:
        argv = sys.argv

    script_path = argv[0]
    input_text = " ".join(argv[1:])

    code, output = run_tiny_on_source(script_path, input_text)

    sys.stdout.write(output)
    add_log("Запуск тестов", output)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
