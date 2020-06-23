from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import blop_catalogue
import tkinter as tk
import ntpath
import shutil
import glob
import re


class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.set_current)
        self.bind('<B1-Motion>', self.shift_selection)
        self.curIndex = None

    def set_current(self, event):
        self.curIndex = self.nearest(event.y)

    def shift_selection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i


def hello():
    print("hello!")


def show_btn(dev_button):
    # WARNING hard coded values
    dev_button.grid(row=0, column=2, pady=15, padx=10)
    dev_button.focus_set()


def show_template_description(widget, var):
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
        lbl = ttk.Label(message, image=image, text=info, width=100, compound='top')
        lbl.pack()
        lbl.image = image


class Settings(tk.Frame):

    def __init__(self, up_root, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.root = up_root
        # self.root.geometry("800x900")
        self.root.title("Settings")
        self.root.iconphoto(True, tk.PhotoImage(file='./data/icons/settings.png'))
        self.data = {}
        self.kinds = {}
        self.aborts = {}
        self.widgets = {}
        self.base_data = {}
        self.fill_base()
        self.notebook = None
        self.guess = None
        up_root.resizable(False, False)
        self.root.bind("<Control-i>", lambda _: blop_catalogue.show_info('catalogue'))
        self.root.bind("<Control-r>", lambda _: self.run())
        self.root.bind("<Control-l>", lambda _: self.template_window())
        self.root.bind("<Control-Shift-S>", lambda _: self.save_template())
        self.create_widgets()

    def fill_base(self):
        speed_var = tk.DoubleVar(self, value=19.5)
        self.base_data['speed'] = speed_var
        winsize_var = tk.DoubleVar(self, value=800)
        self.base_data['winsize'] = winsize_var

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

        # speed
        speed_lbl = ttk.Label(root, text='Absolute speed', anchor='w')
        speed_var = tk.DoubleVar(self, value=self.base_data['speed'].get())
        speed_lbl.grid(row=1, column=0, padx=15, pady=15, columnspan=2)
        speed_entry = ttk.Entry(root, textvariable=speed_var, justify='right', font=("Helvetica", 10),
                                width=10)
        speed_entry.grid(row=1, column=2, padx=15)

        # size
        size_lbl = tk.Label(root, text='Window size', justify='left')
        size_lbl.grid(row=2, column=0, padx=15, pady=15, columnspan=2)
        size_var = tk.DoubleVar(self, value=self.base_data['winsize'].get())
        size_entry = ttk.Entry(root, textvariable=size_var, justify='right', font=("Helvetica", 10),
                               width=10)
        size_entry.grid(row=2, column=2, padx=15)

        icon = ImageTk.PhotoImage(Image.open("./data/icons/hacker.png").resize((300, 300), Image.ANTIALIAS))
        lbl = ttk.Label(root, image=icon)
        lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        lbl.image = icon

        guess_var = tk.BooleanVar(self)
        check_guess = ttk.Checkbutton(root, text="Disable guesses", variable=guess_var)
        check_guess.grid(row=3, column=0, columnspan=2, padx=0, pady=10)

        abort_var = tk.BooleanVar(self)
        check_abort = ttk.Checkbutton(root, text="Use & in aborts", variable=abort_var)
        check_abort.grid(row=3, column=2, columnspan=2, padx=0, pady=10)

        configs = {'speed': speed_var, 'winsize': size_var, 'guess': guess_var, 'abort': abort_var}

        # control buttons
        save_btn = ttk.Button(root, text='Save', command=lambda: self.update_config(root, configs))
        save_btn.grid(row=4, column=2, padx=10, pady=10)

        cancel_btn = ttk.Button(root, text='Cancel', command=lambda: root.destroy())
        cancel_btn.grid(row=4, column=1, padx=10, pady=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info3.png").resize((30, 30), Image.ANTIALIAS))
        info_btn = tk.Button(root, command=lambda: blop_catalogue.show_info('developer'), image=info_icon, border=0)
        info_btn.image = info_icon
        info_btn.grid(row=4, column=0, padx=(10, 15))

    def update_config(self, mini_root, data):
        for key, value in data.items():
            self.base_data[key].set(value)
        mini_root.destroy()

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
        mini_root.bind("<Control-i>", lambda _: blop_catalogue.show_info('catalogue'))

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

        self.widgets['scenario'] = scenario_options
        # control buttons
        save_btn = ttk.Button(mini_root, text='Save', command=lambda: self.load_config_file(mini_root, scenario_var))
        save_btn.grid(row=2, column=2, padx=10, pady=10)

        cancel_btn = ttk.Button(mini_root, text="Cancel", command=lambda: mini_root.destroy())
        cancel_btn.grid(row=2, column=1, padx=10, pady=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info3.png").resize((30, 30), Image.ANTIALIAS))
        info_btn = tk.Button(mini_root, command=lambda: blop_catalogue.show_info('template'), image=info_icon, border=0)
        info_btn.image = info_icon
        info_btn.grid(row=2, column=0)

    def validate_data(self):
        if self.data['name'].get() == '':
            if messagebox.askokcancel("No name!", "You didn't name your configuration! Proceed with 'Unnamed'?"):
                self.data['name'].set("Unnamed")
            else:
                return False

        if len(self.kinds) == 0:
            messagebox.showerror("No blop data!", "You haven't saved any BlopKind! Make sure to click Save button in "
                                                  "the bottom of BlopKind tab.")
            return False

        print(str(len(self.kinds)) + " :kinds")
        paths = glob.glob("./data/scenarios/*.crum")
        paths[:] = [ntpath.basename(s).replace('.crum', '') for s in paths]
        if self.data['name'].get() in paths:
            messagebox.showerror("Name conflict!", "Configuration with this name already exists!")
            return False
        sum_prob = 0
        benchers = []  # those who will appear as a result of mutations
        for key, value in self.kinds.items():
            ratio = float(value['ratio'].get())
            sum_prob += ratio
            if ratio == 0:
                benchers.append(key)
        if sum_prob != 100:
            messagebox.showerror("Error", "Sum of all apparition probabilities of saved BlopKinds isn't 100%!")
            return False
        to_be_born = []
        for key, value in self.kinds.items():
            to_be_born += list(value['mutate'].keys())

        for bencher in benchers:
            if bencher not in to_be_born:
                name = self.kinds[bencher]['name']
                messagebox.showerror("Unused BlopKind", f'BlopKind {name} will never appear on the board!')
                return False
        messagebox.showinfo("Success", "Your input was accepted!")
        return True

    def save_template(self, run=False):
        self.validate_data()
        s = f'./data/scenarios/{self.data["name"].get()}.crum'
        if run:
            s = f'./data/run/current.crum'
        f = open(s, 'a')
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
        if self.validate_data():
            self.guess_window()
        open('./data/run/current.crum', 'w').close()
        self.save_template(True)

    def load_config_file(self, root, var):
        path = var.get()
        if var.get() != 'None':
            if ':' not in var.get():  # check absolute or relative path
                path = ('./data/scenarios/' + var.get() + '.crum')
            if messagebox.askyesnocancel("Choose", "Run now and don't edit?"):
                pass
                # widget.run()
            else:
                self.fill_settings(path)
        root.destroy()

    def choose_file(self, options_menu, var):
        widget = self
        filename = filedialog.askopenfilename(initialdir="/", title="Select config file",
                                              filetypes=(("crum files", "*.crum"), ("all files", "*.*")))
        if filename != '':
            try:
                widget.decode_template(filename, True)
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

    def decode_template(self, filename, ad=False):
        with open(filename) as file:
            contents = file.read()
        data = {}
        catalogue = {}
        chapters = contents.split('&')
        for line in chapters[0].strip().split("\n"):
            splits = line.strip().split('|')
            data[splits[0]] = splits[1]

        for kind in chapters[1].split("@"):
            blop_kind = {}
            for line2 in kind.strip().split("\n"):
                splits = line2.strip().split('|')
                blop_kind[splits[0]] = splits[1]
            catalogue[blop_kind['name']] = blop_kind

        if chapters[2] != '' and ad:
            message = tk.Toplevel(self)
            ttk.Label(message, text=chapters[2], width=100).pack()
        return data, catalogue

    def create_widgets(self):
        self['padx'] = 10
        self['pady'] = 5

        title = tk.Label(self, text="General Settings", font=("Helvetica", 11))
        title.grid(row=1, column=0, pady=18, columnspan=7)

        # name
        name_lbl = ttk.Label(self, text="Name")
        name_lbl.grid(row=2, column=0, columnspan=2, pady=(8, 4))

        name_icon = ImageTk.PhotoImage(Image.open("./data/icons/resume.png").resize((55, 55), Image.ANTIALIAS))
        name_icon_lbl = ttk.Label(self, image=name_icon)
        name_icon_lbl.image = name_icon
        name_icon_lbl.grid(row=3, column=0, padx=(5, 5), pady=(0, 8))

        name_var = tk.StringVar(self)
        name_field = ttk.Entry(self, width=12, font=("Helvetica", 10), textvariable=name_var)
        self.data['name'] = name_var
        name_field.grid(row=3, column=1)
        name_field.focus_set()

        # design
        design_lbl = ttk.Label(self, text="Theme")
        design_lbl.grid(row=2, column=2, columnspan=2, pady=(0, 0))

        design_icon = ImageTk.PhotoImage(Image.open("./data/icons/design.png").resize((60, 60), Image.ANTIALIAS))
        design_icon_lbl = ttk.Label(self, image=design_icon)
        design_icon_lbl.image = design_icon
        design_icon_lbl.grid(row=3, column=2, padx=(20, 0), pady=8)
        design_var = tk.StringVar(self)
        design_options = ttk.OptionMenu(self, design_var, "Abstract", "Body", "Farm", "Space", "Ground", 'Water',
                                        "Abstract", )
        self.data['design'] = design_var
        design_options.grid(row=3, column=3, padx=(0, 10))

        # - - - - - - - - - - - - - - - - - - - - -
        speed_lbl = ttk.Label(self, text="Time Unit")
        speed_lbl.grid(row=4, column=0, columnspan=2, pady=(8, 4))

        speed_icon = ImageTk.PhotoImage(Image.open("./data/icons/duration.png").resize((60, 60), Image.ANTIALIAS))
        speed_icon_lbl = ttk.Label(self, image=speed_icon)
        speed_icon_lbl.image = speed_icon  # we need to keep reference to it
        speed_icon_lbl.grid(row=5, column=0, padx=(10, 5), pady=(0, 0))

        speed_var = tk.DoubleVar(self)
        slider = tk.DoubleVar(self)
        speed_val_lbl = ttk.Label(self, textvariable=slider)
        speed_val_lbl.grid(row=5, column=1, sticky='n')
        speed_scale = ttk.Scale(self, from_=0.5, to=5, orient=tk.HORIZONTAL, length=100,
                                variable=speed_var, command=lambda s: slider.set('%0.1f' % float(s)))
        speed_scale.grid(row=5, column=1, sticky='ew', padx=(5, 0), pady=(20, 0))
        speed_scale.set(1)
        self.data['speed'] = speed_var

        # - - - - - - - - - - - - - - - - - - - - -
        unit_lbl = ttk.Label(self, text="Duration")
        unit_lbl.grid(row=4, column=2, columnspan=2, pady=(8, 4))

        unit_icon = ImageTk.PhotoImage(Image.open("./data/icons/calendar.png").resize((60, 60), Image.ANTIALIAS))
        unit_icon_lbl = ttk.Label(self, image=unit_icon)
        unit_icon_lbl.image = unit_icon  # we need to keep reference to it
        unit_icon_lbl.grid(row=5, column=2, padx=(10, 5), pady=(0, 0))

        unit_var = tk.DoubleVar(self)
        unit_slider = tk.DoubleVar(self)
        unit_val_lbl = ttk.Label(self, textvariable=unit_slider)
        unit_val_lbl.grid(row=5, column=3, sticky='n')
        unit_scale = ttk.Scale(self, from_=0.2, to=5, orient=tk.HORIZONTAL, length=100,
                               variable=unit_var, command=lambda s: unit_slider.set('%0.1f' % float(s)))
        unit_scale.grid(row=5, column=3, sticky='ew', padx=(5, 0), pady=(20, 0))
        unit_scale.set(1)
        self.data['unit'] = unit_var

        abort_dict = {}
        self.data['abort'] = abort_dict
        abort_icon = ImageTk.PhotoImage(
            Image.open("./data/icons/exit.png").resize((60, 60), Image.ANTIALIAS))
        abort_icon_lbl = ttk.Label(self, image=abort_icon)
        abort_icon_lbl.image = abort_icon
        abort_icon_lbl.grid(row=5, column=4, padx=(20, 0), pady=15)

        abort_btn = ttk.Button(self, text='F-condition', command=lambda: self.abort_window())
        abort_btn.grid(row=5, column=5, pady=15)

        # - - - - - - - - - - - - - - - - - - - - -
        notebook_label = ttk.Label(self, text="Blops Catalogue", font=("Helvetica", 11))
        notebook_label.grid(row=6, column=0, pady=18, columnspan=7)

        notebook = blop_catalogue.BlopCatalogue(self)
        self.notebook = notebook
        self.kinds = notebook.valid_blops
        notebook.grid(row=7, column=0, sticky='wens', pady=4, padx=(0, 0), columnspan=6)
        # - - - - - - - - - - - - - - - - - - - - -

        # -----------buttons--------------
        dev_button = ttk.Button(self, text="Developer mode", command=lambda: self.dev_window())
        self.root.bind("<Control-Alt-e>", lambda _: show_btn(dev_button))
        dev_button.grid_forget()

        load_button = ttk.Button(self, text="Load template", command=lambda: self.template_window())
        load_button.grid(row=0, column=3, pady=15, padx=10)

        save_button = ttk.Button(self, text="Save template", command=lambda: self.save_template())
        save_button.grid(row=0, column=4, pady=15, padx=10)

        run_button = ttk.Button(self, text="Use data", command=lambda: self.run())
        run_button.grid(row=0, column=5, pady=15, padx=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info2.png").resize((30, 30), Image.ANTIALIAS))
        info_btn = tk.Button(self, command=lambda: blop_catalogue.show_info('settings'), image=info_icon, border=0)
        info_btn.image = info_icon
        info_btn.grid(row=0, column=0, padx=(0, 30))

    def guess_window(self):
        mini_root = tk.Toplevel(self)
        mini_root.title('Guess!')
        mini_root.focus_set()
        mini_root.grab_set()
        mini_root.resizable(False, False)
        mini_root.iconphoto(False, tk.PhotoImage(file='./data/icons/guess.png'))

        label = ttk.Label(mini_root, font=("Didot", 12),
                          text="You're ready to go! \nNow let us record your prediction of the simulation "
                               "outcome. \nWe will show you these after simulation ends for comparison. "
                               "\nYou may be surprised by results! Challenge your intuition!")
        label.grid(row=0, column=0, padx=20, pady=20, columnspan=4)

        label2 = ttk.Label(mini_root, font=("Didot", 10),
                           text="Place kinds in descending order")
        label2.grid(row=1, column=2, columnspan=2, sticky='s', pady=15)

        listbox = DragDropListbox(mini_root, height=len(self.kinds), font=("Cambria", 10))
        for idx, key in enumerate(self.kinds):
            listbox.insert((idx + 1), self.kinds[key]['name'].get())
        listbox.grid(row=2, column=2, columnspan=2, sticky='n')

        img = ImageTk.PhotoImage(Image.open("./data/icons/choice.png").resize((200, 200), Image.ANTIALIAS))
        confused = ttk.Label(mini_root, image=img)
        confused.image = img
        confused.grid(row=1, column=0, pady=10, padx=10, columnspan=2, rowspan=2)

        # control buttons
        save_btn = ttk.Button(mini_root, text='Save',
                              command=lambda: self.save_guess(listbox.get(0, tk.END), mini_root))
        save_btn.grid(row=3, column=3, pady=10)

        cancel_btn = ttk.Button(mini_root, text='Cancel', command=lambda: mini_root.destroy())
        cancel_btn.grid(row=3, column=2, pady=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info3.png").resize((30, 30), Image.ANTIALIAS))
        info_btn = tk.Button(mini_root, command=lambda: blop_catalogue.show_info('developer'), image=info_icon,
                             border=0)
        info_btn.image = info_icon
        info_btn.grid(row=3, column=0, padx=(0, 35))

        mini_root.bind("<Escape>", lambda _: mini_root.destroy())
        mini_root.bind("<Control-w>", lambda _: mini_root.destroy())
        mini_root.bind("<Control-s>", lambda _: self.save_guess(listbox.get(0, tk.END), mini_root))
        mini_root.bind("<Control-i>", lambda _: blop_catalogue.show_info('guess'))

    def abort_window(self):
        mini_root = tk.Toplevel(self)
        mini_root.grab_set()
        mini_root.focus_set()
        mini_root.title('Abort')
        mini_root.resizable(False, False)
        mini_root.iconphoto(False, tk.PhotoImage(file='./data/icons/exit.png'))

        conditions_vars = {}
        mini_root.bind("<Escape>", lambda _: mini_root.destroy())
        mini_root.bind("<Control-w>", lambda _: mini_root.destroy())
        mini_root.bind("<Control-s>", lambda _: self.save_abort(mini_root))

        x = 0
        valid = list(self.kinds.items())
        if len(valid) == 0:
            blop_catalogue.show_message(mini_root)
            return

        text_entries = []
        for key, value in valid:
            hex_color = value['color'].get()
            contrast_font = blop_catalogue.contrast(hex_color)
            ttk.Label(mini_root, text=value['name'].get(), background=hex_color, foreground=contrast_font, width=12,
                      justify='center').grid(row=x, column=0)
            text_var = tk.StringVar(mini_root)
            text_entries.append(
                ttk.Entry(mini_root, width=10, font=("Helvetica", 10), textvariable=text_var, justify='right'))

            text_entries[-1].grid(row=x, column=1, pady=5)
            present = self.data['abort'].get(key)

            text_to_insert = "" if (present is None) else present

            text_entries[-1].insert(0, text_to_insert)
            conditions_vars[self.kinds[key]['name'].get()] = text_var
            x += 1

        cancel_btn = ttk.Button(mini_root, text="Cancel", command=lambda: mini_root.destroy())
        cancel_btn.grid(row=x, column=0, padx=10, pady=10)

        save_btn = ttk.Button(mini_root, text='Save',
                              command=lambda: self.save_abort(conditions_vars, mini_root))
        save_btn.grid(row=x, column=1, padx=10, pady=10)

    def save_abort(self, conditions, mini_root):
        for name, var in conditions.items():
            expr: tk.StringVar = var.get()
            if expr != '':
                self.aborts[name] = expr

        self.aborts = conditions

        mini_root.destroy()

    def detect_abort(self, shares_data):
        for name, share in shares_data.items():
            try:
                s = self.aborts[name]
                splits = re.split(r'(-?\d*\.?\d+)', s)
                if splits[0] == '>':
                    if shares_data[name] >= splits[1]:
                        return True
                if splits[0] == '<':
                    if shares_data[name] <= splits[1]:
                        return True
            except Exception:
                messagebox.showerror("Invalid input", "Invalid input!")
                print("Something went wrong!")

    def save_guess(self, param, mini_root):
        self.guess = param
        mini_root.destroy()

    def fill_settings(self, pathname):
        sim_data, catalogue = self.decode_template(pathname)
        for feature, value in sim_data.items():
            try:
                self.data[feature].set(value)
            except Exception:
                print(feature)  # abort

        print(len(self.notebook.tabs()))
        self.notebook.restore_data(catalogue.items())


if __name__ == "__main__":
    root = tk.Tk()
    setting = Settings(root)
    # setting.fill_settings("./data/scenarios/Fabula.crum")
    setting.grid(row=0, column=0)
    root.mainloop()
