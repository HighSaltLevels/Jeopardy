from random import randint
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from questionwindow import QuestionWindow
from dailydouble import DailyDoubleWindow
import json, requests, sys

class Jeopardy(QWidget):

    def __init__(self, parent=None, title=''):

        super(Jeopardy, self).__init__(parent)

        self.double_jeopardy = False
        self.cat_and_questions = {}
        self.categories = []
        self.daily_doubles = []

        self.questions_left = [num for num in range(30)]

        self.loadUI()
        self.loadQuestions()

    def loadUI(self):

        self.setFixedSize(1200,480)
        self.setWindowTitle('Jeopardy!')

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

        self.cat1 = QLabel('label 1', self)
        self.cat2 = QLabel('label 2', self)
        self.cat3 = QLabel('label 3', self)
        self.cat4 = QLabel('label 4', self)
        self.cat5 = QLabel('label 5', self)
        self.cat6 = QLabel('label 6', self)

        self.btnlist = [self.btn11, self.btn12, self.btn13, self.btn14, self.btn15, self.btn16, self.btn21, self.btn22, self.btn23, self.btn24, self.btn25, self.btn26, self.btn31, self.btn32, self.btn33, self.btn34, self.btn35, self.btn36, self.btn41, self.btn42, self.btn43, self.btn44, self.btn45, self.btn46, self.btn51, self.btn52, self.btn53, self.btn54, self.btn55, self.btn56]

        self.catlist = [self.cat1, self.cat2, self.cat3, self.cat4, self.cat5, self.cat6]

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

        self.mainGrid = QGridLayout(self)

        self.rightGrid = QGridLayout()
        self.rightGrid.setVerticalSpacing(100)

        self.leftGrid = QGridLayout()
        self.leftGrid.setVerticalSpacing(50)

        self.rightGrid.addWidget(self.scoreLbl, 0, 0, 2, 1)
        self.rightGrid.addWidget(self.score, 1, 0)
        self.rightGrid.addWidget(self.resetBtn, 2, 0, 2, 1)
        self.rightGrid.addWidget(self.exitBtn, 3, 0)

        column = 0
        for cat in self.catlist:
            cat.setAlignment(Qt.AlignCenter)
            cat.setWordWrap(True)
            cat.setFixedWidth(150)
            self.leftGrid.addWidget(cat, 0, column)
            column+=1

        row, column = 1, 0
        for btn in self.btnlist:
            btn.setFixedWidth(150)
            self.leftGrid.addWidget(btn, row, column)
            column+=1
            if column == 6:
                row+=1
                column = 0

        self.mainGrid.addLayout(self.leftGrid, 0, 0)
        self.mainGrid.addLayout(self.rightGrid, 0, 1)

        self.setLayout(self.mainGrid)

        self.show()

    def changeScore(self, score):
        identity = int(score[0:2])
        current_text = self.score.text()[1:]
        money = int(score[2:])
        new_score = int(current_text) + money
        self.score.setText('${}'.format(new_score))
        res = 'Correct' if money > 0 else 'Incorrect' if money < 0 else 'No Answer'
        self.btnlist[identity].setText(res)
        self.btnlist[identity].setEnabled(False)

        self.questions_left.remove(identity)
        if not self.questions_left:
            if self.double_jeopardy:
                pass
            else:
                msg = QMessageBox.information(self, 'Double Jeopardy', "It's time to move on to Double Jeopardy!")
                self.questions_left = [num for num in range(30)]
                self.startDoubleJeopardy()
                self.double_jeopardy = True

        self.dialog.hide()

    def startDoubleJeopardy(self):
        self.loadQuestions()
        i = 0
        amount = 400
        for btn in self.btnlist:
            btn.setText('${}'.format(amount))
            btn.setEnabled(True)
            i+=1
            if i == 6:
                i = 0
                amount+=400

    def reset(self):
        pass

    def exit(self):
        sys.exit(0)

    def btn11Handler(self):
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[0]][0]
        if 0 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '00', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '00')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn12Handler(self):
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[1]][0]
        if 1 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '01', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '01')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn13Handler(self):
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[2]][0]
        if 2 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '02', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '02')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn14Handler(self):
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[3]][0]
        if 3 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '03', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '03')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn15Handler(self):
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[4]][0]
        if 4 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '04', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '04')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn16Handler(self):
        worth = 400 if self.double_jeopardy else 200
        ques = self.cat_and_questions[self.categories[5]][0]
        if 5 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '05', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '05')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn21Handler(self):
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[0]][1]
        if 6 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '06', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '06')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn22Handler(self):
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[1]][1]
        if 7 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '07', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '07')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn23Handler(self):
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[2]][1]
        if 8 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '08', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '08')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn24Handler(self):
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[3]][1]
        if 9 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '09', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '09')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn25Handler(self):
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[4]][1]
        if 10 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '10', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '10')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn26Handler(self):
        worth = 800 if self.double_jeopardy else 400
        ques = self.cat_and_questions[self.categories[5]][1]
        if 11 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '11', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '11')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn31Handler(self):
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[0]][2]
        if 12 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '12', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '12')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn32Handler(self):
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[1]][2]
        if 13 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '13', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '13')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn33Handler(self):
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[2]][2]
        if 14 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '14', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '14')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn34Handler(self):
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[3]][2]
        if 15 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '15', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '15')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn35Handler(self):
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[4]][2]
        if 16 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '16', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '16')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn36Handler(self):
        worth = 1200 if self.double_jeopardy else 600
        ques = self.cat_and_questions[self.categories[5]][2]
        if 17 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '17', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '17')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn41Handler(self):
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[0]][3]
        if 18 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '18', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '18')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn42Handler(self):
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[1]][3]
        if 19 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '19', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '19')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn43Handler(self):
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[2]][3]
        if 20 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '20', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '20')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn44Handler(self):
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[3]][3]
        if 21 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '21', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '21')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn45Handler(self):
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[4]][3]
        if 22 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '22', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '22')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn46Handler(self):
        worth = 1600 if self.double_jeopardy else 800
        ques = self.cat_and_questions[self.categories[5]][3]
        if 23 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '23', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '23')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn51Handler(self):
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[0]][4]
        if 24 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '24', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '24')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn52Handler(self):
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[1]][4]
        if 25 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '25', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '25')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn53Handler(self):
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[2]][4]
        if 26 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '26', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '26')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn54Handler(self):
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[3]][4]
        if 27 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '27', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '27')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn55Handler(self):
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[4]][4]
        if 28 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '28', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '28')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def btn56Handler(self):
        worth = 2000 if self.double_jeopardy else 1000
        ques = self.cat_and_questions[self.categories[5]][4]
        if 29 in self.daily_doubles:
            msg = QMessageBox.information(self, 'Daily Double!', 'Answer... DAILY DOUBLE!!!!')
            self.dialog = DailyDoubleWindow(self, 'Daily Double', ques, '29', self.score.text()[1:], self.double_jeopardy)
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()
        else:
            self.dialog = QuestionWindow(self, '${} Question'.format(worth), ques, worth, '29')
            self.dialog.result_signal.connect(self.changeScore)
            self.dialog.showQuestion()

    def getQuestions(self):

        response = requests.get('http://jservice.io/api/category?id={}'.format(randint(1,18418)))
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
            question = clues[i]['question'].replace('<i>','').replace('</i>','').replace('\\',' ')
            answer = clues[i]['answer'].replace('<i>','').replace('</i>','').replace('\\',' ')
            question_answer[question] = answer
            questions.append(question_answer)

        return resp['title'], questions

    def loadQuestions(self):
        self.categories = []
        self.cat_and_questions = {}
        self.daily_doubles = []

        for i in range(6):
            category, questions = self.getQuestions()

            self.categories.append(category.upper())
            self.cat_and_questions[category.upper()] = questions
            self.catlist[i].setText(category.upper())

        daily = randint(0,29)
        self.daily_doubles.append(daily)
        second_daily = randint(0,29)
        while second_daily == daily:
            second_daily = randint(0,29)
        self.daily_doubles.append(second_daily)
            

if __name__ == '__main__':

    # Create an instance of a QApplication
    app = QApplication(sys.argv)

    # Create an instance of the Jeopardy class and show the GUI
    window = Jeopardy(None, title='Jeopardy')

    # Keep GUI alive
    sys.exit(app.exec_())

