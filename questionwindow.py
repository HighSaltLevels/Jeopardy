from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *

class QuestionWindow(QMainWindow):

    result_signal = pyqtSignal(str)

    def __init__(self, parent=None, title='Question', question='', worth=0, identity='0'):

        super(QuestionWindow, self).__init__(parent)
        self.setFixedSize(500,300)
        self.setWindowTitle(title)
        self.worth = worth
        self.identity = identity

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
        keys = question.keys()
        for key in keys:
            self.quesLabel.setText(key)
            self.answer = question[key]

    def showQuestion(self):
        self.show()

    def reveal(self):
        self.revealBtn.setText(self.answer)

    def correct(self):
        self.result_signal.emit(self.identity + str(self.worth))

    def incorrect(self):
        self.result_signal.emit(self.identity + str(-1*self.worth))

    def noanswer(self):
        self.result_signal.emit(self.identity + '0')

