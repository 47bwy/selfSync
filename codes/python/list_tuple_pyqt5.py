# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/10 09:30:38
@Author  :   47bwy
@Desc    :   None
'''

import sys

from PyQt5.QtWidgets import (QApplication, QInputDialog, QLabel, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)


class FancyListTupleApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌀 炫酷 List & Tuple 操作器")
        self.setStyleSheet("font-size: 16px; background-color: #f4f4f4;")
        self.setGeometry(300, 200, 400, 400)

        self.list_data = ["A", "B", "C"]
        self.tuple_data = ("X", "Y", "Z")

        self.layout = QVBoxLayout()

        self.list_label = QLabel()
        self.tuple_label = QLabel()
        self.update_labels()

        self.layout.addWidget(self.list_label)
        self.layout.addWidget(self.tuple_label)

        # 列表操作按钮
        self.add_button("➕ 添加到列表", self.add_to_list)
        self.add_button("📌 插入列表元素", self.insert_to_list)
        self.add_button("❌ 删除列表元素", self.remove_from_list)
        self.add_button("🔁 列表转元组", self.list_to_tuple)

        # 元组操作按钮
        self.add_button("🔍 元组索引访问", self.index_tuple)
        self.add_button("✂️ 元组切片", self.slice_tuple)
        self.add_button("🔄 元组转列表", self.tuple_to_list)

        self.setLayout(self.layout)

    def add_button(self, label, func):
        btn = QPushButton(label)
        btn.clicked.connect(func)
        btn.setStyleSheet("padding: 10px; border-radius: 8px; background-color: #0078d7; color: white;")
        self.layout.addWidget(btn)

    def update_labels(self):
        self.list_label.setText(f"📋 当前列表: {self.list_data}")
        self.tuple_label.setText(f"📦 当前元组: {self.tuple_data}")

    def add_to_list(self):
        val, ok = QInputDialog.getText(self, "添加元素", "请输入值：")
        if ok and val:
            self.list_data.append(val)
            self.update_labels()

    def insert_to_list(self):
        idx, ok1 = QInputDialog.getInt(self, "插入位置", "请输入索引：")
        val, ok2 = QInputDialog.getText(self, "插入值", "请输入值：")
        if ok1 and ok2 and val:
            if 0 <= idx <= len(self.list_data):
                self.list_data.insert(idx, val)
                self.update_labels()
            else:
                QMessageBox.warning(self, "错误", "索引超出范围")

    def remove_from_list(self):
        val, ok = QInputDialog.getText(self, "删除元素", "输入要删除的值：")
        if ok and val in self.list_data:
            self.list_data.remove(val)
            self.update_labels()
        else:
            QMessageBox.information(self, "提示", "值不存在于列表中。")

    def list_to_tuple(self):
        self.tuple_data = tuple(self.list_data)
        self.update_labels()

    def index_tuple(self):
        idx, ok = QInputDialog.getInt(self, "索引访问", "输入索引：")
        if ok:
            try:
                val = self.tuple_data[idx]
                QMessageBox.information(self, "索引结果", f"元组[{idx}] = {val}")
            except IndexError:
                QMessageBox.critical(self, "错误", "索引超出范围")

    def slice_tuple(self):
        start, ok1 = QInputDialog.getText(self, "切片起始", "起始索引（可留空）：")
        end, ok2 = QInputDialog.getText(self, "切片结束", "结束索引（可留空）：")
        try:
            s = int(start) if start.strip() else None
            e = int(end) if end.strip() else None
            result = self.tuple_data[s:e]
            QMessageBox.information(self, "切片结果", f"元组[{s}:{e}] = {result}")
        except:
            QMessageBox.critical(self, "错误", "切片参数无效")

    def tuple_to_list(self):
        self.list_data = list(self.tuple_data)
        self.update_labels()


def run_gui():
    app = QApplication(sys.argv)
    window = FancyListTupleApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
