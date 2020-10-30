class Token:
    KEYWORD = [
        'if',
        'elif',
        'else',
        'while',
        'break',
        'func',
        'return'
    ]

    CIRCUIT = [
        'I',
        'X',
        'Y',
        'Z',
        'H',
        'S',
        'T',
        'V',
        'V_H',
        'SWAP',
        'measure'
    ]

    SEPARATOR = [
        '(',
        ')',
        '[',
        ']',
        '\n',
        '\t'
    ]

    OPERATOR = [
        '+',
        '-',
        '*',
        '/',
        '>',
        '<',
        '=',
        '>=',
        '<=',
        '==',
        '+=',
        '-=',
        '*=',
        '/=',
        '!',
        '&',
        '|'
    ]

    def isOPERATOR(ch):
        singleOp = ['+', '-', '*', '/', '>', '<', '=', '&', '|', '!']
        return ch in singleOp
