from tkinter import *
import settings
from cell import Cell

root = Tk()

# Set up window
root.configure(bg="black")
root.geometry(f"{settings.WINDOW_WIDTH}x{settings.WINDOW_HEIGHT}")
root.title("Minesweeper Game")
root.resizable(False, False)

top_frame = Frame(
    root, bg="black", width=settings.WINDOW_WIDTH, height=settings.WINDOW_HEIGHT / 5
)
top_frame.place(x=0, y=0)

left_frame = Frame(
    root,
    bg="black",
    width=settings.WINDOW_WIDTH / 5,
    height=settings.WINDOW_HEIGHT - (settings.WINDOW_HEIGHT / 5),
)
left_frame.place(x=0, y=settings.WINDOW_HEIGHT / 5)

center_frame = Frame(
    root,
    bg="black",
    width=settings.WINDOW_WIDTH * 0.8,
    height=settings.WINDOW_HEIGHT * 0.8,
)
center_frame.place(x=settings.WINDOW_WIDTH * 0.2, y=settings.WINDOW_HEIGHT * 0.2)

# Generate labels
Cell.create_cell_count_label(left_frame)
Cell.cell_count_label.place(x=0, y=0)

# Generate cells
for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_obj(center_frame)
        c.cell_btn.grid(column=x, row=y)

Cell.random_mines()

root.mainloop()
