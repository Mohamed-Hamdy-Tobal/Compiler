import re

TOKEN_TYPES = [
    ("NUMBER", r"\d+(\.\d+)?"),
    ("PLUS", r"\+"),
    ("MINUS", r"\-"),
    ("MULTIPLY", r"\*"),
    ("DIVIDE", r"\/"),
    ("ASSIGN", r"\="),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("VARIABLE", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("STRING", r"\".*?\""),
    ("WHITESPACE", r"\s+"),
    ("UNKNOWN", r"\."),
]

TOKEN_REGEX = [(name, re.compile(pattern)) for name, pattern in TOKEN_TYPES]

def lexer(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            line_token = []
            line = line.strip()
            while line:
                match = None
                for token_name, token_regex in TOKEN_REGEX:
                    regex_match = token_regex.match(line)
                    if regex_match:
                        match = (token_name, regex_match.group(0))
                        if match[0] != "WHITESPACE":
                            line_token.append(match)
                            # line_token.append((match[0], match[1], f"In -> {line_number}"))
                        line = line[regex_match.end() :]
                        break
                if not match:
                    raise ValueError("Error")
            tokens.append(line_token)
    return tokens


class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.current_token_index = 0
    
    def parse(self):
        return self.assignment()
    
    def assignment(self):
        variable_name_token = self.consume("VARIABLE")
        self.consume("ASSIGN")
        expression_value = self.expression()
        return ("=", variable_name_token[1], expression_value)
    
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
    
    def consume(self, *expected_tokens):
        if self.current_token_index >= len(self.tokens):
            raise ValueError("Error")
        current = self.tokens[self.current_token_index]
        if current[0] not in expected_tokens:
            raise ValueError("Error")
        self.current_token_index += 1
        return current


if __name__ == "__main__":
    file_path = 'text1.txt'
    tokens = lexer(file_path)
    try:
        for i, line_tokens in enumerate(tokens, start=1):
            parser = Parser(line_tokens)
            parse_tree = parser.parse()
            print(parse_tree)
            # print(f"\nTokens For Line {i} Are : ")
            # for token in line_tokens:
            #     print(token)
    except:
        raise FileNotFoundError(f"File Not Fount At Path : {file_path}")