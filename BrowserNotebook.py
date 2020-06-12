import tkinter as tk
from tkcolorpicker import askcolor
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import random

"""A ttk Notebook"""

global blops_data


def show_info():
    messagebox.showinfo("Help?", "This is Blop Catalogue. Each tab is used to describe one kind of creatures."
                                 "First tab is created automatically, since at least one kind is required for "
                                 "simulation to exist. Follow these instructions to create valid BlopKind:"
                                 "\n\n1. You must name the kind, and name must be unique"
                                 "\n\n2. Change default speed, replica (HP for breeding) and survival (HP for "
                                 "surviving) thresholds if you wish. Replica value must exceed survival."
                                 "\n\n3. Share field is used to define initial population structure - that is, "
                                 "what part this kind will constitute in it. You can write number from 0 to 100, "
                                 "but keep in mind that total probabilities of saved kinds must be equal to 100 "
                                 "\n\n4. Behavior defines blop paradigm of interaction with other blops"
                                 "\n\n5. Mutations window allows you to establish rules of breeding and evolution. You "
                                 "can assign chance of creating that specific descender of creature of this kind. "
                                 "Default variant is absence of mutations, in other words, bloppy blop will only be "
                                 "able to create bloppy blops"
                                 "\n\n6. Blop characterising color is randomized, but you're able to change it if you "
                                 "wish by clicking on color picker icon. That color will be used in data "
                                 "representation, so it's advised to pick quite distinguishable colors for your "
                                 "convenience"
                                 "\n\n7. Click New if you want to compose another race of blops. Use Clone if you want "
                                 "to create quite similar type - all you entered data, except of unique name, "
                                 "will be copied to the new tab. When you are done with the race, click Save. If you "
                                 "change something later don't forget to Save again."
                        )


def mutate_win(wind, tab, data):
    mini_root = tk.Tk()
    win = ttk.Frame(mini_root)
    # for entry in valid_blops:
    #     print(1)

    save_btn = ttk.Button(win, text='Save', command=lambda: save_mute(data))
    save_btn.grid(row=1, column=1, padx=10, pady=10)

def save_mute():

def proof_read(data):
    print("len:" + str(len(data)))
    # TODO 8 not 7
    if len(data) != 7:
        return "Not all elements all saved!"
    if data[0].get() == "":
        return "No name is saved!"
    if next((x for x in list(valid_blops.values()) if x[0].get() == data[0].get()), None) is not None:
        return "This name is already taken"
    # survival must be < replication
    if data[4].get() > data[5].get():
        return "Replication Q is not bigger than Survival Q"
    if not data[1].get().replace('%', '').isdigit():
        return "Share value is not digit"
    share = float(data[1].get())
    if share > 100:
        return "Share exceeds 100%"
    cur_sum = 0
    for kind in blops_data:
        cur_sum += float(kind[1].get())
    if share + cur_sum > 100:
        return "Total apparition chance for all kinds exceeds 100%"
    print("All is fine")
    return None


def save_blop(widget, tab, data):
    if proof_read(data) is not None:
        messagebox.showerror("Invalid input", proof_read(data))
        print("!")
    else:
        messagebox.showinfo("!", "!")
        valid_blops[widget.select()] = data


def clone_blop(widget, this_tab, this_tab_data):
    # WARNING: 5 is hard coded index of ratio entry field. If layout is changed, this needs TBU
    this_tab.winfo_children()[5].focus_set()
    this_tab.update()
    print(this_tab.winfo_children()[5].get())
    tab = widget.add_filled_tab(True)
    for old_trait, blank_trait in zip(this_tab_data, blops_data[-1]):
        try:
            blank_trait.set(old_trait.get())
        except Exception:
            blank_trait = old_trait
    for kid in widget.winfo_children():
        print(kid)
    # tab.focus_set()


def handle_focus_in(full_name_entry):
    print("focus")
    if full_name_entry.cget("fg") == 'grey':
        full_name_entry.delete(0, tk.END)
        full_name_entry.config(fg='white', font=("Helvetica", 10))


def handle_focus_out(root):
    pass
    # root.focus_set()


def handle_enter(widget, tab, full_name_entry):
    widget.tab(tab, text=full_name_entry.get())


