import sys
from PySide2.QtWidgets import (QLabel, QApplication, QVBoxLayout, QHBoxLayout, QSpacerItem,
                               QSizePolicy, QPushButton, QLineEdit, QDialog, QInputDialog,
                               QTableWidget, QTableWidgetItem, QHeaderView)
from tz_py_wishlist.db import *


class Window(QDialog):
    def check_input(self):
        flag = 0
        if self.newName.text() == "":
            flag += 1
            text, ok = QInputDialog.getText(self, 'Input Dialog',
                                            'Enter lot name:')
            if ok:
                self.newName.setText(str(text))
        if self.newCost.text() == "":
            flag += 1
            text, ok = QInputDialog.getText(self, 'Input Dialog',
                                            'Enter lot cost:')
            if ok:
                self.newCost.setText(str(text))
        if self.newLink.text() == "":
            flag += 1
            text, ok = QInputDialog.getText(self, 'Input Dialog',
                                            'Enter lot link:')
            if ok:
                self.newLink.setText(str(text))
        if self.newNote.text() == "":
            flag += 1
            text, ok = QInputDialog.getText(self, 'Input Dialog',
                                            'Enter lot note:')
            if ok:
                self.newNote.setText(str(text))
        return flag

    def onDeleteButton(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter lot name:')
        if ok:
            delete_wish(str(text))
        self.refresh_table()
        self.table.update()
        self.layout.update()

    def onAddButton(self):
        flag = self.check_input()
        if flag == 0:
            add_lot(self.newName.text(), self.newCost.text(), self.newLink.text(), self.newNote.text())
        self.refresh_table()
        self.table.update()
        self.layout.update()
        self.newName.setText("")
        self.newCost.setText("")
        self.newLink.setText("")
        self.newNote.setText("")


    def createLotLayout(self, name, cost, link, note):
        layout = QHBoxLayout()
        lotName = QLabel(name)
        lotCost = QLabel(cost)
        lotLink = QLabel(link)
        lotNote = QLabel(note)
        layout.addWidget(lotName)
        layout.addWidget(lotCost)
        layout.addWidget(lotLink)
        layout.addWidget(lotNote)
        return layout

    def refresh_table(self):
        self.table.setRowCount(get_size() + 1)
        self.table.setColumnCount(4)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.table.setItem(0, 0, QTableWidgetItem("name"))
        self.table.setItem(0, 1, QTableWidgetItem("cost"))
        self.table.setItem(0, 2, QTableWidgetItem("link"))
        self.table.setItem(0, 3, QTableWidgetItem("note"))

        data = get_wishes()
        tmp = 1
        for i in data:
            self.table.setItem(tmp, 0, QTableWidgetItem(i['name']))
            self.table.setItem(tmp, 1, QTableWidgetItem(i['cost']))
            self.table.setItem(tmp, 2, QTableWidgetItem(i['link']))
            self.table.setItem(tmp, 3, QTableWidgetItem(i['note']))
            tmp += 1

    def setupLayout(self):
        self.table = QTableWidget()
        self.table.setMinimumHeight(725)
        self.refresh_table()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.table)
        inputLayout = QHBoxLayout()
        self.newName = QLineEdit()
        self.newCost = QLineEdit()
        self.newLink = QLineEdit()
        self.newNote = QLineEdit()
        self.addButton = QPushButton()
        self.addButton.pressed.connect(self.onAddButton)
        self.addButton.setText("add")
        inputLayout.addWidget(self.newName)
        inputLayout.addWidget(self.newCost)
        inputLayout.addWidget(self.newLink)
        inputLayout.addWidget(self.newNote)
        inputLayout.addWidget(self.addButton)
        self.layout.addLayout(inputLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.verticalSpacer)

        self.deleteButton = QPushButton()
        self.deleteButton.setText("delete")
        self.deleteButton.pressed.connect(self.onDeleteButton)
        self.layout.addWidget(self.deleteButton)

        self.setLayout(self.layout)

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("Wishlist")
        self.setMinimumSize(1100, 820)

        self.setupLayout()


    def close(self) -> bool:
        close_db()


myApp = QApplication(sys.argv)
window = Window()
window.show()

myApp.exec_()
sys.exit(0)
