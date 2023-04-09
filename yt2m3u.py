import streamlit as st
from pytube import Playlist

st.title("yt2m3u - YouTube Playlist to m3u")

# Input the YouTube playlist URL
channel_url = st.text_input("Enter the YouTube playlist URL:", value="https://m.youtube.com/playlist?list=PLPQsMfVniUSoKIvSuQhaSD8XM56tk9Xar")

if channel_url:
    # Create a Playlist object
    playlistx = Playlist(channel_url)
    print(playlistx.video_urls)  # Debugging line
    # Create a list of video download URLs
    video_urls = [video.streams.get_highest_resolution().url for video in playlistx]
    # Write the video download URLs to a local m3u playlist file named dytchan2.m3u
    with open("pages/dytchan2.m3u", "w") as f:
        f.write("#EXTM3U\n")
        for url in video_urls:
            f.write(f"#EXTINF:-1,{url}\n{url}\n")
    st.success("Playlist downloaded successfully!")
    
    # Create a download button for the m3u file
    with open("pages/dytchan2.m3u", "r") as f:
        file_contents = f.read()
        st.download_button(label="Download m3u file", data=file_contents, file_name="dytchan2.m3u", mime="audio/x-mpegurl")