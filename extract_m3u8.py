import os
import shutil
import requests

# Canlı yayın URL'leri (Mesela Show TV, diğer kanallar)
source_urls = {
    "showtv": "https://www.showtv.com.tr/canli-yayin",
    "nowtv": "https://www.nowtv.com.tr/canli-yayin",
    "tv4": "https://www.tv4.com.tr/canli-yayin",
    "kanal7": "https://www.kanal7.com/canli-izle",
    "showturk": "https://www.showturk.com.tr/canli-yayin/showturk",
    "tvkayseri": "https://www.twitch.tv/kayseri_televizyonu",
    "koytv": "https://www.canlitv.diy/koy-tv",
    "beyaztv": "https://beyaztv.com.tr/canli-yayin",
    # Diğer kanalları ilave edebilirsin
}

stream_folder = "stream"

# Eğer stream klasörü varsa, tam sil
if os.path.exists(stream_folder):
    shutil.rmtree(stream_folder)

# Yeniden stream klasörünü yarat
os.makedirs(stream_folder)

def extract_m3u8(url):
    """
    yt-dlp kullanmadan, m3u8 bağlantısını doğrudan URL'den almak için requests kullanıyoruz. 
    Ancak, daha karmaşık siteler için yt-dlp önerilir.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        
        # Sadece regex ya da aktarışla .m3u8 linki bulunur
        import re
        m3u8_matches = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', text)
        if m3u8_matches:
            return m3u8_matches[0]
        else:
            print(f"{url} sayfasında m3u8 bulunamadı.")
            return None
    except Exception as e:
        print(f"Xəta: {e}")
        return None

def write_multi_variant_m3u8(filename, url):
    """
    multi-variant m3u8 için minimal örnek oluşturmak:
    """
    content = (
        "#EXTM3U\n"
        "#EXT-X-VERSION:3\n"
        f"#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=1280x720\n"
        f"{url}\n"
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    for name, page_url in source_urls.items():
        m3u8_link = extract_m3u8(page_url)
        if m3u8_link:
            file_path = os.path.join(stream_folder, f"{name}.m3u8")
            write_multi_variant_m3u8(file_path, m3u8_link)
            print(f"{file_path} dosya oluşturuldu.")
        else:
            print(f"{name} için link bulunamadı.")
