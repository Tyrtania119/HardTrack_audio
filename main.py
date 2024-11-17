from pydub import AudioSegment
from tkinter import Tk, filedialog, Button, Listbox, Label, Scale, HORIZONTAL, Frame
import pygame

class MixTapeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HardTrack")

        # Główne ramki dla przycisków i listy piosenek
        self.options_frame = Frame(root)
        self.options_frame.pack(side="left", padx=10, pady=10)

        self.list_frame = Frame(root)
        self.list_frame.pack(side="right", padx=10, pady=10)

        self.audio_controls_frame = Frame(self.list_frame)
        self.audio_controls_frame.pack(side="bottom", padx=10, pady=10, fill="x")

        self.controls_frame = Frame(self.audio_controls_frame)
        self.controls_frame.pack(side="bottom", fill="x")

        # Lista utworów
        Label(self.list_frame, text="Lista Piosenek").pack()
        self.song_list = []
        self.listbox = Listbox(self.list_frame, width=40, height=15)
        self.listbox.pack()

        # Lista przebitek
        Label(self.list_frame, text="Lista Przebitek").pack()
        self.snippet_list = []
        self.snippetbox = Listbox(self.list_frame, width=40, height=10)
        self.snippetbox.pack()

        # Przyciski w lewej ramce
        self.create_buttons()

        # Suwak do regulacji głośności
        self.volume_scale = self.create_volume_control()

        # Przyciski kontroli odtwarzania
        self.create_playback_buttons()

        self.mixtape = None
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0

    def create_buttons(self):
        Button(self.options_frame, text="Dodaj Utwór", command=self.add_song).pack(pady=5)
        Button(self.options_frame, text="Dodaj Długą Przebitkę", command=self.add_long_snippet).pack(pady=5)
        Button(self.options_frame, text="Utwórz Składankę", command=self.create_mixtape).pack(pady=5)
        Button(self.options_frame, text="Eksportuj MP3", command=self.export_mixtape).pack(pady=5)

    def create_volume_control(self):
        volume_label = Label(self.audio_controls_frame, text="Głośność:")
        volume_label.pack(side="left", anchor="s")
        volume_scale = Scale(self.audio_controls_frame, from_=0, to_=100, orient=HORIZONTAL, command=self.set_volume)
        volume_scale.pack(side="right", anchor="s")
        volume_scale.set(50)  # Domyślna wartość
        return volume_scale

    def create_playback_buttons(self):
        Button(self.controls_frame, text="Odtwórz", command=self.play_mixtape).pack(pady=5, padx=10, anchor="s", side="left")
        Button(self.controls_frame, text="Zatrzymaj", command=self.stop_mixtape).pack(pady=5, padx=10, anchor="s", side="left")
        Button(self.controls_frame, text="Wznów", command=self.resume_mixtape).pack(pady=5, padx=10, anchor="s", side="left")

    def add_song(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            self.song_list.append(file_path)
            self.listbox.insert("end", file_path.split("/")[-1])

    def add_long_snippet(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if file_path:
            snippet = AudioSegment.from_file(file_path)
            self.snippet_list.append({"type": "long", "audio": snippet})
            self.snippetbox.insert("end", f"Dłuższa: {file_path.split('/')[-1]}")

    def create_mixtape(self):
        if not self.song_list:
            print("Brak utworów!")
            return

        combined = AudioSegment.empty()

        for song_path in self.song_list:
            if self.snippet_list:  # Dodaj pierwszą przebitkę
                combined += self.snippet_list[0]["audio"]

            song = AudioSegment.from_file(song_path)
            combined += song

        self.mixtape = combined
        print("Składanka utworzona!")

        self.play_mixtape()

    def export_mixtape(self):
        if not self.mixtape:
            print("Najpierw utwórz składankę!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if save_path:
            self.mixtape.export(save_path, format="mp3")
            print(f"Składanka zapisana: {save_path}")

    def play_mixtape(self):
        if not self.mixtape:
            print("Brak składanki do odtworzenia!")
            return

        volume = self.volume_scale.get() / 100
        temp_path = "temp_mixtape.mp3"
        self.mixtape.export(temp_path, format="mp3")

        pygame.mixer.init()
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(start=self.current_position)
        self.is_playing = True
        self.is_paused = False
        print("Odtwarzanie składanki rozpoczęte.")

    def stop_mixtape(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.current_position = 0
            print("Odtwarzanie zatrzymane.")

    def resume_mixtape(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.is_paused = False
            print("Wznowiono odtwarzanie.")
        else:
            print("Nie ma nic do wznowienia.")

    def set_volume(self, value):
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)
        print(f"Głośność ustawiona na {value}%")


# Uruchom aplikację
root = Tk()
app = MixTapeApp(root)
root.mainloop()
