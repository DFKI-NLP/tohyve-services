'''
To start it:
python -m main

To use it go to:
http://localhost:8002/mt/

'''
import traceback
import warnings
import sys
from model import MbartTranslatorModels, M2m100TranslatorModels
from mt import MT

warnings.filterwarnings("ignore")

m2m_obj = M2m100TranslatorModels()

# method to launch Gradio!
def launch_mt():
    global m2m_obj
    try:
        mt_obj = MT(m2m_obj)
        mt_obj.do_mt()
        return {"MT": "Task Completed!"}
    except Exception as e:
        return traceback.print_exception(*sys.exc_info())

# the main method
if __name__ == "__main__":
    launch_mt()
