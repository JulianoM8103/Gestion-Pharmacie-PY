import json
from tkinter import *
from tkinter.messagebox import *

class Index(Tk):
    def __init__(self):

        Tk.__init__(self)
        self.title("Gestion de la Pharmacie Saint-Jean")
        self.geometry("1000x600")
        self.window()

    def window(self):
        menubar = Menu(self)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Patients", command=self.patients)
        menu1.add_command(label="Stock", command=self.stock)
        menu1.add_command(label="Trésorerie")
        menu1.add_separator()
        menu1.add_command(label="Quitter")
        menubar.add_cascade(label="Menu", menu=menu1)
        self.config(menu=menubar)

        label1 = Label(self, text="\n\n\n\nPharmacie Saint-Jean", font=("Helvetica", 26))
        label1.pack()
        label2 = Label(self, text="Le logiciel de gestion de la pharmacie Saint-Jean", font=("Helvetica", 19))
        label2.pack()
        label3 = Label(self, text="\nUtilisez le menu de navigation pour accéder aux différents onglets", font=("Helvetica", 15))
        label3.pack()

        self.mainloop()

    def patients(self):
        if askyesno('Patients', 'Êtes-vous sûr de vouloir faire ça?'):
            self.destroy()
            Patients()
        
    def stock(self):
        if askyesno('Stock', 'Êtes-vous sûr de vouloir faire ça ?'):
            self.destroy()
            Stock()

class Patients(Tk):
    def __init__(self):

        Tk.__init__(self)
        self.title("Liste des patients de la pharmacie Saint-Jean")
        self.geometry("1000x600")
        self.window()

    def window(self):
        menubar = Menu(self)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Menu principal", command=self.mainMenu)
        menu1.add_command(label="Stock", command=self.stock)
        menu1.add_command(label="Trésorerie")
        menu1.add_separator()
        menu1.add_command(label="Quitter")
        menubar.add_cascade(label="Menu", menu=menu1)
        self.config(menu=menubar)

        label1 = Label(self, text="Liste des patients de la pharmacie Saint-Jean", font=("Helvetica", 26))
        label1.pack()

        patients_frame = Frame(self)
        patients_frame.pack(side="left", padx=130)

        self.patients_listbox = Listbox(patients_frame)
        self.patients_listbox.pack(side="left", fill="both", expand=True)
        self.patients_listbox.config(height=30, width=100, justify="center")

        task_button_frame = Frame(patients_frame)
        task_button_frame.pack(side="right")

        add_task_button = Button(task_button_frame, text="Ajouter patient", command=self.add_task_window)
        add_task_button.pack(pady=5)

        edit_task_button = Button(task_button_frame, text="Modifier patient", command=self.edit_task_window)
        edit_task_button.pack(pady=5)

        remove_task_button = Button(task_button_frame, text="Retirer patient", command=self.remove_task)
        remove_task_button.pack(pady=5)

        with open("patients.json", "r") as f:
            self.data = json.load(f)

        for patients in self.data["patients"]:
            self.patients_listbox.insert("end", f"{patients['Prenom']} {patients['Nom']} - {patients['Adresse']} - {patients['Traitement']}")

    def add_task_window(self):

        add_task_window = Toplevel(self)

        prenom = Label(add_task_window, text="Prénom")
        prenom.pack()

        prenom_entry = Entry(add_task_window)
        prenom_entry.pack()

        nom = Label(add_task_window, text="Nom")
        nom.pack()

        nom_entry = Entry(add_task_window)
        nom_entry.pack()

        adresse = Label(add_task_window, text="Adresse")
        adresse.pack()

        adresse_entry = Entry(add_task_window)
        adresse_entry.pack()

        traitement = Label(add_task_window, text="Traitement récurrent ?")
        traitement.pack()

        traitement_entry = Entry(add_task_window)
        traitement_entry.pack()

        add_task_button = Button(add_task_window, text="Ajouter un patient", command=lambda: self.add_task(prenom_entry.get(), nom_entry.get(), adresse_entry.get(), traitement_entry.get()))
        add_task_button.pack()

    def add_task(self, Prenom, Nom, Adresse, Traitement):
        self.patients_listbox.insert("end", f"{Prenom} {Nom} - {Adresse} - {Traitement}")

        self.data["patients"].append({"Prenom": Prenom, "Nom": Nom, "Adresse": Adresse, "Traitement": Traitement})

        with open("patients.json", "w") as f:
            json.dump(self.data, f)

    def edit_task_window(self):
        selection = self.patients_listbox.curselection()

        if len(selection) == 1:
            task = self.data["patients"][selection[0]]
            edit_task_window = Toplevel(self)
        
        prenom = Label(edit_task_window, text="Prénom")
        prenom.pack()

        prenom_entry = Entry(edit_task_window)
        prenom_entry.pack()

        nom = Label(edit_task_window, text="Nom")
        nom.pack()

        nom_entry = Entry(edit_task_window)
        nom_entry.pack()

        adresse = Label(edit_task_window, text="Adresse")
        adresse.pack()

        adresse_entry = Entry(edit_task_window)
        adresse_entry.pack()

        traitement = Label(edit_task_window, text="Traitement récurrent ?")
        traitement.pack()

        traitement_entry = Entry(edit_task_window)
        traitement_entry.pack()

        edit_task_button = Button(edit_task_window, text="Modifier patient", command=lambda: self.edit_task(selection[0], prenom_entry.get(), nom_entry.get(), adresse_entry.get(), traitement_entry.get()))
        edit_task_button.pack()

    def edit_task(self, index, Prenom, Nom, Adresse, Traitement):

        self.patients_listbox.delete(index)
        self.patients_listbox.insert(index, f"{Prenom}  {Nom} - {Adresse} - {Traitement}")

        self.data["patients"][index]["Prenom"] = Prenom
        self.data["patients"][index]["Nom"] = Nom
        self.data["patients"][index]["Adresse"] = Adresse
        self.data["patients"][index]["Traitement"] = Traitement
    
        with open("patients.json", "w") as f:
            json.dump(self.data, f)

    def remove_task(self):
        selection = self.patients_listbox.curselection()

        if len(selection) > 0:
            for index in reversed(selection):
                self.patients_listbox.delete(index)

        self.data["patients"] = [task for index, task in enumerate(self.data["patients"]) if index not in selection]

        with open("patients.json", "w") as f:
            json.dump(self.data, f)

    def mainMenu(self):
        if askyesno('Menu principal', 'Êtes-vous sûr de vouloir faire ça ?'):
            self.destroy()
            Index()

    def stock(self):
        if askyesno('Stock', 'Êtes-vous sûr de vouloir faire ça ?'):
            self.destroy()
            Stock()

        self.mainloop()

