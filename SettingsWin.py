import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import glob
import BlopCatalogue
import ntpath


def show_btn(dev_button):
    dev_button.grid(row=7, column=2, pady=15, padx=10)


def show_template_description(widget, var):
    print(var.get())
    if var.get() == "None":
        messagebox.showinfo("Nothing selected!", "You haven't selected anything yet!")
        return
    path = ('./data/scenarios/' + var.get() + '.crum')
    with open(path) as file:
        contents = file.read()
    info = contents.split('&')[2]
    base64 = contents.split('&')[3]
    if info == '':
        messagebox.showinfo("No description!", "File you've chosen doesn't include any description!")
    else:
        message = tk.Toplevel(widget)
        message.title(var.get())
        message.focus_set()
        message.grab_set()
        message.resizable(False, False)
        message.iconphoto(False, tk.PhotoImage(file='./data/icons/scenario.png'))
        image = tk.PhotoImage(data=base64)
        lbl = ttk.Label(message, image=image, text=info, width=100, compound='top').pack()
        lbl.image = image


def show_info(file):
    with open(f'./data/manuals/{file}.txt') as file:
        message = file.read()
    messagebox.showinfo("Help?", message)


def get_options(option_menu):
    menu = option_menu["menu"]
    last = menu.index("end")
    items = []
    for index in range(last + 1):
        items.append(menu.entrycget(index, "label"))
    return items


