import os
import requests
from mutagen.flac import FLAC

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
            # Mengambil hasil pencarian pertama yang paling cocok
            data = response.json()[0]
            
            # Prioritaskan Synced Lyrics (lirik berjalan), jika tidak ada pakai lirik biasa
            if data.get('syncedLyrics'):
                return data['syncedLyrics'], True
            elif data.get('plainLyrics'):
                return data['plainLyrics'], False
        return None, False
    except Exception as e:
        print(f"   [Error] Gagal mengakses API: {e}")
        return None, False

def process_flac_files(folder_path):
    """Memindai folder dan melakukan embedding lirik ke file FLAC."""
    print(f"Memulai pemindaian file FLAC di: {folder_path}\n")
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.flac'):
            file_path = os.path.join(folder_path, filename)
            
            try:
                audio = FLAC(file_path)
                
                # Ambil tag Title dan Artist dari metadata file FLAC
                title = audio.get('title', [None])[0]
                artist = audio.get('artist', [None])[0]
                
                if not title or not artist:
                    print(f"⚠️  [Skip] {filename} tidak memiliki tag 'title' atau 'artist'.")
                    continue
                
                # Cek apakah lirik sudah tertanam sebelumnya
                if 'lyrics' in audio or 'unsyncedlyrics' in audio:
                    print(f"✅ [Skip] {title} - {artist} sudah memiliki lirik internal.")
                    continue
                
                print(f"🔍 Mencari lirik untuk: {title} - {artist}...")
                lyrics, is_synced = fetch_lyrics(title, artist)
                
                if lyrics:
                    # Menanamkan lirik ke standar tag FLAC (Vorbis Comment)
                    # Kita masukkan ke tag 'LYRICS' agar kompatibel dengan mayoritas player/DAP
                    audio['lyrics'] = lyrics
                    audio.save()
                    
                    tipe = "Synced (LRC)" if is_synced else "Plain"
                    print(f"✨ [Sukses] Berhasil menanamkan lirik ({tipe}) ke {filename}")
                else:
                    print(f"❌ [Gagal] Lirik tidak ditemukan di internet untuk {title}.")
                    
            except Exception as e:
                print(f"💥 [Error] Gagal memproses file {filename}: {e}")

if __name__ == "__main__":
    # Ubah jalur ini sesuai folder musik di internal storage-mu
    # Contoh: /storage/emulated/0/Music
    target_folder = input("Masukkan path folder FLAC (kosongkan jika folder saat ini): ").strip()
    
    if not target_folder:
        target_folder = os.getcwd()
        
    if os.path.exists(target_folder):
        process_flac_files(target_folder)
    else:
        print("Folder tidak ditemukan!")
      
