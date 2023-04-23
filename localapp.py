import streamlit as st
import pytube

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
    playlist = pytube.Playlist(playlist_url)
    with st.spinner(f"Extracting {len(playlist.video_urls)} video URLs..."):
        video_data = [get_video_info(url) for url in playlist.video_urls]

    download_links = []
    for video_title, video_url in video_data:
        if video_title and video_url:
            download_links.append(video_url)
            st.write(f"- {video_title}")

    st.write("\n")
    st.write("To download the videos, copy the following links and paste them into a downloader that supports M3U playlists:")
    m3u_links = "\n".join(download_links)
    st.code(m3u_links, language='text')

if __name__ == '__main__':
    main()
