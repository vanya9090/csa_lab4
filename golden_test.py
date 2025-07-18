"""Golden тесты транслятора и машины.

Конфигурационные файлы: "golden/*.yml"
"""

import contextlib
import io
import logging
import os
import tempfile

import machine
import pytest
import translator

MAX_LOG = 50000


@pytest.mark.golden_test("golden/*.yml")
def test_translator_and_machine(golden, caplog):
    """Используется подход golden tests. У него не самая удачная реализация для
    python: https://pypi.org/project/pytest-golden/ , но знать об этом подходе
    крайне полезно.

    Принцип работы следующий: во внешних файлах специфицируются входные и
    выходные данные для теста. При запуске тестов происходит сравнение и если
    выход изменился -- выводится ошибка.

    Если вы меняете логику работы приложения -- то запускаете тесты с ключом:
    `cd python && poetry run pytest . -v --update-goldens`

    Это обновит файлы конфигурации, и вы можете закоммитить изменения в
    репозиторий, если они корректные.

    Формат файла описания теста -- YAML. Поля определяются доступом из теста к
    аргументу `golden` (`golden[key]` -- входные данные, `golden.out("key")` --
    выходные данные).

    Вход:

    - `in_source` -- исходный код
    - `in_stdin` -- данные на ввод процессора для симуляции
    - `is_char_io` -- выбор типа обработки ввода/вывода

    Выход:

    - `out_code` -- аннотированный машинный код
    - `out_stdout` -- стандартный вывод транслятора и симулятора
    - `out_log` -- журнал программы
    """
    # Установим уровень отладочного вывода на DEBUG
    caplog.set_level(logging.DEBUG)

    # Создаём временную папку для тестирования приложения.
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Готовим имена файлов для входных и выходных данных.
        source = os.path.join(tmpdirname, "source.bf")
        input_stream = os.path.join(tmpdirname, "input.txt")
        target = os.path.join(tmpdirname, "target.bin")
        target_hex = os.path.join(tmpdirname, "target.bin.hex")
        data = os.path.join(tmpdirname, "target.bin_data.bin")

        # Записываем входные данные в файлы. Данные берутся из теста.
        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["in_source"])
        with open(input_stream, "w", encoding="utf-8") as file:
            file.write(golden["in_stdin"])

        # Запускаем транслятор и собираем весь стандартный вывод в переменную
        # stdout
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            translator.main(source, target)
            print("============================================================")
            machine.main(target, data, input_stream, 400, 401, is_char_io=golden["is_char_io"])

        # Выходные данные также считываем в переменные.
        with open(target, "rb") as file:
            code = file.read()
        with open(target_hex, encoding="utf-8") as file:
            code_hex = file.read()

        # Проверяем, что ожидания соответствуют реальности.
        assert code == golden.out["out_code"]
        assert code_hex == golden.out["out_code_hex"]
        assert stdout.getvalue() == golden.out["out_stdout"]
        assert caplog.text[0:MAX_LOG] + "EOF" == golden.out["out_log"]