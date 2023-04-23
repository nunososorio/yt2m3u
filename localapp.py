import streamlit as st
import pytube
import youtube_dl
import os

# Function to extract video links and titles using pytube
def get_video_info_pytube(video_url):
    try:
        video = pytube.YouTube(video_url)
        video_title = video.title
        video_streams = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        if video_streams:
            video_url = video_streams[0].url
        else:
            video_url = None
        return video_title, video_url
    except Exception as e:
        st.warning(f"Error extracting video info for {video_url} using pytube: {e}")
        return None, None

# Function to extract video links and titles using youtube_dl
def get_video_info_youtube_dl(video_url):
    try:
        ydl_opts = {
            'outtmpl': '%(id)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_url, download=False)
            video_title = video_info.get('title', 'Unknown Title')
            video_url = ydl.prepare_filename(video_info)
            return video_title, video_url
    except Exception as e:
        st.warning(f"Error extracting video info for {video_url} using youtube_dl: {e}")
        return None, None

# Function to extract video links and titles
def get_video_info(video_url):
    video_title, video_url = get_video_info_pytube(video_url)
    if not video_url:
        video_title, video_url = get_video_info_youtube_dl(video_url)
    if not video_title:
        video_title = 'Unknown Title'
    return video_title, video_url

# Function to extract video links and titles for a playlist
def get_playlist_info(playlist_url):
    try:
        playlist = pytube.Playlist(playlist_url)
        video_links = []
        for video_url in playlist.video_urls:
            video_title, video_url = get_video_info(video_url)
            if video_url:
                video_links.append((video_title, video_url))
        return video_links
    except Exception as e:
        st.error(f"Error extracting video links: {e}")
        return []

# Function to write download links to m3u file
def write_to_m3u(video_links, file_path):
    try:
        with open(file_path, mode='w', encoding='utf-8') as m3u_file:
            for video_title, video_url in video_links:
                m3u_file.write(f'#EXTINF:0,{video_title}\n{video_url}\n')
    except Exception as e:
        st.error(f"Error writing download links to m3u file: {e}")

# Streamlit app
def app():
    st.set_page_config(page_title="YouTube Playlist Downloader", page_icon=":tv:", layout="wide")
    st.title("YouTube Playlist Downloader")

    playlist_url = st.text_input("Enter YouTube Playlist URL:")
    file_path = os.path.join(os.path.dirname(__file__), 'ytplay.m3u')

    if st.button("Download Playlist"):
        st.write("Extracting video links and titles...")
        video_links = get_playlist_info(playlist_url)
        if not video_links:
            st.warning("No videos found in the playlist.")
            return
        st.write(f"Found {len(video_links)} videos in the playlist.")
        st.write("Updating download links in m3u file...")
        write_to_m3u(video_links, file_path)
        with open(file_path, mode='r', encoding='utf-8') as m3u_file:
            m3u_file_contents = m3u_file.read()
        st.code(m3u_file_contents, language='m3u')
        st.download_button(
            label="Download ytplay.m3u",
            data=m3u_file_contents,
            file_name="ytplay.m3u",
            mime="audio/mpegurl"
        )

if __name__ == '__main__':
    app()
