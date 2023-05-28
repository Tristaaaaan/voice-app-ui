import json


class AudioSettings:
    def __init__(self):
        self.audio_settings_file = self.open_audio()

    def open_audio(self):
        # Read the JSON config file
        with open('audio_cfg.json', 'r') as file:
            config = json.load(file)

        return config

    def get_audio_settings(self):
        audio_settings = self.audio_settings_file['Audio_settings']

        silence_seconds = audio_settings['Silence_Seconds']
        silence_threshold = audio_settings['Silence_Threshold']
        max_phrase_seconds = audio_settings['Max_Phrase_Seconds']

        return silence_seconds, silence_threshold, max_phrase_seconds

    def update_audio_settings(self, silence_seconds, silence_threshold, max_phrase_seconds):
        # Update the audio settings with custom values
        self.audio_settings_file['Audio_settings']['Silence_Seconds'] = silence_seconds
        self.audio_settings_file['Audio_settings']['Silence_Threshold'] = silence_threshold
        self.audio_settings_file['Audio_settings']['Max_Phrase_Seconds'] = max_phrase_seconds

        # Write the updated JSON config file
        with open('audio_cfg.json', 'w') as file:
            json.dump(self.audio_settings_file, file, indent=4)
