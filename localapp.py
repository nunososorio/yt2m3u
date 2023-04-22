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

    # Clean the content of the existing file
    with open('ytplay.m3u', 'r') as f:
        content = f.read().strip()

    # Replace the content of the file with the new playlist
    with open('ytplay.m3u', 'w') as f:
        f.write(m3u_content)

    # Display a success message to the user
    st.success("Playlist successfully downloaded!")
