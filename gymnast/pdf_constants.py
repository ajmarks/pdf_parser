"""
Constants needed mostly for PDF character encoding
"""

import binascii
import os

__all__  = ['EOLS', 'WHITESPACE', 'BASE_ENCODINGS', 'GLYPH_LIST']
DATA_DIR = os.path.dirname(os.path.abspath(__file__))+'/data/'

EOLS       = frozenset((b'\r', b'\n', b'\r\n'))
WHITESPACE = frozenset((b' ', b'\t', b'\r', b'\n', b'\f', b'\x00'))

def octal_to_int(oct_str):
    """Convert an octal string to an int, respecting None"""
    return int(oct_str, 8) if oct_str else None

def get_base_encodings():
    """Load the base PDF encoding schemes and parse it into a nice dict."""
    with open(DATA_DIR+'/pdf_encodings.txt') as f:
        lines = [l.split(';') for l in f.read().splitlines() if l[0] != '#']
    encodings = ('StandardEncoding', 'MacRomanEncoding',
                 'WinAnsiEncoding', 'PDFDocEncoding')
    return {l[0]:dict(zip(encodings,map(octal_to_int, l[1:]))) for l in lines}

BASE_ENCODINGS = get_base_encodings()

def decode_hex(hex_str):
    """Convert a hex string to bytes and treat as a utf-16-be string"""
    return b''.join([binascii.unhexlify(i)
                     for i in hex_str.split()]).decode('utf-16-be')

def get_glyph_list():
    """Load the Adobe Glyph list into a dict.
    https://partners.adobe.com/public/developer/en/opentype/glyphlist.txt"""

    with open(DATA_DIR + 'glyphlist.txt') as f:
        lines = [l.split(';') for l in f.read().splitlines() if l[0] != '#']
    return {l[0]: decode_hex(l[1]) for l in lines}

GLYPH_LIST = get_glyph_list()
