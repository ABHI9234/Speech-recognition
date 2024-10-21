import requests
from API_code import API_KEY_ASSEMBLYAI

# Upload and transcript endpoints
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {'authorization': API_KEY_ASSEMBLYAI}

def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(upload_endpoint,
                                     headers=headers,
                                     data=read_file(filename))

    audio_url = upload_response.json().get('upload_url')
    return audio_url

def transcribe(audio_url):
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    job_id = transcript_response.json().get('id')
    return job_id

# Define the filename
filename = "/Users/abhinavtadiparthi/Desktop/PYTHON AI ML/Audio Proccessing Basics/output.wav"

# Upload and get audio_url first
audio_url = upload(filename)  # Move this line here

# Now, call transcribe with the correct audio_url
transcript_id = transcribe(audio_url)  # This now uses audio_url
print(f"Transcription Job ID: {transcript_id}")

# Polling function
def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

# Function to get the transcription result
def get_transcription_result_url(transcript_id):
    while True:
        data = poll(transcript_id)  # Use the existing poll function
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        

def save_transcript(audio_url):
    data, error = get_transcription_result_url(transcript_id)  

    if data:
        text_filename = filename + ".txt"
        with open(text_filename,"w") as f:
            f.write(data['text'])
        print("transcription saved!")
    elif error:
        print("Error!",error)

audio_url = upload(filename)
save_transcript(audio_url)