'''
To start it:
python -m main

To use it go to:
http://localhost:8009/full-stream

'''
import traceback
import sys
import warnings

from pipeline import Pipe



warnings.filterwarnings('ignore')

# method to launch Gradio!
def launch_pipe():
    try:
        asr_obj = Pipe()
        asr_obj.run_pipe()
        return {"Pipeline": "Task Completed!"}
    except Exception as e:
        print(traceback.format_exc())
        # return traceback.print_exception(*sys.exc_info())

# the main method
if __name__ == "__main__":
    launch_pipe()