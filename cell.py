import sys
import settings
from tkinter import Button, Label
import random
import ctypes


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label = None
    recurse_depth = 0

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_marked = False
        self.cell_btn = None
        self.x = x
        self.y = y

        Cell.all.append(self)

    def create_btn_obj(self, location):
        btn = Button(location, width=8, height=3)
        btn.bind("<Button-1>", self.left_click)
        btn.bind("<Button-3>", self.right_click)
        self.cell_btn = btn
        self.cell_btn.configure(bg="white", font=("", 14))

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            text=f"Cells Left: {Cell.cell_count}",
            width=12,
            height=4,
            bg="black",
            fg="white",
            font=("", 16),
        )
        Cell.cell_count_label = lbl

    def get_cell_by_position(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    def left_click(self, event):
        Cell.recurse_depth = 0
        # Check for fail condition
        if self.is_mine:
            self.show_mine()
        # Check for the number of surrounding mines
        else:
            print(self.surrounded_cells)
            if self.surrounded_cells_mines == 0:
                print("Triggered Zero")
                # Open all surrounding cells
                self.check_surrounded_cells()
            self.show_cell()
            # Check if player has won
            if Cell.cell_count == settings.MINE_COUNT:
                ctypes.windll.user32.MessageBoxW(
                    0, "You won the game!", "Congratulations", 0
                )
        self.cell_btn.unbind("<Button-1>")
        self.cell_btn.unbind("<Button-3>")

    def right_click(self, event):
        if not self.is_opened:
            if not self.is_marked:
                self.cell_btn.configure(bg="orange", text="💣")
                self.is_marked = True
            else:
                self.cell_btn.configure(bg="white", text="")
                self.is_marked = False

    def check_surrounded_cells(self):
        if self.surrounded_cells_mines == 0:
            # Open all surrounding cells
            for cell_obj in self.surrounded_cells:
                if not cell_obj.is_opened:
                    cell_obj.show_cell()
                    Cell.recurse_depth += 1
                    print(Cell.recurse_depth)
                    print(cell_obj)
                    cell_obj.check_surrounded_cells()

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn.configure(bg="white", text=f"{self.surrounded_cells_mines}")
            Cell.cell_count_label.configure(text=f"Cells Left: {Cell.cell_count}")
            self.is_opened = True

    def show_mine(self):
        self.cell_btn.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, "You clicked on a mine", "Game Over", 0)
        sys.exit()

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_position(self.x - 1, self.y - 1),
            self.get_cell_by_position(self.x + 0, self.y - 1),
            self.get_cell_by_position(self.x + 1, self.y - 1),
            self.get_cell_by_position(self.x - 1, self.y + 0),
            self.get_cell_by_position(self.x + 1, self.y + 0),
            self.get_cell_by_position(self.x - 1, self.y + 1),
            self.get_cell_by_position(self.x + 0, self.y + 1),
            self.get_cell_by_position(self.x + 1, self.y + 1),
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines(self):
        num_mines = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                num_mines += 1
        return num_mines

    @staticmethod
    def random_mines():
        mines = random.sample(Cell.all, settings.MINE_COUNT)
        for cell in mines:
            cell.is_mine = True

    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y})"
