import concurrent.futures
import streamlit as st
from pytube import Playlist, YouTube

st.title("yt2m3u - YouTube Playlist to m3u")

# Input the YouTube playlist URL
channel_url = st.text_input("Enter the YouTube playlist URL:", value="https://m.youtube.com/playlist?list=PLPQsMfVniUSoKIvSuQhaSD8XM56tk9Xar")

if channel_url:
    # Create a Playlist object
    playlistx = Playlist(channel_url)
    # Create a list of video objects from the playlist URLs
    with concurrent.futures.ThreadPoolExecutor() as executor:
        videos = list(executor.map(YouTube, playlistx))
    # Create a list of video download URLs
    video_urls = [video.streams.get_highest_resolution().url for video in videos]
    # Write the video download URLs to a local m3u playlist file named dytchan2.m3u
    with open("dytchan2.m3u", "w") as f:
        f.write("#EXTM3U\n")
        for url in video_urls:
            f.write(f"#EXTINF:-1,{url}\n{url}\n")
    st.success("Playlist downloaded successfully!")
    st.markdown("Download the m3u file [here](dytchan2.m3u)")