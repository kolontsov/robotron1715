#!/usr/bin/env python3
import png
import unicodedata
from collections import OrderedDict 

class BDF8x16:
    def __init__(self, name, outfile):
        self.name = name
        self.outfile = outfile
        self.nchars = 128
        self.fontboundingbox = '8 16 0 -7'
        self.glyphs = [0]*self.nchars
        # X Logical Font Description
        self.xlfd = OrderedDict()
        self.xlfd['FOUNDRY'] = ''
        self.xlfd['FAMILY_NAME'] = 'Robotron1715'
        self.xlfd['WEIGHT_NAME'] = 'Medium'
        self.xlfd['SLANT'] = 'R'
        self.xlfd['SETWIDTH_NAME'] = 'Normal'
        self.xlfd['ADD_STYLE_NAME'] = ''
        self.xlfd['PIXEL_SIZE'] = 16
        self.xlfd['POINT_SIZE'] = 160
        self.xlfd['RESOLUTION_X'] = 72
        self.xlfd['RESOLUTION_Y'] = 72
        self.xlfd['SPACING'] = 'C'
        self.xlfd['AVERAGE_WIDTH']= 80
        self.xlfd['CHARSET_REGISTRY'] = 'ISO10646'
        self.xlfd['CHARSET_ENCODING'] = '1'
        # Remaining BDF properties
        self.props = OrderedDict(self.xlfd)
        self.props['MIN_SPACE'] = 8
        self.props['FONT_ASCENT'] = 12
        self.props['FONT_DESCENT'] = 4
        self.props['DEFAULT_CHAR'] = 0
    
    def get_xlfd(self):
        return '-'+'-'.join([str(x) for x in self.xlfd.values()])

    def get_props(self):
        repr2 = lambda x: '"{}"'.format(x) if isinstance(x, str) else x 
        props = ['{} {}'.format(item[0], repr2(item[1])) for item in self.props.items()]
        return f'STARTPROPERTIES {len(self.props)}\n' \
            + '\n'.join(props)+'\n' \
            +'ENDPROPERTIES\n'

    def get_glyph(self, code):
        try:
            name = unicodedata.name(chr(code))
        except:
            name = 'U+%04x'%code
        return f'STARTCHAR {name}\n' \
            +f'ENCODING {code}\n' \
            +'SWIDTH 500 0\n' \
            +'DWIDTH 8 0\n' \
            +f'BBX {self.fontboundingbox}\n' \
            +'BITMAP\n' \
            +'\n'.join('%02x'%x for x in self.glyphs[code]) + '\n' \
            +'ENDCHAR\n'

    def get_font(self):
        pixel_size = self.props['PIXEL_SIZE']
        res_x = self.props['RESOLUTION_X']
        res_y = self.props['RESOLUTION_Y']
        return 'STARTFONT 2.1\n' \
            +f'FONT {self.get_xlfd()}\n' \
            +f'SIZE {pixel_size} {res_x} {res_y}\n' \
            +f'FONTBOUNDINGBOX {self.fontboundingbox}\n' \
            +self.get_props() \
            +f'CHARS {self.nchars}\n' \
            +''.join(self.get_glyph(code) for code in range(128)) \
            +'ENDFONT\n'

    def add_char(self, code, data):
        self.glyphs[code] = data

    def write(self):
        with open(self.outfile, 'w') as f:
            f.write(self.get_font())

class RB1715Font:
    def __init__(self, rom):
        with open(rom, 'rb') as f:
            self.rom = f.read()

    def get_data(self, code):
        res = []
        for i in range(0, 16):
            res.append(self.rom[code+i*128])
        return res

class FontPreview:
    def __init__(self, outfile, scale=1):
        self.outfile = outfile
        self.cols = 16
        self.rows = 8
        self.char_width = 8
        self.char_height = 16
        self.scale = scale
        self.width = self.char_width*self.cols*self.scale
        self.height = self.char_height*self.rows*self.scale
        self.image = [[0]*self.width for i in range(self.height)]

    def set_pixel(self, x, y, value):
        for i in range(self.scale):
            for j in range(self.scale):
                self.image[y*self.scale+i][x*self.scale+j] = value

    def add_char(self, code, data):
        y = (code // self.cols)*self.char_height
        x = (code % self.cols)*self.char_width
        for i in range(self.char_height):
            d = data[i]
            for j in range(self.char_width-1,-1,-1):
                self.set_pixel(x+j, y+i, 0 if d&1 else 200)
                d = d >> 1

    def write(self):
        w = png.Writer(width=self.width, height=self.height, greyscale=True)
        with open(self.outfile, 'wb') as f:
            w.write(f, self.image)

def main():
    print('Loading character ROM')
    rb1715 = RB1715Font(rom='s619.bin')
    bdf = BDF8x16(name='Robotron1715', outfile='robotron1715.bdf')
    preview = FontPreview(outfile='robotron1715.png', scale=2)
    
    for code in range(128):
        data = rb1715.get_data(code)
        bdf.add_char(code, data)
        preview.add_char(code, data)

    print('Saving font')
    bdf.write()
    print('Saving preview')
    preview.write()
    print('Done')

if __name__ == '__main__':
    main()
