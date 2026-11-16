import random

PLAYER = "❌"
CPU = "⭕"

def hitung_sos(papan, baris, kolom, emoji):
    ukuran = len(papan)
    papan[baris][kolom] = emoji
    jumlah_sos = 0

    arah = [
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (1, 1), (-1, 1), (1, -1)
    ]

    if emoji == "❌":
        for dr, dc in arah:
            r1, c1 = baris + dr, kolom + dc
            r2, c2 = baris + 2 * dr, kolom + 2 * dc
            if 0 <= r1 < ukuran and 0 <= c1 < ukuran and 0 <= r2 < ukuran and 0 <= c2 < ukuran:
                if papan[r1][c1] == "⭕" and papan[r2][c2] == "❌":
                    jumlah_sos += 1

    elif emoji == "⭕":
        pasangan_arah = [
            ((-1, 0), (1, 0)), ((0, -1), (0, 1)),
            ((-1, -1), (1, 1)), ((-1, 1), (1, -1))
        ]
        for (dr1, dc1), (dr2, dc2) in pasangan_arah:
            r1, c1 = baris + dr1, kolom + dc1
            r2, c2 = baris + dr2, kolom + dc2
            if 0 <= r1 < ukuran and 0 <= c1 < ukuran and 0 <= r2 < ukuran and 0 <= c2 < ukuran:
                if papan[r1][c1] == "❌" and papan[r2][c2] == "❌":
                    jumlah_sos += 1

    papan[baris][kolom] = " "
    return jumlah_sos


def pilih_langkah_cpu(papan):
    ukuran = len(papan)
    sel_kosong = []

    for r in range(ukuran):
        for c in range(ukuran):
            if papan[r][c] == " ":
                sel_kosong.append((r, c))

    if not sel_kosong:
        return None

    # Prioritas 1: ATTACK (Cari poin dari pola ❌-⭕-❌)
    for r, c in sel_kosong:
        for emoji in ["❌", "⭕"]:
            sos_terbentuk = hitung_sos(papan, r, c, emoji)
            if sos_terbentuk > 0:
                return r, c, emoji, sos_terbentuk

    # Prioritas 2: RANDOM jika tidak ada peluang SOS
    r, c = random.choice(sel_kosong)
    emoji = random.choice(["❌", "⭕"])
    return r, c, emoji, 0