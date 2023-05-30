from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivy.core.audio import SoundLoader

from audio import Audio
from audio_settings import AudioSettings

import threading
import datetime
import os

from kivy import platform
ausettings = AudioSettings()
au = Audio()

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET, Permission.WRITE_EXTERNAL_STORAGE,
                         Permission.READ_EXTERNAL_STORAGE])


class ListItemWithIcon(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._txt_left_pad = "10dp"
        self.sound = SoundLoader.load("Recording A.wav")

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.ids._left_container.padding = [
            self._txt_left_pad, "0dp", "0dp", "0dp"]

    def play_rec(self):
        if self.ids.status.icon == 'play':
            self.ids.status.icon = 'stop'
            self.playback_thread = threading.Thread(target=self.play_audio())

        else:
            self.ids.status.icon = 'play'
            self.playback_thread = threading.Thread(
                target=self.stop_audio())

    def play_audio(self):
        self.sound.play()

    def stop_audio(self):
        self.sound.stop()


class FirstWindow(Screen):
    files = ListProperty([])
    Builder.load_file('firstwindow.kv')

    def __init__(self, **kw):
        super().__init__(**kw)

        Clock.schedule_once(self.begin)
        self.sound = SoundLoader.load("Recording A.wav")

    def begin(self, *args):
        if au.FI() is True:
            self.get_audio_files()
        else:
            self.error_dialog(
                message="Sorry, the application failed to establish a connection. Please try again.")

    def audio_play(self):
        self.sound.play()

    def audio_stop(self):
        self.sound.stop()

    def get_audio_files(self):
        if au.CS() is True:
            # Get the directory path where WAV files are located
            directory_path = os.path.abspath("./")

            # Iterate through files in the directory
            for file_name in os.listdir(directory_path):
                # Check if the file has a .wav extension
                if file_name.endswith('.wav'):
                    # Add the file name to the files list
                    self.files.append(file_name)

            # Populate the file list view with the WAV files
            for file_name in self.files:
                list_item = ListItemWithIcon(text=file_name)
                list_item.secondary_text = self.get_recording_length()
                self.ids.container.add_widget(list_item)
            self.files = []
        else:
            self.error_dialog(
                message="Sorry, the application failed to establish a connection. Please try again.")

    def get_recording_length(self):
        audio_length = self.sound.length
        length = datetime.timedelta(seconds=int(audio_length))
        hours, remainder = divmod(length.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours == 0:
            formatted_length = "{:02d}:{:02d}".format(minutes, seconds)
        else:
            formatted_length = "{:02d}:{:02d}:{:02d}".format(
                hours, minutes, seconds)

        return formatted_length

    def error_dialog(self, message):

        close_button = MDFlatButton(
            text='CLOSE',
            text_color=[0, 0, 0, 1],
            on_release=self.close_dialog,
        )
        self.dialog = MDDialog(
            title='[color=#FF0000]Ooops![/color]',
            text=message,
            buttons=[close_button],
            auto_dismiss=False
        )
        self.dialog.open()

    # Close Dialog
    def close_dialog(self, obj):
        MDApp.get_running_app().stop()

    def toggle_recording(self):
        if self.ids.rec.icon == 'record-circle-outline':
            self.ids.rec.icon = 'stop'
        else:
            self.ids.rec.icon = 'record-circle-outline'

    def settings(self):

        self.manager.current = "second"
        self.manager.transition.direction = "left"

    def account(self):

        self.manager.current = "third"
        self.manager.transition.direction = "left"


class SecondWindow(Screen):

    Builder.load_file('secondwindow.kv')

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "first"

    def verify(self):

        ausettings.update_audio_settings(
            int(self.ids.silence_duration.value), int(self.ids.silence_threshold.value) * 100, int(self.ids.recording_length.value))
        self.back()

    def reset(self):

        self.ids.silence_duration.value = int(
            ausettings.get_audio_settings()[0])

        self.ids.silence_threshold.value = int(
            ausettings.get_audio_settings()[1]) / 100

        self.ids.recording_length.value = int(
            ausettings.get_audio_settings()[2])


class ThirdWindow(Screen):

    Builder.load_file('thirdwindow.kv')

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "first"


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):

        return WindowManager()

    def on_start(self):

        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions(Permission.INTERNET,
                                [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        self.root.ids.second.silence_duration.value = int(
            ausettings.get_audio_settings()[0])

        self.root.ids.second.silence_threshold.value = int(
            ausettings.get_audio_settings()[1]) / 100

        self.root.ids.second.recording_length.value = int(
            ausettings.get_audio_settings()[2])

        return super().on_start()


if __name__ == '__main__':
    rawApp().run()
