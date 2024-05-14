# Represents a node in the linked list used for chaining in the hash table.
class HashTableNode:
    def __init__(self, word):
        self.word = word
        self.next = None

# Initializes a hash table with a specified maximum size (default is 7).
# Uses a list (hash_table) to store linked lists
class HashTable:
    def __init__(self, max_size=7):  # Increase max_size to accommodate index 6
        self.max_size = max_size
        self.hash_table = [None] * max_size  # List to store linked lists

    # The Hash Calculation Function
    def hash_function(self, word):
        if not word:
            raise ValueError("Empty word cannot be hashed")
        # Hash(var) = (var word len + Ascii of first character) % hash max 
        return ((len(word) * ord(word[0])) % self.max_size) 

    def insert(self, word):
        hashed_index = self.hash_function(word) # Computes the hash value of the word
        new_node = HashTableNode(word)

        # If the bucket is empty, insert the new node
        if self.hash_table[hashed_index] is None:
            self.hash_table[hashed_index] = new_node
            return

        # Insert the new node while maintaining the order
        current = self.hash_table[hashed_index]
        prev = None
        while current and (len(current.word) * ord(current.word[0])) <= (len(word) * ord(word[0])):
            prev = current
            current = current.next

        if prev:
            prev.next = new_node
        else:
            self.hash_table[hashed_index] = new_node
        new_node.next = current

    # Prints the contents of the hash table.
    def print_hash_table(self):
        print("Hash Table:")
        for i, head in enumerate(self.hash_table):
            if head:
                # Directly iterate through the linked list and print words
                current = head
                print(f"Index {i}: ", end="")
                while current:
                    print(current.word, end=", ")
                    current = current.next
                print("\b\b")  # Remove the trailing comma and space
            else:
                print(f"Index {i}: -")

# Example usage
# words = ["frog", "tree", "hill", "bird", "cat", "bad"]
words = ["ali", "mohamed", "khaled", "saad", "olaa", "amir"]
hash_table = HashTable()
for word in words:
    hash_table.insert(word)

hash_table.print_hash_table()