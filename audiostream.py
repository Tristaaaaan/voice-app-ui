from kivy.lang import Builder
from kivy.app import App
from audiostream import get_input
from kivy.clock import Clock


class AudioRecorderApp(App):
    def build(self):
        return Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Start Recording'
        on_release: app.start_recording()
    Button:
        text: 'Stop Recording'
        on_release: app.stop_recording()
''')

    def __init__(self):
        super(AudioRecorderApp, self).__init__()
        self.audio_stream = None
        self.threshold = 0.1  # Adjust this value according to your needs
        self.is_recording = False

    def start_recording(self):
        self.is_recording = True
        self.audio_stream = get_input()
        self.audio_stream.start()

        # Adjust the interval as needed
        Clock.schedule_interval(self.check_audio_level, 0.1)

    def check_audio_level(self, dt):
        if self.is_recording and self.audio_stream.rms() < self.threshold:
            self.stop_recording()

    def stop_recording(self):
        self.is_recording = False
        self.audio_stream.stop()
        Clock.unschedule(self.check_audio_level)


if __name__ == '__main__':
    AudioRecorderApp().run()
