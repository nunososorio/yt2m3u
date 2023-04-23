import streamlit as st
import pytube
import re
import os

# Function to extract video links
def get_video_links(playlist_url):
    try:
        playlist = pytube.Playlist(playlist_url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        return [f'https://www.youtube.com{video_url}' for video_url in playlist.video_urls]
    except Exception as e:
        st.error(f"Error extracting video links: {e}")
        return []

# Function to write download links to m3u file
def write_to_m3u(video_links, file_path):
    try:
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
    except Exception as e:
        st.error(f"Error writing download links to m3u file: {e}")

# Streamlit app
def main():
    st.title("YouTube Playlist Downloader")
    playlist_url = st.text_input("Enter YouTube Playlist URL:")
    file_path = os.path.join(os.path.dirname(__file__), 'ytplay.m3u')
    if st.button("Download Playlist"):
        st.write("Extracting video links...")
        video_links = get_video_links(playlist_url)
        if not video_links:
            st.warning("No video links found.")
            return
        st.write(f"Found {len(video_links)} videos in the playlist.")
        st.write("Updating download links in m3u file...")
        write_to_m3u(video_links, file_path)
        with open(file_path, mode='r') as m3u_file:
            m3u_file_contents = m3u_file.read()
        st.code(m3u_file_contents, language='m3u')
        st.download_button(
            label="Download ytplay.m3u",
            data=m3u_file_contents,
            file_name="ytplay.m3u",
            mime="audio/mpegurl"
        )

if __name__ == '__main__':
    main()
