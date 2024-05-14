def compute_first(grammar):

    # Initialize an empty set for each non-terminal symbol in the grammar.
    first_sets = {}
    for symbol in grammar:
        first_sets[symbol] = set()

    while True:
        updated = False
        # For each production of the symbol
        for symbol in grammar:
            for production in grammar[symbol]:
                i = 0
                while i < len(production):
                    # Check the first symbol in the production.
                    first_symbol = production[i]
                    if first_symbol in grammar:  # Non-terminal symbol
                        if '' not in first_sets[first_symbol]:  # If epsilon not in First(first_symbol)
                            break # If epsilon is not in the First set of the non-terminal, break the loop.

                        # Otherwise, add all terminals in the First set of the non-terminal to the First set of the current symbol.
                        for terminal in first_sets[first_symbol]:
                            if terminal != '':
                                if terminal not in first_sets[symbol]:
                                    first_sets[symbol].add(terminal)
                                    updated = True
                        i += 1

                    # Terminal symbol
                    else:  
                        if first_symbol not in first_sets[symbol]:
                            first_sets[symbol].add(first_symbol)
                            updated = True
                        break  # Move to the next production
                else:  # Loop completed without breaking, so epsilon production
                    if '' not in first_sets[symbol]:
                        first_sets[symbol].add('')
                        updated = True
                    if i == len(production):  # All symbols in the production are non-terminal
                        if '' not in first_sets[symbol]:
                            first_sets[symbol].add('')
                            updated = True

        if not updated:
            break

    return first_sets


# Example usage

grammar = {
    'S': ['bXY'],
    'X': ['b', 'c'],
    'Y': ['b', ''],
}

# Compute First sets
first_sets = compute_first(grammar)
print('First sets:', first_sets)