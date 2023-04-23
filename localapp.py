import streamlit as st
import pytube
import pafy
import os
import concurrent.futures

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

# Function to extract video links and titles using pafy
def get_video_info_pafy(video_url):
    try:
        video = pafy.new(video_url)
        video_title = video.title
        video_streams = video.streams
        best_video = video.getbestvideo(preftype="mp4")
        best_audio = video.getbestaudio(preftype="m4a")
        video_url = f"{best_video.url}+{best_audio.url}"
        return video_title, video_url
    except Exception as e:
        st.warning(f"Error extracting video info for {video_url} using pafy: {e}")
        return None, None

# Function to extract video links and titles
def get_video_info(video_url):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        pytube_future = executor.submit(get_video_info_pytube, video_url)
        pafy_future = executor.submit(get_video_info_pafy, video_url)
        
        pytube_result = pytube_future.result()
        pafy_result = pafy_future.result()
        
        if pytube_result[0] or not pafy_result[0]:
            return pytube_result
        else:
            return pafy_result

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
        st.text_area("Download Links:", value=m3u_file_contents, height=500)
        st.success("Download links have been updated in the m3u file.")

if __name__ == '__main__':
    app()
