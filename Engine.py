import pygame
import random
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image
from PIL import ImageTk
import os
import Blop
import Food

def hello():
    print("hello!")


root = tk.Tk()
root.iconphoto(False, tk.PhotoImage(file="../data/icons/angry_bird.png"))
root.title("Simulacrum")
embed = tk.Frame(root, width=500, heigh=500)  # creates embed frame for pygame window
embed.grid(columnspan=(600), rowspan=500)  # Adds grid
embed.grid(row=0, column=1)  # packs window to the left
buttonwin = tk.Frame(root, width=200, height=500)
buttonwin.grid(row=0, column=0)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
screen = pygame.display.set_mode((500, 500))
# screen.fill(pygame.Color(25, 155, 255))
background_image = pygame.image.load("../data/icons/space.png").convert()
background_image = pygame.transform.scale(background_image, (500, 500))
screen.blit(background_image, [0, 0])
for i in range(6):
    blop = Blop.Blop(screen)
    blop.draw(40 + round(random.random() * 390), 50 + round(random.random() * 390))
    food = Food.Food(screen)
    food.draw(40 + round(random.random() * 390), 50 + round(random.random() * 390))


root.resizable(False, False)
pygame.display.init()
pygame.display.update()

# menu
menubar = Menu(root)
# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_command(label="Snap", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Manual", command=hello)
helpmenu.add_command(label="About", command=hello)
helpmenu.add_command(label="Donate", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

label = tk.Label(buttonwin, text='Scenarios')
label.config(font=("Calibri", 11))
label.grid(row=0, column=0, columnspan=3, pady=5)

scenario = ttk.Combobox(buttonwin)
scenario['values'] = ("Natural Selection", "Altruism", "Survival")
# scenario.pack(side = TOP)
scenario.grid(row=1, column=0, pady=10, padx=10, columnspan=3)

label = tk.Label(buttonwin, text='Design')
label.config(font=("Calibri", 11))
label.grid(row=2, column=0, columnspan=3, pady=5)

regime = ttk.Combobox(buttonwin)
regime.set('Choose your regime')
regime['values'] = ("Space", "Field", "Human")
regime.grid(row=3, column=0, pady=10, padx=10, columnspan=3)

label = tk.Label(buttonwin, text='Speed')
label.config(font=("Calibri", 11))
label.grid(row=4, column=0, columnspan=3)

speed = Scale(buttonwin, from_=0.5, to=5, orient=tk.HORIZONTAL, resolution=0.1, length=170)
speed.grid(row=6, column=0, pady=5, columnspan=3)

play_icon = ImageTk.PhotoImage(Image.open("../data/icons/play.png").resize((40, 40), Image.ANTIALIAS))
start_btn = Button(buttonwin, text=' Start', command=hello, image=play_icon, border='0')
start_btn.grid(row=8, column=0, pady=35)

pause_icon = ImageTk.PhotoImage(Image.open("../data/icons/pause2.png").resize((40, 40), Image.ANTIALIAS))
pause_btn = Button(buttonwin, text=' Pause', command=hello, image=pause_icon, border="0")
pause_btn.grid(row=8, column=1, pady=35)

stop_icon = ImageTk.PhotoImage(Image.open("../data/icons/stop.png").resize((40, 40), Image.ANTIALIAS))
finish_btn = Button(buttonwin, command=hello, image=stop_icon, text=' Finish', border='0')
finish_btn.grid(row=8, column=2, pady=35)
root.update()

crushed = False
while not crushed:
    pygame.display.update()
    root.update()
