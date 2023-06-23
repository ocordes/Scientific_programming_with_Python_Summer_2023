# mainform.py
#
# written by: Oliver Cordes 2023-06-05
# changed by: Oliver Cordes 2023-06-05

#import os

from ui_form import Ui_MainWindow
from ui_dialog import Ui_Dialog

from PyQt5 import QtWidgets
from PyQt5.QtGui import QBrush, QPen, QFont, QFontMetrics
from PyQt5.QtCore import  QCoreApplication, Qt

translate = QCoreApplication.translate


from word_game import WordGame
from player import SCRABBLE_LETTER_VALUES


# platform specific parts
from sys import platform


"""
this data is somewhat emperical not the best way to do ...
"""
if platform == 'darwin':
   fs1 = 30
   fs2 = 15
   yfs_ofs = 5
else:
   fs1 = 25
   fs2 = 15
   yfs_ofs = -5


class MainUI(Ui_MainWindow):
    def __init__(self, app, window):
        self._wordgame = None

        self._players = []
        self._current_player = None


    def setupUi(self, window):
        """
        setupUi setups a few GUI elements and connect a few buttons and menus.
        """
        super().setupUi(window)

        self._window = window
        self.actionStart.triggered.connect(self.start_game)
        self.actionPlayers.triggered.connect(self.player_settings)

        self.submitWord.clicked.connect(self.submit_word)
        self.finishGame.clicked.connect(self.finish_game)


    def draw_hand(self):
        """
        draw_hand simply draws a hand, this is working with Linux/MacOS
        """
        hand = self._current_player.getHand()

        letters = str(hand)



        font1 = QFont()
        font1.setPointSize(fs1)
        font1.setItalic(False)
        font1.setBold(True)

        font2 = QFont()
        font2.setPointSize(fs2)
        font2.setItalic(False)
        font2.setBold(False)

        fm1 = QFontMetrics(font1)
        fm2 = QFontMetrics(font2)
        #pixelsWide = fm.horizontalAdvance("What's the advance width of self text?")

        # create a scene according to the size of the graphicsview
        width = self.handView.viewport().width()
        height = self.handView.viewport().height()
        scene = QtWidgets.QGraphicsScene(0, 0, width, height)

        # some dynamic variables
        card_width = 50
        card_height = 50

        x = int((width-(card_width*len(letters)+5*(len(letters)-1)))/2)
        y = int((height-card_height)/2)

        # draw cards for all letters
        for letter in letters:
            rect = scene.addRect(0,0,card_width,card_height)
            rect.setPos(x,y)
            rect.setBrush(QBrush(Qt.GlobalColor.white))
            pen = QPen(Qt.GlobalColor.red)
            pen.setWidth(3)
            rect.setPen(pen)

            text = scene.addSimpleText(letter, font=font1)
            wt1 = fm1.horizontalAdvance(letter)
            ht1 = fm1.height()
            text.setPos(x+card_width/2-wt1/2,y+card_height/2-ht1/2)
            val = str(SCRABBLE_LETTER_VALUES[letter])
            text = scene.addSimpleText(val, font=font2)
            wt2 = fm2.horizontalAdvance(val)
            ht2 = fm2.height()
            text.setPos(x+45-wt2,y+yfs_ofs-card_height/4+ht2/2)

            x += card_width + 5
        self.handView.setScene(scene)


    def clear_dashboard(self):
        """
        clear_dashboard simply cleans the dashboard and deactivates the button until
        a new game is started

        the function is called when a game is over!
        """
        print('clear')
        width = self.handView.viewport().width()
        height = self.handView.viewport().height()
        scene = QtWidgets.QGraphicsScene(0, 0, width, height)
        self.handView.setScene(scene)
        self.playerName.setText('')
        self.score_label.setText('0')

        # disable all buttons and editlines
        self.submitWord.setEnabled(False)
        self.finishGame.setEnabled(False)
        self.wordEdit.setEnabled(False)

        # clear previous game
        self._wordgame = None


    def start_game(self):
        """
        start_game start a new game, checks also if a game is also active and
        asks to restart the game
        """
        if self._wordgame is not None:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText('You are already playing, do you awant to restart your game?')
            #msgBox.setInformativeText('Your points will be saved!')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = msgBox.exec()
            if ret == QtWidgets.QMessageBox.Cancel:
                return

        print('Start game')
        self.submitWord.setEnabled(True)
        self.finishGame.setEnabled(True)
        self.wordEdit.setEnabled(True)

        if len(self._players) == 0:
            # nobody is configured to play
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText('You have not configured any player! Abort game!')
            #msgBox.setInformativeText('Your points will be saved!')
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            ret = msgBox.exec()
            return

        self._wordgame = WordGame()
        #self._current_player = self._wordgame.start(self._players)

        # play a player
        self.play_player()


    def update_board(self):
        """
        update_boards sets all GUI elements for the next player
        """
        self.playerName.setText(self._current_player.getName())
        self.score_label.setText(str(self._current_player.getScore()))
        self.draw_hand()


    def submit_word(self):
        # get the entered word
        word = self.wordEdit.text()

        # lets play the word
        res = self._current_player.play(word.lower())

        # update the dashboard
        self.update_board()

        # clear the edited word
        self.wordEdit.setText('')

        # if word is not valid, show a message
        if not res:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText('Your entered word is invalid:')
            msgBox.setInformativeText(f'>> {word} <<')
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.exec()


    def finish_game(self):
        # ask the user to finish the game
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText('You want to finish your game?')
        msgBox.setInformativeText('Your points will be saved!')
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
        ret = msgBox.exec()

        # user wants to quit
        if ret == QtWidgets.QMessageBox.Ok:
            # sets the current user to finish state
            self._current_player.setFinished()

            # play the next player
            self.play_player()


    def play_player(self):
        """
        play_player

        is some logic between human and computer players; if the next player is a computer,
        all things are done immedeately, if a human player play, the program is waiting
        for input

        the function starts with choosing a next player!
        """
        if self._current_player is None:
            # game start!
            self._current_player = self._wordgame.start(self._players)
        else:
            # choose the next player
            self._current_player = self._wordgame.nextPlayer()


        # handle computer player and skip until a human player
        # is available
        while (self._current_player is not None ) and self._current_player.isComputerplayer():
            print(self._current_player.getName())
            self._current_player.play_hand()
            self._current_player.setFinished()
            self._current_player = self._wordgame.nextPlayer()

        if self._current_player is None:
            # game over, everybody has played

            # get a box with the results
            msgBox = QtWidgets.QMessageBox()
            results = self._wordgame.final_scores()
            msgBox.setText('Final scores')
            msgBox.setInformativeText(results)
            ret = msgBox.exec()

            # finally, clear the game
            self.clear_dashboard()
        else:
            # setup for a human player
            self.update_board()


    def player_settings(self):
        print('Player settings')

        dialog = SettingsDialog()

        ret = dialog.exec()

        if ret == 1:
            print('OK')
            self._players = dialog.getdata()
        else:
            print(f'Unknown {ret}')



class SettingsDialog(QtWidgets.QDialog):
    """Employee dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)


    def getdata(self):
        players = []
        s = self.ui.player1name.text()
        if self.ui.player1computer.isChecked():
            players.append(None)
        else:
            if s != '':
                players.append(s)


        s = self.ui.player2name.text()
        if self.ui.player2computer.isChecked():
            players.append(None)
        else:
            if s != '':
                players.append(s)


        s = self.ui.player3name.text()
        if self.ui.player3computer.isChecked():
            players.append(None)
        else:
            if s != '':
                players.append(s)


        s = self.ui.player4name.text()
        if self.ui.player4computer.isChecked():
            players.append(None)
        else:
            if s != '':
                players.append(s)


        s = self.ui.player5name.text()
        if self.ui.player5computer.isChecked():
            players.append(None)
        else:
            if s != '':
                players.append(s)


        s = self.ui.player6name.text()
        if self.ui.player6computer.isChecked():
            players.append(None)
        else:
            if s != '':
                players.append(s)

        return players

