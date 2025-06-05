import re
class Lexer:
    def __init__(self):
        self.token_specs = [
            ('KEYWORD', r'\b(if|else|elif|while|for|in|def|class|return|break|continue|and|or|not|try|except|finally|raise|import|from|as|with|lambda|global|nonlocal|True|False|None|pass|del|yield|assert|async|await|match|case)\b'),
            ('BUILTIN', r'\b(print|input|len|str|int|float|list|dict|tuple|set|range|enumerate|zip|open|abs|max|min|sum|all|any|sorted|reversed|map|filter|type|isinstance|hasattr|getattr|setattr|dir|help|id|hex|oct|bin|format)\b'),
            ('NUMBER', r'\b\d+(\.\d+)?\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
            ('OPERATOR', r'==|!=|<=|>=|\+|-|\*|/|<|>'),
            ('ASSIGN', r'='),
            ('STRING', r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''),
            ('COLON', r':'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COMMA', r','),
            ('LBRACKET', r'\['),
            ('RBRACKET', r'\]'),
            ('COMMENT', r'#[^\n]*'),
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE', r'\n')
        ]
        self.regex = re.compile('|'.join(f'(?P<{name}>{pat})' for name, pat in self.token_specs))

    """Pozisyondan satır hesapla"""
    def get_line_column(self, code, pos):
        lines = code[:pos].split('\n')
        line = len(lines)
        column = len(lines[-1]) + 1
        return line, column

    def tokenize(self, code):
        tokens = []
        pos = 0 # o anki karakterin indexini tutar

        if not code.strip():
            return tokens

        for match in self.regex.finditer(code):
            if match.start() != pos:
                line, col = self.get_line_column(code, pos)
                invalid_char = code[pos:match.start()]
                raise ValueError(f"Invalid character '{invalid_char.strip()}' at line {line}, column {col}")

            token_type = match.lastgroup
            value = match.group()
            line, col = self.get_line_column(code, match.start())

            if token_type == 'STRING':
                if not self.is_valid_string(value):
                    raise ValueError(f"Unclosed string literal at line {line}, column {col}")

            # whitespace ve newline tokenlarını filtrele
            if token_type not in ('WHITESPACE', 'NEWLINE'):
                tokens.append((token_type, value, (line, col)))

            pos = match.end()

        if pos < len(code):
            line, col = self.get_line_column(code, pos)
            invalid_char = code[pos:].strip()
            if invalid_char:
                raise ValueError(f"Invalid character '{invalid_char}' at line {line}, column {col}")

        return tokens

    def tokenize_with_escape_highlighting(self, code):
        """String içindeki escape karakterlerini de renklendirir"""
        tokens = []
        pos = 0

        if not code.strip():
            return tokens

        for match in self.regex.finditer(code):
            if match.start() != pos:
                line, col = self.get_line_column(code, pos)
                invalid_char = code[pos:match.start()]
                raise ValueError(f"Invalid character '{invalid_char.strip()}' at line {line}, column {col}")

            token_type = match.lastgroup
            value = match.group()
            line, col = self.get_line_column(code, match.start())

            # String literal ise escape karakterleri için özel işlem
            if token_type == 'STRING':
                if not self.is_valid_string(value):
                    raise ValueError(f"Unclosed string literal at line {line}, column {col}")

                # String içindeki escape karakterlerini parse et
                string_tokens = self.parse_string_with_escapes(value, line, col)
                tokens.extend(string_tokens)
            else:
                if token_type not in ('WHITESPACE', 'NEWLINE'):
                    tokens.append((token_type, value, (line, col)))

            pos = match.end()

        if pos < len(code):
            line, col = self.get_line_column(code, pos)
            invalid_char = code[pos:].strip()
            if invalid_char:
                raise ValueError(f"Invalid character '{invalid_char}' at line {line}, column {col}")

        return tokens


    #String içindeki escape karakterlerini ayrı tokenlar olarak parse eder
    def parse_string_with_escapes(self, string_value, start_line, start_col):
        tokens = []
        quote_char = string_value[0]  # " veya '
        inner_content = string_value[1:-1]  # Tırnak işaretlerini çıkar

        # String başlangıç tırnağı
        tokens.append(('STRING_QUOTE', quote_char, (start_line, start_col)))

        # Escape patterni
        escape_pattern = r'\\[nrtbfav\\\'\"0]|\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}'

        pos = 0
        current_line = start_line
        current_col = start_col + 1  # ilk tırnak sonrası

        for match in re.finditer(escape_pattern, inner_content):
            # escape öncesi normal string kısmı
            if match.start() > pos:
                normal_part = inner_content[pos:match.start()]
                if normal_part:
                    tokens.append(('STRING_CONTENT', normal_part, (current_line, current_col)))
                    current_col += len(normal_part)

            # escape karakteri
            escape_seq = match.group()
            tokens.append(('ESCAPE_CHAR', escape_seq, (current_line, current_col)))
            current_col += len(escape_seq)
            pos = match.end()

        # son kısım
        if pos < len(inner_content):
            remaining = inner_content[pos:]
            tokens.append(('STRING_CONTENT', remaining, (current_line, current_col)))

        # string bitiş tırnağı
        tokens.append(('STRING_QUOTE', quote_char, (current_line, start_col + len(string_value) - 1)))

        return tokens

    def is_valid_string(self, string_value):
        """String literal'ın geçerli olup olmadığını kontrol et"""
        if len(string_value) < 2:
            return False

        if string_value.startswith('"'):
            return string_value.endswith('"')
        elif string_value.startswith("'"):
            return string_value.endswith("'")

        return False


if __name__ == "__main__":
    lexer = Lexer()
    test_cases = [
        'if x == 42: print("Hello") # comment',
        'if x > 10: print("big") elif x > 5: print("medium") else: print("small")',
        'def add(a, b): return a + b',
        'for i in range(10): x = 3.14',
        'class MyClass: pass',
        'x = [1, 2, 3] # list example',
        'total = sum([1, 2, 3])',
        'text_length = len("Hello")',
        'x123 = 456',
        'a = "test \\"quote\\"" # Escaped quotes',
        'try: x = 1\nexcept ValueError: pass',
        'raise ValueError("Error")',
        'try: x = 1\nexcept: pass\nfinally: print("Done")',
    ]

    print("=== Normal Tokenization Test ===")
    for code in test_cases:
        try:
            print(f"Input: '{code}'")
            tokens = lexer.tokenize(code)
            print(f"Output: {[(t[0], t[1]) for t in tokens]}")
        except ValueError as e:
            print(f"Error: {e}")
        print("-" * 50)

    print("\n=== Escape Highlighting Test ===")
    escape_test_cases = [
        'a = "test \\"quote\\""',
        'b = "newline\\nchar"',
        'c = "tab\\tchar"',
    ]

    for code in escape_test_cases:
        try:
            print(f"Input: '{code}'")
            tokens = lexer.tokenize_with_escape_highlighting(code)
            print(f"Output: {[(t[0], t[1]) for t in tokens]}")
        except ValueError as e:
            print(f"Error: {e}")
        print("-" * 50)