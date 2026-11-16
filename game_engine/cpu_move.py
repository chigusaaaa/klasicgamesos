import random

def hitung_sos(papan, baris, kolom, emoji):
    """
    Menghitung berapa banyak pola 'S-O-S' yang terbentuk 
    jika `emoji` ('❌' atau '⭕') diletakkan pada posisi papan[baris][kolom].
    """
    ukuran = len(papan)
    papan[baris][kolom] = emoji
    jumlah_sos = 0

    # 8 arah vektor pergerakan: (baris, kolom)
    arah = [
        (-1, 0), (1, 0),   # Vertikal (atas, bawah)
        (0, -1), (0, 1),   # Horizontal (kiri, kanan)
        (-1, -1), (1, 1),  # Diagonal utama
        (-1, 1), (1, -1)   # Diagonal sekunder
    ]

    # Jika emoji yang dipasang adalah '❌' (Berada di Ujung Pola: ❌ - ⭕ - ❌)
    if emoji == "❌":
        for dr, dc in arah:
            r1, c1 = baris + dr, kolom + dc
            r2, c2 = baris + 2 * dr, kolom + 2 * dc
            if 0 <= r1 < ukuran and 0 <= c1 < ukuran and 0 <= r2 < ukuran and 0 <= c2 < ukuran:
                if papan[r1][c1] == "⭕" and papan[r2][c2] == "❌":
                    jumlah_sos += 1

    # Jika emoji yang dipasang adalah '⭕' (Berada di Tengah Pola: ❌ - ⭕ - ❌)
    elif emoji == "⭕":
        pasangan_arah = [
            ((-1, 0), (1, 0)),    # Vertikal
            ((0, -1), (0, 1)),    # Horizontal
            ((-1, -1), (1, 1)),   # Diagonal utama
            ((-1, 1), (1, -1))    # Diagonal sekunder
        ]
        for (dr1, dc1), (dr2, dc2) in pasangan_arah:
            r1, c1 = baris + dr1, kolom + dc1
            r2, c2 = baris + dr2, kolom + dc2
            if 0 <= r1 < ukuran and 0 <= c1 < ukuran and 0 <= r2 < ukuran and 0 <= c2 < ukuran:
                if papan[r1][c1] == "❌" and papan[r2][c2] == "❌":
                    jumlah_sos += 1

    # Kembalikan isi sel ke kondisi kosong semula
    papan[baris][kolom] = " "
    return jumlah_sos


def pilih_langkah_cpu(papan):
    """
    Strategi CPU untuk Aturan Game SOS:
    1. ATTACK (Smart Move): Cari sel kosong dan emoji ('❌' atau '⭕') 
       yang langsung bisa mencetak poin SOS.
    2. RANDOM: Jika tidak ada peluang SOS, pilih sel dan emoji ('❌'/'⭕') secara acak.
    
    Mengembalikan tuple 4 nilai: (baris, kolom, emoji, jumlah_sos)
    """
    ukuran = len(papan)
    sel_kosong = []

    # 1. Kumpulkan seluruh koordinat sel kosong
    for r in range(ukuran):
        for c in range(ukuran):
            if papan[r][c] == " " or papan[r][c] == "":
                sel_kosong.append((r, c))

    if not sel_kosong:
        return None

    # 2. Prioritas Utama: Uji setiap sel kosong dengan emoji '❌' dan '⭕'
    for r, c in sel_kosong:
        for emoji in ["❌", "⭕"]:
            sos_terbentuk = hitung_sos(papan, r, c, emoji)
            if sos_terbentuk > 0:
                return r, c, emoji, sos_terbentuk

    # 3. Prioritas Kedua: Jika belum ada peluang SOS, pilih sel & emoji secara acak
    r, c = random.choice(sel_kosong)
    emoji = random.choice(["❌", "⭕"])
    return r, c, emoji, 0