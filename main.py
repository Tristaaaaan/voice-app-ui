from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog

from audio import Audio
from audio_settings import AudioSettings

ausettings = AudioSettings()
au = Audio()


class ListItemWithIcon(TwoLineAvatarIconListItem):
    '''Custom list item'''


class FirstWindow(Screen):

    Builder.load_file('firstwindow.kv')

    def __init__(self, **kw):
        super().__init__(**kw)

        Clock.schedule_once(self.begin)

    def begin(self, *args):
        if au.FI() is True:
            self.get_audio_files()
        else:
            self.error_dialog(
                message="Sorry, the application failed to establish a connection. Please try again.")

    def get_audio_files(self):
        if au.CS() is True:
            pass
        else:
            self.error_dialog(
                message="Sorry, the application failed to establish a connection. Please try again.")

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

        self.root.ids.second.silence_duration.value = int(
            ausettings.get_audio_settings()[0])

        self.root.ids.second.silence_threshold.value = int(
            ausettings.get_audio_settings()[1]) / 100

        self.root.ids.second.recording_length.value = int(
            ausettings.get_audio_settings()[2])

        return super().on_start()


if __name__ == '__main__':
    rawApp().run()
