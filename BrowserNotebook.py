import tkinter as tk
from tkinter import *
from tkcolorpicker import askcolor
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import random

"""A ttk Notebook"""

global blops_data


def proof_read(data):
    print("len:" + str(len(data)))
    # TODO 8 not 7
    if len(data) != 7:
        return "Not all elements all saved!"
    if data[0].get() is None:
        return "No name is saved!"
    if next((x for x in blops_data if x[0] == data[0]), None) is not None:
        return "This name is already taken"
    # survival must be < replication
    if data[4].get() > data[5].get():
        return "Replication Q is not bigger than Survival Q"
    if not data[1].get().isdigit() or data[1] > 100:
        return "Share value is not digit or exceeds 100%"
    cur_sum = 0
    for kind in blops_data:
        cur_sum += kind[1].get()
    if data[1].get() + cur_sum > 100:
        return "Total apparition chance for all kinds exceeds 100%"
    return ''


def save_blop(widget, data):
    if proof_read(data) is not None:
        messagebox.showerror("Invalid input", proof_read(data))
    else:
        blops_data.append(data)
    for dat in data:
        print(dat)

    print(data[0].get())


def clone_blop(widget, this_tab_data):
    widget.manual_add_tab()
    print(len(this_tab_data))
    print(len(blops_data[-1]))
    for old_trait, blank_trait in zip(this_tab_data, blops_data[-1]):
        try:
            blank_trait.set(old_trait.get())
        except Exception:
            blank_trait = old_trait


def handle_focus_in(full_name_entry):
    if full_name_entry.cget("fg") == 'grey':
        full_name_entry.delete(0, tk.END)
        full_name_entry.config(fg='white', font=("Helvetica", 10))


def handle_focus_out(root):
    root.focus_set()


def handle_enter(widget, tab, full_name_entry):
    widget.tab(tab, text=full_name_entry.get())


def pick_color(label, color_var):
    _, rgb = askcolor((255, 255, 0))
    if rgb is not None:
        label.config(background=rgb, text='Picked', compound='right', fg="Black")
        color_var = rgb


