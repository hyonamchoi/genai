from IPython.display import display, Image, Audio  # IPython의 디스플레이와 이미지 및 오디오를 표시하기 위한 모듈을 가져옵니다.
import cv2  # OpenCV 라이브러리를 가져옵니다. 동영상을 읽어오기 위해 사용합니다. (설치 명령: !pip install opencv-python)
import base64  # 이미지 데이터를 base64로 인코딩하고 디코딩하기 위한 모듈을 가져옵니다.
import time  # 시간 지연을 위한 모듈을 가져옵니다.
from openai import OpenAI  # OpenAI API를 사용하기 위한 모듈을 가져옵니다.
import os  # 환경 변수 및 디렉토리 관리를 위한 모듈을 가져옵니다.
import requests  # HTTP 요청을 보내기 위한 모듈을 가져옵니다.

# OpenAI 클라이언트를 초기화합니다.
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

# "tsunami.mp4" 동영상 파일을 읽어옵니다.
video = cv2.VideoCapture("tsunami.mp4")

# 동영상의 각 프레임을 이미지로 변환하고 base64로 인코딩하여 리스트에 저장합니다.
base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

# 동영상을 모두 읽은 후 프레임 수를 출력합니다.
video.release()
print(len(base64Frames), "frames read.")

# IPython 디스플레이를 위한 핸들을 생성합니다.
display_handle = display(None, display_id=True)

# 각 이미지를 IPython 디스플레이에 표시합니다.
#for img in base64Frames:
#    display_output = Image(data=base64.b64decode(img.encode("utf-8")))
#    display_handle = display(display_output, display_id=True)
    ##display_handle.update(Image(data=base64.b64decode(img.encode("utf-8"))))
#    time.sleep(0.025)
       


# 이미지에 대한 음성 오디오 스크립트를 생성합니다.
PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "Create a super-excited Japanese news narrator-style voiceover script that warns the listener about the disaster situation seen in the video so they can be on high alert and evacuate quickly.. He must explain what the current situation is and tell citizens what specific actions to take and what to watch out for. When a disaster situation becomes serious, short and strong warning messages must be shouted several times. Use caps and exclamation marks where necessary to convey excitement. Include only narration, and output must be in English.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::60]),
        ],
    },
]
params = {
    "model": "gpt-4-vision-preview",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)

# 생성된 오디오 스크립트를 OpenAI TTS 모델을 사용하여 음성으로 변환합니다.
response = requests.post(
    "https://api.openai.com/v1/audio/speech",
    headers={
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    },
    json={
        "model": "tts-1-1106",
        "input": result.choices[0].message.content,
        "voice": "nova",
    },
)

# 음성 오디오 데이터를 가져와서 출력합니다.
audio = b""
for chunk in response.iter_content(chunk_size=1024 * 1024):
    audio += chunk
Audio(audio)

# Now, write the `audio` bytes to an MP3 file
with open('output.mp3', 'wb') as file:
    file.write(audio)

print("The MP3 file has been saved locally as 'output.mp3'.")
