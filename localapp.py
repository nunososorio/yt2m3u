import streamlit as st

from pytube import Playlist

from concurrent.futures import ThreadPoolExecutor

st.title("yt2m3u - YouTube Playlist to m3u Downloader")

# Get the playlist URL from the user

playlist_url = st.text_input("Enter YouTube playlist URL:", value="https://m.youtube.com/playlist?list=PL-gWsve6MojDIwDIhpxhMlqEn3dKz8f9a") 

if playlist_url:

    try: 

        playlist = Playlist(playlist_url)

    except KeyError:

        st.error("Invalid playlist URL")

# Write m3u file to disk    

with open("ytplay.m3u", "w") as f:

    f.write("#EXTM3U\n")

progress_bar = st.progress(0)  

with ThreadPoolExecutor() as executor:

    for i, video in enumerate(playlist.videos):     

        # Update progress bar

        progress_bar.progress((i+1)/len(playlist.videos))

        

        # Get video stream 

        try:  

            video_stream = video.streams.filter(progressive=True).order_by("resolution").desc().first()

            video_url = video_stream.url

            with open("ytplay.m3u", "a") as f:

                f.write(f"#EXTINF:-1,{video.title}\n{video_url}\n")

        except KeyError:  

            st.warning(f"No streaming data available for video: {video.title}") 

        except yt.exceptions.VideoPrivate:

            st.warning(f"Video {video.title} is private")

        except yt.exceptions.VideoDeleted:

            st.warning(f"Video {video.title} has been deleted")
