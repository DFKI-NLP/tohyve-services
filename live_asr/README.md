# DFKI ASR (Need to update it!)
It's a tool to extract audio from a video clip than transfrom that audio into text. Later, translate that transformed text into English and German. Afterwards add those translated English and German text as a caption of the inserted video clip. Finally, return the video with translated caption. In audio extraction it uses **moviepy** technology. For text transformation it uses OpenAI's **Wispher**. 

## Installing Using Docker:
* To Pull it: 
```
docker pull akhyarahmed/dfkinludocker:asr_1.1.0
```
* To Run it: 
```
docker run --rm -it -p 8000:8000/tcp akhyarahmed/dfkinludocker:asr_1.1.0
```
## Installing in Local Environment:
### Pre-requsites:
* python 3.8 or above
* pip 22
* create a python/conda environment and install requirements.txt using pip using 
```
pip install -r requirements.txt
```
* then go to:
```
cd dfki_asr
```
* downlaod ffmpeg from https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z
* than  unzip it and set new environment path using cmd
```
setx PATH "<path of unzipped ffmpeg>;%PATH%"
``` 

### To start the API:
```
python3 -m main
```
## To interact with the API:
* Interactive mode: http://localhost:8000/docs/
* Curl-call: http://localhost:8000/translator/?src_text=your_text&tr_ln=target_language_code

## Input Constraints: 
* Each sentence length <= 120 
* Each text length can be > 0 words
* Each text can have multiple sentences!

## Sample Input (Using FAST-API's Interface)
https://user-images.githubusercontent.com/26096858/203446538-9ad777fb-df7b-49e0-8cb7-60d44916b00b.mp4


https://user-images.githubusercontent.com/26096858/203446632-8da4a189-de35-4511-9faf-2a1457df8157.mp4


* Upload a video from asr/uploadfile/
![image](https://user-images.githubusercontent.com/26096858/213194526-0812bfe8-5b5e-42a9-8593-edbb19de4cac.png)
* Go to asr/transform/. It extract all speech and then translate it into english (You have to set is_english to 1 to get translated speech in the caption. If you set is_english to 0 than it will not translate it into english). Later it going to add that translated text into that video as a caption.
![image](https://user-images.githubusercontent.com/26096858/213205409-f402bba2-16bd-49ce-bbc0-1482eb4323e4.png)
* Download the translated video with caption from asr/video/
![image](https://user-images.githubusercontent.com/26096858/213205025-82977fce-ece4-466e-9b04-188b2f668132.png)

* To download only extracted audio please go to asr/audio/
![image](https://user-images.githubusercontent.com/26096858/213207529-6180a11a-e64d-4c3b-8072-c5c6cfaba2c2.png)

## Sample Output:
* sample_video.mp4 output
```yaml
{
  "download_audio": "http://localhost:8000/asr/audio/",
  "download_subtitled_video": "http://localhost:8000/asr/video/",
  "extracted_text": "Hello, this is a video in which we would like to demonstrate the automatic transcription of audio.",
  "execution_time": 81.89
}
```
https://user-images.githubusercontent.com/26096858/213205892-af8f282a-41b7-43d1-97ee-a5d67a26f45d.mp4
* sample_video_1.mp4 output
```yaml
{
  "download_audio": "http://localhost:8000/asr/audio/",
  "download_subtitled_video": "http://localhost:8000/asr/video/",
  "extracted_text": "Hi everyone this is a sample video for ASR",
  "execution_time": 29.43
}
```


https://user-images.githubusercontent.com/26096858/213207098-719a8b11-2dce-4433-8e42-d0ecbd611f14.mp4

