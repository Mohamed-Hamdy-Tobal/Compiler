import re
TOKEN_TYPES = [
    ("NUMBER", r'\d+(\.\d+)?'),
    ("PLUS", r'\+'),
    ("MINUS", r'\-'),
    ("MULTIPLY", r'\*'),
    ("DIVIDE", r'\/'),
    ("ASSIGN", r'\='),
    ("LPAREN", r'\('),
    ("RPAREN", r'\)'),
    ("VARIABLE", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("STRING", r'\".*?\"'),
    ("WHITESPACE", r'\s+'),
    ("UNKNOWN", r'\.'),
]

TOKENS_REGEX = [(name, re.compile(pattern)) for name, pattern in TOKEN_TYPES]

def lexer(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            line_token = []
            line = line.strip()
            while line:
                match = None
                for token_name, token_regex in TOKENS_REGEX:
                    regex_match = token_regex.match(line)
                    if regex_match:
                        match = (token_name, regex_match.group(0))
                        if match[0] != "WHITESPACE":
                            line_token.append(match)
                        line = line[regex_match.end() :]
                        break
                if not match:
                    raise ValueError("error")
            tokens.append(line_token)
    return tokens


class OrderedTable:
    def __init__(self) -> None:
        self.table = []

    def insert(self, name, datatype, line_declare):
        self.table.append((name, datatype, line_declare))

    def lookup(self, name):
        for i in self.table:
            if i[0] == name:
                return i[1]
        return None
    
    def sorted_table(self):
        return sorted(self.table, key=lambda x: x[0])
    

class Parser:
    def __init__(self, tokens, table) -> None:
        self.table = table
        self.tokens = tokens
        self.current_token_index = 0

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
        token_type, token_value = self.consume("NUMBER", "VARIABLE", "STRING", "LPAREN")
        if token_type == "NUMBER" or token_type == "VARIABLE" or token_type == "STRING" :
            return token_value
        elif token_type == "LPAREN" :
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
    

table = OrderedTable()
file_path = 'text1.txt'
tokens = lexer(file_path)

print('Parse Tree : ')
for line_num, line_tokens in enumerate(tokens, start=1):
    parser = Parser(line_tokens, table)
    parser.current_line = line_num  # Track the line number where the variable was declared
    parse_tree = parser.parse()
    print(parse_tree)



file_content = []
with open(file_path, 'r') as file:
    main_content = file.readlines()
    for item in main_content:
        file_content.append(item.strip())

print("\nSymbol Table : ")
print("Counter | Variable | Data Type | Line Declare | Line Repeat")
for count, entry in enumerate(table.sorted_table(), start=1):
    variable_name = entry[0]
    datatype = entry[1]
    line_declare = entry[2]
    
    line_repeat = [i + 1 for i, line in enumerate(file_content) if i + 1 != line_declare and line.strip().startswith(variable_name + " = ")]
    line_repeat_str = ', '.join(map(str, line_repeat)) if line_repeat else []
    
    print(f"{count:<7} | {variable_name:<8} | {datatype:<9} | {line_declare:<12} | {line_repeat_str}")

