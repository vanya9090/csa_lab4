# Lisp. Транслятор и модель

---

- Выполнил: Миронов Иван Николаевич
- `lisp | cisc | neum | mc | tick | binary | stream | mem | cstr | prob2 | cache`


## Язык программирования
Lisp


``` ebnf
<program> ::= <s_expression> | <s_expression> <s_expression>
<s_expression> ::= "(" <atom> | <atom> <s_expression> | <s_expression> <s_expression> | <operation> <s_expression>")"

<atom> ::= <letter> <atom_part> | <number>
<string_atom> = " <atom_part> "
<atom_part> ::= <empty> | <letter> <atom_part> | <digit> <atom_part>
<number> ::= <digit> | <digit> <number>
<letter> ::= "a" | "b" | ... | "z"
<digit> ::= "0" | "1" | ... | "9"
<operation> := '+' | '-' | '*' | '/' | '%' | '=' | '!=' | '>' | '<=' 
<empty> ::= " "

comment ::= ; <any symbols>
```
Пример программы:
```lisp
(begin
    (defun factorial (begin x)
        (begin
            (cond (<= x 1) (begin 1)
                  (> x 1)  (begin (* x (factorial (- x 1))))
            )
        )
    )
    (print (factorial 5))
)
```

- Стратегия вычисления: вызов по значению (eager)
- Область видимости: локальная в рамках функций
- Типизация: неявная, динамическая
- Литералы: целые числа (int32), строки (cstring)
- Поддерживается рекурсия

Операции:
- `(print expr)` - вывести результат выполнения выражения
- `(input)` - ввод строки или числа
- `(cond (condition1 result1) (condition2 result2) ...)` - если `condition_i`=T, выполнить `result_i`. `condition_i=<s_expression> | <atom>`, `result_i=<s_expression>`
- `(defun name (arg1, arg2, ...) body)` - объявление функции с именем `name=<atom>`, аргументами `arg1=<atom>, arg2=<atom>, ...` и телом функции `body=<s_expression>`
- `(call fname)` - вызов функции
- `(begin expr_1 expr_2 ...)` - вычисляет все `expr_i`, результатом выражения является значение `expr_last`
- `(setq var expr)` - вычисляет `expr` и присваивает по адресу переменной `var`
- `(while (cond body) body)` - цикл "пока"
- `(cond (cond_i) (body_i) ...)` - все условия последовательно проверяются, результат выполнения - последнее тело с верным условием
- `(alloc n)` - выделяет `n` машинных слов в куче, возвращает адрес первого слова
- `(store addr value)` - записывает `value` по адресу `addr`
- `(deref addr)` - возвращает слово по адресу `addr`
- `(cons value addr)` - создает новый узел списка в куче 
- `(car addr)` - возвращает адрес первого узла в списка
- `(cdr addr)` - возвращает адрес второго узла в списка
- `(insert value, addr)` - вставляет элемент со значением `value` после узла `addr`
- `(+ <atom1> <atom2>)` -  суммирование операндов
- `(- <atom1> <atom2>)` -  вычитание операндов
- `(/ <atom1> <atom2>)` - деление операндов
- `(* <atom1> <atom2>)` - умножение операндов
- `(% <atom1> <atom2>)` - взятие остатка операндов
- `(and <atom1> <atom2>)` - логическое И операндов
- `(or <atom1> <atom2>)`- логическое ИЛИ операндов
- `(= <atom1> <atom2>)` - проверка, что операнды равны
- `(!= <atom1> <atom2>)`- проверка, что операнды не равны
- `(> <atom1> <atom2>)` - проверка, что операнд1 > операнд2
- `(<= <atom1> <atom2>)` - проверка, что операнд1 <= операнд2


## Орагнизация памяти
- Архитектура Фон Неймана - общая память для инструкций и данных
- Размер машинного слова - 32 бит
- Память адресуется по машинным словам

### Разделы памяти
Память состоит из 4х секций:
- Инструкции хранятся в области `.text`, начиная с адреса 0
- Статические данные (константные строки и переменные) хранятся в области `.data`, начиная с адреса 200
- Динамические данные (динамические строки и списки) хранятся в `heap`, начиная с адреса 500, куча растет к большим адресам. Регистр `RHP` был назначен, как регистр для выделения памяти на куче. Явное управление (alloc).
- фреймы функций (локальные переменные и адреса возврата) хранятся на `stack`, начиная с адреса 1024, стек растет к меньшим адресам. Регистр `RSP` был назначен, как регистр для перемещения по стеку.
```
+-----------------------+
|    000: .text         | Код
+-----------------------+
|    200: .data         | Статические данные
+-----------------------+
|    500: heap (↓)      | Динамическая память
+-----------------------+
|   1024: stack (↑)     | Стек вызовов
+-----------------------+
```

