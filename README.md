# emflrc - FLAC Batch Lyrics Embedder

Skrip Python untuk menanamkan (*embed*) lirik secara massal langsung ke metadata file FLAC lokal menggunakan API gratis dari LRCLIB. Skrip ini otomatis memprioritaskan lirik berjalan (*synced lyrics* berformat `.lrc`) dan akan menggunakan lirik biasa jika lirik sinkronisasi tidak tersedia di database.

## Cara Instalasi & Penggunaan di Termux (Android)

Salin seluruh blok perintah di bawah ini, lalu tempel (*paste*) langsung ke dalam aplikasi Termux Anda:

```bash
termux-setup-storage && pkg update && pkg install python git -y && pip install mutagen requests && git clone [https://github.com/WimpiAgustian/emflrc.git](https://github.com/WimpiAgustian/emflrc.git) && cd emflrc && python embed_lyrics.py
