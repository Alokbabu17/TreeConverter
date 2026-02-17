import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def get_height(self, node):
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x
    
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y
    
    def insert(self, node, data):
        if not node:
            return Node(data)
        
        if data < node.data:
            node.left = self.insert(node.left, data)
        elif data > node.data:
            node.right = self.insert(node.right, data)
        else:
            return node
        
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)
        
        # Left Left
        if balance > 1 and data < node.left.data:
            return self.right_rotate(node)
        
        # Right Right
        if balance < -1 and data > node.right.data:
            return self.left_rotate(node)
        
        # Left Right
        if balance > 1 and data > node.left.data:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # Right Left
        if balance < -1 and data < node.right.data:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node
    
    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    
    def delete(self, node, data):
        if not node:
            return node
        
        if data < node.data:
            node.left = self.delete(node.left, data)
        elif data > node.data:
            node.right = self.delete(node.right, data)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            temp = self.min_value_node(node.right)
            node.data = temp.data
            node.right = self.delete(node.right, temp.data)
        
        if not node:
            return node
        
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)
        
        # Left Left
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)
        
        # Left Right
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)
        
        # Right Right
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)
        
        # Right Left
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)
        
        return node

class BinarySearchTree:
    def insert(self, node, data):
        if not node:
            return Node(data)
        
        if data < node.data:
            node.left = self.insert(node.left, data)
        elif data > node.data:
            node.right = self.insert(node.right, data)
        
        return node
    
    def min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    
    def delete(self, node, data):
        if not node:
            return node
        
        if data < node.data:
            node.left = self.delete(node.left, data)
        elif data > node.data:
            node.right = self.delete(node.right, data)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            temp = self.min_value_node(node.right)
            node.data = temp.data
            node.right = self.delete(node.right, temp.data)
        
        return node

class TreeMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TREE MAKER")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        
        self.tree_root = None
        self.tree_type = None
        self.avl = AVLTree()
        self.bst = BinarySearchTree()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Heading
        heading = tk.Label(
            self.root,
            text="🌳 TREE MAKER 🌳",
            font=("Arial", 28, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        heading.pack(pady=20)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg="#34495e", relief=tk.RAISED, bd=3)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Tree Type Selection
        tk.Label(
            control_frame,
            text="Select Tree Type:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.tree_type_var = tk.StringVar()
        tree_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.tree_type_var,
            values=["Create AVL Tree", "Create Binary Search Tree"],
            font=("Arial", 11),
            state="readonly",
            width=25
        )
        tree_dropdown.grid(row=0, column=1, padx=10, pady=10)
        tree_dropdown.current(0)
        
        # Values Input
        tk.Label(
            control_frame,
            text="Enter Values (comma-separated):",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.values_entry = tk.Entry(
            control_frame,
            font=("Arial", 11),
            width=30,
            relief=tk.SOLID,
            bd=2
        )
        self.values_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Build Tree Button
        build_btn = tk.Button(
            control_frame,
            text="🌲 Build Tree",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5,
            command=self.build_tree
        )
        build_btn.grid(row=1, column=2, padx=10, pady=10)
        
        # Delete Node Section
        tk.Label(
            control_frame,
            text="Delete Node:",
            font=("Arial", 12, "bold"),
            bg="#34495e",
            fg="#ecf0f1"
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.delete_entry = tk.Entry(
            control_frame,
            font=("Arial", 11),
            width=30,
            relief=tk.SOLID,
            bd=2
        )
        self.delete_entry.grid(row=2, column=1, padx=10, pady=10)
        
        delete_btn = tk.Button(
            control_frame,
            text="🗑️ Delete Node",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5,
            command=self.delete_node
        )
        delete_btn.grid(row=2, column=2, padx=10, pady=10)
        
        # Canvas Frame with Scrollbars
        canvas_frame = tk.Frame(self.root, bg="#2c3e50")
        canvas_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            relief=tk.SUNKEN,
            bd=3,
            scrollregion=(0, 0, 2000, 2000)
        )
        
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    def build_tree(self):
        try:
            values_str = self.values_entry.get().strip()
            if not values_str:
                messagebox.showwarning("Warning", "Please enter some values!")
                return
            
            values = [int(x.strip()) for x in values_str.split(",")]
            tree_type = self.tree_type_var.get()
            
            self.tree_root = None
            
            if tree_type == "Create AVL Tree":
                self.tree_type = "AVL"
                for val in values:
                    self.tree_root = self.avl.insert(self.tree_root, val)
            else:
                self.tree_type = "BST"
                for val in values:
                    self.tree_root = self.bst.insert(self.tree_root, val)
            
            self.draw_tree()
            messagebox.showinfo("Success", f"{tree_type} created successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid comma-separated numbers!")
    
    def delete_node(self):
        if not self.tree_root:
            messagebox.showwarning("Warning", "Please create a tree first!")
            return
        
        try:
            value = int(self.delete_entry.get().strip())
            
            if self.tree_type == "AVL":
                self.tree_root = self.avl.delete(self.tree_root, value)
            else:
                self.tree_root = self.bst.delete(self.tree_root, value)
            
            self.draw_tree()
            self.delete_entry.delete(0, tk.END)
            messagebox.showinfo("Success", f"Node {value} deleted successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number to delete!")
    
    def draw_tree(self):
        self.canvas.delete("all")
        
        if not self.tree_root:
            self.canvas.create_text(
                500, 300,
                text="Tree is empty!",
                font=("Arial", 24, "bold"),
                fill="#95a5a6"
            )
            return
        
        # Calculate tree dimensions
        def get_tree_height(node):
            if not node:
                return 0
            return 1 + max(get_tree_height(node.left), get_tree_height(node.right))
        
        height = get_tree_height(self.tree_root)
        self.canvas.configure(scrollregion=(0, 0, max(2000, 150 * (2 ** height)), max(2000, 120 * height)))
        
        self.draw_node(self.tree_root, 1000, 50, 400)
    
    def draw_node(self, node, x, y, offset):
        if not node:
            return
        
        node_radius = 25
        
        # Draw left child
        if node.left:
            left_x = x - offset
            left_y = y + 100
            self.canvas.create_line(
                x, y + node_radius,
                left_x, left_y - node_radius,
                fill="#34495e",
                width=3
            )
            self.draw_node(node.left, left_x, left_y, offset // 2)
        
        # Draw right child
        if node.right:
            right_x = x + offset
            right_y = y + 100
            self.canvas.create_line(
                x, y + node_radius,
                right_x, right_y - node_radius,
                fill="#34495e",
                width=3
            )
            self.draw_node(node.right, right_x, right_y, offset // 2)
        
        # Draw node as green ball
        self.canvas.create_oval(
            x - node_radius, y - node_radius,
            x + node_radius, y + node_radius,
            fill="#27ae60",
            outline="#229954",
            width=3
        )
        
        # Draw data inside node
        self.canvas.create_text(
            x, y,
            text=str(node.data),
            font=("Arial", 14, "bold"),
            fill="white"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeMakerApp(root)
    root.mainloop()