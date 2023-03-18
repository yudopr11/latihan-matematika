# latihan-matematika
Aplikasi kuis latihan matematika untuk belajar ujian masuk perguruan tinggi negeri. Aplikasi ini di desain untuk tampil lebih menarik saat dibuka melalui browser smartphone.
## Demo Live Aplikasi
url (tba)
## Fitur
- Mendukung soal pilihan ganda.
- Mendukung soal tabel benar salah.
- Mendukung latex.
- Mendukung rich text formatting untuk mempermudah mengetik soal dan penjelasan (untuk latex harus ketik manual dimulai dengan `$` dan diakhiri `$`).
- User dapat memfilter soal dari sumber soal.
## Cara Pakai
1. Lakukan clone terhadap repositori ini. <br>
```
git clone https://github.com/yudopr11/latihan-matematika.git
```
2. Buat virtual environment di dalam folder repositori. Kamu bisa namain nama virtual environment (tanpa tanda petik ' ) sesuka hati.
```
python -m venv 'nama-virtual-env'
```
3. Aktifkan virtual environment di folder dengan menjalan command `venv\Scripts\activate.bat` untuk cmd atau `venv\Scripts\Activate.ps1` untuk shell.
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
7. Buat super user dengan command berikut.
```
python manage.py createsuperuser
```
8. Jalankan dua command berikut untuk membuat tabel di db.sqlite.
```
python manage.py makemigrations
python manage.py migrate
```
9. Jalankan command berikut untuk mengumpulkan file static (image, js, css, dll).
```
python manage.py runserver
```
10. Masuk ke Django Admin (`http://127.0.0.1:8000/admin`). Pada kolom kiri pilih `Bank soals` dan klik `ADD BANK SOAL` untuk memasukan soal ke database sqlite.<br><br>
Berikut ini contoh soal pilihan ganda.
![Piliha Ganda](https://res.cloudinary.com/dnf9bfdne/image/upload/v1679148039/pilihan-ganda_yxb1ya.jpg)<br><br>
Berikut ini contoh soal tabel benar salah.
![Tabel Benar Salah](https://res.cloudinary.com/dnf9bfdne/image/upload/v1679148247/tabel-benar-salah_esgxpn.jpg)<br><br>
11. Setelah membuat soal, kamu bisa langsung keluar dari admin dan menuju `http://127.0.0.1:8000`. Berikut ini contoh tampilan aplikasi saat dibuka melalui browser smartphone.
<video width="320" height="240" controls>
  <source src="https://res.cloudinary.com/dnf9bfdne/video/upload/v1679149451/demo_gubauf.mp4" type="video/mp4">
</video>
