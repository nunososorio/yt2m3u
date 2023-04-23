import importlib
import streamlit as st
import concurrent.futures

# Function to extract video links and titles using the appropriate downloader module
def get_video_info(video_url, downloader_module):
    try:
        if downloader_module == pytube:
            video = downloader_module.YouTube(video_url)
            video_title = video.title
            video_streams = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            if video_streams:
                video_url = video_streams[0].url
            else:
                video_url = None
        elif downloader_module == pafy:
            video = downloader_module.new(video_url)
            video_title = video.title
            video_url = video.getbest().url
        elif downloader_module == youtube_dl:
            video = downloader_module.YoutubeDL().extract_info(video_url, download=False)
            video_title = video['title']
            video_url = video['url']
        elif downloader_module == yt_dlp:
            video = downloader_module.YoutubeDL().extract_info(video_url, download=False)
            video_title = video['title']
            video_url = video['url']
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

    downloader_choice = st.selectbox("Select a downloader:", ("pafy", "youtube_dl", "pytube", "yt_dlp"))

    try:
        downloader_module = importlib.import_module(downloader_choice)
    except ImportError:
        st.warning("Invalid downloader choice.")
        return

    st.write("Extracting video information...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use a list comprehension to store the video information
        if downloader_choice == "pafy":
            playlist = [info for info in executor.map(lambda url: get_video_info(url, downloader_module), pafy.get_playlist(playlist_url).items)]
        elif downloader_choice == "youtube_dl" or downloader_choice == "yt_dlp":
            playlist = [info for info in executor.map(lambda url: get_video_info(url, downloader_module), [playlist_url])]
        else:
            playlist = [info for info in executor.map(lambda url: get_video_info(url, downloader_module), downloader_module.Playlist(playlist_url).video_urls)]

    download_links = []
    for video_title, video_url in playlist:
        if video_title and video_url:
            download_links.append(video_url)
            st.write(f"Video title: {video_title}")
            st.write(f"Video URL: {video_url}")
            st.write("")

    if download_links:
        st.write("To download the videos:")
        for download_link in download_links:
            st.write(download_link)

if __name__ == "__main__":
    main()
