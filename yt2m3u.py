import streamlit as st
from pytube import Playlist

st.title('YouTube Playlist Downloader')

playlist_url = st.text_input('Enter YouTube playlist URL:')

if playlist_url:
    playlist = Playlist(playlist_url)
    m3u_content = '#EXTM3U\n'
    for video in playlist.videos:
        video_stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
        video_url = video_stream.url
        m3u_content += f'#EXTINF:-1,{video.title}\n{video_url}\n'
    st.download_button(label='Download m3u file', data=m3u_content, mime='audio/x-mpegurl', file_name='playlist.m3u')