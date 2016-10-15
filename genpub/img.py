# -*- coding: utf-8 -*-

def _copy_file(orig, tmp_path='/tmp/'):
  from shutil import copyfile
  from os import sep
  if orig.endswith('.png'):
    target = orig.split(sep)[-1]
    full_target = tmp_path+target
    copyfile(orig, full_target)
    return full_target
  return False

def _thumbnail(name, size):
  try:
    from PIL import Image
  except Exception:
    import Image

  thumb = _copy_file(name)
  if thumb:
    img = Image.open(thumb)
    img = img.convert('RGBA')
    img.thumbnail((size, size))
    pixels = img.load()
    r, g, b, a = pixels[0, 0]

    if a >= 255:
      a = 254

    pixels[0, 0] = r, g, b, a
    img.save(thumb)

  return thumb

