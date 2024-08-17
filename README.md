Berikut adalah deskripsi untuk file `README.md` dalam bahasa Indonesia dengan format yang mudah dibaca:

---

# Pengunggah Otomatis ke Hugging Face

Script ini secara otomatis memantau direktori tertentu untuk file gambar baru dan mengunggahnya ke repository Hugging Face. Script ini dirancang untuk bekerja dengan gambar yang dihasilkan oleh Stable Diffusion dan dapat menangani format file `.tmp` dan `.png`.

## Fitur

- **Pemantauan Direktori**: Memantau direktori tertentu secara otomatis untuk file baru yang dibuat.
- **Penanganan File**: Mendeteksi file `.tmp` sementara, menunggu hingga file tersebut dikonversi menjadi `.png`, lalu mengunggah file `.png` ke Hugging Face.
- **Integrasi dengan Hugging Face**: Mengunggah file langsung ke repository Hugging Face, mendukung tipe repository model dan dataset.
- **Antarmuka Gradio**: Menyediakan antarmuka web yang intuitif untuk memulai pemantauan dan pengunggahan file.

## Penggunaan

1. Jalankan script untuk memulai antarmuka Gradio:
   ```bash
   python your_script.py
   ```
2. Di antarmuka Gradio:
   - Masukkan token Hugging Face Anda.
   - Pilih tipe repository (`model` atau `dataset`).
   - Masukkan ID repository tempat file akan diunggah.
   - Klik tombol "Start Monitoring".

## Cara Kerja

- **Pemantauan File**: Script ini menggunakan library Watchdog untuk memantau direktori tertentu (`/kaggle/working/stable-diffusion-webui/outputs/txt2img-images/2024-08-07`) untuk file baru.
- **Pengunggahan File**: Saat file baru terdeteksi, script akan memeriksa formatnya:
  - Jika file berformat `.tmp`, script akan menunggu beberapa detik dan memeriksa apakah file tersebut berubah menjadi `.png`. Jika ya, file `.png` akan diunggah ke repository Hugging Face.
  - Jika file sudah dalam format `.png`, file tersebut akan langsung diunggah.
  
## Kustomisasi

- Direktori yang dipantau dapat diubah dengan memodifikasi `path` di fungsi `start_watcher`.
- Script ini mendukung berbagai tipe repository (`model`, `dataset`). Pastikan tipe repository yang benar dipilih di antarmuka Gradio.

## Kontribusi

Silakan fork repository ini, laporkan masalah, atau berkontribusi melalui pull request.

## Lisensi

Proyek ini dilisensikan di bawah MIT License.

---

README ini menyajikan deskripsi yang jelas mengenai fungsionalitas script dan memberikan panduan kepada pengguna tentang cara menginstal dan menggunakannya dengan efektif.
