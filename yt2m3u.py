import streamlit as st
from pytube import Playlist

st.title('YouTube Playlist Downloader')

playlist_url = st.text_input('Enter YouTube playlist URL:')

if playlist_url:
    playlist = Playlist(playlist_url)
    m3u_content = ''
    for video in playlist.videos:
        video_url = video.streams.filter(progressive=True).first().url
        m3u_content += video_url + '\n'
    st.download_button(label='Download m3u file', data=m3u_content, mime='audio/x-mpegurl', file_name='playlist.m3u')