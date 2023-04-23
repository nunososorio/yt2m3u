import streamlit as st

import pytube

import os

import concurrent.futures

# Function to extract video links and titles using pytube

def get_video_info(video_url):

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

        st.warning(f"Error extracting video information for {video_url}: {e}")

        return None, None

# Main function

def main():

    st.title("YouTube Playlist Downloader")

    playlist_url = st.text_input("Enter YouTube playlist URL:")

    if not playlist_url:

        st.warning("Please enter a playlist URL.")

        return

    st.write("Extracting video information...")

    with concurrent.futures.ThreadPoolExecutor() as executor:

        # Use a list comprehension to store the video information

        playlist = [info for info in executor.map(get_video_info, pytube.Playlist(playlist_url).video_urls)]

    download_links = []

    for video_title, video_url in playlist:

        if video_title and video_url:

            download_links.append(video_url)

            st.write(f"Video title: {video_title}")

            st.write(f"Video URL: {video_url}")

        else:

            st.warning("Could not extract information for one or more videos in the playlist.")

    if download_links:

        st.write(f"Total videos to download: {len(download_links)}")

        st.write("Download links:")

        m3u_file = "#EXTM3U\n"

        for i, download_link in enumerate(download_links):

            m3u_file += f"#EXTINF:0,{playlist[i][0]}\n{download_link}\n"

        st.code(m3u_file, language='m3u')
