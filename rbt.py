import tkinter as tk
from tkinter import ttk, messagebox
import math

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.parent = None
        self.color = "RED"  # New nodes are always RED

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None)
        self.NIL.color = "BLACK"
        self.root = self.NIL
    
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        
        if y.right != self.NIL:
            y.right.parent = x
        
        y.parent = x.parent
        
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        
        y.right = x
        x.parent = y
    
    def insert(self, data):
        node = Node(data)
        node.left = self.NIL
        node.right = self.NIL
        
        parent = None
        current = self.root
        
        while current != self.NIL:
            parent = current
            if node.data < current.data:
                current = current.left
            elif node.data > current.data:
                current = current.right
            else:
                return  # Duplicate value
        
        node.parent = parent
        
        if parent == None:
            self.root = node
        elif node.data < parent.data:
            parent.left = node
        else:
            parent.right = node
        
        node.color = "RED"
        self.insert_fixup(node)
    
    def insert_fixup(self, node):
        while node.parent and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                if uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                
                if uncle.color == "RED":
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.left_rotate(node.parent.parent)
        
        self.root.color = "BLACK"
    
    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent
    
    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node
    
    def delete(self, data):
        node = self.search_node(self.root, data)
        
        if node == self.NIL:
            return False
        
        y = node
        y_original_color = y.color
        
        if node.left == self.NIL:
            x = node.right
            self.transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            
            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        
        if y_original_color == "BLACK":
            self.delete_fixup(x)
        
        return True
    
    def delete_fixup(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    w = x.parent.right
                
                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self.right_rotate(w)
                        w = x.parent.right
                    
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    w = x.parent.left
                
                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self.left_rotate(w)
                        w = x.parent.left
                    
                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        
        x.color = "BLACK"
    
    def search_node(self, node, data):
        if node == self.NIL or data == node.data:
            return node
        
        if data < node.data:
            return self.search_node(node.left, data)
        return self.search_node(node.right, data)

class RBTMakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RBT (Red Black Tree) MAKER")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a2e")
        
        self.rbt = RedBlackTree()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Heading
        heading = tk.Label(
            self.root,
            text="🔴⚫ RBT (Red Black Tree) MAKER ⚫🔴",
            font=("Arial", 26, "bold"),
            bg="#1a1a2e",
            fg="#eee"
        )
        heading.pack(pady=20)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg="#16213e", relief=tk.RAISED, bd=3)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Values Input
        tk.Label(
            control_frame,
            text="Enter Values (comma-separated):",
            font=("Arial", 12, "bold"),
            bg="#16213e",
            fg="#eee"
        ).grid(row=0, column=0, padx=10, pady=15, sticky="w")
        
        self.values_entry = tk.Entry(
            control_frame,
            font=("Arial", 11),
            width=35,
            relief=tk.SOLID,
            bd=2
        )
        self.values_entry.grid(row=0, column=1, padx=10, pady=15)
        
        # Build Tree Button
        build_btn = tk.Button(
            control_frame,
            text="🌲 Build RBT",
            font=("Arial", 12, "bold"),
            bg="#e63946",
            fg="white",
            activebackground="#d62828",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5,
            command=self.build_tree
        )
        build_btn.grid(row=0, column=2, padx=10, pady=15)
        
        # Delete Node Section
        tk.Label(
            control_frame,
            text="Delete Node:",
            font=("Arial", 12, "bold"),
            bg="#16213e",
            fg="#eee"
        ).grid(row=1, column=0, padx=10, pady=15, sticky="w")
        
        self.delete_entry = tk.Entry(
            control_frame,
            font=("Arial", 11),
            width=35,
            relief=tk.SOLID,
            bd=2
        )
        self.delete_entry.grid(row=1, column=1, padx=10, pady=15)
        
        delete_btn = tk.Button(
            control_frame,
            text="🗑️ Delete Node",
            font=("Arial", 12, "bold"),
            bg="#f77f00",
            fg="white",
            activebackground="#d62828",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5,
            command=self.delete_node
        )
        delete_btn.grid(row=1, column=2, padx=10, pady=15)
        
        # Clear Tree Button
        clear_btn = tk.Button(
            control_frame,
            text="🔄 Clear Tree",
            font=("Arial", 12, "bold"),
            bg="#457b9d",
            fg="white",
            activebackground="#1d3557",
            relief=tk.RAISED,
            bd=3,
            padx=15,
            pady=5,
            command=self.clear_tree
        )
        clear_btn.grid(row=1, column=3, padx=10, pady=15)
        
        # Canvas Frame with Scrollbars
        canvas_frame = tk.Frame(self.root, bg="#1a1a2e")
        canvas_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#f8f9fa",
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
            
            # Clear existing tree
            self.rbt = RedBlackTree()
            
            # Insert all values
            for val in values:
                self.rbt.insert(val)
            
            self.draw_tree()
            messagebox.showinfo("Success", "Red Black Tree created successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid comma-separated numbers!")
    
    def delete_node(self):
        if self.rbt.root == self.rbt.NIL:
            messagebox.showwarning("Warning", "Please create a tree first!")
            return
        
        try:
            value = int(self.delete_entry.get().strip())
            
            if self.rbt.delete(value):
                self.draw_tree()
                self.delete_entry.delete(0, tk.END)
                messagebox.showinfo("Success", f"Node {value} deleted successfully!")
            else:
                messagebox.showwarning("Warning", f"Node {value} not found in tree!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number to delete!")
    
    def clear_tree(self):
        self.rbt = RedBlackTree()
        self.values_entry.delete(0, tk.END)
        self.delete_entry.delete(0, tk.END)
        self.draw_tree()
        messagebox.showinfo("Success", "Tree cleared successfully!")
    
    def draw_tree(self):
        self.canvas.delete("all")
        
        if self.rbt.root == self.rbt.NIL:
            self.canvas.create_text(
                500, 300,
                text="Tree is empty!",
                font=("Arial", 24, "bold"),
                fill="#6c757d"
            )
            return
        
        # Calculate tree dimensions
        def get_tree_height(node):
            if node == self.rbt.NIL:
                return 0
            return 1 + max(get_tree_height(node.left), get_tree_height(node.right))
        
        height = get_tree_height(self.rbt.root)
        self.canvas.configure(scrollregion=(0, 0, max(2000, 150 * (2 ** height)), max(2000, 120 * height)))
        
        self.draw_node(self.rbt.root, 1000, 50, 400)
    
    def draw_node(self, node, x, y, offset):
        if node == self.rbt.NIL:
            return
        
        node_radius = 28
        
        # Draw left child
        if node.left != self.rbt.NIL:
            left_x = x - offset
            left_y = y + 100
            self.canvas.create_line(
                x, y + node_radius,
                left_x, left_y - node_radius,
                fill="#495057",
                width=3
            )
            self.draw_node(node.left, left_x, left_y, offset // 2)
        
        # Draw right child
        if node.right != self.rbt.NIL:
            right_x = x + offset
            right_y = y + 100
            self.canvas.create_line(
                x, y + node_radius,
                right_x, right_y - node_radius,
                fill="#495057",
                width=3
            )
            self.draw_node(node.right, right_x, right_y, offset // 2)
        
        # Draw node with color (RED or BLACK)
        if node.color == "RED":
            fill_color = "#e63946"
            outline_color = "#d62828"
        else:
            fill_color = "#212529"
            outline_color = "#000000"
        
        self.canvas.create_oval(
            x - node_radius, y - node_radius,
            x + node_radius, y + node_radius,
            fill=fill_color,
            outline=outline_color,
            width=3
        )
        
        # Draw data inside node (white text)
        self.canvas.create_text(
            x, y,
            text=str(node.data),
            font=("Arial", 13, "bold"),
            fill="white"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = RBTMakerApp(root)
    root.mainloop()