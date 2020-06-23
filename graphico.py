import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from tkinter import *

matplotlib.use('TkAgg')


def get_share_data():
    sample1 = np.random.uniform(low=0.0, high=37.0, size=(50,))
    sample2 = np.random.uniform(low=20.0, high=33.0, size=(50,))
    sample3 = np.random.uniform(low=40.0, high=60.0, size=(50,))
    share_data = {'Klopp': sample3, 'Blopify': sample2, 'Truber': sample1}
    return share_data


def decode_template(filename):
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
    return data, catalogue


class Graphics:

    def __init__(self, root, catalogue):
        self.cat = catalogue
        self.window = root
        self.box = Entry(root)
        self.button = Button(root, text="check", command=self.plot)
        self.box.grid(row=0, column=0)
        self.button.grid(row=0, column=0)

    def process(self):
        for cat in self.cat:
            pass

    def plot(self):
        data = get_share_data()
        slots = len(next(iter(data.values())))
        print(slots)

        span_sum, speed_sum, replica_sum, survival_sum = [0] * slots, [0] * slots, [0] * slots, [0] * slots
        for key, value in data.items():
            print(key)
            print(span_sum)
            span = self.cat[key]['span']
            print(span)
            speed = self.cat[key]['speed']
            replica = self.cat[key]['replica']
            survival = self.cat[key]['survive']

            for idx, val in enumerate(value):
                span_sum[idx] += float(span) * val.item() / 100.
                speed_sum[idx] += float(speed) * val.item() / 100.
                replica_sum[idx] += float(replica) * val.item() / 100.
                survival_sum[idx] += float(survival) * val.item() / 100.

        print(span_sum)

        fig = Figure(figsize=(5, 5))

        a = fig.add_subplot(111)
        a.plot(speed_sum, c=np.random.rand(3, ), label='Speed')
        a.plot(survival_sum, c=np.random.rand(3, ), label='Survival')
        a.plot(span_sum, c=np.random.rand(3, ), label='Lifespan')
        a.plot(replica_sum, c=np.random.rand(3, ), label='Replication')

        fig.legend(loc='upper right')
        a.set_title("Simulation Overview", fontsize=16)
        a.set_ylabel("Features", fontsize=14)
        a.set_xlabel("Time", fontsize=14)
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().grid(row=1, column=0)

        # ____________________
        fig2 = Figure(figsize=(5, 5))
        b = fig2.add_subplot(111)
        for key, value in data.items():
            b.plot(value, c=np.random.rand(3, ), label=key)

        fig2.legend(loc='upper right')
        b.set_title("Population over time", fontsize=16)
        b.set_ylabel("Population", fontsize=14)
        b.set_xlabel("Time", fontsize=14)
        canvas = FigureCanvasTkAgg(fig2, master=self.window)
        canvas.get_tk_widget().grid(row=1, column=1)

        # ____________________

        labels = []
        values = []
        for key, value in data.items():
            labels.append(key)
            values.append(value[-1])

        fig3 = plt.figure(figsize=(5, 5))
        fig3.suptitle("Final Population", fontsize=18)
        explode = list()
        for _ in labels:
            explode.append(0.03)
        pie = plt.pie(values, labels=labels, explode=explode, autopct='%1.2f%%')
        plt.legend(pie[0], labels, loc="upper right")
        canvas = FigureCanvasTkAgg(fig3, master=self.window)
        canvas.get_tk_widget().grid(row=0, column=1)

        # ____________________
        labels = []
        values = []
        for key, value in data.items():
            labels.append(key)
            values.append(value[1])

        fig3 = plt.figure(figsize=(5, 5))
        fig3.suptitle("Initial Population", fontsize=18)
        explode = list()
        for _ in labels:
            explode.append(0.03)
        pie = plt.pie(values, labels=labels, explode=explode, autopct='%1.2f%%')
        plt.legend(pie[0], labels, loc="upper right")
        canvas = FigureCanvasTkAgg(fig3, master=self.window)
        canvas.get_tk_widget().grid(row=0, column=0)

        # ______________________________
        canvas.draw()


_, cat = decode_template("./data/scenarios/Fabula.crum")
window = Tk()
start = Graphics(window, cat)
window.mainloop()
