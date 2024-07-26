# YouTube Headline Summary Generator


## Overview
This project automates the process of extracting, summarizing, and presenting news headlines from various Pakistani news channels on YouTube. It fetches the latest videos with "Headline" in the title, extracts their subtitles, summarizes the content, translates it to Urdu, and converts the translation into audio.

## Features
Automated fetching of the latest headline videos from specified YouTube channels.
Extraction and processing of subtitles from the fetched videos.
Summarization of extracted Hindi text.
Translation of summarized text to Urdu.
Conversion of Urdu text to speech.

## Technologies Used
    Selenium
    Streamlit
    youtube_transcript_api
    ChatGPT-API
    gTTS (Google Text-to-Speech)

## Usage

### Run the application:

bash:

    streamlit run app.py

### Interact with the Streamlit interface:

    Click the button to fetch the latest video IDs from the specified YouTube   channels.
    Click the button to fetch subtitles from the videos.
    Click the button to summarize the text.
    Click the button to convert the summary to Urdu.
    Click the button to convert the Urdu summary to audio.

## Your code implementation here

### Contributing
    Fork the repository.
    Create a new branch.
    Make your changes and commit them.
    Push your changes to the branch.
    Create a pull request.
