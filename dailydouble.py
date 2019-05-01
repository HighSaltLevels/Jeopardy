from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *

class DailyDoubleWindow(QMainWindow):

    result_signal = pyqtSignal(str)

    def __init__(self, parent=None, title='Question', question='', identity='0', amount=0, double_jeopardy=False):

        super(DailyDoubleWindow, self).__init__(parent)
        self.setFixedSize(500,350)
        self.setWindowTitle(title)
        self.current_amount = int(amount)
        self.identity = identity
        self.double_jeopardy = double_jeopardy

        self.quesLabel = QLabel('', self)
        self.quesLabel.setFont(QFont("Times", 14))
        self.quesLabel.setWordWrap(True)
        self.quesLabel.setGeometry(10,10,450,100)
        self.revealBtn = QPushButton('Reveal Answer', self)
        self.revealBtn.resize(400,50)
        self.revealBtn.move(50,150)
        self.revealBtn.clicked.connect(self.reveal)
        self.correctBtn = QPushButton('Correct Answer', self)
        self.correctBtn.resize(125,50)
        self.correctBtn.move(50,225)
        self.correctBtn.clicked.connect(self.correct)
        self.incorrectBtn = QPushButton('Incorrect Answer', self)
        self.incorrectBtn.resize(125,50)
        self.incorrectBtn.move(187.5,225)
        self.incorrectBtn.clicked.connect(self.incorrect)
        self.noanswerBtn = QPushButton('No Answer', self)
        self.noanswerBtn.resize(125,50)
        self.noanswerBtn.move(325,225)
        self.noanswerBtn.clicked.connect(self.noanswer)
        self.betLbl = QLabel('Wager:', self)
        self.betLbl.setFont(QFont('Times', 14))
        self.betLbl.resize(100,100)
        self.betLbl.move(10,262.5)
        self.betAmountEdit = QLineEdit(self)
        self.betAmountEdit.resize(400,25)
        self.betAmountEdit.move(80,300)
        keys = question.keys()
        for key in keys:
            self.quesLabel.setText(key)
            self.answer = question[key]

    def showQuestion(self):
        self.show()

    def reveal(self):
        self.revealBtn.setText(self.answer)

    def correct(self):
        try:
            wager = self.checkForErrors()
            self.result_signal.emit(self.identity + str(wager))

        except ValueError:
            msg = QMessageBox.information(self, 'Error', 'You have to make a wager. It can be up to any amount you have or up to the highest amount on the Jeopardy board.')
        except Exception:
            pass

    def incorrect(self):
        try:
            wager = self.checkForErrors()
            self.result_signal.emit(self.identity + str(-1*wager))

        except ValueError:
            msg = QMessageBox.information(self, 'Error', 'You have to make a wager. It can be up to any amount you have or up to the highest amount on the Jeopardy board.')
        except Exception:
            pass

    def noanswer(self):
        try:
            wager = self.checkForErrors()
            self.result_signal.emit(self.identity + str(-1*wager))

        except ValueError:
            msg = QMessageBox.information(self, 'Error', 'You have to make a wager. It can be up to any amount you have or up to the highest amount on the Jeopardy board.')
        except Exception:
            pass

    def checkForErrors(self):
        text = self.betAmountEdit.text()
        if not text:
            msg = QMessageBox.information(self, 'Error', 'You have to make a wager. It can be up to any amount you have or up to the highest amount on the Jeopardy board.')
            raise Exception

        bet_amount = int(text)
        if bet_amount < 0:
            msg = QMessageBox.information(self, 'Error', 'You cannot wager an amount less than 0!')
            raise Exception
        highest_board_value = 2000 if self.double_jeopardy else 1000
        if bet_amount > highest_board_value and bet_amount > self.current_amount:
            msg = QMessageBox.information(self, 'Error', 'You cannot wager more than you have or more than the highest amount on the Jeopardy board')
            raise Exception

        return bet_amount

