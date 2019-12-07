## robotron1715-font

This utility takes [Robotron 1715](https://en.wikipedia.org/wiki/PC_1715) ([ru](https://ru.wikipedia.org/wiki/Robotron_1715)) character ROM and saves font to [BDF format](https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format), which can be used in Unix or converted to other format (for example, [PSF](https://en.wikipedia.org/wiki/PC_Screen_Font)). It serves no purpose except historical interest.

Currently, only Latin ROM (see `s619.bin` below) is included in bdf.

### Preview

| Latin character ROM (s619.bin) | Cyrillic character ROM (s605.bin) | Latin+Cyrillic character ROM (s643.bin) |
| ---- | --- | --- |
| ![Latin](https://github.com/kolontsov/robotron1715-font/blob/master/s619.png)  | ![Cyrillic Only](https://github.com/kolontsov/robotron1715-font/blob/master/s605.png) | ![Latin+Cyrillic](https://github.com/kolontsov/robotron1715-font/blob/master/s643.png) |

### Install

~~~ bash
cp robotron1715.bdf ~/.fonts
fc-cache -f -v
~~~

In Ubuntu, you may need to [enable bitmap fonts first](https://wiki.ubuntu.com/Fonts#Enabling_Bitmapped_Fonts). Also, when using font choose it's native size 16 (it doesn't scale well).

### Rebuild

~~~ bash
pip3 install pypng
./rb1715font.py
~~~

By default, it loads `s619.bin` and generates `robotron1715.bdf` (font) and `robotron1715.png` (preview).

### License

MIT
