import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import BlopCatalogue
import copy


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


def dev_win(old_root):
    messagebox.showwarning("Attention!",
                           "You're entering the dangerous zone! Manipulating values presented here may "
                           "result in unforeseen consequences")
    root = tk.Toplevel(old_root)
    root.grab_set()
    root.focus_set()


def show_btn(dev_button):
    dev_button.grid(row=6, column=2, pady=15, padx=10)


class Settings(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frame = tk.Frame(self)
        # self.geometry("800x900")
        self.title("Settings")
        self.iconphoto(False, tk.PhotoImage(file='./data/icons/settings.png'))
        self.data = {}
        self.create_widgets()
        self.configuration = None
        self.bind("<Control-i>", lambda _: show_info())

    def validate_data(self):
        print(len(self.data['kinds']))
        sum_prob = 0
        benchers = []
        for key, value in self.data['kinds'].items():
            ratio = float(value['ratio'].get())
            print(ratio)
            sum_prob += ratio
            if ratio == 0:
                benchers.append(key)
        if sum_prob != 100:
            messagebox.showerror("Error", "Sum of all apparition probabilities of saved BlopKinds isn't 100%!")
        to_be_born = []
        for key, value in self.data['kinds'].items():
            to_be_born += list(value['mutate'].keys())

        for bencher in benchers:
            if bencher not in to_be_born:
                name = self.data['kinds'][bencher]['name']
                messagebox.showerror("Unused BlopKind", f'BlopKind {name} will never appear on the board!')
                return
        messagebox.showinfo("Success", "Your input was accepted!")

    def save_template(self):
        self.validate_data()
        pass

    def run(self):
        self.validate_data()
        # ??? pygame.start

    def load_template(self):
        if self.data['scenario'].get() != "None":
            pairs = {}
            try:
                lines = open(f'./data/scenarios/{self.data["scenario"].get()}.crum').readlines()
            except FileNotFoundError:
                messagebox.showerror("No such file", "Config file was moved or deleted!")
                return
            for line in lines:
                part1, part2 = line.split(':')
                pairs[part1] = part2
        else:
            messagebox.showerror("No template selected", "Choose template among Scenarios above.")

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

        # design
        design_lbl = ttk.Label(self, text="Theme")
        design_lbl.grid(row=1, column=2, columnspan=2, pady=(0, 0))

        design_icon = ImageTk.PhotoImage(Image.open("./data/icons/design.png").resize((60, 60), Image.ANTIALIAS))
        design_icon_lbl = ttk.Label(self, image=design_icon)
        design_icon_lbl.image = design_icon
        design_icon_lbl.grid(row=2, column=2, padx=(20, 0), pady=8)
        design_var = tk.StringVar(self)
        design_options = ttk.OptionMenu(self, design_var, "None", "Body", "Farm", "Space", "Ground", 'Water')
        self.data['design'] = design_var
        design_options.grid(row=2, column=3, padx=(0, 10))

        # scenario
        scenario_lbl = ttk.Label(self, text="Scenarios")
        scenario_lbl.grid(row=1, column=4, columnspan=2, pady=(0, 0))

        scenario_icon = ImageTk.PhotoImage(Image.open("./data/icons/scenario.png").resize((60, 60), Image.ANTIALIAS))
        scenario_icon_lbl = ttk.Label(self, image=scenario_icon)
        scenario_icon_lbl.image = scenario_icon
        scenario_icon_lbl.grid(row=2, column=4, padx=(20, 0), pady=8)

        scenario_var = tk.StringVar(self)
        scenario_options = ttk.OptionMenu(self, scenario_var, "None", "Altruism", "Nepotism", "Cooperation",
                                          "Competition")

        self.data['scenario'] = scenario_var
        scenario_options.grid(row=2, column=5, padx=(0, 10))

        # blop_data.append(speed_var)

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
        self.data['kinds'] = notebook.valid_blops
        notebook.grid(row=6, column=0, sticky='wens', pady=4, padx=(30, 0), columnspan=6)
        # - - - - - - - - - - - - - - - - - - - - -

        # -----------buttons--------------
        dev_button = ttk.Button(self, text="Developer mode", command=lambda: dev_win(self))
        self.bind("<Control-Alt-e>", lambda _: show_btn(dev_button))
        dev_button.grid_forget()

        load_button = ttk.Button(self, text="Load template", command=lambda: self.load_template())
        load_button.grid(row=7, column=3, pady=15, padx=10)

        save_button = ttk.Button(self, text="Save template", command=lambda: self.save_template())
        save_button.grid(row=7, column=4, pady=15, padx=10)

        run_button = ttk.Button(self, text="Run", command=lambda: self.run())
        run_button.grid(row=7, column=5, pady=15, padx=10)

        info_icon = ImageTk.PhotoImage(Image.open("./data/icons/info2.png").resize((24, 24), Image.ANTIALIAS))
        info_btn = tk.Button(self, command=show_info, image=info_icon, border=0)
        info_btn.image = info_icon
        info_btn.grid(row=7, column=0)


program = Settings()
program.mainloop()
