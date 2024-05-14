import re

TOKEN_TYPES = [
    ("NUMBER", r"\d+"),
    ("STRING", r'"[^"]*"'),
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
                src = src[match.end() :]
                break
        else:
            raise Exception("Invalid character: " + src[0])
    return tokens


class UnorderedTable:
    def __init__(self) -> None:
        self.table = {}

    def insert(self, name, datatype, line_declare):
        if name not in self.table:
            self.table[name] = (len(self.table) + 1, datatype, line_declare)

    # checks if the variable name matches the given name.
    # If a match is found, it returns True, indicating that the variable exists in the table.
    # If no match is found after checking all entries, it returns False, indicating that the variable is not present in the table.
    def look_up(self, name):
        return name in self.table


class Parser:
    def __init__(self, tokens, table):
        self.tokens = tokens
        self.current_token_index = 0
        self.table = table # parameter refers to the symbol table where variable declarations are stored.

    def parse(self):
        return self.assignment()

    # It starts by consuming the next token, expecting it to be a variable name.
    # it consumes the assignment operator token.
    #  it parses the expression on the right-hand side of the assignment.
    # If the variable name is not found in the symbol table, it inserts a new entry with the variable name, datatype "int", and the current line number.
    def assignment(self):
        variable_name_token = self.consume("VARIABLE")
        self.consume("ASSIGN")
        value = self.expression()
        # -- For Table --
        if not self.table.look_up(variable_name_token[1]):
            self.table.insert(variable_name_token[1], "int", self.current_line)

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


src = """x = 33
z = 44
x = 4 
y = 0"""

table = UnorderedTable()

src = src.split("\n")

print('Parse Tree : ')
for line_num, line in enumerate(src, start=1):
    tokens = tokenize(line)
    parser = Parser(tokens, table)
    parser.current_line = line_num  # Track the line number where the variable was declared
    parse_tree = parser.parse()
    print(parse_tree)


print("\nSymbol Table : ")
print("Counter | Variable | Data Type | Line Declare | Line Repeat")
for name, entry in table.table.items():
    line_declare = entry[2]
    line_repeat = [i + 1 for i, line in enumerate(src) if i + 1 != line_declare and line.strip().startswith(name + " =")]
    print(f"{entry[0]:<7} | {name:<8} | {entry[1]:<9} | {line_declare:<12} | {line_repeat}")
