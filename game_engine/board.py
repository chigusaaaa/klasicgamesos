class Board:
    TENGAH = [(0, 1), (1, 0), (1, 1), (1, -1)]
    UJUNG = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    def __init__(self, size=3):
        self.size = size
        self.grid = [[" "] * size for _ in range(size)]

    def in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def is_full(self):
        return all(cell != " " for row in self.grid for cell in row)

    def count_line(self, r, c):
        """Hitung garis 3 simbol sama yang melibatkan sel (r, c)."""
        s = self.grid[r][c]
        count = 0
        for dr, dc in self.TENGAH:  # sel di tengah
            a, b = (r - dr, c - dc), (r + dr, c + dc)
            if self.in_bounds(*a) and self.in_bounds(*b):
                if self.grid[a[0]][a[1]] == s and self.grid[b[0]][b[1]] == s:
                    count += 1
        for dr, dc in self.UJUNG:  # sel di ujung
            a, b = (r + dr, c + dc), (r + 2 * dr, c + 2 * dc)
            if self.in_bounds(*a) and self.in_bounds(*b):
                if self.grid[a[0]][a[1]] == s and self.grid[b[0]][b[1]] == s:
                    count += 1
        return count

    def place(self, r, c, symbol):
        """Taruh simbol, return jumlah garis yang kebentuk."""
        if not self.in_bounds(r, c):
            raise ValueError("Di luar papan")
        if self.grid[r][c] != " ":
            raise ValueError("Sel sudah terisi")
        self.grid[r][c] = symbol
        return self.count_line(r, c)

    def render(self):
        lines = ["    " + "   ".join(str(i) for i in range(self.size))]
        for i, row in enumerate(self.grid):
            lines.append(f"{i}   " + "  ".join(c if c != " " else "·" for c in row))
        return "\n".join(lines)