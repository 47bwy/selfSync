# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/10 09:27:13
@Author  :   47bwy
@Desc    :   None
'''

import tkinter as tk
from tkinter import messagebox, simpledialog


class ListTupleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("列表 & 元组 操作器")
        self.list_data = [1, 2, 3]
        self.tuple_data = (4, 5, 6)

        self.list_label = tk.Label(root, text=f"列表: {self.list_data}")
        self.list_label.pack(pady=5)

        self.tuple_label = tk.Label(root, text=f"元组: {self.tuple_data}")
        self.tuple_label.pack(pady=5)

        # 按钮区域
        tk.Button(root, text="添加到列表", command=self.add_to_list).pack(fill='x')
        tk.Button(root, text="插入列表元素", command=self.insert_to_list).pack(fill='x')
        tk.Button(root, text="从列表删除", command=self.remove_from_list).pack(fill='x')
        tk.Button(root, text="列表转元组", command=self.list_to_tuple).pack(fill='x')

        tk.Button(root, text="索引访问元组", command=self.index_tuple).pack(fill='x')
        tk.Button(root, text="切片元组", command=self.slice_tuple).pack(fill='x')
        tk.Button(root, text="元组转列表", command=self.tuple_to_list).pack(fill='x')

        tk.Button(root, text="退出", command=root.quit, bg="lightgray").pack(fill='x', pady=10)

    def update_labels(self):
        self.list_label.config(text=f"列表: {self.list_data}")
        self.tuple_label.config(text=f"元组: {self.tuple_data}")

    def add_to_list(self):
        val = simpledialog.askstring("添加元素", "输入要添加的值：")
        if val:
            self.list_data.append(val)
            self.update_labels()

    def insert_to_list(self):
        try:
            idx = simpledialog.askinteger("插入位置", "输入索引位置：")
            val = simpledialog.askstring("插入值", "输入值：")
            self.list_data.insert(idx, val)
            self.update_labels()
        except:
            messagebox.showerror("错误", "索引无效。")

    def remove_from_list(self):
        val = simpledialog.askstring("删除元素", "输入要删除的值：")
        if val in self.list_data:
            self.list_data.remove(val)
            self.update_labels()
        else:
            messagebox.showinfo("提示", "值不在列表中。")

    def list_to_tuple(self):
        self.tuple_data = tuple(self.list_data)
        self.update_labels()

    def index_tuple(self):
        try:
            idx = simpledialog.askinteger("索引访问", "输入索引：")
            val = self.tuple_data[idx]
            messagebox.showinfo("索引结果", f"元组[{idx}] = {val}")
        except:
            messagebox.showerror("错误", "索引无效。")

    def slice_tuple(self):
        try:
            start = simpledialog.askstring("切片", "起始索引（留空为默认）：")
            end = simpledialog.askstring("切片", "结束索引（留空为默认）：")
            s = int(start) if start else None
            e = int(end) if end else None
            result = self.tuple_data[s:e]
            messagebox.showinfo("切片结果", f"元组[{s}:{e}] = {result}")
        except:
            messagebox.showerror("错误", "切片无效。")

    def tuple_to_list(self):
        self.list_data = list(self.tuple_data)
        self.update_labels()


if __name__ == "__main__":
    root = tk.Tk()
    app = ListTupleApp(root)
    root.mainloop()
