import streamlit as st
from pytube import Playlist

st.title('YouTube Playlist Downloader')

playlist_url = st.text_input('Enter YouTube playlist URL:')

if playlist_url:
    playlist = Playlist(playlist_url)
    m3u_file = open('playlist.m3u', 'w')
    for video in playlist.videos:
        video_url = video.streams.filter(progressive=True).first().url
        m3u_file.write(video_url + '\n')
    m3u_file.close()
    st.download_button(label='Download m3u file', data='playlist.m3u', mime='audio/x-mpegurl')