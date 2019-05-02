from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QuestionWindow(QMainWindow):
    '''
        This is the QuestionWindow class that creates the Question Window GUI for
        the user.
    '''

    # This is a pyqt signal that returns a string and triggers a function in the
    # main GUI
    result_signal = pyqtSignal(str)

    def __init__(self, parent=None, title='Question', question='', worth=0, identity='0', daily_double=False):
        '''
            function:
                __init__: This is the constructor for the QuestionWindow GUI

            args:
                parent:       Parent class if one is passed in
                title:        Title of the GUI if one is passed in
                question:     Dictionary that has the question and answer
                worth:        How much the question is worth
                identity:     Unique identifier for the question on the board
                daily_double: Boolean value to indicate if this is a daily double
                              or not

            returns:
                None

            raises:
                None
        '''

        # Call the parent constructor and build the GUI. Also set the class
        # variables to the arguments passed in
        super(QuestionWindow, self).__init__(parent)
        self.setFixedSize(500,300)
        self.setWindowTitle(title)
        self.worth = worth
        self.identity = identity
        self.daily_double = daily_double

        # Create and position all of the GUI elements
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

        # Set the question in the label
        keys = question.keys()
        for key in keys:
            self.quesLabel.setText(key)
            self.answer = question[key]

    def showQuestion(self):
        '''
            function:
                showQuestion: This function shows this GUI window

            args:
                None

            returns:
                None

            raises:
                None
        '''
        self.show()

    def reveal(self):
        '''
            function:
                reveal: This function reveals the answer on the button

            args:
                None

            returns:
                None

            raises:
                None
        '''
        self.revealBtn.setEnabled(False)
        self.revealBtn.setText(self.answer)

    def correct(self):
        '''
            function:
                correct: This function is called when the correct button is 
                         pressed

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Make sure the user revealed the question before saying if it is correct
        if self.checkForRevealed():
            self.result_signal.emit(self.identity + str(self.worth))
        else:
            self.showWarning()

    def incorrect(self):
        '''
            function:
                incorrect: This function is called when the incorrect button is
                           pressed

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Make sure the user revealed the question before saying if it is
        # incorrect
        if self.checkForRevealed():
            self.result_signal.emit(self.identity + str(-1*self.worth))
        else:
            self.showWarning()

    def noanswer(self):
        '''
            function:
                noanswer: This function is called when the noanswer button is
                          pressed

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Make sure the user revealed the question before saying if he did not
        # answer
        if self.checkForRevealed():
            penalty = str(-1*self.worth) if self.daily_double else '0'
            self.result_signal.emit(self.identity + penalty)
        else:
            self.showWarning()

    def checkForRevealed(self):
        '''
            function:
                checkForRevealed: This function verifies that the user revealed
                                  the answer

            args:
                None

            returns:
                None

            raises:
                None
        '''

        return self.revealBtn.text() != 'Reveal Answer'

    def showWarning(self):
        '''
            function:
                showWarning: This function shows a warning dialog since the user
                             had not revealed the answer yet.

            args:
                None

            returns:
                None

            raises:
                None
        '''

        msg = QMessageBox.information(self, 'Warning', 'You need to reveal the answer before you can determine if you got it right or wrong')

