from random import randint
import json, requests, wx

class Jeopardy(wx.Frame):

    def __init__(self, parent, title):

        super(Jeopardy, self).__init__(parent, title=title, size=(800,480))
        self.loadUI()

    def loadUI(self):
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

if __name__ == '__main__':

    # Create an instance of a wx Application
    app = wx.App()

    # Create an instance of the Jeopardy class and show the GUI
    window = Jeopardy(None, title='Jeopardy')
    window.Show()

    # Keep GUI alive
    app.MainLoop()
