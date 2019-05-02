from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *

class DailyDoubleWindow(QMainWindow):
    '''
        This is the DailyDoubleWindow class that creates a window that asks for
        a wager when the user gets a daily double.
    '''

    # This is a pyqt signal that returns a string and triggers a function in the
    # main GUI
    result_signal = pyqtSignal(str)

    def __init__(self, parent=None, title='Question', double_jeopardy=False, amount = '', identity = ''):
        '''
            function:
                __init__: Constructor that builds the DailyDoubleWindow GUI

            args:
                parent:          Parent GUI if one is passed in
                title:           Title to use for this window
                double_jeopardy: Boolean that represents if we're in double
                                 jeopardy or not
                amount:          Current amount of money the user has
                identity:        Identifier for the question being asked

            returns:
                None

            raises:
                None
        '''

        # Call the parent constructor and set the size of the window
        super(DailyDoubleWindow, self).__init__(parent)
        self.setFixedSize(200,87.5)
        self.setWindowTitle(title)

        # Set the class variables to the variables passed in
        self.double_jeopardy = double_jeopardy
        self.current_amount = int(amount)
        self.identity = identity

        # Create the label, lineedit, and button for the GUI and set the button
        # to trigger self.wager when pushed
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
        '''
            function:
                showQuestion: This function shows the GUI

            args:
                None

            returns:
                None

            raises:
                None
        '''

        self.show()

    def wager(self):
        '''
            function:
                wager: this function returns the wager amount and also checks for
                       user input errors

            args:
                None

            returns:
                A string formatted like this. 30xxyy... where xx represents the
                question identifier and yy... represents the wager amount

            raises:
                None
        '''

        # Check to make sure there are no user errors. If not, return the string
        wager, success = self.checkForErrors()
        if success:
            self.result_signal.emit('30' + str(self.identity) + str(wager))

    def checkForErrors(self):
        '''
            function:
                checkForErrors: This function validates the user's input

            args:
                None

            returns:
                A tuple containing the input the user gave as well as a boolean
                that represents whether the user gave valid (True) or invalid
                (False) input

            raises:
                None
        '''

        # Get the text and verify that it is not blank
        text = self.wagerEdit.text()
        if not text:
            msg = QMessageBox.information(self, 'Error', 'You have to make a wager. It can be up to any amount you have or up to the highest amount on the Jeopardy board.')
            return '', False

        try:
            # Parse the wager into an integer. It will fail the try and go to the
            # except for a ValueError if it is not a valid integer.
            wager = int(text)

            # Verify the number is non-negative
            if wager < 0:
                msg = QMessageBox.information(self, 'Error', 'You cannot wager an amount less than 0!')
                return '', False

            # Verify that the wager is less than or equal to the current amount
            # or less than the highest value on the board. (1000 if jeopardy and
            # (2000) if double jeopardy)
            highest_board_value = 2000 if self.double_jeopardy else 1000
            if wager > highest_board_value and wager > self.current_amount:
                msg = QMessageBox.information(self, 'Error', 'You cannot wager more than you have or more than the highest amount on the Jeopardy board')
                return '', False

            # If these checks pass, then return the wager and True
            return wager, True

        # Verify that the value in the wager is an integer.
        except ValueError:
            msg = QMessageBox.information(self, 'Error', 'You have to make a wager. It can be up to any amount you have or up to the highest amount on the Jeopardy board.')
            return '', False

