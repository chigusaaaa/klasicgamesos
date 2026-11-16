#!/usr/bin/env python3
"""Generator kode lisensi SOS PLUS. SIMPAN PRIBADI, jangan dikirim ke pembeli.

Pakai:  python3 keygen.py "Nama Pembeli"
"""
import sys

from main import make_key

if len(sys.argv) < 2:
    sys.exit('Pakai: python3 keygen.py "Nama Pembeli"')

name = " ".join(sys.argv[1:])
print(f"Nama  : {name}")
print(f"Kode  : {make_key(name)}")
