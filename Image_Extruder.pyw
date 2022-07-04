import pprint
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os


import gene_3d_v5_slik as gene_slik
import gene_3d_v5_step as gene_step


class App:
    def __init__(self):
        try:
            os.mkdir("stl_projects")
        except FileExistsError:
            pass

        try:
            os.mkdir("img")
        except FileExistsError:
            pass

        self.bg = "#ccc"
        self.bg_not_ok = "#f55"
        self.bg_ok = "#5bf"

        self.root = tk.Tk()
        self.root.title("Image Extruder")

        # ##################### dimension + window position ######################
        w = 800
        h = 600
        self.root.configure(background=self.bg)
        p_r = int(self.root.winfo_screenwidth() / 2 - w / 2)
        p_d = int(self.root.winfo_screenheight() / 2 - h / 2 - 50)
        self.root.geometry("{}x{}+{}+{}".format(w, h, p_r, p_d))

        # ##################### presentation ######################
        l_titre = tk.Label(self.root, text="Image Extruder", font=("Calibri", 30), bg=self.bg)
        l_titre.pack(padx=10, pady=20)

        # ##################### import file ######################
        f_import = tk.LabelFrame(self.root, bg=self.bg)

        l_import = tk.Label(f_import, text="Import image:", bg=self.bg)
        self.file = tk.StringVar()
        e_import = tk.Entry(f_import, width=50, textvariable=self.file)
        b_import = tk.Button(f_import, text="...", command=self.__browseFiles, width=5)

        l_import.pack(side=tk.LEFT, padx=5)
        e_import.pack(side=tk.LEFT)
        b_import.pack(side=tk.LEFT, padx=5, pady=5)

        f_import.pack()

        # ##################### Parameter control ######################
        f_param = tk.LabelFrame(self.root, bg=self.bg, text="Parameters")

        # ##################### Algo ######################
        algo_label = tk.Label(f_param, text="Algo : ", bg=self.bg)
        algo = ['Step', 'Slik']
        self.algo_list = ttk.Combobox(f_param, values=algo)
        self.algo_list.current(1)

        algo_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)
        self.algo_list.grid(column=1, row=0, sticky=tk.W, padx=5, pady=10)

        # ##################### Color select ######################
        self.color_sel = False
        self.b_color_sel = tk.Button(f_param, text="Color Select", bg=self.bg, command=self.__color_select)
        self.b_color_sel.grid(column=0, row=1, sticky=tk.W, padx=5)

        # ##################### Levels ######################
        self.lvl = []
        self.levels = False
        self.b_levels = tk.Button(f_param, text="Levels", bg=self.bg, width=10, command=self.__levels)
        self.b_levels.config(state=tk.DISABLED)
        self.b_levels.grid(column=0, row=2, sticky=tk.W, padx=5, pady=10)

        # ##################### Offset ######################
        self.offset = tk.StringVar()
        self.offset.set(0)
        l_offset = tk.Label(f_param, bg=self.bg, text="Offset:")
        e_offset = tk.Entry(f_param, textvariable=self.offset)
        l_offset.grid(column=0, row=3, sticky=tk.W, padx=5)
        e_offset.grid(column=1, row=3, sticky=tk.W, padx=5)

        # ##################### Gain ######################
        self.gain = tk.StringVar()
        self.gain.set(1)
        l_gain = tk.Label(f_param, text="Gain:", bg=self.bg)
        e_gain = tk.Entry(f_param, textvariable=self.gain)
        l_gain.grid(column=0, row=4, sticky=tk.W, padx=5, pady=10)
        e_gain.grid(column=1, row=4, sticky=tk.W, padx=5, pady=10)

        # ##################### Out file ######################
        self.out_name = tk.StringVar()
        l_out = tk.Label(f_param, bg=self.bg, text="Out:")
        e_out = tk.Entry(f_param, textvariable=self.out_name)
        l_out.grid(column=0, row=5, sticky=tk.W, padx=5, pady=10)
        e_out.grid(column=1, row=5, padx=5, sticky=tk.W, pady=10)

        f_param.pack(side=tk.LEFT, anchor=tk.N, padx=45, pady=10)

        # ##################### Colors set ######################
        self.f_col = tk.LabelFrame(self.root, bg=self.bg, text="Colors")
        b_set_colors = tk.Button(self.f_col, bg=self.bg, text="Add colors", command=self.add_colors)

        self.tolerence = tk.StringVar()
        self.tolerence.set(5)
        l_toler = tk.Label(self.f_col, bg=self.bg, text="Tolerence:")
        e_toler = tk.Entry(self.f_col, textvariable=self.tolerence)

        self.colors = []
        self.t_colors = tk.Text(self.f_col, bg=self.bg, width=30, height=8, state=tk.DISABLED)

        b_set_colors.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)
        l_toler.grid(column=0, row=1, padx=5)
        e_toler.grid(column=1, row=1)
        self.t_colors.grid(row=2, columnspan=2, padx=5, pady=10)

        self.r = 1
        self.c = 0
        self.pop = tk.Toplevel
        self.yes = False
        self.canv = tk.Canvas

        # ##################### Generation ######################
        b_gene = tk.Button(self.root, text="Generate", command=self.generate)
        b_gene.pack(side=tk.BOTTOM, anchor=tk.W, pady=20)

        self.bare = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=300)
        self.bare_label = tk.Label(self.root, text="Calcul 0%", bg=self.bg)

        self.root.mainloop()

    def __color_select(self):
        if self.color_sel:
            self.color_sel = False
            self.b_color_sel.config(bg=self.bg)
            self.f_col.pack_forget()
            self.b_levels.config(state=tk.DISABLED, bg=self.bg)
            self.levels = False

        else:
            self.f_col.pack(anchor=tk.N, padx=20, pady=10)
            self.color_sel = True
            self.b_color_sel.config(bg=self.bg_ok)
            self.b_levels.config(state=tk.NORMAL)

    def __levels(self):
        if self.levels:
            self.levels = False
            self.b_levels.config(bg=self.bg)
        else:
            self.levels = True
            self.b_levels.config(bg=self.bg_ok)

    def add_colors(self):
        if self.file.get() == "":
            messagebox.showerror("Error", "File has been not set")
            return

        img = Image.open(self.file.get())

        self.pop = tk.Toplevel(self.root, bg=self.bg)
        w = 900
        h = 900
        pR = int(self.pop.winfo_screenwidth() / 2 - w / 2)
        pD = int(self.pop.winfo_screenheight() / 2 - h / 2 - 50)
        self.pop.geometry("{}x{}+{}+{}".format(w, h, pR, pD))

        self.canv = tk.Canvas(self.pop, bg="white", width=900, height=900)
        self.canv.image = ImageTk.PhotoImage(self.resize(img))
        self.canv.create_image(0, 0, anchor=tk.NW, image=self.canv.image)
        self.canv.bind("<Button-1>", self.get_color)
        self.canv.pack()

        self.pop.grab_set()
        self.root.wait_window(self.pop)

    def get_color(self, event):
        img = Image.open(self.file.get())

        x = int(event.x * self.r)
        y = int(event.y * self.r)

        r = img.getpixel((x, y))[0]
        g = img.getpixel((x, y))[1]
        b = img.getpixel((x, y))[2]
        color = (r, g, b)

        i = self.color_exist(color)

        if i is not None:
            if self.levels:
                pop_lvl = tk.Toplevel(self.pop, bg=self.bg)

                w = 300
                h = 100
                pR = int(pop_lvl.winfo_screenwidth() / 2 - w / 2)
                pD = int(pop_lvl.winfo_screenheight() / 2 - h / 2 - 50)
                pop_lvl.geometry("{}x{}+{}+{}".format(w, h, pR, pD))

                f_lvl = tk.LabelFrame(pop_lvl, bg=self.bg)
                l_lvl = tk.Label(f_lvl, bg=self.bg, text="Color already set, modify level ?")
                self.yes = False
                b_yes = tk.Button(f_lvl, bg=self.bg, text="Yes", width=10, command=self.toogle_yes)
                b_no = tk.Button(f_lvl, bg=self.bg, text="No", width=10, command=self.close_pop)
                l_lvl.pack(padx=5)
                b_yes.pack(side=tk.LEFT, padx=10, pady=10)
                b_no.pack(side=tk.RIGHT, padx=10, pady=10)
                f_lvl.pack(padx=10, pady=10)

                pop_lvl.grab_set()
                self.pop.wait_window(pop_lvl)

                if self.yes:
                    lvl = self.pop_level()
                    self.yes = False
                    self.lvl[i] = lvl

                    self.t_colors.config(state=tk.NORMAL)
                    self.t_colors.replace("{}.0".format(i+1), "{}.30".format(i+1),
                                          "{}# {} --> lvl:{}".format(i+1, self.colors[i], self.lvl[i]))
                    self.t_colors.config(state=tk.DISABLED)

            else:
                messagebox.showerror("Error", "{} already in list".format(color))

            self.pop.grab_set()
            self.root.wait_window(self.pop)
            return

        self.c += 1

        t_r = str(hex(255-color[0])).replace("0x", "")
        if len(t_r) == 1:
            t_r = "0"+t_r

        t_g = str(hex(255-color[1])).replace("0x", "")
        if len(t_g) == 1:
            t_g = "0"+t_g

        t_b = str(hex(255-color[2])).replace("0x", "")
        if len(t_b) == 1:
            t_b = "0"+t_b

        t_c = "#{}{}{}".format(t_r, t_g, t_b)
        print(t_c)

        self.canv.create_text(event.x, event.y, text="{}".format(self.c), font=("Bold", 10), fill=t_c)

        t_lvl = ""
        if self.levels:
            lvl = self.pop_level()
            t_lvl = " --> lvl:{}".format(lvl)
            self.lvl.append(lvl)

        self.colors.append(color)

        self.t_colors.config(state=tk.NORMAL)
        self.t_colors.insert(tk.END, "{}# {}{}\n".format(self.c, color, t_lvl))
        self.t_colors.see(tk.END)
        self.t_colors.config(state=tk.DISABLED)

        self.pop.grab_set()
        self.root.wait_window(self.pop)

    def toogle_yes(self):
        self.yes = True
        self.close_pop()

    def color_exist(self, color):
        t = int(self.tolerence.get())
        for c in self.colors:
            rt = [c[0]-t, c[0]+t]
            gt = [c[1]-t, c[1]+t]
            bt = [c[2]-t, c[2]+t]

            RED = rt[0] < color[0] < rt[1]
            GREEN = gt[0] < color[1] < gt[1]
            BLUE = bt[0] < color[2] < bt[1]

            if RED and GREEN and BLUE:
                return self.colors.index(c)

        return None

    def pop_level(self):
        pop_lvl = tk.Toplevel(self.pop, bg=self.bg)

        w = 300
        h = 100
        pR = int(pop_lvl.winfo_screenwidth() / 2 - w / 2)
        pD = int(pop_lvl.winfo_screenheight() / 2 - h / 2 - 50)
        pop_lvl.geometry("{}x{}+{}+{}".format(w, h, pR, pD))

        lvl = tk.StringVar()
        lvl.set("1")

        f_lvl = tk.LabelFrame(pop_lvl, bg=self.bg, text="Give level")
        e_lvl = tk.Entry(f_lvl, textvariable=lvl)
        b_lvl = tk.Button(f_lvl, text="Valid", command=self.close_pop)
        e_lvl.pack(side=tk.LEFT, padx=5, pady=10)
        b_lvl.pack(side=tk.LEFT, padx=5)
        f_lvl.pack(padx=10, pady=10)

        pop_lvl.grab_set()
        self.pop.wait_window(pop_lvl)

        return int(lvl.get())

    def resize(self, img):
        c = 900

        q = img.size[0]/img.size[1]

        if img.size[0] >= img.size[1]:
            r = img.size[0]/c
            m_x = c
            m_y = int(c/q)
        else:
            r = img.size[1]/c
            m_y = c
            m_x = int(c*q)

        re_img = Image.new(mode="RGB", size=(m_x, m_y))
        re_pix = re_img.load()

        self.r = r

        for x in range(0, m_x):
            for y in range(0, m_y):
                re_pix[x, y] = img.getpixel((int(x * r), int(y * r)))

        return re_img

    def __browseFiles(self):
        file = ""

        rep = os.path.abspath(os.getcwd())
        filename_s = filedialog.askopenfilename(initialdir=rep,
                                                title="Select a File",
                                                filetypes=(("PNG files", "*.png"),
                                                           ("all files", "*.*")))
        if filename_s != "":
            filename = filename_s
        else:
            filename = file
        # Change label contents
        self.file.set(filename)

        self.colors = []
        self.levels = []

        self.t_colors.config(state=tk.NORMAL)
        self.t_colors.delete("1.0", tk.END)
        self.t_colors.config(state=tk.DISABLED)
        self.c = 0

        self.bare.pack_forget()
        self.bare_label.pack_forget()

    def close_pop(self):
        k = list(self.pop.children.keys())
        s = self.pop.children.get(k[len(k) - 1])
        s.destroy()

    def generate(self):
        pprint.pprint(self.colors)
        pprint.pprint(self.lvl)

        if self.out_name.get() == "":
            messagebox.showerror("Error", "Out file name is not set")
            return

        f_r = []
        f_g = []
        f_b = []
        for c in self.colors:
            f_r.append(int(c[0]))
            f_g.append(int(c[1]))
            f_b.append(int(c[2]))

        s_RGB = [f_r, f_g, f_b, int(self.tolerence.get())]
        pprint.pprint(s_RGB)

        self.bare.pack(side=tk.BOTTOM, anchor=tk.W)
        self.bare_label.pack(side=tk.BOTTOM, anchor=tk.W)

        if self.algo_list.get() == "Slik":
            print("Slik")
            gene_slik.generate(self.file.get(),
                               self.out_name.get(),
                               float(self.offset.get()),
                               float(self.gain.get()),
                               self.color_sel,
                               self.levels,
                               self.lvl,
                               self.bare,
                               self.bare_label,
                               s_RGB)
        else:
            print("Step")
            gene_step.generate(self.file.get(),
                               self.out_name.get(),
                               float(self.offset.get()),
                               float(self.gain.get()),
                               self.color_sel,
                               self.levels,
                               self.lvl,
                               self.bare,
                               self.bare_label,
                               s_RGB)


if __name__ == '__main__':
    app = App()
