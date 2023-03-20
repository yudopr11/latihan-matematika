# latihan-matematika
Aplikasi ini dibuat menggunakan Django, salah satu framework yang ada di python untuk membuat website secara fullstack. Latihan Matematika ini berbentuk kuis yang berguna untuk belajar ujian masuk perguruan tinggi negeri. Aplikasi ini di desain untuk tampil lebih menarik saat dibuka melalui browser smartphone.
## Demo Live Aplikasi
https://yudopr.up.railway.app/latihan-matematika/
## Fitur
- Mendukung soal pilihan ganda.
- Mendukung soal tabel benar salah.
- Mendukung latex.
- Mendukung rich text formatting untuk mempermudah mengetik soal dan penjelasan (untuk latex harus ketik manual dimulai dengan `$` dan diakhiri `$`).
- Pilihan jawaban selalu acak.
- User dapat memfilter soal dari sumber soal.
- User dapat melihat progress pengerjaan quiz mereka.
## Cara Pakai
1. Lakukan clone terhadap repositori ini. <br>
```
git clone https://github.com/yudopr11/latihan-matematika.git
```
2. Buat virtual environment di dalam folder repositori. Kamu bisa namain nama virtual environment (`nama-virtual-env`) sesuka hati.
```
python -m venv nama-virtual-env
```
3. Aktifkan virtual environment di folder dengan menjalan command `nama-virtual-env\Scripts\activate.bat` untuk cmd atau `nama-virtual-env\Scripts\Activate.ps1` untuk shell.
4. Install requirement packages yang diperlukan.
```
pip install -r requirements.txt
```
5. Buat file `.env` di dalam folder repositori dengan isi sebagai berikut.
```
SECRET_KEY=SECRET_KEY_DJANGO
DEBUG=True
ALLOWED_HOSTS='*'
```
6. Kamu bisa ubah nilai `DEBUG` menjadi `True` atau `False`. Sedangkan untuk mendapatkan `SECRET_KEY_DJANGO`, kamu bisa menjalankan command berikut.
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
7. Jalankan dua command berikut untuk membuat tabel di db.sqlite.
```
python manage.py makemigrations
python manage.py migrate
```
8. Buat super user dengan command berikut.
```
python manage.py createsuperuser
```
9. Jalankan command berikut untuk mengumpulkan file static (image, js, css, dll).
```
python manage.py collectstatic
```
10. Jalan command berikut untuk menjalankan server di lokal komputer.
```
python manage.py runserver
```
11. Masuk ke Django Admin (`http://127.0.0.1:8000/admin`). Pada kolom kiri, pilih `Bank soals` dan klik `ADD BANK SOAL` untuk memasukan soal ke db.sqlite.<br><br>
Berikut ini contoh soal pilihan ganda.
![Piliha Ganda](https://res.cloudinary.com/dnf9bfdne/image/upload/v1679148039/pilihan-ganda_yxb1ya.jpg)<br><br>
Berikut ini contoh soal tabel benar salah.
![Tabel Benar Salah](https://res.cloudinary.com/dnf9bfdne/image/upload/v1679148247/tabel-benar-salah_esgxpn.jpg)<br><br>
12. Setelah membuat soal, kamu bisa langsung keluar dari admin dan menuju `http://127.0.0.1:8000`. Berikut ini contoh tampilan aplikasi saat dibuka melalui browser smartphone.<br>
![Demo Aplikasi](https://user-images.githubusercontent.com/107313576/226112267-85455bbe-ec43-4530-8b2a-acad0de1c223.mp4)
