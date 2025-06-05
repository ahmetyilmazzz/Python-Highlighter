from tkinter import ttk

from lexer import Lexer

# Gramer bilgileri
GRAMMAR_INFO = {
    "Program": "Program: Kodun ana yapısı, tüm ifadeleri içerir.",
    "IfStatement": "if ifadesi: Koşullu kontrol yapısı, bir koşul doğruysa kod bloğunu çalıştırır.",
    "Assignment": "atama: Bir değişkene değer atar (örneğin, x = 5).",
    "FunctionDef": "fonksiyon tanımı: Yeni bir fonksiyon oluşturur (örneğin, def add(a, b)).",
    "WhileStatement": "while döngüsü: Koşul doğru olduğu sürece kod bloğunu tekrarlar.",
    "ForStatement": "for döngüsü: Bir dizi üzerinde döngü yapar (örneğin, for i in range(10)).",
    "ClassDef": "sınıf tanımı: Yeni bir sınıf oluşturur (örneğin, class MyClass).",
    "Return": "return ifadesi: Fonksiyondan değer döndürür.",
    "TryStatement": "try-except: Hata yakalama yapısı, hataları yönetir.",
    "ExceptClause": "except bloğu: Hataları yakalar ve işler.",
    "Raise": "raise ifadesi: Hata fırlatır (örneğin, raise ValueError).",
    "MatchStatement": "match ifadesi: Desen eşleştirme yapar (Python 3.10+).",
    "CaseClause": "case bloğu: Match ifadesinde bir desenle eşleşen kod bloğu.",
    "ExpressionStmt": "ifade: Tek başına çalışan bir ifade (örneğin, print(x)).",
    "LogicalExpr": "mantıksal ifade: and/or operatörleriyle ifadeleri birleştirir.",
    "ComparisonExpr": "karşılaştırma: ==, !=, <, > gibi operatörlerle karşılaştırır.",
    "AddExpr": "toplama/çıkarma: + veya - operatörleriyle işlem yapar.",
    "MulExpr": "çarpma/bölme: * veya / operatörleriyle işlem yapar.",
    "Term": "terim: Bir değişken, sayı veya metin gibi temel bir ifade.",
    "Number": "sayı: Sayısal bir değer (örneğin, 42).",
    "String": "metin: Tırnak içindeki metin (örneğin, 'hello').",
    "StringLiteral": "metin literali: Tırnaklar ve kaçış karakterleri dahil metin.",
    "ListLiteral": "liste: Köşeli parantez içindeki değerler (örneğin, [1, 2, 3]).",
    "FunctionCall": "fonksiyon çağrısı: Bir fonksiyonu çağırır (örneğin, print(x)).",
    "Constant": "sabit: True, False veya None gibi sabit değerler.",
    "NotExpr": "not ifadesi: Mantıksal olumsuzlama yapar (örneğin, not True).",
    "ParenExpr": "parantezli ifade: Parantez içindeki ifade (örneğin, (x + 1))."
}

