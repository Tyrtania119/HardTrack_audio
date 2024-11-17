from pydub import AudioSegment
from tkinter import Tk, filedialog, Button, Listbox, Label, Scale, HORIZONTAL
import pygame
import time


class MixTapeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MixTape Creator")

        # Lista utworów
        self.song_list = []
        self.listbox = Listbox(root, width=50, height=15)
        self.listbox.pack()

        # Przyciski
        Button(root, text="Dodaj Utwór", command=self.add_song).pack()
        Button(root, text="Utwórz Składankę", command=self.create_mixtape).pack()
        Button(root, text="Eksportuj MP3", command=self.export_mixtape).pack()
        Button(root, text="Odtwórz", command=self.play_mixtape).pack()
        Button(root, text="Zatrzymaj", command=self.stop_mixtape).pack()
        Button(root, text="Wznów", command=self.resume_mixtape).pack()

        # Suwak do regulacji głośności
        self.volume_label = Label(root, text="Głośność:")
        self.volume_label.pack()
        self.volume_scale = Scale(root, from_=0, to_=100, orient=HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(50)  # Ustawienie domyślnej głośności na 50%
        self.volume_scale.pack()

        self.mixtape = None
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0  # Pozwala na wznawianie odtwarzania od miejsca, w którym zostało zatrzymane
        self.current_song = None  # Przechowuje aktualnie odtwarzany utwór
        self.current_song_length = 0  # Długość aktualnie odtwarzanego utworu w sekundach

    def add_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.song_list.append(file_path)
            self.listbox.insert("end", file_path.split("/")[-1])

    def create_mixtape(self):
        if not self.song_list:
            print("Brak utworów!")
            return

        combined = AudioSegment.empty()
        for song_path in self.song_list:
            audio = AudioSegment.from_file(song_path)
            combined += audio

        self.mixtape = combined
        print("Składanka utworzona!")

    def export_mixtape(self):
        if not self.mixtape:
            print("Najpierw utwórz składankę!")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav")],
            title="Zapisz składankę jako"
        )

        if save_path:
            self.mixtape.export(save_path, format="mp3")
            print(f"Składanka zapisana: {save_path}")

    def play_mixtape(self):
        selected_song_index = self.listbox.curselection()  # Zwraca krotkę z indeksem
        if not selected_song_index:
            print("Wybierz utwór z listy!")
            return

        # Pobieramy ścieżkę do pliku z listy
        selected_song_path = self.song_list[selected_song_index[0]]

        if self.mixtape:
            # Jeśli składanka została utworzona, odtwarzamy ją
            temp_path = "temp_mixtape.mp3"
            self.mixtape.export(temp_path, format="mp3")
            pygame.mixer.init()
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play(start=self.current_position)
            self.is_playing = True
            self.is_paused = False
            self.current_song = temp_path
            self.current_song_length = self.mixtape.duration_seconds
            print("Odtwarzanie składanki rozpoczęte.")
        else:
            # Jeśli składanka nie została stworzona, odtwarzamy wybrany utwór
            pygame.mixer.init()
            pygame.mixer.music.load(selected_song_path)
            pygame.mixer.music.play(start=self.current_position)
            self.is_playing = True
            self.is_paused = False
            self.current_song = selected_song_path
            song = AudioSegment.from_file(selected_song_path)
            self.current_song_length = song.duration_seconds
            print(f"Odtwarzanie {selected_song_path} rozpoczęte.")

    def stop_mixtape(self):
        if not self.is_playing:
            print("Nie ma nic do zatrzymania.")
            return

        # Zatrzymaj odtwarzanie
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0  # Zresetuj pozycję do początku
        print("Odtwarzanie zatrzymane.")

    def resume_mixtape(self):
        if self.is_paused:
            # Wznowienie odtwarzania od miejsca, w którym zostało zatrzymane
            pygame.mixer.music.play(start=self.current_position)
            self.is_playing = True
            self.is_paused = False
            print("Wznowiono odtwarzanie.")
        else:
            print("Nie ma nic do wznowienia.")

    def set_volume(self, value):
        volume = int(value) / 100  # Skala w pygame to wartość od 0 do 1
        pygame.mixer.music.set_volume(volume)  # Ustawia głośność
        print(f"Głośność ustawiona na {value}%")


# Uruchom aplikację
root = Tk()
app = MixTapeApp(root)
root.mainloop()
