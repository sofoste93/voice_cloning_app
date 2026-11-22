import asyncio
from pathlib import Path

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import (
    QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QMessageBox, QPushButton, QSlider, QTextEdit, QVBoxLayout,
    QWidget,
)

from src.tts_engine.tts_model import AUDIO_DIR, SOURCE_AUDIO_DIR, TextToSpeech
from src.ui.neptune_banner import NeptuneBanner
from src.utils.audio_utils import AudioPlayer


STYLE = """
QWidget { color: #eaf2ff; font: 14px "Segoe UI"; }
QWidget#studio { background: #080e1e; }
QFrame#card { background: #101a30; border: 1px solid #233453; border-radius: 15px; }
QLabel#brand { color: #aacaff; font-size: 13px; font-weight: 600; }
QLabel#title { font-size: 48px; font-weight: 700; }
QLabel#section { font-size: 18px; font-weight: 650; }
QLabel#muted { color: #a9b9d5; }
QTextEdit, QListWidget, QComboBox {
    background: #0a1327; border: 1px solid #293d60; border-radius: 8px;
    padding: 7px; selection-background-color: #294d80;
}
QTextEdit:focus, QListWidget:focus, QComboBox:focus, QPushButton:focus {
    border: 1px solid #9acbff;
}
QListWidget::item { padding: 6px; }
QPushButton {
    background: #182946; border: 1px solid #30476d; border-radius: 8px;
    padding: 7px 11px;
}
QPushButton:hover { background: #253b62; }
QPushButton#primary { background: #a8d3ff; color: #0b1830; font-weight: 700; }
QPushButton#primary:hover { background: #c2e1ff; }
QPushButton:disabled, QPushButton#primary:disabled {
    background: #121e35; color: #9aabc8; border-color: #253552;
}
QSlider::groove:horizontal { background: #2b4164; height: 4px; border-radius: 2px; }
QSlider::handle:horizontal { background: #a8d3ff; width: 12px; margin: -4px 0; border-radius: 6px; }
"""


def label(text, style=None):
    widget = QLabel(text)
    widget.setTextFormat(Qt.TextFormat.PlainText)
    if style:
        widget.setObjectName(style)
    return widget


def button(text, action):
    widget = QPushButton(text)
    widget.clicked.connect(action)
    return widget


