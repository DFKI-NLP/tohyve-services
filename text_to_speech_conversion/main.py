'''
To start it:
python -m main

To use it go to:
http://localhost:8003/tts/

'''
import traceback
import sys
import warnings
from convert import TTS


warnings.filterwarnings("ignore", category=UserWarning)

# root directory for created files
created_data_dir = "./created_audio"


# method to launch Gradio
def launch_tts():
    try:
        tts_obj = TTS(created_data_dir)
        tts_obj.do_tts()
        return {"TTS": "Task Completed!"}
    except Exception as e:
        return traceback.print_exception(*sys.exc_info())


# the main method
if __name__ == "__main__":
    launch_tts()
