from random import randint
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import json, requests, sys

class Jeopardy(QWidget):

    def __init__(self, parent, title):

        super().__init__()

        self.cat_and_questions = {}

        self.loadUI()
        self.loadQuestions()

    def loadUI(self):

        self.setFixedSize(1200,480)
        self.setWindowTitle('Jeopardy!')

        self.btn11 = QPushButton('$100',self)
        self.btn11.clicked.connect(self.btn11Handler)
        self.btn12 = QPushButton('$100',self)
        self.btn12.clicked.connect(self.btn12Handler)
        self.btn13 = QPushButton('$100',self)
        self.btn13.clicked.connect(self.btn13Handler)
        self.btn14 = QPushButton('$100',self)
        self.btn14.clicked.connect(self.btn14Handler)
        self.btn15 = QPushButton('$100',self)
        self.btn15.clicked.connect(self.btn15Handler)
        self.btn16 = QPushButton('$100',self)
        self.btn16.clicked.connect(self.btn16Handler)
        self.btn21 = QPushButton('$200',self)
        self.btn21.clicked.connect(self.btn21Handler)
        self.btn22 = QPushButton('$200',self)
        self.btn22.clicked.connect(self.btn22Handler)
        self.btn23 = QPushButton('$200',self)
        self.btn23.clicked.connect(self.btn23Handler)
        self.btn24 = QPushButton('$200',self)
        self.btn24.clicked.connect(self.btn24Handler)
        self.btn25 = QPushButton('$200',self)
        self.btn25.clicked.connect(self.btn25Handler)
        self.btn26 = QPushButton('$200',self)
        self.btn26.clicked.connect(self.btn26Handler)
        self.btn31 = QPushButton('$400',self)
        self.btn31.clicked.connect(self.btn31Handler)
        self.btn32 = QPushButton('$400',self)
        self.btn32.clicked.connect(self.btn32Handler)
        self.btn33 = QPushButton('$400',self)
        self.btn33.clicked.connect(self.btn33Handler)
        self.btn34 = QPushButton('$400',self)
        self.btn34.clicked.connect(self.btn34Handler)
        self.btn35 = QPushButton('$400',self)
        self.btn35.clicked.connect(self.btn35Handler)
        self.btn36 = QPushButton('$400',self)
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

        btnlist = [self.btn11, self.btn12, self.btn13, self.btn14, self.btn15, self.btn16, self.btn21, self.btn22, self.btn23, self.btn24, self.btn25, self.btn26, self.btn31, self.btn32, self.btn33, self.btn34, self.btn35, self.btn36, self.btn41, self.btn42, self.btn43, self.btn44, self.btn45, self.btn46, self.btn51, self.btn52, self.btn53, self.btn54, self.btn55, self.btn56]

        self.catlist = [self.cat1, self.cat2, self.cat3, self.cat4, self.cat5, self.cat6]

        self.scoreLbl = QLabel('Score', self)
        self.scoreLbl.setAlignment(Qt.AlignCenter)
        self.scoreLbl.setFont(QFont("Times", 32, QFont.Bold))
        self.score = QLabel('$0.00',self)
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
            cat.setFixedWidth(150)
            self.leftGrid.addWidget(cat, 0, column)
            column+=1

        row, column = 1, 0
        for btn in btnlist:
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

    def reset(self):
        pass

    def exit(self):
        sys.exit(0)

    def btn11Handler(self):
        pass

    def btn12Handler(self):
        pass

    def btn13Handler(self):
        pass

    def btn14Handler(self):
        pass

    def btn15Handler(self):
        pass

    def btn16Handler(self):
        pass

    def btn21Handler(self):
        pass

    def btn22Handler(self):
        pass

    def btn23Handler(self):
        pass

    def btn24Handler(self):
        pass

    def btn25Handler(self):
        pass

    def btn26Handler(self):
        pass

    def btn31Handler(self):
        pass

    def btn32Handler(self):
        pass

    def btn33Handler(self):
        pass

    def btn34Handler(self):
        pass

    def btn35Handler(self):
        pass

    def btn36Handler(self):
        pass

    def btn41Handler(self):
        pass

    def btn42Handler(self):
        pass

    def btn43Handler(self):
        pass

    def btn44Handler(self):
        pass

    def btn45Handler(self):
        pass

    def btn46Handler(self):
        pass

    def btn51Handler(self):
        pass

    def btn52Handler(self):
        pass

    def btn53Handler(self):
        pass

    def btn54Handler(self):
        pass

    def btn55Handler(self):
        pass

    def btn56Handler(self):
        pass

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
            question_answer[clues[i]['question']] = clues[i]['answer']
            questions.append(question_answer)

        return resp['title'], questions

    def loadQuestions(self):
        for i in range(6):
            category, questions = self.getQuestions()
            if len(category) > 15:
                pos = 15
                for char in category[15:]:
                    if char == ' ':
                        category = category[:pos] + '\n' + category[pos:]
                        break
                    pos+=1

            self.cat_and_questions[category.upper()] = questions
            self.catlist[i].setText(category.upper())
            

if __name__ == '__main__':

    # Create an instance of a QApplication
    app = QApplication(sys.argv)

    # Create an instance of the Jeopardy class and show the GUI
    window = Jeopardy(None, title='Jeopardy')

    # Keep GUI alive
    sys.exit(app.exec_())

