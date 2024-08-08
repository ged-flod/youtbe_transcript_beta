"""
This script generates a cohesive script based on the transcripts of multiple YouTube videos
using the YouTube Transcript API and the GoogleGemini API.

"""

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
# import google.generativeai as genai
from pytube import YouTube


# Streamlit app configuration
st.set_page_config(page_title="YouTube Transcript", page_icon=":video_camera:")

# Page title
st.title("YouTube Transcript")
st.divider()

# User input for YouTube video IDs
st.sidebar.header("Video Youtube :")
video_1_url = st.sidebar.text_input("Tapez l'url de votre video", "https://youtu.be/CBJz0r0mSuk")
# Selectionnez une langue :
all_supported_languages = {"Français": "fr", "Anglais": "en", "Espagnol": "es", "Portugais": "pt"}
language = st.sidebar.selectbox("Choisissez une langue :", list(all_supported_languages.keys()))

# Filter out empty URLs
videos_urls = [url for url in [video_1_url] if url]

# Variable to store the YouTube objects
videos_ids = []


def fetch_youtube_data():
    """
    Fetches YouTube data for the given URLs.
    """
    columns = st.columns(len(videos_urls)) 
    for url in videos_urls:
        if url is not None and url != "":
            yt = YouTube(url)
            videos_ids.append(yt)
    for i, col in enumerate(columns):
        with col:
            st.write(f"Video {i+1}")
            st.image(videos_ids[i].thumbnail_url, )
            st.write(videos_ids[i].title)


# User input for Gemini API key
# api_key = st.sidebar.text_input("Gemini API Key", type="password", value="*******************************")

if st.sidebar.button("Transcrire les vidéos"):
    # Fetch transcripts for all videos
    st.write("Récupération de la vidéo YouTube ...")
    fetch_youtube_data()
    videos = [t.video_id for t in videos_ids]
    st.write(f"{len(videos)} Video")
    try:
        language = all_supported_languages[language]
        videos_transcripts = YouTubeTranscriptApi.get_transcripts(videos, languages=[language])
        videos_transcripts_list = []
        for index, video_id in enumerate(videos):
            videos_transcripts_dict = {"duration": videos_ids[index].length}
            videos_transcripts_dict["video_id"] = video_id
            videos_transcripts_dict["author"] = videos_ids[index].author
            videos_transcripts_dict["title"] = videos_ids[index].title
            videos_transcripts_dict["transcript"] = " ".join([t["text"] for t in videos_transcripts[0][video_id]])
            videos_transcripts_dict["transcript"] = videos_transcripts_dict["transcript"].replace("\n", " ")
            videos_transcripts_list.append(videos_transcripts_dict)
        st.success("Les transcriptions ont été récupérées avec succès !")
        st.json(videos_transcripts_list)
    except Exception as e:
        st.error(f"Erreur lors de la récupération des transcriptions: {e}")
    
    # # Generate prompt template
    # role = "YouTube Script Generator"
    # prompt = """
    # Create an one complete script from all these video transcriptions by synthesizing information from various sources into a single one coherent context by following the following Instructions:
    # """
    # instructions = custom_instructions
    # prompt_template = f"""Your role is: {role}.

    # I have {len(videos_urls)} videos from YouTube, and those are the transcripts:

    # {" ".join([t["transcript"] for t in videos_transcripts_list])}

    # Prompt = {prompt}

    # Instructions = {instructions}
    # """

    # # Configure Gemini API
    # try:
    #     st.write("Generating script...")
    #     genai.configure(api_key=api_key)
    #     # Choose a model
    #     model = genai.GenerativeModel('gemini-1.0-pro-latest')
    #     # Generate content
    #     response = model.generate_content(prompt_template)
    #     st.subheader("Generated Script")
    #     st.write(response.text)
    #     st.subheader("Generated Script Editable")
    #     st.text_area(label="Script", value=response.text, height=500)
    # except Exception as e:
    #     st.error(f"Error generating script: {e}")


