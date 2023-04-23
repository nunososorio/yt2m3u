import streamlit as st
import pytube
import pafy
import os
import concurrent.futures
import asyncio
import aiohttp

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
        st.warning(f"Error extracting video information for {video_url}: {e}")
        return None, None

# Function to extract video links and titles using pafy
def get_video_info_pafy(video_url):
    try:
        video = pafy.new(video_url)
        video_title = video.title
        video_best = video.getbest(preftype="mp4")
        video_url = video_best.url
        return video_title, video_url
    except Exception as e:
        st.warning(f"Error extracting video information for {video_url}: {e}")
        return None, None

# Function to download a video using aiohttp
async def download_video(session, video_url, video_title):
    try:
        async with session.get(video_url) as response:
            with open(video_title, 'wb') as f:
                f.write(await response.read())
    except Exception as e:
        st.warning(f"Error downloading {video_url}: {e}")

# Main function
def main():
    st.title("YouTube Playlist Downloader")
    playlist_url = st.text_input("Enter YouTube playlist URL:")
    if not playlist_url:
        st.warning("Please enter a playlist URL.")
        return

    st.write("Extracting video information...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if "youtube.com" in playlist_url:
            get_video_info_func = get_video_info_pytube
        else:
            get_video_info_func = get_video_info_pafy

        with st.spinner("Extracting video information..."):
            playlist = executor.map(get_video_info_func, pytube.Playlist(playlist_url).video_urls)

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

        st.write("Downloading videos...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        with aiohttp.ClientSession(loop=loop) as session:
            tasks = [download_video(session, video_url, f"{i}.mp4") for i, video_url in enumerate(download_links)]
            loop.run_until_complete(asyncio.gather(*tasks))

        st.write("Writing download links to file...")
        with open('ytplay.m3u', 'w') as f:
            f.write('#EXTM3U\n')
            for i, video_url in enumerate(download_links):
                f.write(f'#EXTINF:0,{i}\n')
                f.write(f'{i}.mp4\n')

        st.success("Download complete!")
        if st.button("Download ytplay.m3u"):
            with open('ytplay.m3u', 'r') as f:
                contents = f.read()
            return st.download_button(
                label="Download playlist file",
                data=contents,
                file_name="ytplay.m3u",
                mime='audio/x-mpegurl'
            )

        if st.button("Download video files as zip"):
            zip_file_name = 'ytplay.zip'
            with st.spinner(f"Creating {zip_file_name}..."):
                os.system(f"zip -r {zip_file_name} ./*.mp4")
            st.success(f"{zip_file_name} created!")
            return st.download_button(
                label="Download videos",
                data=zip_file_name,
                file_name=zip_file_name,
                mime='application/zip'
            )

if __name__ == '__main__':
    main()