# Düğüm türü çevirileri
NODE_TYPE_MAP = {
    "Program": "Program",
    "IfStatement": "if ifadesi",
    "Assignment": "atama",
    "FunctionDef": "fonksiyon tanımı",
    "WhileStatement": "while döngüsü",
    "ForStatement": "for döngüsü",
    "ClassDef": "sınıf tanımı",
    "Return": "return ifadesi",
    "TryStatement": "try-except",
    "ExceptClause": "except bloğu",
    "Raise": "raise ifadesi",
    "MatchStatement": "match ifadesi",
    "CaseClause": "case bloğu",
    "ExpressionStmt": "ifade",
    "LogicalExpr": "mantıksal ifade",
    "ComparisonExpr": "karşılaştırma",
    "AddExpr": "toplama/çıkarma",
    "MulExpr": "çarpma/bölme",
    "Term": "terim",
    "Number": "sayı",
    "String": "metin",
    "StringLiteral": "metin literali",
    "ListLiteral": "liste",
    "FunctionCall": "fonksiyon çağrısı",
    "Constant": "sabit",
    "NotExpr": "not ifadesi",
    "ParenExpr": "parantezli ifade"
}

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.tree = []

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return

    def get_line_column(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos][2]
        return (0, 0)

    def consume(self, expected_kind):
        current = self.peek()
        if current and current[0] == expected_kind:
            self.pos += 1
            return current
        else:
            line, col = self.get_line_column()
            current_desc = f"'{current[1]}' ({current[0]})" if current else "end of input"
            raise SyntaxError(f"{expected_kind} expected at line {line}, column {col}, found: {current_desc}")

    def consume_keyword(self, expected_keyword):
        current = self.peek()
        if current and current[0] == 'KEYWORD' and current[1] == expected_keyword:
            self.pos += 1
            return current
        else:
            line, col = self.get_line_column()
            current_desc = f"'{current[1]}'" if current else "end of input"
            raise SyntaxError(f"'{expected_keyword}' expected at line {line}, column {col}, found: {current_desc}")

    def parse(self):
        self.tree = []
        if not self.tokens:
            return
        self.parse_program()
        if self.peek() is not None:
            line, col = self.get_line_column()
            current = self.peek()
            raise SyntaxError(f"Unexpected token '{current[1]}' ({current[0]}) at line {line}, column {col}")

    def populate_treeview(self, treeview):
        treeview.delete(*treeview.get_children())
        self._populate_treeview_recursive(self.tree, treeview, "")

    def _populate_treeview_recursive(self, nodes, treeview, parent, line=1):
        for node in nodes:
            if isinstance(node, tuple):
                node_type, value = node
                node_type_display = NODE_TYPE_MAP.get(node_type, node_type)
                detail = str(value) if not isinstance(value, list) else ""
                grammar = GRAMMAR_INFO.get(node_type, "")
                tag = f"line_{line}" if isinstance(value, list) else node_type.lower()
                treeview.insert(parent, "end", values=(node_type_display, detail, grammar), tags=(tag,))
                if isinstance(value, list):
                    self._populate_treeview_recursive(value, treeview, treeview.get_children()[-1], line)
            line += 1

    def parse_program(self):
        self.tree.append(("Program", []))
        self.parse_statement_list(self.tree[-1][1])

    def parse_statement_list(self, parent):
        parsed_statements = 0
        max_statements = 1000
        while self.peek() is not None and parsed_statements < max_statements:
            old_pos = self.pos
            current = self.peek()
            if current and current[0] in ('STRING_QUOTE', 'STRING_CONTENT', 'ESCAPE_CHAR'):
                self.pos += 1
                continue
            parent.append(self.parse_statement())
            if self.pos == old_pos:
                line, col = self.get_line_column()
                current = self.peek()
                raise SyntaxError(
                    f"Unable to parse statement at line {line}, column {col}: '{current[1]}' ({current[0]})")
            parsed_statements += 1
        if parsed_statements >= max_statements:
            raise SyntaxError("Too many statements - possible infinite loop in parser")

    def parse_statement(self):
        current = self.peek()
        if not current:
            return
        if current[0] in ('STRING_QUOTE', 'STRING_CONTENT', 'ESCAPE_CHAR'):
            self.pos += 1
            return
        if current[0] == 'KEYWORD':
            keyword = current[1]
            if keyword == 'if':
                return self.parse_if_statement()
            elif keyword == 'while':
                return self.parse_while_statement()
            elif keyword == 'for':
                return self.parse_for_statement()
            elif keyword == 'def':
                return self.parse_function_def()
            elif keyword == 'class':
                return self.parse_class_def()
            elif keyword == 'return':
                return self.parse_return_statement()
            elif keyword == 'try':
                return self.parse_try_statement()
            elif keyword == 'raise':
                return self.parse_raise_statement()
            elif keyword == 'match':
                return self.parse_match_statement()
            elif keyword in ('break', 'continue', 'pass'):
                self.consume('KEYWORD')
                return ("Statement", keyword)
        elif current[0] == 'COMMENT':
            self.consume('COMMENT')
            return
        elif current[0] in ('IDENTIFIER', 'BUILTIN'):
            next_token = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if next_token and next_token[0] == 'ASSIGN':
                return self.parse_assignment_statement()
            else:
                return self.parse_expression_statement()
        else:
            line, col = self.get_line_column()
            raise SyntaxError(f"Unexpected token: '{current[1]}' ({current[0]}) at line {line}, column {col}")

    def parse_match_statement(self):
        self.consume_keyword('match')
        expr = self.parse_expression()
        self.consume('COLON')
        cases = []
        while self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'case':
            cases.append(self.parse_case_clause())
        if not cases:
            line, col = self.get_line_column()
            raise SyntaxError(f"match sonrası en az bir case lazım, hata: satır {line}, sütun {col}")
        result = [expr]
        for case in cases:
            result.append(case)
        return ("MatchStatement", result)

    def parse_case_clause(self):
        self.consume_keyword('case')
        expr = self.parse_expression()
        self.consume('COLON')
        stmt = None
        if self.peek() and self.peek()[0] != 'KEYWORD':
            stmt = self.parse_statement()
        result = [expr]
        if stmt:
            result.append(stmt)
        return ("CaseClause", result)

    def parse_assignment_statement(self):
        current = self.peek()
        identifier = self.consume(current[0])[1]
        self.consume('ASSIGN')
        expr = self.parse_expression()
        return ("Assignment", [identifier, expr])

    def parse_return_statement(self):
        self.consume_keyword('return')
        expr = None
        if self.peek() and self.peek()[0] in ('IDENTIFIER', 'BUILTIN', 'NUMBER', 'STRING', 'LBRACKET', 'LPAREN'):
            expr = self.parse_expression()
        result = []
        if expr:
            result.append(expr)
        return ("Return", result)

    def parse_if_statement(self):
        self.consume_keyword('if')
        condition = self.parse_expression()
        self.consume('COLON')
        then_stmt = None
        if self.peek() and self.peek()[0] != 'KEYWORD':
            then_stmt = self.parse_statement()
        elif_clauses = []
        while self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'elif':
            self.consume_keyword('elif')
            elif_condition = self.parse_expression()
            self.consume('COLON')
            elif_stmt = None
            if self.peek() and self.peek()[0] != 'KEYWORD':
                elif_stmt = self.parse_statement()
            result = [elif_condition]
            if elif_stmt:
                result.append(elif_stmt)
            elif_clauses.append(("Elif", result))
        else_clause = None
        if self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'else':
            self.consume_keyword('else')
            self.consume('COLON')
            else_stmt = None
            if self.peek() and self.peek()[0] != 'KEYWORD':
                else_stmt = self.parse_statement()
            if else_stmt:
                else_clause = ("Else", [else_stmt])
            else:
                else_clause = ("Else", [])
        result = [condition]
        if then_stmt:
            result.append(then_stmt)
        for clause in elif_clauses:
            result.append(clause)
        if else_clause:
            result.append(else_clause)
        return ("IfStatement", result)

    def parse_while_statement(self):
        self.consume_keyword('while')
        condition = self.parse_expression()
        self.consume('COLON')
        stmt = None
        if self.peek() and self.peek()[0] not in ('KEYWORD', 'COMMENT'):
            stmt = self.parse_statement()
        result = [condition]
        if stmt:
            result.append(stmt)
        return ("WhileStatement", result)

    def parse_function_def(self):
        self.consume_keyword('def')
        name = self.consume('IDENTIFIER')[1]
        self.consume('LPAREN')
        params = []
        if self.peek() and self.peek()[0] == 'IDENTIFIER':
            params = self.parse_parameter_list()
        self.consume('RPAREN')
        self.consume('COLON')
        stmt = None
        if self.peek() and self.peek()[0] not in ('KEYWORD', 'COMMENT'):
            stmt = self.parse_statement()
        result = [name, params]
        if stmt:
            result.append(stmt)
        return ("FunctionDef", result)

    def parse_class_def(self):
        self.consume_keyword('class')
        name = self.consume('IDENTIFIER')[1]
        parents = []
        if self.peek() and self.peek()[0] == 'LPAREN':
            self.consume('LPAREN')
            if self.peek() and self.peek()[0] == 'IDENTIFIER':
                parents = self.parse_parameter_list()
            self.consume('RPAREN')
        self.consume('COLON')
        stmt = None
        if self.peek() and self.peek()[0] not in ('KEYWORD', 'COMMENT'):
            stmt = self.parse_statement()
        result = [name, parents]
        if stmt:
            result.append(stmt)
        return ("ClassDef", result)

    def parse_try_statement(self):
        self.consume_keyword('try')
        self.consume('COLON')
        try_stmt = None
        if self.peek() and self.peek()[0] not in ('KEYWORD', 'COMMENT'):
            try_stmt = self.parse_statement()
        if not (self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'except'):
            line, col = self.get_line_column()
            raise SyntaxError(f"try sonrası except lazım, hata: satır {line}, sütun {col}")
        except_clauses = []
        except_clauses.append(self.parse_except_clause())
        finally_clause = None
        if self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'finally':
            self.consume_keyword('finally')
            self.consume('COLON')
            finally_stmt = None
            if self.peek() and self.peek()[0] not in ('KEYWORD', 'COMMENT'):
                finally_stmt = self.parse_statement()
            if finally_stmt:
                finally_clause = ("Finally", [finally_stmt])
            else:
                finally_clause = ("Finally", [])
        result = []
        if try_stmt:
            result.append(try_stmt)
        for clause in except_clauses:
            result.append(clause)
        if finally_clause:
            result.append(finally_clause)
        return ("TryStatement", result)

    def parse_for_statement(self):
        self.consume_keyword('for')
        identifier = self.consume('IDENTIFIER')[1]
        self.consume_keyword('in')
        expr = self.parse_expression()
        self.consume('COLON')
        stmt = None
        if self.peek() and self.peek()[0] not in ('KEYWORD', 'COMMENT'):
            stmt = self.parse_statement()
        result = [identifier, expr]
        if stmt:
            result.append(stmt)
        return ("ForStatement", result)

    def parse_except_clause(self):
        self.consume_keyword('except')
        exception = None
        if self.peek() and self.peek()[0] == 'IDENTIFIER':
            exception = self.consume('IDENTIFIER')[1]
        self.consume('COLON')
        stmt = None
        if self.peek() and self.peek()[0] not in ('KEYWORD', 'COMMENT'):
            stmt = self.parse_statement()
        result = []
        if exception:
            result.append(exception)
        if stmt:
            result.append(stmt)
        if self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'except':
            next_except = self.parse_except_clause()
            result.append(next_except)
        return ("ExceptClause", result)

    def parse_raise_statement(self):
        self.consume_keyword('raise')
        expr = None
        if self.peek() and self.peek()[0] in ('IDENTIFIER', 'BUILTIN', 'NUMBER', 'STRING', 'LBRACKET', 'LPAREN'):
            expr = self.parse_expression()
        result = []
        if expr:
            result.append(expr)
        return ("Raise", result)

    def parse_parameter_list(self):
        params = []
        params.append(self.consume('IDENTIFIER')[1])
        while self.peek() and self.peek()[0] == 'COMMA':
            self.consume('COMMA')
            params.append(self.consume('IDENTIFIER')[1])
        return params

    def parse_expression(self):
        return self.parse_logical_expr()

    def parse_logical_expr(self):
        expr = self.parse_comparison_expr()
        while self.peek() and self.peek()[0] == 'KEYWORD' and self.peek()[1] in ('and', 'or'):
            op = self.consume('KEYWORD')[1]
            right = self.parse_comparison_expr()
            expr = ("LogicalExpr", [op, expr, right])
        return expr

    def parse_comparison_expr(self):
        expr = self.parse_add_expr()
        while self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] in ('==', '!=', '<', '>', '<=', '>='):
            op = self.consume('OPERATOR')[1]
            right = self.parse_add_expr()
            expr = ("ComparisonExpr", [op, expr, right])
        return expr

    def parse_add_expr(self):
        expr = self.parse_mul_expr()
        while self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] in ('+', '-'):
            op = self.consume('OPERATOR')[1]
            right = self.parse_mul_expr()
            expr = ("AddExpr", [op, expr, right])
        return expr

    def parse_mul_expr(self):
        expr = self.parse_term()
        while self.peek() and self.peek()[0] == 'OPERATOR' and self.peek()[1] in ('*', '/'):
            op = self.consume('OPERATOR')[1]
            right = self.parse_term()
            expr = ("MulExpr", [op, expr, right])
        return expr

    def parse_term(self):
        current = self.peek()
        if not current:
            line, col = self.get_line_column()
            raise SyntaxError(f"Expression expected at line {line}, column {col}")
        if current[0] in ('IDENTIFIER', 'BUILTIN'):
            value = self.consume(current[0])[1]
            if self.peek() and self.peek()[0] == 'LPAREN':
                return self.parse_function_call(value)
            return ("Term", value)
        elif current[0] == 'NUMBER':
            value = self.consume('NUMBER')[1]
            return ("Number", value)
        elif current[0] == 'STRING':
            value = self.consume('STRING')[1]
            return ("String", value)
        elif current[0] == 'STRING_QUOTE':
            return self.parse_string_literal()
        elif current[0] == 'LBRACKET':
            return self.parse_list_literal()
        elif current[0] == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return ("ParenExpr", [expr])
        elif current[0] == 'KEYWORD' and current[1] == 'not':
            self.consume('KEYWORD')
            term = self.parse_term()
            return ("NotExpr", [term])
        elif current[0] == 'KEYWORD' and current[1] in ('True', 'False', 'None'):
            value = self.consume('KEYWORD')[1]
            return ("Constant", value)
        else:
            line, col = self.get_line_column()
            raise SyntaxError(f"Unexpected term: '{current[1]}' ({current[0]}) at line {line}, column {col}")

    def parse_string_literal(self):
        self.consume('STRING_QUOTE')
        content = []
        while self.peek() and self.peek()[0] in ('STRING_CONTENT', 'ESCAPE_CHAR'):
            content.append(self.consume(self.peek()[0])[1])
        if self.peek() and self.peek()[0] == 'STRING_QUOTE':
            self.consume('STRING_QUOTE')
            return ("StringLiteral", content)
        line, col = self.get_line_column()
        raise SyntaxError(f"Kapanış tırnağı eksik, hata: satır {line}, sütun {col}")

    def parse_list_literal(self):
        self.consume('LBRACKET')
        elements = []
        if self.peek() and self.peek()[0] != 'RBRACKET':
            elements = self.parse_expression_list()
        self.consume('RBRACKET')
        return ("ListLiteral", elements)

    def parse_expression_list(self):
        elements = []
        elements.append(self.parse_expression())
        while self.peek() and self.peek()[0] == 'COMMA':
            self.consume('COMMA')
            elements.append(self.parse_expression())
        return elements

    def parse_expression_statement(self):
        expr = self.parse_expression()
        result = []
        result.append(expr)
        return ("ExpressionStmt", result)

    def parse_function_call(self, name):
        self.consume('LPAREN')
        args = []
        if self.peek() and self.peek()[0] != 'RPAREN':
            args = self.parse_expression_list()
        self.consume('RPAREN')
        result = [name]
        result.append(args)
        return ("FunctionCall", result)

if __name__ == "__main__":
    lexer = Lexer()
    test_cases = [
        'x = 42',
        'if x == 42: y = 10',
        'if x > 10: print("big") elif x > 5: print("medium") else: print("small")',
        'def add(a, b): return a + b',
        'for i in range(10): x = 3.14',
        'class MyClass: pass',
        'while x > 0: x = x - 1',
        'x = [1, 2, 3]',
        'try: x = 1\nexcept ValueError: pass',
        'a = "test \\"quote\\""',
    ]

    for code in test_cases:
        try:
            print(f"Input: '{code}'")
            tokens = lexer.tokenize(code)
            print(f"Tokens: {[(t[0], t[1]) for t in tokens]}")
            parser = Parser(tokens)
            parser.parse()
            print("✓ Parse successful")
            print("Parse Tree:")
            treeview = ttk.Treeview()
            parser.populate_treeview(treeview)
            print("-" * 60)
        except (ValueError, SyntaxError) as e:
            print(f"✗ Error: {e}")
        print("-" * 60)