Все глобальные перменные хранятся в области статических данных, локальные переменные хранятся в стеке.
- Константные строки - строки, заданные в программе
- Динамические строки - строки, требующие заранее аллоцированного места на куче, заранее неизвестны
- Списки - структура данных, каждый узел которой состоит из двух машинных слов: [значение][адрес следующего элемента]. 
#### Строки
- Строки сохраняются посимвольно, по одному символу в машинное слово.
- Значением строкового литерала является первый элемент строки
- Передача значения строкового литерала осуществляется передачей адреса первого элемента строки
- Для выделения памяти под динамическую строку можно использовать команду `(alloc n)`, которая вернет адрес первого символа будущей строки и выделит `n` машинных слов, в которые можно поместить `n` символов
#### Списки
- Каждый узел списка состоит из двух машинных слов: [значение][адрес следующего элемента]
- Значением списочной переменной является адрес первого элемента списка
- Для выделения памяти используется `(alloc n)`, либо команда `(cons value addr)`, которая выделяет место на куче под один элемент.
- Основыми командами для работы со списками являются `cdr` и `car`, которые возращают адрес первого элемента и адрес второго элемента.
- Также реализована команда `(insert value addr)`, которая предназначена для вставки элемента в любое место списка
### Регистры
После вычисления любого из выражений результат кладется в один из свободных регистров. Также регистры используются для временного хранения значений при выполнении операции.

Переменные не отображаются на регистры

- R_0, ... R_5 - 32-битные регистры общего назначения
- RSP - указатель стека, аппаратно поддерживает инкремент и декремент за 1 такт
- RHP - указатель кучи

## Система команд
- Переменная длина инструкций 
- Инструкции зачастую требуют несколько тактов для выполнения
- MMIO - ввод/вывод происходит с помощью записи/чтения значений из ячеек памяти, являющихся интерфесами к устройствам ввода-вывода
- Инструкции `NADD, NMUL, NSUB, NAND, NOR` поддерживают переменное количество операндов (от 1 до 31)
### Кодирование инструкций
![isa](resources/isa.png)
Прямое отображение - опкод выступает в роли адреса микрокода
### Адресация
- immediate - значение берется непосредственно из команды
- direct - значение берется из памяти по адресу
- indirect - значение берется из памяти по адресу адреса
- stack - команда работает со RSP (push, pop)

Также команда может быть безадресной
### Принцип работы с данными
Каждая арифметическая/логическая операция включают в себя следующие типы:
- Register-to-Register - вычисления проводятся с регистрами и сохраняются в регистр
- Memory-to-Memory - вычисления проводятся с ячейками памяти и сохраняются в память
- Memory-to-Register - вычисления проводятся с ячейками памяти и сохраняются в регистр

Каждая из команд является комбинацией различных типов адресаций и принципов работы с данными.

### Циклы исполнения
- instruction fetch - 4 такта (переход на нужный адрес в памяти микрокоманд)
- operand fetch - 1-4 такта (выборка операндов с нужной адресацией)
- execute - 1 такт (выполнение АЛУ)
- memory access - 1-3 такта


## Транслятор
Транслятор реализован в [translator.py](src/translator.py)

Входные данные:
На вход транслятору подается название файла с исходным кодом на языке Lisp, а также название выходного файла.

Выходные данные:
Транслятор сохраняет бинарный машинный код, 16-ричное представление с мнемониками и статическую память в файлы.

Использование:
```
python translator.py <input> <output>

входные данные:
input - исходный код

выходные данные: 
output - бинарный машинный код
output.hex - 16-ричное представление
output_data.bin - бинарная статическая память
```

Этапы трансляции программы:
- tokenize - разбивает исходный код на следующие типы токенов
    - скобки (для группировки выражений)
    - атомарные значения (последовательность цифр, строковые литералы, идентификаторы)
- parse - рекурсивный спуск по токенам, возвращает AST
    - `Atom` - листы дерева
    - `s-expr` - вершины, состоящие из операторов и операндов
- generate - обход AST и перевод каждой операции в инструкции процессора

## Модель процессора
Модель процессора реализована в [machine.py](src/machine.py)
Микрокод реализован в [microprogram.py](src/microprogram.py)

Использование:
```
python machine.py <code> <data> <input> <is_char_io>

входные данные:
code - бинарный машинный код
data - бинарная статическая память
input - входные данные процессора
is_char_io - тип ввода/вывода

выходные данные: 
stdout - выходные данные процессора и логи
```

### Datapath
![datapath](resources/datapath.png)
### Control unit
![datapath](resources/control.png)


## Тестирование
Тестирование выполняется при помощи golden test-ов.
- [golden/hello.yml](golden/hello.yml) - напечатать hello world
- [golden/cat.yml](golden/cat.yml) - печатать данные, поданные через ввод (размер ввода потенциально бесконечен)
- [golden/hello_user_name.yml](golden/hello_user_name.yml) - запросить у пользователя его имя, считать его, вывести на экран приветствие
- [golden/sort.yml](golden/sort.yml) - пользователь загружает в систему список чисел и выводит их в отсортированном формате
- [golden/bigint.yml](golden/bigint.yml) - арифметика двойной точности
- [golden/prob2.yml](golden/prob2.yml) - проблема 2 из проекта Эйлера
- [golden/factorial.yml](golden/factorial.yml) - рекурсивное вычисление факториала

Скрипт выполнения golden тестов: [golden_test.py](golden_test.py)
Запуск тестов: `pytest -v`
Обновление тестов: `pytest -v --update-goldens`