class BrowserNotebook(ttk.Notebook):

    def fill_tab(self, tab1):
        print(tab1.__class__)
        # name
        name_lbl = tk.Label(tab1, text="Name")
        name_lbl.grid(row=0, column=0, columnspan=2, pady=(8, 4))

        name_icon = ImageTk.PhotoImage(Image.open("./data/icons/brand.png").resize((45, 45), Image.ANTIALIAS))
        name_icon_lbl = tk.Label(tab1, image=name_icon)
        name_icon_lbl.image = name_icon
        name_icon_lbl.grid(row=1, column=0, padx=(5, 5), pady=(0, 8))

        blop_data = []

        name_var = StringVar(tab1)
        name_field = tk.Entry(tab1, width=12, font=("Helvetica", 10), fg='grey', textvariable=name_var)
        blop_data.append(name_var)
        name_field.grid(row=1, column=1)
        name_field.insert(tk.END, "Bloppy Blop")
        name_field.bind("<FocusIn>", lambda _: handle_focus_in(name_field))
        name_field.bind("<FocusOut>", lambda _: handle_focus_out(tab1))
        name_field.bind("<Return>", lambda _: handle_enter(self, tab1, name_field))

        # population share
        ratio_lbl = tk.Label(tab1, text="Share")
        ratio_lbl.grid(row=2, column=0, columnspan=2, pady=(0, 0))

        ratio_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/piechart.png").resize((55, 55), Image.ANTIALIAS))
        ratio_icon_lbl = tk.Label(tab1, image=ratio_icon)
        ratio_icon_lbl.image = ratio_icon
        ratio_icon_lbl.grid(row=3, column=0, padx=(10, 10), pady=8)

        ratio_var = StringVar(tab1)
        ratio_field = tk.Entry(tab1, width=12, font=("Helvetica", 10), fg='grey', justify='right',
                               textvariable=ratio_var)
        blop_data.append(ratio_var)

        ratio_field.grid(row=3, column=1)
        ratio_field.insert(tk.END, str(random.randint(0, 100)) + "%")
        ratio_field.bind("<FocusIn>", lambda _: handle_focus_in(ratio_field))
        ratio_field.bind("<FocusOut>", lambda _: handle_focus_out(tab1))

        # speed section
        speed_lbl = tk.Label(tab1, text="Speed")
        speed_lbl.grid(row=4, column=0, columnspan=2, pady=(8, 4))

        speed_icon = ImageTk.PhotoImage(Image.open("./data/icons/speed2.png").resize((50, 50), Image.ANTIALIAS))
        speed_icon_lbl = tk.Label(tab1, image=speed_icon)
        speed_icon_lbl.image = speed_icon  # we need to keep reference to it
        speed_icon_lbl.grid(row=5, column=0, padx=(10, 5), pady=(0, 0))

        speed_var = DoubleVar(tab1)
        speed_scale = tk.Scale(tab1, from_=0.5, to=5, orient=tk.HORIZONTAL, resolution=0.1, length=100,
                               variable=speed_var)
        speed_scale.grid(row=5, column=1, sticky='new', padx=(5, 0))
        speed_scale.set(1)
        blop_data.append(speed_var)

        # color label
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        color_var = color
        picked_color_lbl = tk.Label(tab1, background=color, width=12, height=1,
                                    text="Random", fg='black', font=("Helvetica", 10))
        picked_color_lbl.grid(row=6, column=1, pady=25, padx=(10, 6))

        color_icon = ImageTk.PhotoImage(Image.open("./data/icons/colorpicker.png").resize((50, 50), Image.ANTIALIAS))
        color_btn = tk.Button(tab1, image=color_icon, command=lambda: pick_color(picked_color_lbl, color_var), border=0)
        color_btn.image = color_icon
        color_btn.grid(row=6, column=0, pady=25, padx=10)
        blop_data.append(color_var)

        # survival section
        survive_lbl = tk.Label(tab1, text="Survival")
        survive_lbl.grid(row=0, column=2, columnspan=2, pady=(8, 4))

        survive_icon = ImageTk.PhotoImage(Image.open("./data/icons/life.png").resize((50, 50), Image.ANTIALIAS))
        survive_icon_lbl = tk.Label(tab1, image=survive_icon)
        survive_icon_lbl.image = survive_icon
        survive_icon_lbl.grid(row=1, column=2, padx=(20, 0))

        survive_var = DoubleVar(tab1)
        survive_scale = tk.Scale(tab1, from_=0.5, to=5, orient=tk.HORIZONTAL, resolution=0.1, length=100,
                                 variable=survive_var)
        blop_data.append(survive_var)
        survive_scale.grid(row=1, column=3, sticky='new', padx=(0, 10))
        survive_scale.set(1)

        # replicate section
        replica_lbl = tk.Label(tab1, text="Replication")
        replica_lbl.grid(row=2, column=2, columnspan=2, pady=(10, 0))

        replica_icon = ImageTk.PhotoImage(Image.open("./data/icons/cycle2.png").resize((55, 55), Image.ANTIALIAS))
        replica_icon_lbl = tk.Label(tab1, image=replica_icon)
        replica_icon_lbl.image = replica_icon
        replica_icon_lbl.grid(row=3, column=2, padx=(20, 0), pady=8)

        replica_var = DoubleVar(tab1)
        replica_scale = tk.Scale(tab1, from_=0.5, to=5, orient=tk.HORIZONTAL, resolution=0.1, length=120,
                                 variable=replica_var)
        blop_data.append(replica_var)
        replica_scale.grid(row=3, column=3, sticky='new', padx=(0, 10))
        replica_scale.set(2)

        # encounter
        encounter_lbl = tk.Label(tab1, text="Behavior")
        encounter_lbl.grid(row=4, column=2, columnspan=2, pady=(0, 0))

        encounter_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/boxing.png").resize((60, 60), Image.ANTIALIAS))
        encounter_icon_lbl = tk.Label(tab1, image=encounter_icon)
        encounter_icon_lbl.image = encounter_icon
        encounter_icon_lbl.grid(row=5, column=2, padx=(20, 0), pady=8)

        encounter_var = StringVar(tab1)
        encounter_options = ttk.OptionMenu(tab1, encounter_var, "Neutral",  # <- pre-chosen
                                           "Aggressive", "Submissive", "Neutral")  # all options
        blop_data.append(encounter_var)
        encounter_options.grid(row=5, column=3, padx=(0, 10))

        # mutations
        mutation_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/dna3.png").resize((50, 50), Image.ANTIALIAS))
        mutation_icon_lbl = tk.Label(tab1, image=mutation_icon)
        mutation_icon_lbl.image = mutation_icon
        mutation_icon_lbl.grid(row=6, column=2, padx=(20, 0), pady=15)

        mutation_btn = ttk.Button(tab1, text='Mutations', command=lambda: save_blop(self, tab1))
        mutation_btn.grid(row=6, column=3, pady=15)

        # control buttons
        save_btn = ttk.Button(tab1, text='Save', command=lambda: save_blop(self, blop_data))
        save_btn.grid(row=7, column=3, padx=10, pady=10)

        clone_btn = ttk.Button(tab1, text='Clone', command=lambda: clone_blop(self, blop_data))
        clone_btn.grid(row=7, column=2, padx=10, pady=10)

        new_btn = ttk.Button(tab1, text='New', command=lambda: self.manual_add_tab())
        new_btn.grid(row=7, column=1, padx=10, pady=10)

    __initialized = False

    def __init__(self, parent, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)
        self.notebook = ttk.Notebook(parent)
        self._active = None
        self.parent = parent
        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        global blops_data
        blops_data = []
        tab = tk.Frame(self)
        self.fill_tab(tab)
        self.add(tab, text='first kind')

    """Called when the button is pressed over the close button"""

    def on_close_press(self, event):
        element = self.identify(event.x, event.y)

        if "close" in element:
            if messagebox.askokcancel("Quit", "Do you want to quit? All entered data will be erased!"):
                index = self.index("@%d,%d" % (event.x, event.y))
                self.state(['pressed'])
                self._active = index
                self.update()
                self.on_close_release(event)

    def on_close_release(self, event):
        """Called when the button is released over the close button"""
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        with open('./data/close_base64.txt', 'r') as file:
            data = file.read().replace('\n', '')
        with open('./data/close_red_base64.txt', 'r') as file:
            data2 = file.read().replace('\n', '')

        self.images = (
            tk.PhotoImage("img_close", data=data),
            tk.PhotoImage("img_closeactive", data=data2),
            tk.PhotoImage("img_closepressed", data=data2)
        )

        style.element_create("close", "image", "img_close",
                             ("active", "pressed", "!disabled", "img_closepressed"),
                             ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])

    def manual_add_tab(self):
        new_tab = tk.Frame(self)
        self.fill_tab(new_tab)
        self.add(new_tab, text="new kind")


if __name__ == "__main__":
    root = tk.Tk()
    notebook = BrowserNotebook(root)
    notebook.grid(row=0, column=0, sticky="nsew")
    root.mainloop()

