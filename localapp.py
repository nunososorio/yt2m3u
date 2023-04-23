import streamlit as st
import pytube
import re

# Function to extract video links
def get_video_links(playlist_url):
    playlist = pytube.Playlist(playlist_url)
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    return [f'https://www.youtube.com{video_url}' for video_url in playlist.video_urls]

# Function to write download links to m3u file
def write_to_m3u(video_links, file_path):
    # Clean the m3u file by removing all lines that don't start with #EXTINF:
    with open(file_path, mode='r') as m3u_file:
        lines = m3u_file.readlines()
    with open(file_path, mode='w') as m3u_file:
        for line in lines:
            if line.startswith('#EXTINF:'):
                m3u_file.write(line)
    # Write the new download links to the m3u file in the correct format
    with open(file_path, mode='a') as m3u_file:
        for video_link in video_links:
            m3u_file.write(f'#EXTINF:0,{video_link}\n{video_link}\n')

# Streamlit app
def main():
    st.title("YouTube Playlist Downloader")
    playlist_url = st.text_input("Enter YouTube Playlist URL:")
    if st.button("Download Playlist"):
        st.write("Extracting video links...")
        video_links = get_video_links(playlist_url)
        st.write(f"Found {len(video_links)} videos in the playlist.")
        st.write("Updating download links in m3u file...")
        write_to_m3u(video_links, 'ytplay.m3u')
        st.write("Done!")
