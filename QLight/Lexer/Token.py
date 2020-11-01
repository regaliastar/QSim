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
        '{',
        '}',
        ':'
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

    def isKEYWORD(str):
        return str in Token.KEYWORD

    def isCIRCUIT(str):
        return str in Token.CIRCUIT

    def isSEPARATOR(str):
        return str in Token.SEPARATOR