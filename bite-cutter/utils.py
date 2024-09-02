"""Util functions for the bite cutter docker."""

import os
import requests
import datetime
from nltk.tokenize import sent_tokenize, word_tokenize
from pydub import AudioSegment


async def process_loop(tts_url, text, language):
    """Sends input text recursively to TTS and splits it if needed.

    Returns a list of filepaths to the soundfiles."""

    # make a http request to the TTS model
    output = requests.post(tts_url, json={"data": [language, text]})
    output = output.json()

    # base case: text can be processed
    if was_processed(output):
        return [extract_filepath(output)]

    # use the custom split method
    bites = split(text)

    # start the recursion for all text bites
    filepaths = []
    for bite in bites:
        filepaths.extend(await process_loop(tts_url, bite, language))

    return filepaths


def was_processed(output):
    """Checks if the TTS service could handle the text input.

    The TTS service output is a hash map either containing the key 'data' if
    processing was successful or containing the key 'error' if unsuccessful.
    """

    if 'data' in output.keys():
        return True
    elif 'error' in output.keys():
        return False
    else:
        raise AssertionError


def extract_filepath(output):
    return output['data'][0]['name']


def split(text):
    """Splits text into sentences or sentences into half the number of
    words."""

    # split into sentences and return if there are more than one
    sentences = sent_tokenize(text)

    if len(sentences) > 1:
        return sentences

    # split into words and join everything to the mid point
    words = word_tokenize(text)

    mid = len(words) // 2
    words_first_half = ' '.join(words[:mid])
    words_second_half = ' '.join(words[mid:])

    return [words_first_half, words_second_half]


class WavHandler():

    def __init__(self,
                 download_dir,
                 upload_dir,
                 get_file_url,
                 remote_filepaths):
        """Make folders for the download and file providing.

        download_dir: dir to save wav bites from tts
        upload_dir: dir to provide the finished wav to user
        get_file_url: base-url from tts service to get the wav file
        remote_filepaths: second half of wav file on tts service
        local_filepaths: full paths to all downloaded wav snippets
        """
        self.code = self._create_code()
        self.download_dir = download_dir + self.code + '/'
        self.upload_dir = upload_dir
        self.get_file_url = get_file_url
        self.remote_filepaths = remote_filepaths
        self.local_filepaths = []
        self.output_path = self.upload_dir + self.code

        os.mkdir(self.download_dir)

    def _create_code(self):
        """Create time code to use for file specification."""
        code = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')

        return code

    async def download(self):
        """Download files from TTS service and save filepaths."""

        local_file = "_downloaded.wav"

        for idx, path in enumerate(self.remote_filepaths):

            # set the full remote and local paths
            full_remote_path = self.get_file_url + path
            full_local_path = self.download_dir + str(idx) + local_file

            # send a http GET to download from the TTS service
            file_response = requests.get(full_remote_path)

            # save the file to the local folder
            with open(full_local_path, 'wb') as file:
                file.write(file_response.content)

            self.local_filepaths.append(full_local_path)

    async def concatenate(self):
        """Use AudioSegment to concatenate the wav files."""

        # initialize Audiosegment and concatenate the wav files onto it
        big_wav = AudioSegment.empty()

        for wav in self.local_filepaths:
            # Check if file already exists
            if os.path.exists(wav):
                big_wav += AudioSegment.from_wav(wav)
                big_wav += self._create_break()
            else:
                raise FileNotFoundError

        # Save the output file
        big_wav.export(self.output_path, format='wav')

        # Clean up wav snippets
        self._delete_wav()

    def _create_break(self):
        """Create a 0.4s long silence to insert between snippets."""

        # create a silence of 0.4 seconds
        break_duration = 400
        silence = AudioSegment.silent(duration=break_duration)

        return silence

    def _delete_wav(self):
        """Deletes temporary wav bites."""

        for wav in self.local_filepaths:
            if os.path.exists(wav):
                os.remove(wav)

    def get_output(self):
        return self.code
