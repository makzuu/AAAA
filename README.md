## Intructions

### LABELS

syntax: `<LABEL>:`

### NOP

syntax: `NOP`

desc: no operation

### MOV

syntax: `MOV <SRC>, <DST>`

desc: mov `<src>` to `<dst>`

### SWP

syntax: `SWP`

desc: swap `acc` and `bak`

### SAV

syntax: `SAV`

desc: sav `acc` to `bak`

### ADD

syntax: `ADD <SRC>`

desc: add `<src>` to `acc`

### SUB

syntax: `SUB <SRC>`

desc: subtract `<src>` from `acc`

### NEG

syntax: `NEG`

desc: negate `acc`

### JMP

syntax: `JMP <LABEL>`

desc: jump to `<label>`

### JEZ

syntax: `JEZ <LABEL>`

desc: jump to `<label>` if `acc = 0`

### JNZ

syntax: `JNZ <LABEL>`

desc: jump to `<label>` if `acc != 0`

### JGZ

syntax: `JGZ <LABEL>`

desc: jump to `<label>` if `acc > 0`

### JLZ

syntax: `JLZ <LABEL>`

desc: jump to `<label>` if `acc < 0`

### JRO

syntax: `JRO <SRC>`

desc: jump to relative offset `<src>`

## Tokens

```python
class TokenType(Enum):
    EOF                 =  -1
    NL                  =   0
    COMMA               =   1
    COLON               =   2
    ASTERISK            =   3
    OPEN_PAREN          =   4
    CLOSE_PAREN         =   5

    # Keywords
    NOP                 = 101
    MOV                 = 102
    SWP                 = 103
    SAV                 = 104
    ADD                 = 105
    SUB                 = 106
    NEG                 = 107
    JMP                 = 108
    JEZ                 = 109
    JNZ                 = 110
    JGZ                 = 111
    JLZ                 = 112
    JRO                 = 113

    PUSH                = 114
    POP                 = 115
    READ                = 116
    WRITE               = 117
    DEFINE              = 118
    CALL                = 119
    RET                 = 120

    IDENT               = 201
    NUMBER              = 202
```

## Grammar

- `{}`: zero or more.
- `[]`: zero or one.
- `+`: one or more of whatever is to the left.
- `()`: grouping.
- `|`: OR.

```
program ::= {statement}

statement ::=
	| nop nl
	| mov expression "," dst nl
	| swp nl
	| sav nl
	| add expression nl
	| sub expression nl
	| neg nl
	| jmp indent nl
	| jez indent nl
	| jnz indent nl
	| jgz indent nl
	| jlz indent nl
	| jro expression nl

	| indent ":"
	| push expression nl
	| pop dst nl
	| read nl
	| write expression nl
	| define indent "," expression nl
	| call indent nl
	| ret nl

dst ::=
	| acc
	| bp "(" expression ")"
	| "*" bp "(" expression ")"
	| sp "(" expression ")"
	| "*" sp "(" expression ")"

expression ::=
	| number
	| nil
	| acc
	| const
	| bp "(" expression ")"
	| "*" bp "(" expression ")"
	| sp "(" expression ")"
	| "*" sp "(" expression ")"

nl ::= nl+
```
