from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *

class DailyDoubleWindow(QMainWindow):

    result_signal = pyqtSignal(str)

    def __init__(self, parent=None, title='Question', double_jeopardy=False, amount = '', identity = ''):

        super(DailyDoubleWindow, self).__init__(parent)
        self.setFixedSize(200,87.5)
        self.setWindowTitle(title)

        self.double_jeopardy = double_jeopardy
        self.current_amount = int(amount)
        self.identity = identity

        self.wagerLbl = QLabel('Wager:', self)
        self.wagerLbl.resize(100,50)
        self.wagerLbl.move(10,0)

        self.wagerEdit = QLineEdit(self)
        self.wagerEdit.resize(125,25)
        self.wagerEdit.move(62.5,10)

        self.wagerBtn = QPushButton('Wager!', self)
        self.wagerBtn.resize(50,25)
        self.wagerBtn.move(75,50)
        self.wagerBtn.clicked.connect(self.wager)

    def showQuestion(self):
        self.show()

    def wager(self):
        wager, success = self.checkForErrors()
        if success:
            self.result_signal.emit('30' + str(self.identity) + str(wager))

    def checkForErrors(self):
        text = self.wagerEdit.text()
        if not text:
            msg = QMessageBox.information(self, 'Error', 'You have to make a wager. It can be up to any amount you have or up to the highest amount on the Jeopardy board.')
            return '', False

        try:
            wager = int(text)
            if wager < 0:
                msg = QMessageBox.information(self, 'Error', 'You cannot wager an amount less than 0!')
                return '', False

            highest_board_value = 2000 if self.double_jeopardy else 1000
            if wager > highest_board_value and wager > self.current_amount:
                msg = QMessageBox.information(self, 'Error', 'You cannot wager more than you have or more than the highest amount on the Jeopardy board')
                return '', False

            return wager, True

        except ValueError:
            msg = QMessageBox.information(self, 'Error', 'You have to make a wager. It can be up to any amount you have or up to the highest amount on the Jeopardy board.')
            return '', False

