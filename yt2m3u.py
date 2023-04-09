import streamlit as st
from pytube import Playlist

st.title('yt2m3u - YouTube Playlist to m3u Downloader')

playlist_history = st.session_state.get('playlist_history', [])

playlist_url = st.text_input('Enter YouTube playlist URL:', value='https://m.youtube.com/playlist?list=PL-gWsve6MojDIwDIhpxhMlqEn3dKz8f9a')

if playlist_url:
    playlist_history.append(playlist_url)
    st.session_state['playlist_history'] = playlist_history[-5:]
    
    st.write('Playlist history:')
    for url in playlist_history:
        st.write(url)
    
    playlist = Playlist(playlist_url)
    m3u_content = '#EXTM3U\n'
    for video in playlist.videos:
        video_stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
        video_url = video_stream.url
        m3u_content += f'#EXTINF:-1,{video.title}\n{video_url}\n'
    st.download_button(label='Download m3u file', data=m3u_content, mime='audio/x-mpegurl', file_name='playlist.m3u')