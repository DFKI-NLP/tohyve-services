'''
To use the automatic-speecg-recognition api we can use this script!!

Before using it please read some instructions below:
*   It will always ecpect three parameters (see client.predict() method below!!). 
*   If you wanted to use only file upload than please send empty string to microphone otherwise you can send empty string to file-upload if you wanted to use microphone only.
*   You can't use both file-upload and microphone at a time. 

To use it:
python -m api_client
'''
import traceback
import sys
from gradio_client import Client


# prints the transcribed result
def print_result(x):
    print(f"\nThe transcribed output:\n{x}")


# send the client request to the api
def run_asr_api():
    client = Client("http://localhost:8000/")

    job = client.submit(
        "de",	# str representing string value in 'Input_language' Textbox component.
        "",	# str representing filepath or URL to file in 'Microphone' Audio component.
        "C:/Users/ASUS/Downloads/trans_audio.mp3",	# str representing filepath or URL to file in 'File_upload' Audio component.
        api_name="/predict", 
        result_callbacks=[print_result]
        )
    job.done()


# the main method
if __name__ == "__main__":
    try:
        run_asr_api()
    except Exception as e:
        print(traceback.print_exception(*sys.exc_info()))