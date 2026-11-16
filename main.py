import sys, os
import hashlib
import hmac

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_engine"))

from board import Board
import game_state as gs
import cpu_move

# Kunci rahasia untuk mengacak kode lisensi (bisa kamu ganti bebas)
SECRET_SALT = b"SOS_PLUS_RAHASIA_2026"
LICENSE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".license")


def make_key(name: str) -> str:
    """Membuat kode lisensi unik berdasarkan nama pembeli."""
    clean_name = name.strip().lower().encode("utf-8")
    digest = hmac.new(SECRET_SALT, clean_name, hashlib.sha256).hexdigest().upper()
    # Format output contoh: SOS-4A1B-9C2D-8E3F
    return f"SOS-{digest[:4]}-{digest[4:8]}-{digest[8:12]}"


def verifikasi_lisensi():
    """Mengecek apakah user sudah mengaktifkan lisensi sebelum bermain."""
    # 1. Cek apakah sudah ada file lisensi yang tersimpan dan valid
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines()]
                if len(lines) >= 2:
                    saved_name, saved_key = lines[0], lines[1]
                    if hmac.compare_digest(saved_key, make_key(saved_name)):
                        print(f"Lisensi aktif untuk: {saved_name}")
                        return True
        except Exception:
            pass

    # 2. Jika belum ada lisensi, tahan user di layar aktivasi
    print("==========================================")
    print("         🔒 AKTIVASI SOS PLUS 🔒          ")
    print("==========================================")
    print("Game ini berbayar. Silakan lakukan pembayaran")
    print("untuk mendapatkan Kode Lisensi permainan.\n")

    nama = input("Masukkan Nama Pembeli : ").strip()
    kode = input("Masukkan Kode Lisensi : ").strip().upper()

    if not nama or not kode:
        print("\n[!] Nama dan kode tidak boleh kosong.")
        sys.exit(1)

    # Cocokkan kode yang diinput dengan hasil make_key(nama)
    if hmac.compare_digest(kode, make_key(nama)):
        try:
            with open(LICENSE_FILE, "w", encoding="utf-8") as f:
                f.write(f"{nama}\n{kode}\n")
        except Exception:
            pass
        print("\n[+] Aktivasi berhasil! Selamat bermain.")
    else:
        print("\n[!] Kode lisensi tidak valid! Silakan hubungi penjual.")
        sys.exit(1)


def baca_langkah(b):
    while True:
        teks = input("Langkah kamu (baris kolom, contoh: 0 1): ").split()
        if len(teks) != 2 or not all(t.isdigit() for t in teks):
            print("Format salah. Contoh: 0 1")
            continue
        r, c = int(teks[0]), int(teks[1])
        if not b.in_bounds(r, c):
            print("Di luar papan.")
            continue
        if b.grid[r][c] != " ":
            print("Sel sudah terisi.")
            continue
        return r, c


def main():
    # Panggil pengecekan lisensi sebelum game dimulai
    verifikasi_lisensi()

    gs.reset_game()
    b = Board(gs.ukuran_papan)

    while gs.status == "berlangsung":
        s = gs.ambil_status()
        print()
        print(b.render())
        print(f"Skor: Player {s['skor_player']} - {s['skor_cpu']} CPU | Giliran: {s['giliran']}")

        if gs.giliran == 0:
            r, c = baca_langkah(b)
            poin = b.place(r, c, cpu_move.PLAYER)
        else:
            r, c, emoji, _ = cpu_move.pilih_langkah_cpu(b.grid)
            poin = b.place(r, c, emoji)
            print(f"CPU jalan di {r} {c}")

        if poin > 0:
            print(f"+{poin} poin! Jalan lagi.")
        gs.proses_giliran(poin)

    s = gs.ambil_status()
    print()
    print(b.render())
    print(f"SELESAI. Player {s['skor_player']} - {s['skor_cpu']} CPU")
    print("Hasil:", "Seri" if s["pemenang"] == "Seri" else f"{s['pemenang']} menang")


if __name__ == "__main__":
    main()