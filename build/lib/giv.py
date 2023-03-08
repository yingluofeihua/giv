# @Time : 2023/3/7 1:21
# @Author : Administrator
# @File : test.py
# @Software: PyCharm

import json
import time

import openai
import requests
from gtts import gTTS

import config
import argparse

did_api_key = config.did_api_key


def answer_gpt35():
    openai.api_key = config.openai.api_key
    prompt = config.gpt_problem
    # 访问OpenAI接口
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    # 3.返回
    return response.choices[0].message.content


def generate_image():
    response = openai.Image.create(
        prompt=config.image_description,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']

    response = requests.get(image_url)

    # 保存图片到本地
    with open('image.jpg', 'wb') as f:
        f.write(response.content)

    print('图片下载完成')
    return image_url


def synthetic_audio():
    text = answer_gpt35()
    tts = gTTS(text, lang='en')
    tts.save("synthetic_audio.mp3")


def did_id():
    headers = {
        'accept': 'application/json',
        # Already added when you pass json=
        # 'Content-Type': 'application/json',
        # 'Authorization': 'Basic WTI5bVpXbEFZMmhsYm5wb1pXNW9kV0V1ZUhsNjp4OXZRcU1UTTUtNWFhUS1lMGxVc1Y=',
        'Authorization': did_api_key,
    }

    json_data = {
        "source_url": "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/ben.jpg",
        "driver_url": "bank://classics/driver-feliz-navidad",
        "config": {"mute": False}
    }
    response = requests.post('https://api.d-id.com/animations', headers=headers, json=json_data)

    res_id = json.loads(response.text)['id']
    return res_id


def did_result():
    headers = {
        'Authorization': did_api_key,
    }

    url = 'https://api.d-id.com/animations/' + did_id()
    i = 1
    while True:
        try:
            time.sleep(5)
            response = requests.get(url, headers=headers)
            result_url = json.loads(response.text)['result_url']
            print('视频生成完成，等待下载。')
            break

        except(KeyError):
            print("第" + str(i) + "次无结果，正在继续...")
            i = i + 1
    return result_url


def did_video():
    url = did_result()
    response = requests.get(url, stream=True)
    with open('did_video.mp4', 'wb') as f:
        f.write(response.content)

def generative():
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, default='video', help='video or image')
    args = parser.parse_args()
    if args.type == 'video':
        did_video()
    elif args.type == 'image':
        url = generate_image()
        print(url)
    elif args.type == 'audio':
        synthetic_audio()
    elif args.type == 'chatgpt':
        text = answer_gpt35()
        print(text)
    else:
        raise ValueError('type must be video or image')


if __name__ == '__main__':
    generative()
