import os

from pydub import AudioSegment


class AudioUtility:

    def high_pass_filter(self):
        pass

    def convert_to_mp3(self, root_directory,files):
        converted_mp3_list = []
        for subdir in os.walk(root_directory):
            for file in files:
                file_path = subdir + os.sep + file
                if file_path.endswith(".wav"):
                    # Add to array so it can be added to the archive
                    sound = AudioSegment.from_wav(file_path)
                    filename = file_path.replace(".wav", ".mp3")
                    sound.export(filename, format="mp3")
                    converted_mp3_list.append(filename)
                else:
                    converted_mp3_list.append(file_path)
        return converted_mp3_list
