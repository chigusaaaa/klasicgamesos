import random

# Definisi simbol untuk CPU dan Player
CPU = "🤖"
PLAYER = "😎"

def hitung_sos(papan, baris, kolom, emoji):
    """
    Menghitung apakah penempatan `emoji` di (baris, kolom) 
    membentuk 3 simbol sejajar yang sama (😎😎😎 atau 🤖🤖🤖).
    """
    ukuran = len(papan)
    papan[baris][kolom] = emoji
    jumlah_poin = 0

    # Arah pemeriksaan: Vertikal, Horizontal, Diagonal Utama (\), Diagonal Sekunder (/)
    pasangan_arah = [
        ((-1, 0), (1, 0)),    # Vertikal
        ((0, -1), (0, 1)),    # Horizontal
        ((-1, -1), (1, 1)),   # Diagonal Utama
        ((-1, 1), (1, -1))    # Diagonal Sekunder
    ]

    # 1. Cek jika sel ini menjadi TENGAH dari 3 simbol sejajar 
    for (dr1, dc1), (dr2, dc2) in pasangan_arah:
        r1, c1 = baris + dr1, kolom + dc1
        r2, c2 = baris + dr2, kolom + dc2
        if 0 <= r1 < ukuran and 0 <= c1 < ukuran and 0 <= r2 < ukuran and 0 <= c2 < ukuran:
            if papan[r1][c1] == emoji and papan[r2][c2] == emoji:
                jumlah_poin += 1

    # 2. Cek jika sel ini menjadi UJUNG dari 3 simbol sejajar 
    arah_tunggal = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (1, 1), (-1, 1), (1, -1)
    ]
    for dr, dc in arah_tunggal:
        r1, c1 = baris + dr, kolom + dc
        r2, c2 = baris + 2 * dr, kolom + 2 * dc
        if 0 <= r1 < ukuran and 0 <= c1 < ukuran and 0 <= r2 < ukuran and 0 <= c2 < ukuran:
            if papan[r1][c1] == emoji and papan[r2][c2] == emoji:
                jumlah_poin += 1

    papan[baris][kolom] = " "
    return jumlah_poin


def pilih_langkah_cpu(papan, emoji_cpu=CPU, emoji_player=PLAYER):
    """
    Strategi CPU:
    1. ATTACK  : Cari sel yang bisa membuat 3 🤖 sejajar.
    2. DEFENSE : Blokir sel yang bisa membuat Player mendapat 3 😎 sejajar.
    3. RANDOM  : Pilih sel acak.
    """
    ukuran = len(papan)
    sel_kosong = []

    for r in range(ukuran):
        for c in range(ukuran):
            if papan[r][c] == " ":
                sel_kosong.append((r, c))

    if not sel_kosong:
        return None

    # Prioritas 1: ATTACK (Poin untuk CPU)
    for r, c in sel_kosong:
        poin_cpu = hitung_sos(papan, r, c, emoji_cpu)
        if poin_cpu > 0:
            return r, c, emoji_cpu, poin_cpu

    # Prioritas 2: DEFENSE (Blokir Poin Player)
    for r, c in sel_kosong:
        poin_player = hitung_sos(papan, r, c, emoji_player)
        if poin_player > 0:
            return r, c, emoji_cpu, 0

    # Prioritas 3: RANDOM
    r, c = random.choice(sel_kosong)
    return r, c, emoji_cpu, 0