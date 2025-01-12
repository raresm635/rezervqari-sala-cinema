import tkinter as tk
from tkinter import messagebox, simpledialog

class CinemaApp:
    """
    Clasa care definește interfața grafică a aplicației pentru rezervările la cinema.
    """

    def __init__(self, root):
        """
        Constructorul clasei CinemaApp. Inițializează elementele interfeței grafice și
        conectează funcțiile principale ale aplicației.
        """
        self.cinema = Cinema()  # Obiectul care gestionează logica cinematografului
        self.root = root
        self.root.title("Sistem de Rezervări Cinema")  # Titlul ferestrei aplicației

        # Elemente principale ale interfeței grafice
        self.movie_label = tk.Label(root, text="Filme disponibile:")  # Etichetă pentru lista de filme
        self.movie_label.pack()

        self.movie_listbox = tk.Listbox(root)  # Lista de filme disponibile
        self.movie_listbox.pack()

        # Buton pentru afișarea locurilor disponibile la filmul selectat
        self.show_seats_button = tk.Button(root, text="Vizualizează locuri", command=self.show_seats)
        self.show_seats_button.pack()

        # Buton pentru rezervarea unui loc
        self.reserve_button = tk.Button(root, text="Rezervare loc", command=self.reserve_seat)
        self.reserve_button.pack()

        # Buton pentru adăugarea unui film (doar pentru administratori)
        self.add_movie_button = tk.Button(root, text="Adaugă film (Admin)", command=self.add_movie)
        self.add_movie_button.pack()

        # Buton pentru ștergerea unui film
        self.delete_movie_button = tk.Button(root, text="Șterge film (Admin)", command=self.delete_movie)
        self.delete_movie_button.pack()

        # Buton pentru ștergerea unui loc
        self.delete_seat_button = tk.Button(root, text="Șterge rezervare loc", command=self.delete_seat)
        self.delete_seat_button.pack()

        # Buton pentru mutarea unui loc
        self.move_seat_button = tk.Button(root, text="Mută loc", command=self.move_seat)
        self.move_seat_button.pack()

        # Actualizarea listei de filme afișate în interfață
        self.update_movie_list()

    def update_movie_list(self):
        """
        Actualizează lista de filme afișată în interfața grafică.
        """
        self.movie_listbox.delete(0, tk.END)  # Șterge filmele existente din listă
        for movie in self.cinema.movies.keys():  # Iterează prin filmele din cinematograf
            if not self.cinema.movies[movie]["deleted"]:  # Nu afișa filmele șterse
                self.movie_listbox.insert(tk.END, movie)  # Adaugă fiecare film în listă

    def show_seats(self):
        """
        Afișează locurile disponibile și rezervate pentru filmul selectat.
        """
        selected = self.movie_listbox.curselection()  # Obține filmul selectat din listă
        if not selected:  # Dacă nu este selectat niciun film
            messagebox.showwarning("Atenție", "Selectați un film!")
            return

        movie_name = self.movie_listbox.get(selected)  # Numele filmului selectat
        seats = self.cinema.movies[movie_name]["sala"]  # Harta locurilor pentru film
        # Creează o reprezentare text a sălii (O = loc liber, X = loc rezervat)
        seat_map = "\n".join([" ".join(["O" if seat == 0 else "X" for seat in row]) for row in seats])

        # Afișează harta locurilor într-o fereastră de informații
        messagebox.showinfo(f"Locuri pentru {movie_name}", seat_map)

    def reserve_seat(self):
        """
        Rezervă un loc la filmul selectat. Solicită utilizatorului rândul și coloana.
        """
        selected = self.movie_listbox.curselection()  # Obține filmul selectat
        if not selected:  # Dacă nu este selectat niciun film
            messagebox.showwarning("Atenție", "Selectați un film!")
            return

        movie_name = self.movie_listbox.get(selected)  # Numele filmului selectat

        # Solicită utilizatorului rândul și coloana
        row = int(self.simple_input_dialog("Rând", "Introduceți rândul (1, 2, ...):")) - 1
        col = int(self.simple_input_dialog("Coloană", "Introduceți coloana (1, 2, ...):")) - 1

        # Rezervă locul prin metoda din clasa Cinema
        self.cinema.reserve_seat(movie_name, row, col)
        self.update_movie_list()  # Actualizează lista de filme după rezervare

    def add_movie(self):
        """
        Adaugă un film nou în cinematograf. Solicită utilizatorului numele filmului și dimensiunile sălii.
        """
        # Solicită informațiile despre film
        movie_name = self.simple_input_dialog("Nume film", "Introduceți numele filmului:")
        rows = int(self.simple_input_dialog("Rânduri", "Introduceți numărul de rânduri:"))
        cols = int(self.simple_input_dialog("Coloane", "Introduceți numărul de coloane:"))

        # Adaugă filmul în cinematograf
        self.cinema.add_movie(movie_name, rows, cols)
        self.update_movie_list()  # Actualizează lista de filme

    def delete_movie(self):
        """
        Șterge un film din cinematograf fără a șterge rezervările.
        """
        movie_name = self.simple_input_dialog("Ștergere film", "Introduceți numele filmului de șters:")
        self.cinema.delete_movie(movie_name)
        self.update_movie_list()  # Actualizează lista de filme

    def delete_seat(self):
        """
        Șterge o rezervare pentru un loc.
        """
        selected = self.movie_listbox.curselection()  # Obține filmul selectat
        if not selected:  # Dacă nu este selectat niciun film
            messagebox.showwarning("Atenție", "Selectați un film!")
            return

        movie_name = self.movie_listbox.get(selected)  # Numele filmului selectat

        # Solicită utilizatorului rândul și coloana locului de șters
        row = int(self.simple_input_dialog("Rând de șters", "Introduceți rândul locului de șters (1, 2, ...):")) - 1
        col = int(self.simple_input_dialog("Coloană de șters", "Introduceți coloana locului de șters (1, 2, ...):")) - 1

        # Șterge locul din sala respectivă
        self.cinema.delete_seat(movie_name, row, col)
        self.update_movie_list()  # Actualizează lista de filme

    def move_seat(self):
        """
        Mută un loc rezervat într-o altă locație.
        """
        selected = self.movie_listbox.curselection()  # Obține filmul selectat
        if not selected:  # Dacă nu este selectat niciun film
            messagebox.showwarning("Atenție", "Selectați un film!")
            return

        movie_name = self.movie_listbox.get(selected)  # Numele filmului selectat

        # Solicită utilizatorului rândul și coloana locului de mutat
        row_from = int(self.simple_input_dialog("Rând de mutat", "Introduceți rândul locului de mutat (1, 2, ...):")) - 1
        col_from = int(self.simple_input_dialog("Coloană de mutat", "Introduceți coloana locului de mutat (1, 2, ...):")) - 1

        # Solicită utilizatorului rândul și coloana locului unde se va muta
        row_to = int(self.simple_input_dialog("Rând destinație", "Introduceți rândul destinație (1, 2, ...):")) - 1
        col_to = int(self.simple_input_dialog("Coloană destinație", "Introduceți coloana destinație (1, 2, ...):")) - 1

        # Mută locul în sala de cinema
        self.cinema.move_seat(movie_name, row_from, col_from, row_to, col_to)
        self.update_movie_list()  # Actualizează lista de filme

    def simple_input_dialog(self, title, prompt):
        """
        Afișează o fereastră simplă de introducere a datelor și returnează răspunsul utilizatorului.
        """
        return simpledialog.askstring(title, prompt)


