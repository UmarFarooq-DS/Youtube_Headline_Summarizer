# # Code to generate seperate subtitles text files for each latest headline video

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from youtube_transcript_api import YouTubeTranscriptApi
# import re
# import time

# def fetch_headline_video_id(channel_url):
#     print(f"Initializing WebDriver for channel: {channel_url}")
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#     wait = WebDriverWait(driver, 15)
    
#     try:
#         print(f"Opening YouTube channel: {channel_url}")
#         driver.get(channel_url)
#         time.sleep(5)  # Wait for the page to load

#         print("Finding video elements")
#         """
#             <div id="video-title">Breaking News: Event A</div>
#             <div id="video-title">Headline: Major Update</div>
#             <div id="video-title">Headline: Important Announcement</div>
#         """
#         videos = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="video-title"]')))
#         print(videos)
        
#         for video in videos:
#             print(f"Checking video title: {video.text}")
#             if "Headline" in video.text:
#                 parent_element = video.find_element(By.XPATH, '..')
#                 video_url = parent_element.get_attribute('href')
                
#                 if video_url:
#                     fetched_video_id = video_url.split('v=')[-1].split('&')[0]
#                     print(f"Found 'Headline' video: {video_url}")
#                     print(f"Video ID: {fetched_video_id}")
#                     return fetched_video_id, video_url
#                 else:
#                     print("Could not fetch video URL from the parent element")
#                     return None, None
        
#         print("No video with 'Headline' in the title found")
#         return None, None

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None, None

#     finally:
#         print("Closing WebDriver")
#         driver.quit()

# def fetch_and_process_subtitles(video_id, file_name):
#     try:
#         print(f"Fetching subtitles for video ID: {video_id}")
#         transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
        
#         words = []
#         for entry in transcript:
#             words.extend(entry['text'].split())
        
#         print("Filtering Hindi words")
#         hindi_words = [word for word in words if re.match(r'[\u0900-\u097F]', word)]
        
#         print(f"Saving subtitles to {file_name}")
#         with open(file_name, 'w', encoding='utf-8') as file:
#             file.write(' '.join(hindi_words))
        
#         print(f"Replacing newlines with spaces in {file_name}")
#         with open(file_name, 'r', encoding='utf-8') as file:
#             content = file.read()
        
#         cleaned_content = content.replace('\n', ' ')
        
#         with open(file_name, 'w', encoding='utf-8') as file:
#             file.write(cleaned_content)
        
#         print(f"Newlines replaced with spaces in {file_name}")
#     except Exception as e:
#         print(f"Could not fetch subtitles for video {video_id}: {e}")

# # List of channel URLs
# channel_urls = [
#     'https://www.youtube.com/@Samaatv/videos',
#     'https://www.youtube.com/@ArynewsTvofficial/videos',
#     'https://www.youtube.com/@geonews/videos',
#     'https://www.youtube.com/@DunyanewsOfficial/videos',
#     'https://www.youtube.com/@24NewsHD/videos',
#     'https://www.youtube.com/@92newshdTv/videos'
#     # Add more channel URLs as needed
# ]

# for channel_url in channel_urls:
#     print(f"Processing channel: {channel_url}")
#     fetched_video_id, video_url = fetch_headline_video_id(channel_url)
#     if fetched_video_id:
#         channel_name = channel_url.split('@')[1].split('/')[0]
#         file_name = f"{channel_name}_subtitles.txt"
#         fetch_and_process_subtitles(fetched_video_id, file_name)
#         print(f"Hindi words saved to {file_name}")
#     else:
#         print(f"Failed to fetch video ID for channel: {channel_url}")

# print("Processing complete")




# code for sending message to whatsapp





from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the WebDriver using ChromeDriverManager to automatically manage the driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')

# Wait for user to scan the QR code
input("Press Enter after scanning QR code")

# The phone number of the recipient (include country code without '+' e.g., '919876543210' for India)
phone_number = '923014730287'  # Replace with your friend's phone number

# Open the chat with the specified phone number
driver.get(f'https://web.whatsapp.com/send?phone={phone_number}')

# Wait for the chat to load
time.sleep(10)  # Adjust this time as necessary based on your internet speed

# Message to be sent
message = "Hello Api Humra, Hareem this side."

# Locate the message input box
input_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')

# Send the message 5 times
for _ in range(5):
    input_box.send_keys(message)
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)  # Adding a delay between messages

# Close the WebDriver
driver.quit()
