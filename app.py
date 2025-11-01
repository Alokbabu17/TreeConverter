import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class LNCTDSAConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("LNCT DSA CONVERTER")
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        width = int(screen_w * 0.8)
        height = int(screen_h * 0.8)
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg="#f0f0f0")

        self.tree = None
        self.canvas = None

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#007acc", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(header, text="LNCT DSA CONVERTER", font=("Arial", 28, "bold"),
                         fg="white", bg="#007acc")
        title.pack(expand=True)

        # Main Container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left Panel
        left_panel = tk.Frame(main_frame, bg="white", relief="groove", bd=2)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Right Panel
        right_panel = tk.Frame(main_frame, bg="white", relief="groove", bd=2)
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self.setup_left_panel(left_panel)
        self.setup_right_panel(right_panel)

        # Canvas with Scrollbars for Tree Visualization
        canvas_frame = tk.Frame(self.root, bg="white")
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # === Scrollbars Added ===
        self.canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0, scrollregion=(0, 0, 2000, 2000))
        hbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        vbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        hbar.pack(side="bottom", fill="x")
        vbar.pack(side="right", fill="y")
        self.canvas.pack(fill="both", expand=True, side="left")

    def setup_left_panel(self, parent):
        tk.Label(parent, text="Build Tree & Convert", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        tk.Label(parent, text="Enter Level Order (space separated, 'null' for None):", bg="white").pack(anchor="w", padx=20)
        self.level_input = tk.Entry(parent, width=50)
        self.level_input.pack(pady=5, padx=20)

        tk.Button(parent, text="Build Tree from Level Order", bg="#28a745", fg="white",
                  command=self.build_tree_from_level).pack(pady=5)

        tk.Label(parent, text="Convert to:", bg="white").pack(anchor="w", padx=20, pady=(15,5))
        self.convert_var = tk.StringVar(value="Inorder")
        convert_menu = ttk.Combobox(parent, textvariable=self.convert_var,
                                    values=["Inorder", "Preorder", "Postorder"], state="readonly", width=20)
        convert_menu.pack(pady=5)

        tk.Button(parent, text="Convert Tree", bg="#007acc", fg="white",
                  command=self.convert_tree).pack(pady=10)

        self.left_result = tk.Text(parent, height=4, width=50, state="disabled", bg="#f8f9fa")
        self.left_result.pack(pady=10, padx=20)

    def setup_right_panel(self, parent):
        tk.Label(parent, text="Build Tree from Traversals", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        tk.Label(parent, text="Select First Traversal:", bg="white").pack(anchor="w", padx=20)
        self.trav1_var = tk.StringVar(value="Inorder")
        trav1_menu = ttk.Combobox(parent, textvariable=self.trav1_var,
                                  values=["Inorder", "Preorder", "Postorder"], state="readonly")
        trav1_menu.pack(pady=5)

        tk.Label(parent, text="Enter values (space separated):", bg="white").pack(anchor="w", padx=20)
        self.trav1_input = tk.Entry(parent, width=40)
        self.trav1_input.pack(pady=5, padx=20)

        tk.Label(parent, text="Select Second Traversal:", bg="white").pack(anchor="w", padx=20, pady=(15,5))
        self.trav2_var = tk.StringVar(value="Preorder")
        trav2_menu = ttk.Combobox(parent, textvariable=self.trav2_var,
                                  values=["Inorder", "Preorder", "Postorder"], state="readonly")
        trav2_menu.pack(pady=5)

        tk.Label(parent, text="Enter values (space separated):", bg="white").pack(anchor="w", padx=20)
        self.trav2_input = tk.Entry(parent, width=40)
        self.trav2_input.pack(pady=5, padx=20)

        tk.Button(parent, text="Build Tree from Traversals", bg="#dc3545", fg="white",
                  command=self.build_tree_from_traversals).pack(pady=15)

    def build_tree_from_level(self):
        try:
            values = self.level_input.get().strip().split()
            if not values:
                raise ValueError("Empty input")
            self.tree = self.construct_tree_level_order(values)
            self.draw_tree()
            messagebox.showinfo("Success", "Tree built from level order!")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def construct_tree_level_order(self, values):
        if not values or values[0].lower() == 'null':
            return None
        root = TreeNode(values[0])
        queue = deque([root])
        i = 1
        while queue and i < len(values):
            node = queue.popleft()
            if i < len(values) and values[i].lower() != 'null':
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
            if i < len(values) and values[i].lower() != 'null':
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
        return root

    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append(root.val)
            self.inorder(root.right, result)

    def preorder(self, root, result):
        if root:
            result.append(root.val)
            self.preorder(root.left, result)
            self.preorder(root.right, result)

    def postorder(self, root, result):
        if root:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.val)

    def convert_tree(self):
        if not self.tree:
            messagebox.showwarning("No Tree", "Build a tree first!")
            return
        result = []
        choice = self.convert_var.get()
        if choice == "Inorder":
            self.inorder(self.tree, result)
        elif choice == "Preorder":
            self.preorder(self.tree, result)
        else:
            self.postorder(self.tree, result)

        self.left_result.config(state="normal")
        self.left_result.delete(1.0, tk.END)
        self.left_result.insert(tk.END, f"{choice}: {' '.join(result)}")
        self.left_result.config(state="disabled")

    def build_tree_from_traversals(self):
        try:
            trav1 = self.trav1_input.get().strip().split()
            trav2 = self.trav2_input.get().strip().split()
            if len(trav1) != len(trav2) or not trav1:
                raise ValueError("Both traversals must have same length and non-empty")

            t1, t2 = self.trav1_var.get(), self.trav2_var.get()
            inorder = None
            other = None

            if "Inorder" in [t1, t2]:
                if t1 == "Inorder":
                    inorder, other = trav1, trav2
                    other_type = t2
                else:
                    inorder, other = trav2, trav1
                    other_type = t1
            else:
                raise ValueError("One traversal must be Inorder!")

            self.tree = self.build_tree_from_in_and_other(inorder, other, other_type)
            self.draw_tree()
            messagebox.showinfo("Success", f"Tree built from {t1} + {t2}!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def build_tree_from_in_and_other(self, inorder, other, other_type):
        if not inorder:
            return None
        in_map = {val: i for i, val in enumerate(inorder)}
        self.index = 0 if other_type == "Preorder" else len(other) - 1

        def helper(in_start, in_end):
            if in_start > in_end:
                return None

            if other_type == "Preorder":
                val = other[self.index]
                self.index += 1
            else:
                val = other[self.index]
                self.index -= 1

            if val not in in_map:
                return None

            root = TreeNode(val)
            idx = in_map[val]

            if other_type == "Preorder":
                root.left = helper(in_start, idx - 1)
                root.right = helper(idx + 1, in_end)
            else:
                root.right = helper(idx + 1, in_end)
                root.left = helper(in_start, idx - 1)
            return root

        return helper(0, len(inorder) - 1)

    def draw_tree(self):
        self.canvas.delete("all")
        if not self.tree:
            return
        self.canvas.create_text(600, 30, text="Binary Tree Visualization", font=("Arial", 14, "bold"), fill="#333")

        def draw(node, x, y, dx):
            if not node:
                return
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="#4CAF50", outline="black")
            self.canvas.create_text(x, y, text=node.val, font=("Arial", 12, "bold"), fill="white")
            if node.left:
                self.canvas.create_line(x, y+20, x-dx, y+70, fill="black")
                draw(node.left, x-dx, y+70, dx//2)
            if node.right:
                self.canvas.create_line(x, y+20, x+dx, y+70, fill="black")
                draw(node.right, x+dx, y+70, dx//2)

        draw(self.tree, 600, 80, 250)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = LNCTDSAConverter(root)
    root.mainloop()
