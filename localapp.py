import streamlit as st 
import pytube 

def get_links(playlist_url): 
    links = [] 
    response = requests.get(playlist_url) 
    html = response.text 
  
    for link in re.findall('https://www.youtube.com/watch\?v=(.*?)"', html): 
        video_link = f"https://www.youtube.com/watch?v={link}"
        video = pytube.YouTube(video_link)
        mp4_link = video.streams.first().url 
        title = video.title 
        links.append(f"#EXTINF:-1,{title}\n{mp4_link}\n") 
    return links 

def write_to_m3u(links, filename): 
    with open(filename, 'w') as f: 
        for link in links: 
            f.write(f'{link}') 

url = st.text_input('Enter a YouTube playlist URL') 
st.button('Get Download Links', key='download_links_btn') 
if st.button('Get Download Links', key='download_links_btn'): 
    links = get_links(url) 
    write_to_m3u(links, 'ytplay.m3u') 
    st.success('Download links saved to ytplay.m3u!')

if __name__ == '__main__': 
    main()
