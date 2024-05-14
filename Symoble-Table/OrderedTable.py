import re

TOKEN_TYPES = [
    ("NUMBER", r"\d+(\.\d+)?"),  # Allowing float numbers
    ("STRING", r'\'[^\']*\'|\"[^\"]*\"'),  # Allowing single or double quoted strings
    ("VARIABLE", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("ASSIGN", r"="),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"/"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("WHITESPACE", r"\s+"),
]


def tokenize(src) -> list:
    tokens = []
    while src:
        for token_type, pattern in TOKEN_TYPES:
            match = re.match(pattern, src)
            if match:
                token_value = match.group(0)
                if token_type != "WHITESPACE":
                    tokens.append((token_type, token_value))
                src = src[match.end():]
                break
        else:
            raise Exception("Invalid character: " + src[0])
    return tokens


class OrderedTable:
    def __init__(self):
        self.table = []

    def insert(self, name, datatype, line_declare):
        self.table.append((name, datatype, line_declare))

    def lookup(self, name):
        for i in self.table:
            if i[0] == name:
                return i[1]  # Return the value associated with the name
        return None  # Return None if the name is not found

    def sorted_table(self):
        return sorted(self.table, key=lambda x: x[0])  # Sort the table alphabetically by variable name


class Parser:
    def __init__(self, tokens, table):
        self.tokens = tokens
        self.current_token_index = 0
        self.table = table

    def parse(self):
        return self.assignment()

    def assignment(self):
        variable_name_token = self.consume("VARIABLE")
        self.consume("ASSIGN")
        expression_value = self.expression()
        value = expression_value if isinstance(expression_value, str) else expression_value[2]
        datatype = "float" if "." in value else "int" if value.replace(".", "").isdigit() else "str"
        if not self.table.lookup(variable_name_token[1]):
            self.table.insert(variable_name_token[1], datatype, self.current_line)
        return ("=", variable_name_token[1], value)

    def factor(self):
        token_type, token_value = self.consume("NUMBER", "STRING", "VARIABLE", "LPAREN")
        if token_type == "NUMBER" or token_type == "STRING" or token_type == "VARIABLE":
            return token_value
        elif token_type == "LPAREN":
            expression_value = self.expression()
            self.consume("RPAREN")
            return expression_value

    def term(self):
        result = self.factor()
        while self.current_token_index < len(self.tokens):
            if self.tokens[self.current_token_index][0] in {"MULTIPLY", "DIVIDE"}:
                operator_token = self.consume("MULTIPLY", "DIVIDE")
                result = (operator_token[1], result, self.factor())
            else:
                break
        return result

    def expression(self):
        result = self.term()
        while self.current_token_index < len(self.tokens):
            if self.tokens[self.current_token_index][0] in {"PLUS", "MINUS"}:
                operator_token = self.consume("PLUS", "MINUS")
                result = (operator_token[1], result, self.term())
            else:
                break
        return result

    def consume(self, *expected_token_types):
        if self.current_token_index >= len(self.tokens):
            raise ValueError("Unexpected end of input")
        current_token = self.tokens[self.current_token_index]
        if current_token[0] not in expected_token_types:
            raise ValueError(f"Expected one of {expected_token_types}, got {current_token}")
        self.current_token_index += 1
        return current_token


textLines = """b = 4 
c = 'mohamed'
a = 4.2 
b = 55"""

table = OrderedTable()

textLines = textLines.split("\n")

print('Parse Tree : ')
for line in textLines:
    tokens = tokenize(line)
    parser = Parser(tokens, table)
    parser.current_line = textLines.index(line) + 1  # Track the line number where the variable was declared
    parse_tree = parser.parse()
    print(parse_tree)

print("\nSymbol Table : ")
print("Counter | Variable | Data Type | Line Declare | Line Repeat")
for idx, entry in enumerate(table.sorted_table(), start=1):
    line_declare = entry[2]
    line_repeat = [i + 1 for i, line in enumerate(textLines) if i + 1 != line_declare and line.strip().startswith(entry[0] + " =")]
    print(f"{idx:<8} | {entry[0]:<8} | {entry[1]:<9} | {line_declare:<12} | {line_repeat}")