def pick_color(label, color_var):
    _, rgb = askcolor((255, 255, 0))
    if rgb is not None:
        label.config(background=rgb, text='Picked', compound='right', fg="Black")
        color_var = rgb


class BlopCatalogue(ttk.Notebook):

    def fill_tab(self, tab1, auto=False):
        print(tab1.__class__)
        # name
        name_lbl = ttk.Label(tab1, text="Name")
        name_lbl.grid(row=0, column=0, columnspan=2, pady=(8, 4))

        name_icon = ImageTk.PhotoImage(Image.open("./data/icons/brand.png").resize((45, 45), Image.ANTIALIAS))
        name_icon_lbl = ttk.Label(tab1, image=name_icon)
        name_icon_lbl.image = name_icon
        name_icon_lbl.grid(row=1, column=0, padx=(5, 5), pady=(0, 8))

        blop_data = []
        name_var = tk.StringVar(tab1)
        name_field = ttk.Entry(tab1, width=12, font=("Helvetica", 10), textvariable=name_var)
        blop_data.append(name_var)
        name_field.grid(row=1, column=1)
        name_field.bind("<Return>", lambda _: handle_enter(self, tab1, name_field))

        # population share
        ratio_lbl = ttk.Label(tab1, text="Share")
        ratio_lbl.grid(row=2, column=0, columnspan=2, pady=(0, 0))

        ratio_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/piechart.png").resize((55, 55), Image.ANTIALIAS))
        ratio_icon_lbl = ttk.Label(tab1, image=ratio_icon)
        ratio_icon_lbl.image = ratio_icon
        ratio_icon_lbl.grid(row=3, column=0, padx=(10, 10), pady=8)

        # fg = ('grey', 'white')[auto]
        ratio_var = tk.StringVar(tab1)
        ratio_field = ttk.Entry(tab1, width=12, font=("Helvetica", 10), justify='right',
                                textvariable=ratio_var)
        blop_data.append(ratio_var)
        ratio_field.grid(row=3, column=1)

        # speed section
        speed_lbl = ttk.Label(tab1, text="Speed")
        speed_lbl.grid(row=4, column=0, columnspan=2, pady=(8, 4))

        speed_icon = ImageTk.PhotoImage(Image.open("./data/icons/speed2.png").resize((50, 50), Image.ANTIALIAS))
        speed_icon_lbl = ttk.Label(tab1, image=speed_icon)
        speed_icon_lbl.image = speed_icon  # we need to keep reference to it
        speed_icon_lbl.grid(row=5, column=0, padx=(10, 5), pady=(0, 0))

        # speed_val = ttk.
        speed_var = tk.DoubleVar(tab1)
        slider = tk.DoubleVar(tab1)
        speed_val_lbl = ttk.Label(tab1, textvariable=slider)
        speed_val_lbl.grid(row=5, column=1, sticky='n')
        speed_scale = ttk.Scale(tab1, from_=0.5, to=5, orient=tk.HORIZONTAL, length=100,
                                variable=speed_var, command=lambda s: slider.set('%0.1f' % float(s)))
        speed_scale.grid(row=5, column=1, sticky='ew', padx=(5, 0), pady=(20, 0))
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
        survive_lbl = ttk.Label(tab1, text="Survival")
        survive_lbl.grid(row=0, column=2, columnspan=2, pady=(8, 4))

        survive_icon = ImageTk.PhotoImage(Image.open("./data/icons/life.png").resize((50, 50), Image.ANTIALIAS))
        survive_icon_lbl = ttk.Label(tab1, image=survive_icon)
        survive_icon_lbl.image = survive_icon
        survive_icon_lbl.grid(row=1, column=2, padx=(20, 0))

        survive_val = tk.DoubleVar(tab1)
        survive_val_lbl = ttk.Label(tab1, textvariable=survive_val)
        survive_val_lbl.grid(row=1, column=3, sticky='n', pady=(0, 50))

        survive_var = tk.DoubleVar(tab1)
        survive_scale = ttk.Scale(tab1, from_=0.5, to=5, orient=tk.HORIZONTAL, length=100,
                                  variable=survive_var, command=lambda s: survive_val.set('%0.1f' % float(s)))
        blop_data.append(survive_var)
        survive_scale.grid(row=1, column=3, sticky='ew', padx=(0, 10), pady=(20, 0))
        survive_scale.set(1)

        # replicate section
        replica_lbl = ttk.Label(tab1, text="Replication")
        replica_lbl.grid(row=2, column=2, columnspan=2, pady=(10, 0))

        replica_icon = ImageTk.PhotoImage(Image.open("./data/icons/cycle2.png").resize((55, 55), Image.ANTIALIAS))
        replica_icon_lbl = ttk.Label(tab1, image=replica_icon)
        replica_icon_lbl.image = replica_icon
        replica_icon_lbl.grid(row=3, column=2, padx=(20, 0), pady=8)

        replica_val = tk.DoubleVar(tab1)
        replica_val_lbl = ttk.Label(tab1, textvariable=replica_val)
        replica_val_lbl.grid(row=3, column=3, sticky='n', pady=(0, 50))

        replica_var = tk.DoubleVar(tab1)
        replica_scale = ttk.Scale(tab1, from_=0.5, to=5, orient=tk.HORIZONTAL, length=120,
                                  variable=replica_var, command=lambda s: replica_val.set('%0.1f' % float(s)))
        blop_data.append(replica_var)
        replica_scale.grid(row=3, column=3, sticky='ew', padx=(0, 10), pady=(20, 0))
        replica_scale.set(2)

        # encounter
        encounter_lbl = ttk.Label(tab1, text="Behavior")
        encounter_lbl.grid(row=4, column=2, columnspan=2, pady=(0, 0))

        encounter_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/boxing.png").resize((60, 60), Image.ANTIALIAS))
        encounter_icon_lbl = ttk.Label(tab1, image=encounter_icon)
        encounter_icon_lbl.image = encounter_icon
        encounter_icon_lbl.grid(row=5, column=2, padx=(20, 0), pady=8)

        encounter_var = tk.StringVar(tab1)
        encounter_options = ttk.OptionMenu(tab1, encounter_var, "Neutral",  # <- pre-chosen
                                           "Aggressive", "Submissive", "Neutral")  # all options
        blop_data.append(encounter_var)
        encounter_options.grid(row=5, column=3, padx=(0, 10))

        # mutations
        mutation_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/dna3.png").resize((50, 50), Image.ANTIALIAS))
        mutation_icon_lbl = ttk.Label(tab1, image=mutation_icon)
        mutation_icon_lbl.image = mutation_icon
        mutation_icon_lbl.grid(row=6, column=2, padx=(20, 0), pady=15)

        mutation_btn = ttk.Button(tab1, text='Mutations', command=lambda: mutate_win(self, tab1, blop_data))
        mutation_btn.grid(row=6, column=3, pady=15)

        # control buttons
        save_btn = ttk.Button(tab1, text='Save', command=lambda: save_blop(self, tab1, blop_data))
        save_btn.grid(row=7, column=3, padx=10, pady=10)

        new_btn = ttk.Button(tab1, text='New', command=lambda: self.add_filled_tab())
        new_btn.grid(row=7, column=2, padx=10, pady=10)

        clone_btn = ttk.Button(tab1, text='Clone', command=lambda: clone_blop(self, tab1, blop_data))
        clone_btn.grid(row=7, column=1, padx=10, pady=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info2.png").resize((24, 24), Image.ANTIALIAS))
        finish_btn = tk.Button(tab1, command=show_info, image=info_icon, border=0)
        finish_btn.image = info_icon
        finish_btn.grid(row=7, column=0)

        blops_data.append(blop_data)

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
        global blops_data, valid_blops
        blops_data, valid_blops = [], {}
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
        with open('./data/base64/close_base64.txt', 'r') as file:
            data = file.read().replace('\n', '')
        with open('./data/base64/close_red_base64.txt', 'r') as file:
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

    def add_filled_tab(self, auto=False):
        new_tab = tk.Frame(self)
        self.fill_tab(new_tab, auto)
        self.add(new_tab, text="new kind")
        return new_tab


if __name__ == "__main__":
    root = tk.Tk()
    notebook = BlopCatalogue(root)
    notebook.grid(row=0, column=0, sticky="nsew")
    root.mainloop()
