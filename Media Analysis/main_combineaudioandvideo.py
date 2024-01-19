import cv2
import base64
import requests
from openai import OpenAI
from IPython.display import Audio
from moviepy.editor import VideoFileClip, AudioFileClip

v_path = "samplevideo.mp4"

video = cv2.VideoCapture(v_path)

base64Frames = []

while video.isOpened():
    success, frame = video.read()

    if not success:
        break

    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
video.release()

client = OpenAI(api_key="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")

prompts = [
    {
        "role": "user",
        "content": [
            '''Here are the frames of video, generate a voiceover script for this video.
            Include only narration and no other text or preamble. The length of the voiceover should align with
            the duration of the video which is about 23secs long''',
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50])
        ]
    }
]
parameters = {
    "model": "gpt-4-vision-preview",
    "messages": prompts,
    "max_tokens": 200
}

result = client.chat.completions.create(**parameters)

# print(result.choices[0].message.content.strip())

file = open("video_script.txt", "w")

file.write(result.choices[0].message.content.strip())

file.close()

with open("video_script.txt", "r") as file_read:
    script = file_read.read().rstrip()

# print(script)

api_key = "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"

response = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {api_key}"
    },
    json={
        "model": "tts-1-1106",
        "input": script,
        "voice": "onyx"
    }
)
# print(response)

audio = b""
for chunk in response.iter_content(chunk_size=1024 * 1024):
    audio += chunk

# print(audio)

Audio(audio)

with open("", "wb") as file:
    file.write()

video_clip = VideoFileClip("samplevideo.mp4")
audio_clip = AudioFileClip()
