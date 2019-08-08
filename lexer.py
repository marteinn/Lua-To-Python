# Convert source to tokens

import re


def lexer(source):
    chars = list(source)
    tokens = []

    while len(chars):
        char = chars[0]

        if char == "\n":
            char = chars.pop(0)
            tokens.append({"type": "NL"})
            continue

        if chars[0:4] == ["-", "-", "[", "["]:
            comment = extract_multiline_comment(chars)
            tokens.append({"type": "MULTI-COMMENT", "value": comment})
            continue

        if chars[0:3] == ['n', 'i', 'l']:
            tokens.append({"type": "NIL", "value": 'nil'})
            del chars[0:3]
            continue

        if chars[0:2] == ["-", "-"]:
            comment = extract_comment(chars)
            tokens.append({"type": "COMMENT", "value": comment})
            continue

        if chars[0:3] == ["n", "o", "t"]:
            tokens.append({"type": "OP", "value": "not"})
            del chars[0:3]
            continue

        if chars[0:2] == ["~", "="]:
            tokens.append({"type": "OP", "value": "~="})
            del chars[0:2]
            continue

        if chars[0:2] == [".", "."]:
            tokens.append({"type": "OP", "value": ".."})
            del chars[0:2]
            continue

        if chars[0:2] == [">", "="]:
            tokens.append({"type": "OP", "value": ">="})
            del chars[0:2]
            continue

        if chars[0:2] == ["<", "="]:
            tokens.append({"type": "OP", "value": "<="})
            del chars[0:2]
            continue

        if is_operator(char):
            operator = extract_operator(chars)
            tokens.append({"type": "OP", "value": operator})
            continue

        if char == "'":
            string = extract_str("'", chars)
            tokens.append({"type": "STRING", "value": string})
            continue

        if char == '"':
            string = extract_str('"', chars)
            tokens.append({"type": "STRING", "value": string})
            continue

        if chars[0:2] == ["[", "["]:
            comment = extract_multiline_str(chars)
            tokens.append({"type": "STRING", "value": comment})
            continue

        if is_num(char):
            num = extract_num(chars)
            tokens.append({"type": "NUMBER", "value": num})
            continue

        if is_letter(char):
            word = extract_word(chars)

            if is_keyword(word):
                tokens.append({"type": "KEYWORD", "value": word})
                continue

            if word in ["true", "false"]:
                tokens.append({"type": "BOOLEAN", "value": word})
                continue

            tokens.append({"type": "NAME", "value": word})
            continue

        chars.pop(0)

    return tokens


def is_operator(char):
    return char in ["~=", "=", "==", "(", ")", "<", "+", "-", "*", ">", "<", "not"]


KEYWORDS = [
    "while", "do", "end", "if", "elseif", "else", "then", "function", "return"
]


def is_keyword(word):
    return word in KEYWORDS


def is_letter(char):
    return re.search(r'[a-zA-Z]|_', char)


def is_num(char):
    return re.search(r'[0-9]', char)


def extract_operator(chars):
    op = ""
    for letter in chars:
        if not is_operator(op+letter):
            break

        op = op+letter
    del chars[0:len(op)]
    return op


def extract_num(chars):
    num = ""
    for letter in chars:
        if not is_num(letter):
            break

        num = num+letter
    del chars[0:len(num)]
    return num


def extract_str(indicator, chars):
    out = ""
    for letter in chars[1:]:
        if letter == indicator:
            break

        out = out+letter
    del chars[0:len(out)+2]
    return out


def extract_word(chars):
    word = ""
    for letter in chars:
        if not is_letter(letter):
            break

        word = word+letter
    del chars[0:len(word)]
    return word


def extract_multiline_comment(chars):
    string_chars = "".join(chars)
    end_index = string_chars.index("--]]")

    val = string_chars[0:end_index]
    del chars[0:end_index+4]
    return val


def extract_comment(chars):
    string_chars = "".join(chars)
    end_index = string_chars.index("\n")

    val = string_chars[2:end_index]
    del chars[0:end_index]
    return val


def extract_multiline_str(chars):
    string_chars = "".join(chars)
    end_index = string_chars.index("]]")

    val = string_chars[2:end_index]
    del chars[0:end_index+2]
    return val