class Cinema:
    """
    Clasa care gestionează logica cinematografului, inclusiv filmele și rezervările.
    """

    def __init__(self):
        """
        Constructorul clasei Cinema.
        """
        self.movies = {}  # Dicționarul de filme, unde cheia este numele filmului

    def add_movie(self, movie_name, rows, cols):
        """
        Adaugă un film nou în cinematograf.
        """
        self.movies[movie_name] = {
            "sala": [[0] * cols for _ in range(rows)],  # Crează o sală de cinema (locuri libere)
            "deleted": False  # Marca filmul ca neșters
        }

    def delete_movie(self, movie_name):
        """
        Șterge un film din cinematograf (fără a șterge rezervările).
        """
        if movie_name in self.movies:
            self.movies[movie_name]["deleted"] = True  # Marchează filmul ca șters

    def reserve_seat(self, movie_name, row, col):
        """
        Rezervă un loc într-un film.
        """
        if movie_name in self.movies:
            if self.movies[movie_name]["sala"][row][col] == 0:  # Verifică dacă locul este liber
                self.movies[movie_name]["sala"][row][col] = 1  # Marchează locul ca rezervat
            else:
                messagebox.showwarning("Eroare", "Locul este deja rezervat!")

    def delete_seat(self, movie_name, row, col):
        """
        Șterge o rezervare de loc.
        """
        if movie_name in self.movies:
            self.movies[movie_name]["sala"][row][col] = 0  # Marchează locul ca liber

    def move_seat(self, movie_name, row_from, col_from, row_to, col_to):
        """
        Mută o rezervare de loc.
        """
        if movie_name in self.movies:
            if self.movies[movie_name]["sala"][row_from][col_from] == 1:  # Verifică dacă locul de plecare este rezervat
                self.movies[movie_name]["sala"][row_from][col_from] = 0  # Eliberează locul de plecare
                self.movies[movie_name]["sala"][row_to][col_to] = 1  # Rezervă locul de destinație
            else:
                messagebox.showwarning("Eroare", "Locul de plecare nu este rezervat!")

# Inițializare aplicație
if __name__ == "__main__":
    root = tk.Tk()
    app = CinemaApp(root)
    root.mainloop()
