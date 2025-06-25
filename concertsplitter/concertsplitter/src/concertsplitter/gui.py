import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pathlib import Path
from .audio_utils import process_folder, generate_waveform_preview, preview_audio


class ConcertSplitterApp(toga.App):
    def startup(self):
        # Main container
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Pick folder button
        self.pick_button = toga.Button("Pick Folder", on_press=self.pick_folder, style=Pack(padding=5))
        self.status_label = toga.Label("No folder selected.", style=Pack(padding=(5, 0)))

        self.main_box.add(self.pick_button)
        self.main_box.add(self.status_label)

        # Create window and show
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def pick_folder(self, widget):
        # Use future + callback for folder picker (Toga safe pattern)
        future = self.main_window.select_folder_dialog("Select Concert Folder")
        future.add_done_callback(self.process_folder)

    def process_folder(self, future):
        folder = future.result()
        if not folder:
            return

        self.status_label.text = f"Selected: {folder}"
        self.track_data = process_folder(Path(folder))

        # Display tracks with preview buttons
        for idx, track in enumerate(self.track_data):
            title = f"Track {idx + 1}: {track['title']}"
            time_str = f"Suggested start: {track['start']:.2f}s"

            preview_btn = toga.Button(
                "▶ Preview",
                on_press=lambda w, i=idx: preview_audio(self.track_data[i]),
                style=Pack(padding=5)
            )
            wave_btn = toga.Button(
                "📈 Waveform",
                on_press=lambda w, i=idx: generate_waveform_preview(self.track_data[i]),
                style=Pack(padding=5)
            )

            self.main_box.add(toga.Label(f"{title} — {time_str}", style=Pack(padding=3)))
            self.main_box.add(toga.Box(children=[preview_btn, wave_btn], style=Pack(direction=ROW)))

        self.main_window.content.refresh()
