class TreeNode:
    def __init__(self, key, value):
        self.key = key  # Key of the node
        self.value = value  # Value associated with the key
        self.left = None  # Pointer to the left child node
        self.right = None  # Pointer to the right child node


class BinaryTree:
    def __init__(self):
        self.root = None  # Root node of the binary tree

    def insert(self, key, value):
        if not self.root:  # If the tree is empty
            self.root = TreeNode(key, value)  # Create root node
        else:
            self._insert_recursive(self.root, key, value)  # Call recursive insert function

    def _insert_recursive(self, node, key, value):
        if key < node.key:  # If the new key is less than current node's key
            if node.left is None:  # If left child is empty
                node.left = TreeNode(key, value)  # Create left child node
            else:
                self._insert_recursive(node.left, key, value)  # Recursive call for left subtree
        elif key > node.key:  # If the new key is greater than current node's key
            if node.right is None:  # If right child is empty
                node.right = TreeNode(key, value)  # Create right child node
            else:
                self._insert_recursive(node.right, key, value)  # Recursive call for right subtree
        else:
            # If the key already exists, update the value
            node.value = value

    def search(self, key):
        return self._search_recursive(self.root, key)  # Call recursive search function

    def _search_recursive(self, node, key):
        if node is None or node.key == key:  # If node is None or key is found
            return node.value  # Return value associated with key
        if key < node.key:  # If key is less than current node's key
            return self._search_recursive(node.left, key)  # Recursive call for left subtree
        return self._search_recursive(node.right, key)  # Recursive call for right subtree

    def inorder_traversal(self):
        return self._inorder_traversal_recursive(self.root)  # Call recursive inorder traversal function

    def _inorder_traversal_recursive(self, node):
        if node is not None:
            self._inorder_traversal_recursive(node.left)  # Traverse left subtree
            print(f"({node.key}: {node.value})", end=" ")  # Print node key-value pair
            self._inorder_traversal_recursive(node.right)  # Traverse right subtree


# Example of using the binary tree
tree = BinaryTree()
tree.insert(5, "Apple")
tree.insert(3, "Banana")
tree.insert(7, "Cherry")
tree.insert(2, "Date")
tree.insert(4, "Elderberry")
tree.insert(6, "Fig")
tree.insert(8, "Grape")

print("Tree Structure :")
tree.inorder_traversal()

# Output:
# Tree Structure:
# (2: Date) (3: Banana) (4: Elderberry) (5: Apple) (6: Fig) (7: Cherry) (8: Grape)