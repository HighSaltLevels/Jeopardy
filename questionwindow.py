from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QuestionWindow(QMainWindow):

    result_signal = pyqtSignal(str)

    def __init__(self, parent=None, title='Question', question='', worth=0, identity='0', daily_double=False):

        super(QuestionWindow, self).__init__(parent)
        self.setFixedSize(500,300)
        self.setWindowTitle(title)
        self.worth = worth
        self.identity = identity
        self.daily_double = daily_double

        self.quesLabel = QLabel('', self)
        self.quesLabel.setFont(QFont("Times", 14))
        self.quesLabel.setWordWrap(True)
        self.quesLabel.setGeometry(10,10,475,100)
        self.quesLabel.setAlignment(Qt.AlignCenter)
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
        self.revealBtn.setEnabled(False)
        self.revealBtn.setText(self.answer)

    def correct(self):
        if self.checkForRevealed():
            self.result_signal.emit(self.identity + str(self.worth))
        else:
            self.showWarning()

    def incorrect(self):
        if self.checkForRevealed():
            self.result_signal.emit(self.identity + str(-1*self.worth))
        else:
            self.showWarning()

    def noanswer(self):
        if self.checkForRevealed():
            penalty = str(-1*self.worth) if self.daily_double else '0'
            self.result_signal.emit(self.identity + penalty)
        else:
            self.showWarning()

    def checkForRevealed(self):
        return self.revealBtn.text() != 'Reveal Answer'

    def showWarning(self):
        msg = QMessageBox.information(self, 'Warning', 'You need to reveal the answer before you can determine if you got it right or wrong')

