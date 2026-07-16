import os
import requests
import mutagen
from mutagen.id3 import USLT, ID3

def fetch_lyrics(title, artist):
    """Mencari lirik di API LRCLIB berdasarkan judul dan artis."""
    url = "https://lrclib.net/api/search"
    params = {
        'track_name': title,
        'artist_name': artist
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            if data.get('syncedLyrics'):
                return data['syncedLyrics'], True
            elif data.get('plainLyrics'):
                return data['plainLyrics'], False
        return None, False
    except Exception as e:
        print(f"   [Error] Gagal mengakses API: {e}")
        return None, False

def get_audio_metadata(audio, ext):
    """Membaca Title, Artist, dan status lirik berdasarkan format file."""
    title, artist, has_lyrics = None, None, False

    # 1. Format FLAC
    if ext == '.flac':
        title = audio.get('title', [None])[0]
        artist = audio.get('artist', [None])[0]
        has_lyrics = 'lyrics' in audio or 'unsyncedlyrics' in audio

    # 2. Format MP3 & WAV (Menggunakan sistem ID3)
    elif ext in ['.mp3', '.wav']:
        if audio.tags is None:
            audio.add_tags()
        
        title = str(audio.tags.get('TIT2', '')) or None
        artist = str(audio.tags.get('TPE1', '')) or None
        
        # Cek apakah tag USLT (lirik) sudah ada
        for key in audio.tags.keys():
            if key.startswith('USLT'):
                has_lyrics = True
                break

    # 3. Format M4A & ALAC (Menggunakan kontainer MP4/iTunes)
    elif ext in ['.m4a', '.alac', '.mp4']:
        title = audio.get('\xa9nam', [None])[0]
        artist = audio.get('\xa9ART', [None])[0]
        has_lyrics = '\xa9lyr' in audio

    return title, artist, has_lyrics

def embed_lyrics_to_audio(audio, ext, lyrics):
    """Menanamkan lirik ke dalam file sesuai formatnya."""
    # 1. Format FLAC
    if ext == '.flac':
        audio['lyrics'] = lyrics

    # 2. Format MP3 & WAV
    elif ext in ['.mp3', '.wav']:
        # Set tag lirik menggunakan format USLT standard ID3
        audio.tags.setall('USLT', [USLT(encoding=3, lang='eng', desc='', text=lyrics)])

    # 3. Format M4A & ALAC
    elif ext in ['.m4a', '.alac', '.mp4']:
        audio['\xa9lyr'] = [lyrics]

    audio.save()

def process_audio_files(folder_path):
    """Memindai folder dan melakukan embedding ke semua format audio yang didukung."""
    supported_extensions = ['.flac', '.mp3', '.m4a', '.alac', '.wav']
    print(f"Memulai pemindaian file audio di: {folder_path}\n")
    
    for filename in os.listdir(folder_path):
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in supported_extensions:
            file_path = os.path.join(folder_path, filename)
            
            try:
                audio = mutagen.File(file_path)
                if audio is None:
                    continue
                
                title, artist, has_lyrics = get_audio_metadata(audio, ext)
                
                if not title or not artist:
                    print(f"⚠️  [Skip] {filename} tidak memiliki metadata 'title' atau 'artist' yang lengkap.")
                    continue
                
                if has_lyrics:
                    print(f"✅ [Skip] {title} - {artist} ({ext.upper()}) sudah memiliki lirik internal.")
                    continue
                
                print(f"🔍 Mencari lirik untuk: {title} - {artist} ({ext.upper()})...")
                lyrics, is_synced = fetch_lyrics(title, artist)
                
                if lyrics:
                    embed_lyrics_to_audio(audio, ext, lyrics)
                    tipe = "Synced (LRC)" if is_synced else "Plain"
                    print(f"✨ [Sukses] Berhasil menanamkan lirik ({tipe}) ke {filename}")
                else:
                    print(f"❌ [Gagal] Lirik tidak ditemukan di internet untuk {title}.")
                    
            except Exception as e:
                print(f"💥 [Error] Gagal memproses file {filename}: {e}")

if __name__ == "__main__":
    target_folder = input("Masukkan path folder musik (kosongkan jika folder saat ini): ").strip()
    
    if not target_folder:
        target_folder = os.getcwd()
        
    if os.path.exists(target_folder):
        process_audio_files(target_folder)
    else:
        print("Folder tidak ditemukan!")
