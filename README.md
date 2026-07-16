# emflrc - Multi-Format Batch Lyrics Embedder

Skrip Python untuk menanamkan (*embed*) lirik secara massal langsung ke metadata berbagai file audio lokal (**FLAC, MP3, M4A, ALAC, WAV**) menggunakan API gratis dari LRCLIB. Skrip ini otomatis memprioritaskan lirik berjalan (*synced lyrics* berformat `.lrc`) dan menggunakan lirik biasa jika lirik sinkronisasi tidak tersedia.


## Cara Instalasi & Penggunaan di Termux (Android)

Jalankan perintah-perintah di bawah ini di dalam aplikasi Termux Anda baris demi baris secara berurutan:

1. Izin Akses Penyimpanan HP
```bash
termux-setup-storage
```
2. Install Dependensi Modul Python
```bash
pip install mutagen requests
```
3. Clone repo
```bash
git clone https://github.com/WimpiAgustian/emflarc.git
```
4. Masuk ke folder proyek
```bash
cd emflarc
```
5. Jalankan skrip
```bash
python embed_lyrics.py
```

### Notes

Catatan Penggunaan:
Setelah skrip utama dijalankan, Anda akan diminta memasukkan lokasi folder musik. Ketik atau tempel path folder tempat file FLAC disimpan.
Contoh: /storage/emulated/0/Music/LaguFLAC
