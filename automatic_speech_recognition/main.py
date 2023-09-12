'''
To start it:
python -m main

To use it go to:
http://localhost:8001/asr/

'''
import traceback
import sys
import warnings


from transcribe import ASR
from model import init_model

warnings.filterwarnings('ignore')

# init our model
pipe, MODEL_NAME = init_model()

# method to launch Gradio!
def launch_asr():
    try:
        asr_obj = ASR(pipe, MODEL_NAME)
        asr_obj.do_asr()
        return {"ASR": "Task Completed!"}
    except Exception as e:
        return traceback.print_exception(*sys.exc_info())

# the main method
if __name__ == "__main__":
    launch_asr()
