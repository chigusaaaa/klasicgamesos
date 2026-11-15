import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "game engine"))





from board import Board
import game_state as gs
import cpu_move


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