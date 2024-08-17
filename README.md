# EKSTENSI AUTOMASI UPLOAD OUPUT KE HUGGINGFACE UNTUK STABLE DIFFUSION

Script ini secara otomatis memantau direktori output untuk file gambar baru dan mengunggahnya ke repository Hugging Face. Script ini dirancang untuk bekerja dengan gambar yang dihasilkan oleh Stable Diffusion. 

## Fitur

- **Pemantauan Direktori**: Memantau direktori tertentu secara otomatis untuk file baru yang dibuat.
- **Penanganan File**: Mendeteksi file `.tmp` sementara, menunggu hingga file tersebut dikonversi menjadi `.png`, lalu mengunggah file `.png` ke Hugging Face.
- **Integrasi dengan Hugging Face**: Mengunggah file langsung ke repository Hugging Face, mendukung tipe repository model dan dataset.
- **Antarmuka Gradio**: Menyediakan antarmuka web yang intuitif untuk memulai pemantauan dan pengunggahan file.

## Penggunaan

Di antarmuka Gradio:
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
- Script ini mendukung berbagai tipe repository (`model`, `dataset`). Pastikan tipe repository yang benar dipilih di antarmuka Gradio@.


---

@jekverse
