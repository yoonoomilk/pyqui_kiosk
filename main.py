import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import uic

uifile = uic.loadUiType(os.path.dirname(os.path.abspath(__file__))+"\\main.ui")[0]
uifile_second = uic.loadUiType(os.path.dirname(os.path.abspath(__file__))+"\\second.ui")[0]
pay_success = False

ITEM_INFO = list(map(int, "2500 3000 3000 4000 700 1000 700".split()))
ITEM_NAME = "milddeok ssalddeok chapsundae squidsundae gimmari squidtuigim shrimptuigim".split()

class WindowClass(QMainWindow, uifile):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.item_selected = [0]*7
        self.item_total = 0
        for i in range(7):
            exec(f"self.btn_{ITEM_NAME[i]}.clicked.connect(lambda: myWindow.item_clicked({i}))")
        self.btn_reset.clicked.connect(self.item_clearall)
        self.btn_pay.clicked.connect(lambda: item_pay(myWindow.item_total))

    def item_show(self):
        model = QStandardItemModel()
        for i in range(7):
            if self.item_selected[i]:
                model.appendRow(QStandardItem(f"{ITEM_NAME[i]}를 {self.item_selected[i]}개 주문했습니다"))
        self.foodList.setModel(model)
        self.totalPrice.setText(f"{self.item_total}원")

    def item_clicked(self, item):
        self.item_selected[item] += 1
        self.item_total += ITEM_INFO[item]
        self.item_show()

    def item_clearall(self):
        self.item_selected = [0]*7
        self.item_total = 0
        self.item_show()

def item_pay(total):
    global pay_success
    myWindow.hide()
    second = Secondwindow(total)
    pay_success = False
    second.exec()
    if pay_success:
        myWindow.item_clearall()
    myWindow.show()

class Secondwindow(QDialog, QWidget, uifile_second):
    def __init__(self, total):
        super(Secondwindow, self).__init__()
        self.setupUi(self)
        self.totalPrice.setText(f"{total}원")
        self.pay_card.clicked.connect(self.card)
        self.pay_cash.clicked.connect(self.cash)
        self.show()

    def card(self):
        global pay_success
        if QMessageBox.question(self, "결제 확인", "결제를 진행하시겠습니다?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            pay_success = True
            self.close()

    def cash(self):
        while True:
            if QMessageBox.question(self, "결제 확인", "결제를 진행하시겠습니다?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                QMessageBox.question(self, "경고", "돈을 넣어!", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.question(self, "경고", "도망갈 수 없다!", QMessageBox.Yes, QMessageBox.Yes)
app = QApplication([__file__])
myWindow = WindowClass()
myWindow.show()
app.exec()