def card():
    frame = QFrame()
    frame.setObjectName("card")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(16, 13, 16, 13)
    layout.setSpacing(8)
    return frame, layout


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("studio")
        self.setWindowTitle("Neptune · Studio vocal")
        self.resize(1080, 800)
        self.setMinimumSize(840, 730)
        self.setStyleSheet(STYLE)
        self.settings = QSettings("Neptune", "StudioVocal")
        self.tts_engine = TextToSpeech()
        self.audio_player = AudioPlayer()
        self.player = self.audio_player.player
        self.generation = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(14)
        hero = NeptuneBanner()
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(27, 19, 27, 22)
        hero_layout.addStretch()
        hero_layout.addWidget(label("STUDIO VOCAL", "brand"))
        hero_layout.addWidget(label("Neptune", "title"))
        hero_layout.addWidget(label("Un espace pour écouter et retrouver une voix.", "muted"))
        hero_layout.addStretch()
        root.addWidget(hero)

        columns = QHBoxLayout()
        columns.setSpacing(14)
        studio, compose = card()
        archive, library = card()
        columns.addWidget(studio, 6)
        columns.addWidget(archive, 5)
        root.addLayout(columns, 1)

        compose.addWidget(label("Créer un extrait", "section"))
        modes = QHBoxLayout()
        self.mode = QComboBox()
        self.mode.addItem("Voix de référence · local", "clone")
        self.mode.addItem("Voix standard · en ligne", "standard")
        self.mode.setAccessibleName("Type de voix")
        self.language = QComboBox()
        self.language.addItem("Français", "fr")
        self.language.addItem("Anglais", "en")
        self.language.setAccessibleName("Langue du texte")
        modes.addWidget(self.mode, 1)
        modes.addWidget(self.language)
        compose.addLayout(modes)
        self.mode_hint = label("", "muted")
        self.mode_hint.setWordWrap(True)
        compose.addWidget(self.mode_hint)
        self.text_input = QTextEdit()
        self.text_input.setAcceptRichText(False)
        self.text_input.setAccessibleName("Texte à lire")
        self.text_input.setPlaceholderText("Écris les mots que tu aimerais entendre…")
        compose.addWidget(self.text_input, 1)
        footer = QHBoxLayout()
        self.count = label("0 / 1 000", "muted")
        footer.addWidget(self.count)
        footer.addStretch()
        self.generate_button = button("Créer l’extrait", self.start_generation)
        self.generate_button.setObjectName("primary")
        footer.addWidget(self.generate_button)
        compose.addLayout(footer)
        self.status = label("Choisis une référence audio pour commencer.", "muted")
        self.status.setWordWrap(True)
        compose.addWidget(self.status)

        library.addWidget(label("Enregistrements d’origine", "section"))
        self.references = QListWidget()
        self.references.setAccessibleName("Enregistrements d’origine")
        library.addWidget(self.references, 1)
        ref_buttons = QHBoxLayout()
        ref_buttons.addWidget(button("Ajouter des fichiers", self.add_references))
        self.remove_button = button("Retirer de la liste", self.remove_reference)
        ref_buttons.addWidget(self.remove_button)
        library.addLayout(ref_buttons)
        library.addWidget(label("Extraits générés", "section"))
        self.recordings = QListWidget()
        self.recordings.setAccessibleName("Extraits générés")
        library.addWidget(self.recordings, 1)
        library.addWidget(label("Double-clique sur un fichier pour l’écouter.", "muted"))
        for items in (self.references, self.recordings):
            items.itemActivated.connect(self.play_item)
        self.references.currentItemChanged.connect(self.refresh_controls)

        playback, player_layout = card()
        self.track = label("Aucun extrait sélectionné", "section")
        player_layout.addWidget(self.track)
        timeline = QHBoxLayout()
        self.elapsed = label("0:00", "muted")
        self.seek = QSlider(Qt.Orientation.Horizontal)
        self.seek.setAccessibleName("Position de lecture")
        self.seek.setRange(0, 0)
        self.seek.sliderMoved.connect(self.player.setPosition)
        self.duration = label("0:00", "muted")
        timeline.addWidget(self.elapsed)
        timeline.addWidget(self.seek, 1)
        timeline.addWidget(self.duration)
        player_layout.addLayout(timeline)
        transport = QHBoxLayout()
        self.play_button = button("Écouter", self.toggle_playback)
        self.stop_button = button("Arrêter", self.player.stop)
        transport.addWidget(self.play_button)
        transport.addWidget(self.stop_button)
        transport.addStretch()
        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setAccessibleName("Volume")
        self.volume.setFixedWidth(110)
        self.volume.setRange(0, 100)
        self.volume.setValue(65)
        self.audio_player.audio_output.setVolume(0.65)
        self.volume.valueChanged.connect(lambda value: self.audio_player.audio_output.setVolume(value / 100))
        transport.addWidget(label("Volume", "muted"))
        transport.addWidget(self.volume)
        player_layout.addLayout(transport)
        root.addWidget(playback)
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.playbackStateChanged.connect(self.refresh_controls)
        self.player.errorOccurred.connect(self.playback_error)
        self.mode.currentIndexChanged.connect(self.refresh_controls)
        self.text_input.textChanged.connect(self.refresh_controls)

        for saved in self.settings.value("references", [], type=list):
            self.add_item(self.references, Path(saved))
        self.load_recordings()
        self.refresh_controls()

    @staticmethod
    def add_item(items, path):
        item = QListWidgetItem(path.name)
        item.setToolTip(str(path))
        item.setData(Qt.ItemDataRole.UserRole, str(path))
        items.addItem(item)
        return item

    def load_recordings(self):
        paths = {path.resolve() for folder in (AUDIO_DIR, SOURCE_AUDIO_DIR.parents[1] / "audio")
                 for path in folder.glob("*") if path.suffix.lower() in {".mp3", ".wav"}
                 and path.is_file() and not path.name.startswith(".")}
        for path in sorted(paths, key=lambda path: path.name, reverse=True):
            self.add_item(self.recordings, path)

    def reference_paths(self):
        return [self.references.item(index).data(Qt.ItemDataRole.UserRole)
                for index in range(self.references.count())]

    def add_references(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Ajouter des enregistrements d’origine", "",
            "Fichiers audio (*.wav *.mp3 *.flac)"
        )
        known = set(map(Path, self.reference_paths()))
        for name in paths:
            path = Path(name).resolve()
            if path not in known:
                self.add_item(self.references, path)
                known.add(path)
        if paths:
            self.status.setText("Enregistrements de référence ajoutés.")
            self.save_references()

    def remove_reference(self):
        self.references.takeItem(self.references.currentRow())
        self.save_references()

    def save_references(self):
        self.settings.setValue("references", self.reference_paths())
        self.refresh_controls()

    def refresh_controls(self):
        length = len(self.text_input.toPlainText().strip())
        self.count.setText(f"{length:,} / 1 000".replace(",", " "))
        local = self.mode.currentData() == "clone"
        self.mode_hint.setText("Utilise les enregistrements ajoutés comme références."
                               if local else "Le texte est envoyé au service vocal Microsoft.")
        self.remove_button.setEnabled(self.references.currentItem() is not None)
        self.generate_button.setEnabled(self.generation is None and 0 < length <= 1000
                                        and (not local or self.references.count() > 0))
        active = not self.player.source().isEmpty()
        playing = self.player.playbackState() == self.player.PlaybackState.PlayingState
        self.play_button.setEnabled(active)
        self.stop_button.setEnabled(active)
        self.play_button.setText("Pause" if playing else "Écouter")

    def start_generation(self):
        if self.generation is not None:
            return
        text = self.text_input.toPlainText().strip()
        local = self.mode.currentData() == "clone"
        refs = self.reference_paths()
        if not 0 < len(text) <= 1000 or (local and not refs):
            return
        if local and not self.settings.value("xtts_license", False, type=bool):
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Première utilisation de XTTS")
            dialog.setTextFormat(Qt.TextFormat.RichText)
            dialog.setText(
                "La première synthèse télécharge le modèle XTTS v2. "
                "Tes enregistrements et le texte restent sur cet ordinateur.<br><br>"
                "Accepter la <a href='https://huggingface.co/coqui/XTTS-v2/blob/main/LICENSE.txt'>"
                "licence Coqui pour un usage non commercial</a> ?"
            )
            dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            dialog.setDefaultButton(QMessageBox.StandardButton.No)
            dialog.button(QMessageBox.StandardButton.Yes).setText("Accepter et continuer")
            dialog.button(QMessageBox.StandardButton.No).setText("Annuler")
            if dialog.exec() != QMessageBox.StandardButton.Yes:
                return
            self.settings.setValue("xtts_license", True)
        self.generation = asyncio.create_task(
            self.generate(text, refs, self.language.currentData(), local)
        )
        self.refresh_controls()

    async def generate(self, text, refs, language, local):
        self.status.setText("Synthèse locale en cours. Le premier démarrage peut prendre un moment…"
                            if local else "Synthèse en ligne en cours…")
        try:
            if local:
                file = await asyncio.to_thread(self.tts_engine.clone_voice, text, refs, language)
            else:
                self.tts_engine.voice = {"fr": "fr-FR-HenriNeural", "en": "en-US-GuyNeural"}[language]
                file = await self.tts_engine.generate_voice(text)
            item = self.add_item(self.recordings, Path(file))
            self.recordings.insertItem(0, self.recordings.takeItem(self.recordings.row(item)))
            self.recordings.setCurrentItem(item)
            self.load_item(item)
            self.status.setText("Extrait enregistré. Appuie sur Écouter quand tu veux.")
        except Exception as error:
            self.status.setText("La synthèse a échoué.")
            dialog = QMessageBox(self)
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setWindowTitle("Synthèse interrompue")
            dialog.setTextFormat(Qt.TextFormat.PlainText)
            dialog.setText("Impossible de créer cet extrait.")
            dialog.setDetailedText(str(error))
            dialog.exec()
        finally:
            self.generation = None
            self.refresh_controls()

    def load_item(self, item):
        path = Path(item.data(Qt.ItemDataRole.UserRole))
        if not path.is_file():
            self.status.setText(f"Fichier introuvable : {path.name}")
            return False
        self.audio_player.add_audio(str(path))
        self.track.setText(path.name)
        self.refresh_controls()
        return True

    def play_item(self, item):
        if self.load_item(item):
            self.player.play()

    def toggle_playback(self):
        if self.player.playbackState() == self.player.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def playback_error(self, error, message):
        self.status.setText(f"Lecture impossible : {message}")

    @staticmethod
    def timecode(milliseconds):
        minutes, seconds = divmod(milliseconds // 1000, 60)
        return f"{minutes}:{seconds:02d}"

    def update_position(self, position):
        if not self.seek.isSliderDown():
            self.seek.setValue(position)
        self.elapsed.setText(self.timecode(position))

    def update_duration(self, duration):
        self.seek.setRange(0, duration)
        self.duration.setText(self.timecode(duration))

    def closeEvent(self, event):
        if self.generation is not None:
            self.status.setText("Attends la fin de la synthèse avant de fermer Neptune.")
            event.ignore()
            return
        self.player.stop()
        super().closeEvent(event)
