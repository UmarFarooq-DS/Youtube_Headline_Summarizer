import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from youtube_transcript_api import YouTubeTranscriptApi 
import re
import time
import os
import requests
from gtts import gTTS

# Set API key and endpoint
api_key = "sk-proj-qSRWqGrxyJbfp3L0PSq2T3BlbkFJmhUPTUwNDQlXFTswfgWx"
api_url = "https://api.openai.com/v1/chat/completions"

def fetch_headline_video_id(channel_url):
    print(f"Fetching headline video ID for channel: {channel_url}")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get(channel_url)
        print("Page loaded")
        time.sleep(5)  # Wait for the page to load

        videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="video-title"]')))
        print(f"Found {len(videos)} videos")

        for video in videos:
            if "Headline" in video.text:
                print(f"Found headline video: {video.text}")
                parent_element = video.find_element(By.XPATH, '..')
                video_url = parent_element.get_attribute('href')
                
                if video_url:
                    fetched_video_id = video_url.split('v=')[-1].split('&')[0]
                    print(f"Video URL: {video_url}, Video ID: {fetched_video_id}")
                    driver.quit()
                    return fetched_video_id, video_url
        
        print("No headline video found")
        driver.quit()
        return None, None

    except Exception as e:
        print(f"Error fetching video ID: {e}")
        driver.quit()
        return None, None

def fetch_and_process_subtitles(video_id, file_name):
    print(f"Fetching and processing subtitles for video ID: {video_id}")
    try:
        # transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
        a = st.text_input("Enter your video id: ")
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
        print("Transcript fetched")

        words = []
        for entry in transcript:
            words.extend(entry['text'].split())
        
        hindi_words = [word for word in words if re.match(r'[\u0900-\u097F]', word)]
        print(f"Extracted {len(hindi_words)} Hindi words")

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(' '.join(hindi_words))
        print(f"Hindi words saved to {file_name}")
        
        with open(file_name, 'r', encoding='utf-8') as file:
            content = file.read()
        
        cleaned_content = content.replace('\n', ' ')
        
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
        print(f"Cleaned content saved to {file_name}")

    except Exception as e:
        st.error(f"Could not fetch subtitles for video {video_id}: {e}")
        print(f"Error fetching subtitles: {e}")

def summarize_text():
    print("Summarizing text from all text files")
    model = "gpt-4-turbo"
    prompt = "समीक्षा करें: निम्नलिखित पाठ्य सामग्री का सारांश 800-900 शब्दों में लिखें।"
    
    combined_text = ""
    for filename in os.listdir():
        if filename.endswith(".txt") and not filename.startswith("summary"):
            with open(filename, "r", encoding="utf-8") as file:
                combined_text += file.read() + " "
    print("Combined text fetched from all files")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": combined_text}
        ]
    }

    response = requests.post(api_url, headers=headers, json=data)
    response_json = response.json()
    print("Received response from API")

    summary = response_json["choices"][0]["message"]["content"]

    with open("summary.txt", "w", encoding="utf-8") as file:
        file.write(summary)
    print("Summary saved to summary.txt")

def convert_summary_to_urdu():
    print("Converting summary to Urdu")
    model = "gpt-4-turbo"
    prompt = "براہ کرم مندرجہ ذیل ہندی مواد کا اردو میں ترجمہ کریں:"
    
    with open("summary.txt", "r", encoding="utf-8") as file:
        hindi_summary = file.read()
    print("Fetched Hindi summary")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": hindi_summary}
        ]
    }

    response = requests.post(api_url, headers=headers, json=data)
    response_json = response.json()
    print("Received response from API")

    urdu_summary = response_json["choices"][0]["message"]["content"]

    with open("summary_urdu.txt", "w", encoding="utf-8") as file:
        file.write(urdu_summary)
    print("Urdu summary saved to summary_urdu.txt")
    
    return urdu_summary

def convert_urdu_summary_to_audio():
    print("Converting Urdu summary to audio")
    input_file_path = "summary_urdu.txt"
    output_audio_path = "urdu_audio.mp3"

    with open(input_file_path, 'r', encoding='utf-8') as file:
        urdu_text = file.read()
    print("Fetched Urdu summary")

    tts = gTTS(text=urdu_text, lang='ur', slow=False)
    tts.save(output_audio_path)
    print("Audio saved to urdu_audio.mp3")

    return output_audio_path

channel_urls = [
    'https://www.youtube.com/@Samaatv/videos',
    'https://www.youtube.com/@DunyanewsOfficial/videos',
    'https://www.youtube.com/@24NewsHD/videos'
]

# Streamlit interface)
st.title('YouTube Headline Summary Generator')

if st.button('Fetch Latest Video IDs'):
    video_ids = {}
    for channel_url in channel_urls:
        fetched_video_id, video_url = fetch_headline_video_id(channel_url)
        if fetched_video_id:
            channel_name = channel_url.split('@')[1].split('/')[0]
            video_ids[channel_name] = fetched_video_id
            st.success(f"Fetched video ID for {channel_name}: {fetched_video_id}")
        else:
            st.error(f"Failed to fetch video ID for channel: {channel_url}")
    
    st.session_state.video_ids = video_ids
    print("Fetched video IDs:", video_ids)

if 'video_ids' in st.session_state:
    if st.button('Fetch Subtitles'):
        for channel_name, video_id in st.session_state.video_ids.items():
            file_name = f"{channel_name}_subtitles.txt"
            fetch_and_process_subtitles(video_id, file_name)
            st.success(f"Hindi words saved to {file_name}")

if st.button('Summarize Text'):
    summarize_text()
    st.success('Summary saved to summary.txt')

if st.button('Convert Summary to Urdu'):
    urdu_summary = convert_summary_to_urdu()
    st.success('Summary converted to Urdu and saved to summary_urdu.txt')
    st.write(urdu_summary)

if st.button('Convert Urdu Summary to Audio'):
    audio_path = convert_urdu_summary_to_audio()
    st.success('Urdu summary converted to audio and saved to urdu_audio.mp3')
    audio_file = open(audio_path, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/mp3')

st.write("Processing complete")
