import streamlit as st
from pytube import Playlist
from concurrent.futures import ThreadPoolExecutor

st.title('yt2m3u - YouTube Playlist to m3u Downloader')

playlist_url = st.text_input('Enter YouTube playlist URL:', value='https://m.youtube.com/playlist?list=PL-gWsve6MojDIwDIhpxhMlqEn3dKz8f9a')

if playlist_url:
    playlist = Playlist(playlist_url)
    m3u_content = '#EXTM3U\n'

    def get_video_stream(video):
        video_stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
        video_url = video_stream.url
        return f'#EXTINF:-1,{video.title}\n{video_url}\n'

    with ThreadPoolExecutor() as executor:
        m3u_content += ''.join(executor.map(get_video_stream, playlist.videos))

    st.download_button(label='Download m3u file', data=m3u_content, mime='audio/x-mpegurl', file_name='playlist.m3u')