class Stock(Tk):
    def __init__(self):

        Tk.__init__(self)
        self.title("Stock de la Pharmacie Saint-Jean")
        self.geometry("1000x600")
        self.window()
    
    def window(self):
        menubar = Menu(self)
        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Menu principal")
        menu1.add_command(label="Patients")
        menu1.add_command(label="Trésorerie")
        menu1.add_separator()
        menu1.add_command(label="Quitter")
        menubar.add_cascade(label="Menu", menu=menu1)
        self.config(menu=menubar)

        label1 = Label(self, text="Stock de la pharmacie Saint-Jean", font=("Helvetica", 26))
        label1.pack()

        stock_frame = Frame(self)
        stock_frame.pack(side="left", padx=130)

        self.stock_listbox = Listbox(stock_frame)
        self.stock_listbox.pack(side="left", fill="both", expand=True)
        self.stock_listbox.config(height=30, width=100, justify="center")

        task_button_frame = Frame(stock_frame)
        task_button_frame.pack(side="right")

        add_task_button = Button(task_button_frame, text="Ajouter médicament", command=self.add_task_window)
        add_task_button.pack(pady=5)

        edit_task_button = Button(task_button_frame, text="Modifier médicament", command=self.edit_task_window)
        edit_task_button.pack(pady=5)

        remove_task_button = Button(task_button_frame, text="Retirer médicament", command=self.remove_task)
        remove_task_button.pack(pady=5)

        with open("stock.json", "r") as f:
            self.data = json.load(f)

        for stock in self.data["stock"]:
            self.stock_listbox.insert("end", f"{stock['title']} - {stock['number']} - {stock['price']}€/u")

        
    def add_task_window(self):

        add_task_window = Toplevel(self)

        title = Label(add_task_window, text="Nom médicament")
        title.pack()

        title_entry = Entry(add_task_window)
        title_entry.pack()

        number = Label(add_task_window, text="Nombre")
        number.pack()

        number_entry = Entry(add_task_window)
        number_entry.pack()

        price = Label(add_task_window, text="Prix à l'unité")
        price.pack()

        price_entry = Entry(add_task_window)
        price_entry.pack()

        add_task_button = Button(add_task_window, text="Ajouter un médicament", command=lambda: self.add_task(title_entry.get(), number_entry.get(), price_entry.get()))
        add_task_button.pack()

    def add_task(self, title, number, price):
        self.stock_listbox.insert("end", f"{title} - {number} - {price}€/u")

        self.data["stock"].append({"title": title, "number": number, "price": price})

        with open("stock.json", "w") as f:
            json.dump(self.data, f)

    def edit_task_window(self):
        selection = self.stock_listbox.curselection()

        if len(selection) == 1:
            task = self.data["stock"][selection[0]]
            edit_task_window = Toplevel(self)
        
        prenom = Label(edit_task_window, text="Nom médicament")
        prenom.pack()

        prenom_entry = Entry(edit_task_window)
        prenom_entry.pack()

        nom = Label(edit_task_window, text="Quantité")
        nom.pack()

        nom_entry = Entry(edit_task_window)
        nom_entry.pack()

        adresse = Label(edit_task_window, text="Prix à l'unité")
        adresse.pack()

        adresse_entry = Entry(edit_task_window)
        adresse_entry.pack()

        edit_task_button = Button(edit_task_window, text="Modifier patient", command=lambda: self.edit_task(selection[0], prenom_entry.get(), nom_entry.get(), adresse_entry.get()))
        edit_task_button.pack()

    def edit_task(self, index, title, number, price):

        self.stock_listbox.delete(index)
        self.stock_listbox.insert(index, f"{title} - {number} - {price}€/u")

        self.data["stock"][index]["title"] = title
        self.data["stock"][index]["number"] = number
        self.data["stock"][index]["price"] = price
    
        with open("stock.json", "w") as f:
            json.dump(self.data, f)

    def remove_task(self):
        selection = self.stock_listbox.curselection()

        if len(selection) > 0:
            for index in reversed(selection):
                self.stock_listbox.delete(index)

        self.data["stock"] = [task for index, task in enumerate(self.data["stock"]) if index not in selection]

        with open("stock.json", "w") as f:
            json.dump(self.data, f)

        self.mainloop()

class Tresorerie(Tk):
    def __init__(self):

        Tk.__init__(self)
        self.title("Stock de la Pharmacie Saint-Jean")
        self.geometry("1000x600")
        self.window()



window = Index()