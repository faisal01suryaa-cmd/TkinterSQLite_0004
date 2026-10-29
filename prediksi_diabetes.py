import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Membuat database
conn = sqlite3.connect("prediksi_diabetes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pasien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pasien TEXT,
    usia INTEGER,
    gula_darah REAL,
    bmi REAL,
    riwayat_ortu TEXT,
    hasil_prediksi TEXT
)
""")

conn.commit()


# Menentukan hasil prediksi
def prediksi():
    nama = ent_nama.get()
    usia = ent_usia.get()
    gula = ent_gula.get()
    bmi = ent_bmi.get()
    riwayat = cb_riwayat.get()

    # Validasi input kosong
    if not nama or not usia or not gula or not bmi or not riwayat:
        messagebox.showwarning("Peringatan", "Semua data harus diisi!")
        return

    try:
        usia = int(usia)
        gula = float(gula)
        bmi = float(bmi)
    except ValueError:
        messagebox.showwarning("Peringatan", "Usia, gula darah, dan BMI harus angka!")
        return

    # Logika prediksi
    if gula >= 200:
        hasil = "Sangat Tinggi" if bmi >= 30 or riwayat == "Ya" else "Tinggi"
    elif gula >= 140:
        hasil = "Tinggi" if bmi >= 30 or riwayat == "Ya" else "Sedang"
    elif bmi >= 30:
        hasil = "Sedang" if riwayat == "Ya" else "Waspada"
    elif riwayat == "Ya":
        hasil = "Waspada"
    else:
        hasil = "Rendah"

    # Menyimpan data
    cursor.execute("""
        INSERT INTO pasien
        (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nama, usia, gula, bmi, riwayat, hasil))

    conn.commit()

    warna = {
        "Rendah": "green",
        "Waspada": "orange",
        "Sedang": "darkorange",
        "Tinggi": "red",
        "Sangat Tinggi": "darkred"
    }

    lbl_hasil.config(
        text="Hasil: " + hasil,
        fg=warna[hasil]
    )


# Menampilkan data pasien
def lihat_data():
    data_window = tk.Toplevel(root)
    data_window.title("Data Pasien")
    data_window.geometry("800x300")

    kolom = ("id", "nama", "usia", "gula", "bmi", "riwayat", "hasil")
    tabel = ttk.Treeview(data_window, columns=kolom, show="headings")

    judul = [
        "ID", "Nama", "Usia", "Gula Darah",
        "BMI", "Riwayat Ortu", "Hasil"
    ]

    for nama_kolom, teks in zip(kolom, judul):
        tabel.heading(nama_kolom, text=teks)

    cursor.execute("SELECT * FROM pasien")

    for data in cursor.fetchall():
        tabel.insert("", tk.END, values=data)

    tabel.pack(fill="both", expand=True)


# Membuat tampilan
root = tk.Tk()
root.title("Prediksi Risiko Diabetes")
root.geometry("450x400")

tk.Label(
    root,
    text="PREDIKSI RISIKO DIABETES",
    font=("Arial", 15, "bold")
).pack(pady=15)

tk.Label(root, text="Nama Pasien").pack()
ent_nama = tk.Entry(root, width=30)
ent_nama.pack()

tk.Label(root, text="Usia").pack()
ent_usia = tk.Entry(root, width=30)
ent_usia.pack()

tk.Label(root, text="Gula Darah").pack()
ent_gula = tk.Entry(root, width=30)
ent_gula.pack()

tk.Label(root, text="BMI").pack()
ent_bmi = tk.Entry(root, width=30)
ent_bmi.pack()

tk.Label(root, text="Riwayat Diabetes Orang Tua").pack()
cb_riwayat = ttk.Combobox(
    root,
    values=["Ya", "Tidak"],
    state="readonly",
    width=27
)
cb_riwayat.pack()

tk.Button(
    root,
    text="Prediksi dan Simpan",
    command=prediksi
).pack(pady=10)

tk.Button(
    root,
    text="Lihat Data",
    command=lihat_data
).pack()

lbl_hasil = tk.Label(
    root,
    text="Hasil: -",
    font=("Arial", 14, "bold")
)
lbl_hasil.pack(pady=15)

root.mainloop()

