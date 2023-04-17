import streamlit as st
from pytube import Playlist
from concurrent.futures import ThreadPoolExecutor

st.title("yt2m3u - YouTube Playlist to m3u Downloader")

# Get the playlist URL from the user
playlist_url = st.text_input("Enter YouTube playlist URL:", value="https://m.youtube.com/playlist?list=PL-gWsve6MojDIwDIhpxhMlqEn3dKz8f9a")

if playlist_url:
    playlist = Playlist(playlist_url)
    m3u_content = "#EXTM3U\n"

    # Define a function to get the video stream for a given video
    def get_video_stream(video):
        # Try to get the video stream, and handle any errors that might occur
        try:
            video_stream = video.streams.filter(progressive=True).order_by("resolution").desc().first()
            video_url = video_stream.url
            return f"#EXTINF:-1,{video.title}\n{video_url}\n"
        except KeyError:
            st.warning(f"No streaming data available for video: {video.title}")
        except Exception as e:
            st.error(f"Error processing video {video.title}: {e}")

    # Use a thread pool to download video streams concurrently
    with ThreadPoolExecutor() as executor:
        # Try to get the video stream for each video in the playlist, and handle any errors that might occur
        try:
            m3u_content += "".join(executor.map(get_video_stream, playlist.videos))
        except Exception as e:
            st.error(f"Error processing playlist: {e}")

    # Add a download button for the m3u file
    st.download_button(label="Download m3u file", data=m3u_content, mime="audio/x-mpegurl", file_name="playlist.m3u")

# Add some usage examples and a disclaimer
st.write("## Potential Use Cases")
st.write("The `yt2m3u` app can be useful in a variety of situations. For example, you could use it to:")
st.write("- Download an m3u file for a YouTube playlist so that you can play the videos in a media player that supports m3u files.")
st.write("## Disclaimer")
st.write("Please note that `yt2m3u` is an experimental app for testing and development purposes only. Use it at your own risk.")
st.write("When using `yt2m3u`, please be aware of copyright issues and YouTube policies. It is your responsibility to ensure that you have the necessary rights and permissions to download and use the content from YouTube playlists.")
