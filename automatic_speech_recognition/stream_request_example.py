import requests
import json

# url = "https://dfki-3109.dfki.de/asr/web-stream"
url = "http://localhost:8001/asr/web-stream"
params = {
    "url": "https://st01.sslstream.dlf.de/dlf/01/128/mp3/stream.mp3?aggregator=web",
    "source_language": "de"
}

response = requests.get(url, params=params, stream=True)
responses_ls = []
if response.status_code == 200:
    print("Response received successfully!")
    if response.iter_content():
        for i, line in enumerate(response.iter_lines()):
            if line:
                response_str = line.decode('utf-8')
                if "}{" in response_str:
                    responses_ls.append(response_str[0])
                    responses_str = " ".join(responses_ls)
                    full_response = json.dumps(json.loads(responses_str), indent=4)
                    print(full_response)
                    responses_ls = []
                    responses_ls.append(response_str[1])
                else:
                    responses_ls.append(response_str)
    else:
        print("No content received from the server.")
else:
    print(f"Request failed with status code {response.status_code}")


