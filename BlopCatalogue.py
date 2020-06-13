# print("EXCEPTION<!>: ___404___" + old_trait)
import copy
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from PIL import Image, ImageTk
from tkcolorpicker import askcolor

global max_tabs
max_tabs = 5


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
                                 "\n\nP.S. You can use shortcuts to trigger buttons: Ctrl+I - for helpbox, Ctrl+C - "
                                 "to clone, Ctrl+N -to create new kind, Ctrl+S - to save, Ctrl-W - to close current tab"
                                 " Ctrl-M - to open mutations window"
                        )


def handle_enter(widget, tab, full_name_entry):
    widget.tab(tab, text=full_name_entry.get())


def contrast(hex_color):
    h = hex_color.lstrip('#')
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return ("#FFFFFF", "#000000")[rgb[0] * 0.299 + rgb[1] * 0.587 + rgb[2] * 0.114 > 186]


def pick_color(label, color_var):
    _, rgb = askcolor((255, 255, 0))
    if rgb is not None:
        label.config(background=rgb, text='Picked', compound='right', foreground=contrast(rgb))
        color_var.set(rgb)


def show_message(mini_root):
    ttk.Label(mini_root, text="You haven't saved any (other) BlopKind yet!").grid(row=0, column=1, pady=50, padx=10)
    img = ImageTk.PhotoImage(Image.open("./data/icons/confused.png").resize((50, 50), Image.ANTIALIAS))
    confused = ttk.Label(mini_root, image=img)
    confused.image = img
    confused.grid(row=0, column=0, pady=50, padx=10)


def mutate_win(widget, data):
    mini_root = tk.Toplevel(widget)
    mini_root.grab_set()
    mini_root.iconphoto(False, tk.PhotoImage(file='./data/icons/dna4.png'))
    mini_root.title('Mutations')
    mini_root.focus_set()
    mini_root.bind("<Escape>", lambda _: mini_root.destroy())
    mini_root.bind("<Control-w>", lambda _: mini_root.destroy())
    mini_root.bind("<Control-s>", lambda _: save_mute(data[-1], new_dict, mini_root))
    mini_root.resizable(False, False)
    x = 0
    new_dict = {}
    items = list(widget.valid_blops.items())
    if len(items) == 0 or (len(items) == 1 and widget.select() in widget.valid_blops):
        show_message(mini_root)
        return

    entries = []
    # WARNING hardcoded 6 for color picker
    for key, value in items:
        if key != widget.select():
            hex_color = value[6].get()
            contrast_font = contrast(hex_color)
            ttk.Label(mini_root, text=value[0].get(), background=hex_color, foreground=contrast_font, width=12,
                      justify='center').grid(row=x, column=0)
            text_var = tk.StringVar(mini_root)
            entries.append(ttk.Entry(mini_root, width=10, font=("Helvetica", 10),
                                     textvariable=text_var, justify='right'))

            entries[-1].grid(row=x, column=1, pady=5)
            present = data[-1].get(key)

            text_to_insert = "" if (present is None) else present

            print("!: " + text_to_insert)
            entries[-1].insert(0, text_to_insert)
            new_dict[key] = text_var
            x += 1

    # for entry, key, value in zip(entries, items):
    #     entry.insert(0, data[-1].get(key))

    cancel_btn = ttk.Button(mini_root, text="Cancel", command=lambda: mini_root.destroy())
    cancel_btn.grid(row=x, column=0, padx=10, pady=10)

    # WARNING -1 is hardcoded for mutation entry
    save_btn = ttk.Button(mini_root, text='Save', command=lambda: save_mute(data[-1], new_dict, mini_root))
    save_btn.grid(row=x, column=1, padx=10, pady=10)


def save_mute(base_dict, new_dict, mini_root):
    sum_all = 0
    backup = copy.deepcopy(base_dict)
    for val in new_dict.values():
        if val.get() != "":
            sum_all += float(val.get())
    if sum_all > 100:
        messagebox.showerror("Invalid input", "Sum of entered probabilities exceeds 100, you data was discarded!")
        return
    sum_all = 0
    for key, val in new_dict.items():
        if val.get() != "":
            sum_all += float(val.get())
        if sum_all > 100:
            messagebox.showerror("Invalid input", "Sum of entered probabilities exceeds 100, you data was discarded!")
            # base_dict = backup
            return
        base_dict[key] = val.get() if val != '' else 0

    mini_root.destroy()


