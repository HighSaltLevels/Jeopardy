#!/usr/bin/env python3

from random import randint
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from questionwindow import QuestionWindow
from dailydouble import DailyDoubleWindow
import json, requests, sys

class Jeopardy(QWidget):
    '''
        Jeopardy class that is used to play this jeopardy game. This is a game
        that I came up with because I watched a Youtube/Twitch Streamer make
        his own Jeopardy game (shoutout to Northernlion). His was pretty fun,
        but I thought it would be fun to make my own.
    '''

    def __init__(self, parent=None, title=''):
        '''
            function:
                __init__: This is the constructor for the Jeopardy class. It
                          builds the GUI and prepares the questions.

            args:
                parent: Parent GUI if created as a child class.
                title:  Title of the GUI if one is passed in

            returns:
                None

            raises:
                None
        '''

        # Call the constructor of the parent class
        super(Jeopardy, self).__init__(parent)

        # These class variables help to share information across the funcitons
        self.double_jeopardy = False
        self.cat_and_questions = {}
        self.categories = []
        self.daily_doubles = []

        # Create a list of numbers 0 through 29 to represent each question.
        # A number will be removed when that question is answered
        self.questions_left = [num for num in range(30)]

        # Load the GUI and load the questions
        self.loadUI()
        self.loadQuestions()

    def loadUI(self):
        '''
            function:
                loadUI: This function builds the GUI completely and creates a
                        couple of useful lists that contain the buttons and
                        category labels that will be used throughout the program.

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Set a fixed window size and set the title
        self.setFixedSize(1200,480)
        self.setWindowTitle('Jeopardy!')

        # Create all the buttons and bind them to their corresponding functions
        self.btn11 = QPushButton('$200',self)
        self.btn11.clicked.connect(self.btn11Handler)
        self.btn12 = QPushButton('$200',self)
        self.btn12.clicked.connect(self.btn12Handler)
        self.btn13 = QPushButton('$200',self)
        self.btn13.clicked.connect(self.btn13Handler)
        self.btn14 = QPushButton('$200',self)
        self.btn14.clicked.connect(self.btn14Handler)
        self.btn15 = QPushButton('$200',self)
        self.btn15.clicked.connect(self.btn15Handler)
        self.btn16 = QPushButton('$200',self)
        self.btn16.clicked.connect(self.btn16Handler)
        self.btn21 = QPushButton('$400',self)
        self.btn21.clicked.connect(self.btn21Handler)
        self.btn22 = QPushButton('$400',self)
        self.btn22.clicked.connect(self.btn22Handler)
        self.btn23 = QPushButton('$400',self)
        self.btn23.clicked.connect(self.btn23Handler)
        self.btn24 = QPushButton('$400',self)
        self.btn24.clicked.connect(self.btn24Handler)
        self.btn25 = QPushButton('$400',self)
        self.btn25.clicked.connect(self.btn25Handler)
        self.btn26 = QPushButton('$400',self)
        self.btn26.clicked.connect(self.btn26Handler)
        self.btn31 = QPushButton('$600',self)
        self.btn31.clicked.connect(self.btn31Handler)
        self.btn32 = QPushButton('$600',self)
        self.btn32.clicked.connect(self.btn32Handler)
        self.btn33 = QPushButton('$600',self)
        self.btn33.clicked.connect(self.btn33Handler)
        self.btn34 = QPushButton('$600',self)
        self.btn34.clicked.connect(self.btn34Handler)
        self.btn35 = QPushButton('$600',self)
        self.btn35.clicked.connect(self.btn35Handler)
        self.btn36 = QPushButton('$600',self)
        self.btn36.clicked.connect(self.btn36Handler)
        self.btn41 = QPushButton('$800',self)
        self.btn41.clicked.connect(self.btn41Handler)
        self.btn42 = QPushButton('$800',self)
        self.btn42.clicked.connect(self.btn42Handler)
        self.btn43 = QPushButton('$800',self)
        self.btn43.clicked.connect(self.btn43Handler)
        self.btn44 = QPushButton('$800',self)
        self.btn44.clicked.connect(self.btn44Handler)
        self.btn45 = QPushButton('$800',self)
        self.btn45.clicked.connect(self.btn45Handler)
        self.btn46 = QPushButton('$800',self)
        self.btn46.clicked.connect(self.btn46Handler)
        self.btn51 = QPushButton('$1000',self)
        self.btn51.clicked.connect(self.btn51Handler)
        self.btn52 = QPushButton('$1000',self)
        self.btn52.clicked.connect(self.btn52Handler)
        self.btn53 = QPushButton('$1000',self)
        self.btn53.clicked.connect(self.btn53Handler)
        self.btn54 = QPushButton('$1000',self)
        self.btn54.clicked.connect(self.btn54Handler)
        self.btn55 = QPushButton('$1000',self)
        self.btn55.clicked.connect(self.btn55Handler)
        self.btn56 = QPushButton('$1000',self)
        self.btn56.clicked.connect(self.btn56Handler)

        # Create a label for each category
        self.cat1 = QLabel('label 1', self)
        self.cat2 = QLabel('label 2', self)
        self.cat3 = QLabel('label 3', self)
        self.cat4 = QLabel('label 4', self)
        self.cat5 = QLabel('label 5', self)
        self.cat6 = QLabel('label 6', self)

        # Create a list of each button object
        self.btnlist = [self.btn11, self.btn12, self.btn13, self.btn14, self.btn15, self.btn16, self.btn21, self.btn22, self.btn23, self.btn24, self.btn25, self.btn26, self.btn31, self.btn32, self.btn33, self.btn34, self.btn35, self.btn36, self.btn41, self.btn42, self.btn43, self.btn44, self.btn45, self.btn46, self.btn51, self.btn52, self.btn53, self.btn54, self.btn55, self.btn56]

        # Create a list of each category label object
        self.catlist = [self.cat1, self.cat2, self.cat3, self.cat4, self.cat5, self.cat6]

        # Create the other GUI elements. The score label, the score, the reset
        # button and the exit button
        self.scoreLbl = QLabel('Score', self)
        self.scoreLbl.setAlignment(Qt.AlignCenter)
        self.scoreLbl.setFont(QFont("Times", 32, QFont.Bold))
        self.score = QLabel('$0',self)
        self.score.setAlignment(Qt.AlignCenter)
        self.score.setFont(QFont("Times", 26, QFont.Bold))
        self.resetBtn = QPushButton('Reset Game', self)
        self.resetBtn.clicked.connect(self.reset)
        self.exitBtn = QPushButton('Exit', self)
        self.exitBtn.clicked.connect(self.exit)

        # Create 3 grid layouts. A left side, a right side, and a main layout to
        # hold both the left and the right side.
        self.mainGrid = QGridLayout(self)

        self.rightGrid = QGridLayout()
        self.rightGrid.setVerticalSpacing(100)

        self.leftGrid = QGridLayout()
        self.leftGrid.setVerticalSpacing(50)

        self.rightGrid.addWidget(self.scoreLbl, 0, 0, 2, 1)
        self.rightGrid.addWidget(self.score, 1, 0)
        self.rightGrid.addWidget(self.resetBtn, 2, 0, 2, 1)
        self.rightGrid.addWidget(self.exitBtn, 3, 0)

        # Set all of the attributes for each category label
        column = 0
        for cat in self.catlist:
            cat.setAlignment(Qt.AlignCenter)
            cat.setWordWrap(True)
            cat.setFixedWidth(150)
            self.leftGrid.addWidget(cat, 0, column)
            column+=1

        # Set all the attributes for each button
        row, column = 1, 0
        for btn in self.btnlist:
            btn.setFixedWidth(150)
            self.leftGrid.addWidget(btn, row, column)
            column+=1
            if column == 6:
                row+=1
                column = 0

        # Set the layouts and show the GUI
        self.mainGrid.addLayout(self.leftGrid, 0, 0)
        self.mainGrid.addLayout(self.rightGrid, 0, 1)

        self.setLayout(self.mainGrid)

        self.show()

    def changeScore(self, score):
        '''
            function:
                changeScore: This function gets called when the QuestionWindow
                             closes or when the DailyDoubleWindow closes. It
                             handles changing the score accordingly and loading
                             the QuestionWindow GUI for a daily double.

            args:
                score: String that is returned by the other GUI windows. It can
                       be formatted in one of two ways. If the DailyDoubleWindow
                       returns the string, it will look like this: 30xxyy...
                       where xx represents the identifier for the question on
                       the board and yy... represents the wager amount.
                       If the QuestionWindow returns the string, it will look
                       like this: xxyyy... Where xx represents the identifier
                       for the question on the board and yyy... can be any
                       length and represents the amount to the change the score.
                       It can be a positive or negative integer.

            returns:
                None

            raises:
                None 

            Note: the identifier represents what question was asked and can be
                  thought of as a number in a 5x6 matrix. It will be mapped in
                  this fashion:

                            [0  1  2  3  4  5 ]
                            [6  7  8  9  10 11]
                            [12 13 14 15 16 17]
                            [18 19 20 21 22 23]
                            [24 25 26 27 28 29]
        '''

        # Get the identifier of the question. 30 = daily double. 0-29 corresponds
        # with the question that was asked on the board
        identity = int(score[:2])
        if identity == 30:
            # Hide the dialog and calculate the row and column based on the
            # identifier. col = identifer % 6. row = (identifer - col) / 6
            self.dialog.hide()
            matrix_num = int(score[2:4])
            column = matrix_num % 6
            row = int((matrix_num - column) / 6)

            # Parse the question from the dictionary of dictionaries
            ques = self.cat_and_questions[self.categories[column]][row]

            # Load a question window for that question
            self.dialog = QuestionWindow(self, 'Daily Double!', ques, int(score[4:]), score[2:4], True)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            # Get the identifier of the question as well as the amount to add or
            # subtract and set the new score
            current_text = self.score.text()[1:]
            money = int(score[2:])
            new_score = int(current_text) + money
            self.score.setText('${}'.format(new_score))

            # Change the button text based on how they answered and disable it
            res = 'Correct' if money > 0 else 'Incorrect' if money < 0 else 'No Answer'
            self.btnlist[identity].setText(res)
            self.btnlist[identity].setEnabled(False)

            # Remove that button's identifier from the list
            self.questions_left.remove(identity)

            # When all the numbers are removed from the list, ask the user to
            # play again or start double jeopardy.
            if not self.questions_left:
                if self.double_jeopardy:
                    res = QMessageBox.question(self, 'Play Again?', 'Would you like to play jeopardy again?')
                    self.reset() if res == QMessageBox.Yes else sys.exit(0)
                else:
                    msg = QMessageBox.information(self, 'Double Jeopardy', "It's time to move on to Double Jeopardy!")
                    self.reset(400, False)
                    self.double_jeopardy = True

            self.dialog.hide()

    def reset(self, amount=200, reset_score=True):
        '''
            function:
                reset: This function either sets everything back to normal or
                       prepares the game for double jeopardy.

            args:
                amount:      200 if starting over or 400 if starting double
                             jeopardy
                reset_score: boolean to indicate whether to reset the score or 
                             not

            returns:
                None

            raises:
                None
        '''

        # If called by button press, the amount somehow becomes a False boolean.
        # Reassign it to the default value I want if that happens
        if not amount:
            amount = 200

        # Reset the score label if requested
        if reset_score:
            self.score.setText('$0')

        # Regenerate the list of numbers and reload the questions
        self.questions_left = [num for num in range(30)]
        self.double_jeopardy = False
        self.loadQuestions()

        # Relabel the buttons accordingly
        i = 0
        iterated_amount = amount
        for btn in self.btnlist:
            btn.setText('${}'.format(iterated_amount))
            btn.setEnabled(True)
            i+=1
            if i == 6:
                i = 0
                iterated_amount+=amount

    def exit(self):
        '''
            function:
                exit: This function gracefully closes the program

            args:
                None

            returns:
                None

            raises:
                None
        '''

        sys.exit(0)

    def btn11Handler(self):
        '''
            function:
                btn11Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[0]][0]
        if 0 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '00')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '00', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn12Handler(self):
        '''
            function:
                btn12Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[1]][0]
        if 1 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '01')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '01', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn13Handler(self):
        '''
            function:
                btn13Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[2]][0]
        if 2 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '02')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '02', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn14Handler(self):
        '''
            function:
                btn14Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[3]][0]
        if 3 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '03')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '03', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn15Handler(self):
        '''
            function:
                btn15Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[4]][0]
        if 4 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '04')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '04', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn16Handler(self):
        '''
            function:
                btn16Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[5]][0]
        if 5 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '05')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '05', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn21Handler(self):
        '''
            function:
                btn21Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[0]][1]
        if 6 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '06')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '06', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn22Handler(self):
        '''
            function:
                btn22Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[1]][1]
        if 7 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '07')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '07', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn23Handler(self):
        '''
            function:
                btn23Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[2]][1]
        if 8 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '08')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '08', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn24Handler(self):
        '''
            function:
                btn24Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[3]][1]
        if 9 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '09')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '09', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn25Handler(self):
        '''
            function:
                btn25Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[4]][1]
        if 10 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '10')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '10', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn26Handler(self):
        '''
            function:
                btn26Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[5]][1]
        if 11 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '11')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '11', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn31Handler(self):
        '''
            function:
                btn31Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[0]][2]
        if 12 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '12')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '12', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn32Handler(self):
        '''
            function:
                btn32Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[1]][2]
        if 13 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '13')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '13', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn33Handler(self):
        '''
            function:
                btn33Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[2]][2]
        if 14 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '14')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '14', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn34Handler(self):
        '''
            function:
                btn34Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[3]][2]
        if 15 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '15')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '15', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn35Handler(self):
        '''
            function:
                btn35Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[4]][2]
        if 16 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '16')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '16', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn36Handler(self):
        '''
            function:
                btn36Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[5]][2]
        if 17 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '17')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '17', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn41Handler(self):
        '''
            function:
                btn41Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[0]][3]
        if 18 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '18')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '18', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn42Handler(self):
        '''
            function:
                btn42Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[1]][3]
        if 19 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '19')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '19', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn43Handler(self):
        '''
            function:
                btn43Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[2]][3]
        if 20 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '20')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '20', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn44Handler(self):
        '''
            function:
                btn44Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[3]][3]
        if 21 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '21')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '21', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn45Handler(self):
        '''
            function:
                btn45Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[4]][3]
        if 22 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '22')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '22', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn46Handler(self):
        '''
            function:
                btn46Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[5]][3]
        if 23 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '23')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '23', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn51Handler(self):
        '''
            function:
                btn51Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[0]][4]
        if 24 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '24')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '24', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn52Handler(self):
        '''
            function:
                btn52Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[1]][4]
        if 25 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '25')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '25', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn53Handler(self):
        '''
            function:
                btn53Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[2]][4]
        if 26 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '26')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '26', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn54Handler(self):
        '''
            function:
                btn54Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[3]][4]
        if 27 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '27')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '27', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn55Handler(self):
        '''
            function:
                btn55Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[4]][4]
        if 28 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '28')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '28', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn56Handler(self):
        '''
            function:
                btn56Handler: This function handles its button press accordingly

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Check if it is a daily double. Handle the GUI creations accordingly
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[5]][4]
        if 29 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', self.double_jeopardy, self.score.text()[1:], '29')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '29', False)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def getQuestions(self):
        '''
            function:
                getQuestions: This function requests a random set of questions
                              from jservice.io. This is where the questions from
                              every past episode of Jeopardy come from

            args:
                None

            returns:
                tuple containing a string as the title and a list of
                dictionaries with the question as the key and the answer as the
                value

            raises:
                None
        '''

        # Get the json from the server
        response = requests.get('http://jservice.io/api/category?id={}'.format(randint(1,18418)))
        # If there is a problem, indicate to the user and fail gracefully
        if response.status_code != 200:
            msg = QMessageBox.information(self, 'Network Error', 'There was a problem getting a request from http://jservice.io/. Could not load questions')
            sys.exit(0)

        # Parse the response into a json object
        resp = response.json()

        # Because there are sometimes more than 5 questions per category,
        # Get a random starting number between 0 and the total number - 6.
        # Subtract 6 because randint is inclusive on both bounds. Then use
        # the next 5 questions from there
        count = int(resp['clues_count'])
        starting_num = randint(0, count-6) if count > 5 else 0

        clues = resp['clues']
        questions = []
        for i in range(starting_num,starting_num+5):
            question_answer = {}

            # Remove any bold and itilics tags that are sometimes in the
            # json responses. Also remove any backslashes
            question = clues[i]['question'].replace('<i>','').replace('</i>','').replace('\\',' ').replace('<b>','').replace('</b>','')
            answer = clues[i]['answer'].replace('<i>','').replace('</i>','').replace('\\',' ').replace('<b>','').replace('</b>','')
            question_answer[question] = answer
            questions.append(question_answer)

        # Return the title and the list of dictionaries
        return resp['title'], questions

    def checkForEmptyQuestions(self, questions_dicts):
        '''
            function:
                checkForEmptyQuestions: This function checks to make sure that
                                        no questions or answers are blank.
                                        This sometimes happens.

            args:
                question_dicts: The list of dictionaries that was created in
                                self.getQuestions()

            returns:
                None

            raises:
                None
        '''

        # Check every question and answer for blanks. Return True if none found
        # of False if any are found
        for question in questions_dicts:
                for key in question.keys():
                    if not key or not question[key]:
                        return False
        return True

    def loadQuestions(self):
        '''
            function:
                loadQuestions: This function loads 5 questions for each category

            args:
                None

            returns:
                None

            raises:
                None
        '''

        # Reset the lists and dictionaries to be empty
        self.categories = []
        self.cat_and_questions = {}
        self.daily_doubles = []

        # Do this 6 times and create the lists accordingly
        for i in range(6):
            category, questions = self.getQuestions()

            while not self.checkForEmptyQuestions(questions):
                category, questions = self.getQuestions()

            self.categories.append(category.upper())
            self.cat_and_questions[category.upper()] = questions
            self.catlist[i].setText(category.upper())

        # Get 2 random numbers for the daily doubles. Make sure that they are
        # not the same number
        daily = randint(0,29)
        self.daily_doubles.append(daily)
        second_daily = randint(0,29)
        while second_daily == daily:
            second_daily = randint(0,29)
        self.daily_doubles.append(second_daily)
            
# This is the main program so it should be the only executable one
if __name__ == '__main__':

    # Create an instance of a QApplication
    app = QApplication(sys.argv)

    # Create an instance of the Jeopardy class and show the GUI
    window = Jeopardy(None, title='Jeopardy')

    # Keep GUI alive
    sys.exit(app.exec_())

