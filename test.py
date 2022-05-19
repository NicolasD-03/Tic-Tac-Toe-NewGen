from tkinter import Tk

from libs.ui.board import Board


window = Tk()
window.geometry("900x900")
board_list = [["", "", ""], ["", "", ""], ["", "", ""]]
board = Board(window, board_list)


window.mainloop()