def save_blop(widget, tab, data):
    tab.focus_set()
    widget.tab(tab, text=data[0].get())
    if widget.proof_read(data) is not None:
        messagebox.showerror("Invalid input", widget.proof_read(data))
        saved_icon = ImageTk.PhotoImage(Image.open("./data/icons/fail.png").resize((15, 15)), Image.ANTIALIAS)
        widget.tab(tab, image=saved_icon, compound='left')
        tab.update()
    else:
        messagebox.showinfo("Success", "Data was recorded!")
        saved_icon = ImageTk.PhotoImage(Image.open("./data/icons/mini_tick.png"))
        widget.tab(tab, image=saved_icon, compound='left')
        tab.image = saved_icon
        widget.valid_blops[widget.select()] = data


def clone_blop(widget, this_tab, this_tab_data):
    widget.add_filled_tab()
    # TODO WTF?
    for old_trait, blank_trait in zip(this_tab_data, widget.blops_data[widget.select()]):
        try:
            blank_trait.set(old_trait.get())
        except Exception:
            print("Couldn't assign value thru set!")
            blank_trait = old_trait


class BlopCatalogue(ttk.Notebook):

    def fill_tab(self, tab):
        data = self.fill_tab_inner(tab)
        print(self.select() + "<><!><>")
        self.blops_data[self.select()] = data

    def fill_tab_inner(self, tab):
        print(tab.__class__)
        blop_data = []
        # name
        name_lbl = ttk.Label(tab, text="Name")
        name_lbl.grid(row=0, column=0, columnspan=2, pady=(8, 4))

        name_icon = ImageTk.PhotoImage(Image.open("./data/icons/brand.png").resize((45, 45), Image.ANTIALIAS))
        name_icon_lbl = ttk.Label(tab, image=name_icon)
        name_icon_lbl.image = name_icon
        name_icon_lbl.grid(row=1, column=0, padx=(5, 5), pady=(0, 8))

        name_var = tk.StringVar(tab)
        name_field = ttk.Entry(tab, width=12, font=("Helvetica", 10), textvariable=name_var)
        blop_data.append(name_var)
        name_field.grid(row=1, column=1)
        name_field.bind("<Return>", lambda _: handle_enter(self, tab, name_field))
        name_field.focus_set()

        # population share
        ratio_lbl = ttk.Label(tab, text="Share")
        ratio_lbl.grid(row=0, column=2, columnspan=2, pady=(0, 0))

        ratio_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/piechart.png").resize((55, 55), Image.ANTIALIAS))
        ratio_icon_lbl = ttk.Label(tab, image=ratio_icon)
        ratio_icon_lbl.image = ratio_icon
        ratio_icon_lbl.grid(row=1, column=2, padx=(10, 10), pady=8)

        # fg = ('grey', 'white')[auto]
        ratio_var = tk.StringVar(tab)
        ratio_field = ttk.Entry(tab, width=12, font=("Helvetica", 10), justify='right',
                                textvariable=ratio_var)
        blop_data.append(ratio_var)
        ratio_field.grid(row=1, column=3, padx=10)

        # encounter
        encounter_lbl = ttk.Label(tab, text="Behavior")
        encounter_lbl.grid(row=0, column=4, columnspan=2, pady=(0, 0))

        encounter_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/boxing.png").resize((60, 60), Image.ANTIALIAS))
        encounter_icon_lbl = ttk.Label(tab, image=encounter_icon)
        encounter_icon_lbl.image = encounter_icon
        encounter_icon_lbl.grid(row=1, column=4, padx=(20, 0), pady=8)

        encounter_var = tk.StringVar(tab)
        encounter_options = ttk.OptionMenu(tab, encounter_var, "Behavior",  # <- pre-chosen
                                           "Aggressive", "Submissive", "Neutral")  # all options
        blop_data.append(encounter_var)
        encounter_options.grid(row=1, column=5, padx=(0, 10))

        # survival section
        survive_lbl = ttk.Label(tab, text="Survival")
        survive_lbl.grid(row=2, column=0, columnspan=2, pady=(8, 4))

        survive_icon = ImageTk.PhotoImage(Image.open("./data/icons/life.png").resize((50, 50), Image.ANTIALIAS))
        survive_icon_lbl = ttk.Label(tab, image=survive_icon)
        survive_icon_lbl.image = survive_icon
        survive_icon_lbl.grid(row=3, column=0, padx=(20, 0))

        survive_val = tk.DoubleVar(tab)
        survive_val_lbl = ttk.Label(tab, textvariable=survive_val)
        survive_val_lbl.grid(row=3, column=1, sticky='n', pady=(0, 50))

        survive_var = tk.DoubleVar(tab)
        survive_scale = ttk.Scale(tab, from_=0.5, to=5, orient=tk.HORIZONTAL, length=100,
                                  variable=survive_var, command=lambda s: survive_val.set('%0.1f' % float(s)))
        blop_data.append(survive_var)
        survive_scale.grid(row=3, column=1, sticky='ew', padx=(0, 10), pady=(20, 0))
        survive_scale.set(1)

        # replicate section
        replica_lbl = ttk.Label(tab, text="Replication")
        replica_lbl.grid(row=2, column=2, columnspan=2, pady=(10, 0))

        replica_icon = ImageTk.PhotoImage(Image.open("./data/icons/cycle2.png").resize((55, 55), Image.ANTIALIAS))
        replica_icon_lbl = ttk.Label(tab, image=replica_icon)
        replica_icon_lbl.image = replica_icon
        replica_icon_lbl.grid(row=3, column=2, padx=(50, 50), pady=8)

        replica_val = tk.DoubleVar(tab)
        replica_val_lbl = ttk.Label(tab, textvariable=replica_val)
        replica_val_lbl.grid(row=3, column=3, sticky='n', pady=(0, 50))

        replica_var = tk.DoubleVar(tab)
        replica_scale = ttk.Scale(tab, from_=0.5, to=5, orient=tk.HORIZONTAL, length=120,
                                  variable=replica_var, command=lambda s: replica_val.set('%0.1f' % float(s)))
        blop_data.append(replica_var)
        replica_scale.grid(row=3, column=3, sticky='ew', padx=(0, 10), pady=(20, 0))
        replica_scale.set(2)

        # speed section
        speed_lbl = ttk.Label(tab, text="Speed")
        speed_lbl.grid(row=2, column=4, columnspan=2, pady=(8, 4))

        speed_icon = ImageTk.PhotoImage(Image.open("./data/icons/speed2.png").resize((50, 50), Image.ANTIALIAS))
        speed_icon_lbl = ttk.Label(tab, image=speed_icon)
        speed_icon_lbl.image = speed_icon  # we need to keep reference to it
        speed_icon_lbl.grid(row=3, column=4, padx=(10, 5), pady=(0, 0))

        speed_var = tk.DoubleVar(tab)
        speed_slider = tk.DoubleVar(tab)
        span_var_lbl = ttk.Label(tab, textvariable=speed_slider)
        span_var_lbl.grid(row=3, column=5, sticky='n')
        span_scale = ttk.Scale(tab, from_=0.5, to=5, orient=tk.HORIZONTAL, length=100,
                               variable=speed_var, command=lambda s: speed_slider.set('%0.1f' % float(s)))
        span_scale.grid(row=3, column=5, sticky='ew', padx=(5, 0), pady=(20, 0))
        span_scale.set(1)
        blop_data.append(speed_var)

        # color label
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        color_var = tk.StringVar()
        color_var.set(color)
        picked_color_lbl = ttk.Label(tab, background=color, width=12,
                                     text="Random", foreground=contrast(color), font=("Helvetica", 10), anchor='center')
        picked_color_lbl.grid(row=6, column=5, pady=25, padx=(10, 6))

        color_icon = ImageTk.PhotoImage(Image.open("./data/icons/colorpicker.png").resize((50, 50), Image.ANTIALIAS))
        color_btn = tk.Button(tab, image=color_icon, command=lambda: pick_color(picked_color_lbl, color_var), border=0)
        color_btn.image = color_icon
        color_btn.grid(row=6, column=4, pady=25, padx=10)
        blop_data.append(color_var)

        # mutations
        mutation_dict = {}
        blop_data.append(mutation_dict)
        mutation_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/dna3.png").resize((50, 50), Image.ANTIALIAS))
        mutation_icon_lbl = ttk.Label(tab, image=mutation_icon)
        mutation_icon_lbl.image = mutation_icon
        mutation_icon_lbl.grid(row=6, column=2, padx=(20, 0), pady=15)

        mutation_btn = ttk.Button(tab, text='Mutations', command=lambda: mutate_win(self.parent, blop_data))
        mutation_btn.grid(row=6, column=3, pady=15)

        # lifespan section
        span_lbl = ttk.Label(tab, text="Lifespan")
        span_lbl.grid(row=5, column=0, columnspan=2, pady=(8, 4))

        span_icon = ImageTk.PhotoImage(Image.open("./data/icons/cardio.png").resize((50, 50), Image.ANTIALIAS))
        span_icon_lbl = ttk.Label(tab, image=span_icon)
        span_icon_lbl.image = span_icon  # we need to keep reference to it
        span_icon_lbl.grid(row=6, column=0, padx=(10, 5), pady=(0, 0))

        span_var = tk.DoubleVar(tab)
        span_slider = tk.DoubleVar(tab)
        span_var_lbl = ttk.Label(tab, textvariable=span_slider)
        span_var_lbl.grid(row=6, column=1, sticky='n')
        span_scale = ttk.Scale(tab, from_=0.5, to=5, orient=tk.HORIZONTAL, length=100,
                               variable=span_var, command=lambda s: span_slider.set('%0.1f' % float(s)))
        span_scale.grid(row=6, column=1, sticky='ew', padx=(5, 0), pady=(20, 0))
        span_scale.set(1)
        blop_data.append(span_var)

        # control buttons
        save_btn = ttk.Button(tab, text='Save', command=lambda: save_blop(self, tab, blop_data))
        save_btn.grid(row=7, column=5, padx=10, pady=10)

        new_btn = ttk.Button(tab, text='New', command=lambda: self.add_filled_tab())
        new_btn.grid(row=7, column=4, padx=10, pady=10)

        clone_btn = ttk.Button(tab, text='Clone', command=lambda: clone_blop(self, tab, blop_data))
        clone_btn.grid(row=7, column=3, padx=10, pady=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info2.png").resize((24, 24), Image.ANTIALIAS))
        finish_btn = tk.Button(tab, command=show_info, image=info_icon, border=0)
        finish_btn.image = info_icon
        finish_btn.grid(row=7, column=0)

        self.parent.bind("<Control-m>", lambda _: mutate_win(self, self.blops_data[self.select()]))
        self.parent.bind("<Control-c>", lambda _: clone_blop(self, tab, self.blops_data[self.select()]))
        self.parent.bind("<Control-s>", lambda _: save_blop(self, tab, self.blops_data[self.select()]))
        self.parent.bind("<Control-n>", lambda _: self.add_filled_tab())
        self.parent.bind("<Control-w>", lambda _: self.close_tab())
        self.parent.bind("<Control-i>", lambda _: show_info())
        self.parent.bind("<Control-Tab>", lambda _: self.next_tab())
        self.parent.bind("<Control-h>", lambda _: show_info())
        print(blop_data)
        return blop_data

    __initialized = False

    def next_tab(self):
        index_num = self.index(self.select())
        desired = (index_num + 1) % len(self.tabs())
        self.select(desired)

    def __init__(self, parent, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)
        self.notebook = ttk.Notebook(parent)
        self._active = None
        self.parent = parent
        self.parent.resizable(False, False)
        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)
        # global blops_data, valid_blops
        # blops_data, valid_blops = {}, {}
        self.blops_data = {}
        self.valid_blops = {}
        tab = tk.Frame(self)
        self.add(tab, text='first kind')
        self.select(len(self.tabs()) - 1)
        self.fill_tab(tab)

    def add_filled_tab(self):
        if len(self.tabs()) > max_tabs - 1:
            messagebox.showerror("Tab overrun", "You cannot create more than {max_tabs} tabs!")
            return
        new_tab = tk.Frame(self)
        self.add(new_tab, text="new kind")
        self.select(len(self.tabs()) - 1)
        self.fill_tab(new_tab)
        new_tab.focus_set()
        return new_tab

    def valid_entries(self):
        return self.valid_blops

    def close_tab(self):
        if len(self.tabs()) == 1:
            messagebox.showerror("Destroying root", "You cannot delete the last tab!")
            return
        if messagebox.askokcancel("Quit", "Do you want to close this tab? All entered data will be erased!"):
            self.forget(self.select())

    def on_close_press(self, event):
        if len(self.tabs()) == 1:
            messagebox.showerror("Destroying root", "You cannot delete the last tab!")
            return

        element = self.identify(event.x, event.y)

        if "close" in element:
            if messagebox.askokcancel("Quit", "Do you want to quit? All entered data will be erased!"):
                index = self.index("@%d,%d" % (event.x, event.y))
                self.state(['pressed'])
                self._active = index
                self.update()
                self.on_close_release(event)

    def on_close_release(self, event):
        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        index = self.index("@%d,%d" % (event.x, event.y))

        if "close" in element and self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def proof_read(self, data):
        print("len:" + str(len(data)))
        if data[0].get() == "":
            return "No name is saved!"
        if data[0].get() in self.valid_blops.values():
            return "This name is already taken"
        # survival must be < replication
        if data[3].get() > data[4].get():
            return "Replication Q is not bigger than Survival Q"
        if not data[1].get().isdigit():
            return "Share value is not digit"
        share = float(data[1].get())
        if share > 100:
            return "Share exceeds 100%"
        cur_sum = 0
        for _, value in self.valid_blops.items():
            cur_sum += float(value[1].get())
        if share + cur_sum > 100:
            return "Total apparition chance for all kinds exceeds 100%"
        print("All is fine")
        return None

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


if __name__ == "__main__":
    root = tk.Tk()
    notebook = BlopCatalogue(root)
    notebook.grid(row=0, column=0, sticky="nsew")
    root.mainloop()