class Settings(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame = tk.Frame(self)
        # self.geometry("800x900")
        self.title("Settings")
        self.iconphoto(False, tk.PhotoImage(file='./data/icons/settings.png'))
        self.data = {}
        self.kinds = {}
        self.widgets = {}
        self.base_data = {}
        self.fill_base()
        self.configuration = None
        self.bind("<Control-i>", lambda _: show_info('catalogue'))
        self.bind("<Control-r>", lambda _: self.run())
        self.bind("<Control-l>", lambda _: self.template_window())
        self.bind("<Control-Shift-S>", lambda _: self.save_template())
        self.create_widgets()

    def fill_base(self):
        self.base_data['speed'] = 19.5
        self.base_data['winsize'] = 800

    def dev_window(self):
        messagebox.showwarning("Attention!",
                               "You're entering the dangerous zone! Manipulating values presented here may "
                               "result in unforeseen consequences")
        root = tk.Toplevel(self)
        root.grab_set()
        root.focus_set()
        root.resizable(False, False)
        root.title("Developer settings")
        root.iconphoto(False, tk.PhotoImage(file='./data/icons/incognito.png'))

        speed_lbl = ttk.Label(root, text='Absolute speed')
        speed_lbl.grid(row=0, column=0)

        speed_var = tk.StringVar(root)
        speed_entry = ttk.Entry(root, text=self.base_data['speed'], textvariable=speed_var)
        speed_entry.grid(row=0, column=1)

    def template_window(self):
        mini_root = tk.Toplevel(self)
        mini_root.title('Scenarios')
        mini_root.focus_set()
        mini_root.grab_set()
        mini_root.resizable(False, False)
        mini_root.iconphoto(False, tk.PhotoImage(file='./data/icons/scenario.png'))

        mini_root.bind("<Escape>", lambda _: mini_root.destroy())
        mini_root.bind("<Control-w>", lambda _: mini_root.destroy())
        mini_root.bind("<Control-s>", lambda _: self.load_config_file(mini_root, scenario_var))
        mini_root.bind("<Control-i>", lambda _: show_info('template'))

        # scenario
        scenario_lbl = ttk.Label(mini_root, text="Choose saved")
        scenario_lbl.grid(row=0, column=1, columnspan=2, pady=(10, 0))

        scenario_lbl2 = ttk.Label(mini_root, text="Open file")
        scenario_lbl2.grid(row=0, column=0, columnspan=1, pady=(10, 0), padx=5)

        paths = glob.glob("./data/scenarios/*.crum")
        paths.insert(0, "None")
        paths[:] = [ntpath.basename(s).replace('.crum', '') for s in paths]

        scenario_var = tk.StringVar(mini_root)
        scenario_options = ttk.OptionMenu(mini_root, scenario_var, *paths)
        # self.widgets['scenario'] = scenario_options
        # self.data['scenario'] = scenario_var
        scenario_options.grid(row=1, column=1, padx=(0, 0))

        folder_icon = ImageTk.PhotoImage(Image.open("./data/icons/folder.png").resize((55, 55), Image.ANTIALIAS))
        folder_btn = tk.Button(mini_root, command=lambda: self.choose_file(scenario_options, scenario_var),
                               image=folder_icon,
                               border=0)
        folder_btn.image = folder_icon
        folder_btn.grid(row=1, column=0, pady=10, padx=(10, 10))

        scenario_icon = ImageTk.PhotoImage(Image.open("./data/icons/scenario.png").resize((60, 60), Image.ANTIALIAS))
        scenario_btn = tk.Button(mini_root, image=scenario_icon, border=0,
                                 command=lambda: show_template_description(mini_root, scenario_var))
        scenario_btn.image = scenario_icon
        scenario_btn.grid(row=1, column=2, padx=(0, 20), pady=8)

        # control buttons
        save_btn = ttk.Button(mini_root, text='Save', command=lambda: self.load_config_file(mini_root, scenario_var))
        save_btn.grid(row=2, column=2, padx=10, pady=10)

        cancel_btn = ttk.Button(mini_root, text="Cancel", command=lambda: mini_root.destroy())
        cancel_btn.grid(row=2, column=1, padx=10, pady=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info2.png").resize((24, 24), Image.ANTIALIAS))
        info_btn = tk.Button(mini_root, command=lambda: show_info('template'), image=info_icon, border=0)
        info_btn.image = info_icon
        info_btn.grid(row=2, column=0)

    def validate_data(self):
        if self.data['name'].get() == '':
            if messagebox.askokcancel("No name!", "You didn't name your configuration! Proceed with 'Unnamed'?"):
                self.data['name'].set("Unnamed")
            else:
                return

        if len(self.kinds) == 0:
            messagebox.showerror("No blop data!", "You haven't saved any BlopKind! Make sure to click Save button in "
                                                  "the bottom of BlopKind tab.")
            return

        print(len(self.kinds))
        if self.data['name'].get() in get_options(self.widgets['scenario']):
            messagebox.showerror("Name conflict!", "Configuration with this name already exists!")
            return
        sum_prob = 0
        if self.data['scenario'].get() != "None":
            q = messagebox.askyesnocancel("We are confused",
                                          "You've chosen lib scenario, but haven't loaded it. Do you want "
                                          "us to load it for you and ignore entered configurations?",
                                          icon='warning', default='no')
            if q:
                print("Yes")
                self.decode_template()
                return
            if q is None:
                print("Cancel")
                return
            else:
                print("No")

        benchers = []  # those who will appear as a result of mutations
        for key, value in self.kinds.items():
            ratio = float(value['ratio'].get())
            print(ratio)
            sum_prob += ratio
            if ratio == 0:
                benchers.append(key)
        if sum_prob != 100:
            messagebox.showerror("Error", "Sum of all apparition probabilities of saved BlopKinds isn't 100%!")
            return
        to_be_born = []
        for key, value in self.kinds.items():
            to_be_born += list(value['mutate'].keys())

        for bencher in benchers:
            if bencher not in to_be_born:
                name = self.kinds[bencher]['name']
                messagebox.showerror("Unused BlopKind", f'BlopKind {name} will never appear on the board!')
                return
        messagebox.showinfo("Success", "Your input was accepted!")

    def save_template(self):
        self.validate_data()
        f = open(f'./data/scenarios/{self.data["name"].get()}.crum', 'a')
        string = ''
        for feature, var in self.data.items():
            try:
                string += feature + "|" + str(var.get()) + "\n"
            except Exception:  # for aborts
                string += feature + "|" + str(var) + "\n"

        string += "#blop_catalogue\n"
        for frame, blop_kind in self.kinds.items():
            string += "@\n"
            for feature, var in blop_kind.items():
                try:
                    string += feature + "|" + str(var.get()) + "\n"
                except Exception:  # for mutations
                    string += feature + "|" + str(var) + "\n"
        f.write(string)
        f.close()

    def run(self):
        self.validate_data()
        # engine = Engine.Engine(data)
        # engine.run()

    def load_config_file(self, root, var):
        path = var.get()
        if var.get() != 'None':
            if ':' not in var.get():  # check absolute or relative path
                path = ('./data/scenarios/' + var.get() + '.crum')
            if messagebox.askyesnocancel("Choose", "Run now and don't edit?"):
                pass
                # widget.run()
            else:
                self.fill_settings(self.decode_template(path))
        root.destroy()

    def choose_file(self, options_menu, var):
        widget = self
        filename = filedialog.askopenfilename(initialdir="/", title="Select config file",
                                              filetypes=(("crum files", "*.crum"), ("all files", "*.*")))
        if filename != '':
            try:
                widget.decode_template(filename)
                if messagebox.askyesno("Save", "Copy file to app directory and add to list?"):
                    # TODO possible name conflict
                    shutil.copy2(filename, "./data/scenarios/")
                    options_menu['menu'].delete(0, 'end')
                    list_paths = glob.glob("./data/scenarios/*.crum")
                    for choice in list_paths:
                        options_menu['menu'].add_command(label=ntpath.basename(choice).replace('.crum', ''),
                                                         command=tk._setit(var, choice))
                else:
                    var.set(filename)
            except Exception:
                messagebox.showerror("Corrupted file",
                                     "We can't extract data from the chosen file. Make sure it's the right one")
                return

    def decode_template(self, filename):
        with open(filename) as file:
            contents = file.read()
        data = []
        catalogue = {}
        chapters = contents.split('&')
        for line in chapters[0].split("\n"):
            splits = line.split('|')
            data[splits[0]] = splits[1]

        for kinds in chapters[1].split("@"):
            blop_kind = {}
            for line2 in kinds.split("\n"):
                splits = line2.split('|')
                blop_kind[splits[0]] = splits[1]
            catalogue.append(blop_kind)

        if chapters[2] != '':
            message = tk.Toplevel(self)
            ttk.Label(message, text=chapters[2], width=100).pack()
        else:
            print("it actually -")

    def create_widgets(self):
        self['padx'] = 5
        self['pady'] = 5

        title = tk.Label(self, text="General Settings", font=("Helvetica", 11))
        title.grid(row=0, column=0, pady=18, columnspan=7)

        # name
        name_lbl = ttk.Label(self, text="Name")
        name_lbl.grid(row=1, column=0, columnspan=2, pady=(8, 4))

        name_icon = ImageTk.PhotoImage(Image.open("./data/icons/resume.png").resize((45, 45), Image.ANTIALIAS))
        name_icon_lbl = ttk.Label(self, image=name_icon)
        name_icon_lbl.image = name_icon
        name_icon_lbl.grid(row=2, column=0, padx=(5, 5), pady=(0, 8))

        name_var = tk.StringVar(self)
        name_field = ttk.Entry(self, width=12, font=("Helvetica", 10), textvariable=name_var)
        self.data['name'] = name_var
        name_field.grid(row=2, column=1)
        name_field.focus_set()

        # design
        design_lbl = ttk.Label(self, text="Theme")
        design_lbl.grid(row=1, column=2, columnspan=2, pady=(0, 0))

        design_icon = ImageTk.PhotoImage(Image.open("./data/icons/design.png").resize((60, 60), Image.ANTIALIAS))
        design_icon_lbl = ttk.Label(self, image=design_icon)
        design_icon_lbl.image = design_icon
        design_icon_lbl.grid(row=2, column=2, padx=(20, 0), pady=8)
        design_var = tk.StringVar(self)
        design_options = ttk.OptionMenu(self, design_var, "Abstract", "Body", "Farm", "Space", "Ground", 'Water')
        self.data['design'] = design_var
        design_options.grid(row=2, column=3, padx=(0, 10))

        # - - - - - - - - - - - - - - - - - - - - -
        speed_lbl = ttk.Label(self, text="Time Unit")
        speed_lbl.grid(row=3, column=0, columnspan=2, pady=(8, 4))

        speed_icon = ImageTk.PhotoImage(Image.open("./data/icons/duration.png").resize((50, 50), Image.ANTIALIAS))
        speed_icon_lbl = ttk.Label(self, image=speed_icon)
        speed_icon_lbl.image = speed_icon  # we need to keep reference to it
        speed_icon_lbl.grid(row=4, column=0, padx=(10, 5), pady=(0, 0))

        speed_var = tk.DoubleVar(self)
        slider = tk.DoubleVar(self)
        speed_val_lbl = ttk.Label(self, textvariable=slider)
        speed_val_lbl.grid(row=4, column=1, sticky='n')
        speed_scale = ttk.Scale(self, from_=0.5, to=5, orient=tk.HORIZONTAL, length=100,
                                variable=speed_var, command=lambda s: slider.set('%0.1f' % float(s)))
        speed_scale.grid(row=4, column=1, sticky='ew', padx=(5, 0), pady=(20, 0))
        speed_scale.set(1)
        self.data['speed'] = speed_var

        # - - - - - - - - - - - - - - - - - - - - -
        unit_lbl = ttk.Label(self, text="Duration")
        unit_lbl.grid(row=3, column=2, columnspan=2, pady=(8, 4))

        unit_icon = ImageTk.PhotoImage(Image.open("./data/icons/calendar.png").resize((60, 60), Image.ANTIALIAS))
        unit_icon_lbl = ttk.Label(self, image=unit_icon)
        unit_icon_lbl.image = unit_icon  # we need to keep reference to it
        unit_icon_lbl.grid(row=4, column=2, padx=(10, 5), pady=(0, 0))

        unit_var = tk.DoubleVar(self)
        unit_slider = tk.DoubleVar(self)
        unit_val_lbl = ttk.Label(self, textvariable=unit_slider)
        unit_val_lbl.grid(row=4, column=3, sticky='n')
        unit_scale = ttk.Scale(self, from_=0.2, to=5, orient=tk.HORIZONTAL, length=100,
                               variable=unit_var, command=lambda s: unit_slider.set('%0.1f' % float(s)))
        unit_scale.grid(row=4, column=3, sticky='ew', padx=(5, 0), pady=(20, 0))
        unit_scale.set(1)
        self.data['unit'] = unit_var

        abort_dict = {}
        self.data['abort'] = abort_dict
        abort_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/checkedfile.png").resize((60, 60), Image.ANTIALIAS))
        abort_icon_lbl = ttk.Label(self, image=abort_icon)
        abort_icon_lbl.image = abort_icon
        abort_icon_lbl.grid(row=4, column=4, padx=(20, 0), pady=15)

        abort_btn = ttk.Button(self, text='F-condition', command=lambda: self.destroy)
        abort_btn.grid(row=4, column=5, pady=15)

        # - - - - - - - - - - - - - - - - - - - - -
        notebook_label = ttk.Label(self, text="Blops Catalogue", font=("Helvetica", 11))
        notebook_label.grid(row=5, column=0, pady=18, columnspan=7)

        notebook = BlopCatalogue.BlopCatalogue(self)
        self.kinds = notebook.valid_blops
        notebook.grid(row=6, column=0, sticky='wens', pady=4, padx=(30, 0), columnspan=6)
        # - - - - - - - - - - - - - - - - - - - - -

        # -----------buttons--------------
        dev_button = ttk.Button(self, text="Developer mode", command=lambda: self.dev_window())
        self.bind("<Control-Alt-e>", lambda _: show_btn(dev_button))
        dev_button.grid_forget()

        load_button = ttk.Button(self, text="Load template", command=lambda: self.template_window())
        load_button.grid(row=7, column=3, pady=15, padx=10)

        save_button = ttk.Button(self, text="Save template", command=lambda: self.save_template())
        save_button.grid(row=7, column=4, pady=15, padx=10)

        run_button = ttk.Button(self, text="Run", command=lambda: self.run())
        run_button.grid(row=7, column=5, pady=15, padx=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info2.png").resize((24, 24), Image.ANTIALIAS))
        info_btn = tk.Button(self, command=lambda _: show_info('catalogue'), image=info_icon, border=0)
        info_btn.image = info_icon
        info_btn.grid(row=7, column=0)


program = Settings()
program.mainloop()
