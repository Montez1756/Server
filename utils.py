from yt_dlp import YoutubeDL

ydl_opts = {
    "restrictfilenames": True,             # avoid special characters in filenames
    "outtmpl": "./ytdlp/%(extractor)s_%(id)s.%(ext)s",# save to ./ytdlp/ with video title
    "format": "best/bestvideo+bestaudio",  # best quality video+audio
    "merge_output_format": "mp4",          # merge into mp4 when possible
    "cookiefile":"cookies.txt"
}

def download_url(url):
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info["requested_downloads"][0].get("filename")
