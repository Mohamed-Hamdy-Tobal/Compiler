import re

# Define token types
TOKEN_TYPES = [
    ('NUMBER', r'\d+(\.\d+)?'),       # Matches integers and floats
    ('PLUS', r'\+'),                  # Matches addition operator
    ('MINUS', r'\-'),                 # Matches subtraction operator
    ('MULTIPLY', r'\*'),              # Matches multiplication operator
    ('DIVIDE', r'\/'),                # Matches division operator
    ('LPAREN', r'\('),                # Matches left parenthesis
    ('RPAREN', r'\)'),                # Matches right parenthesis
    ('ASSIGN', r'\='),                # Matches assignment operator
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'), # Matches identifiers (variable names)
    ('STRING', r'\".*?\"'),           # Matches string literals enclosed in double quotes
    ('WHITESPACE', r'\s+'),           # Matches whitespace
    ('UNKNOWN', r'.'),                # Matches any other character
]

# Compile regular expressions for token types 
# RE هحول التوكنزل ال 
# creates a regex object that represents that pattern. This compiled regex object can then be used multiple times for matching operations

TOKEN_REGEXES = [(name, re.compile(pattern)) for name, pattern in TOKEN_TYPES] # array of tuples
#  is a list of tuples where each tuple contains a token type name and its corresponding regular expression pattern.

# function takes a file path as input, reads the content of the file, and tokenizes it. It iterates through each line of the file and tokenizes it line by line.
def lexer(file_path):
    tokens = []
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):  # For Every Line
            line_tokens = []
            line = line.strip()  # Remove leading and trailing whitespace
            while line: #  iterates over the line until it is empty.
                match = None
                for token_name, token_regex in TOKEN_REGEXES:
                    regex_match = token_regex.match(line)
                    if regex_match:
                        match = (token_name, regex_match.group(0))  #  If a match is found, it assigns a tuple to match containing the token name (token_name) and the matched string 
                        if token_name != "WHITESPACE":
                            line_tokens.append((match[0], match[1], f"Line : {line_number}"))
                        line = line[regex_match.end():]
                        break
                if not match:
                    raise ValueError(f'Invalid token at line {line_number}: {line}')
            tokens.append(line_tokens)
    return tokens

# Test the lexer
if __name__ == "__main__":
    file_path = "text.txt"
    try:
        tokens = lexer(file_path)
        print(" ## Tokens : ##")
        for i, line_token in enumerate(tokens, 1):
            print(f"\nTokens For Line {i} Are :")
            for token in line_token:
                print(token)
        print("\n- Number of Tokens:", len(tokens))
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except ValueError as e:
        print(str(e))