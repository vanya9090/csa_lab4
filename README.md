# Lisp. Транслятор и модель

**Table of Contents**

- [Lisp. Транслятор и модель](#lisp-транслятор-и-модель)
    - [Язык программирования](#язык-программирования)

---

- Выполнил: Миронов Иван Николаевич
- `lisp | cisc | neum | mc | tick | binary | stream | mem | cstr | prob2 | cache`


## Язык программирования
Lisp


``` ebnf
<program> ::= <s_expression> | <s_expression> <s_expression>
<s_expression> ::= "(" <atom> | <atom> <s_expression> | <s_expression> <s_expression> | <operation> <s_expression>")"

<atom> ::= <letter> <atom_part> | <number>
<string_atom> = "\"" <atom_part> "\""
<atom_part> ::= <empty> | <letter> <atom_part> | <digit> <atom_part>
<number> ::= <digit> | <digit> <number>
<letter> ::= "a" | "b" | ... | "z"
<digit> ::= "0" | "1" | ... | "9"
operation := '+' | '-' | '*' | '/' | '%' | '=' | '!=' | '<' | '>' | '<=' | '>='
<empty> ::= " "

comment ::= ; <any symbols>
``