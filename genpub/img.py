# -*- coding: utf-8 -*-

def _copy_file(recent, tmp_path):
  from shutil import copyfile
  from os import sep
  for t in recent:
    if t.endswith('.png'):
      target = t.split(sep)[-1]
      full_target = tmp_path+sep+target
      copyfile(t, full_target)
      return full_target
  return False

def _thumbnail(recent, size):
  try:
    from PIL import Image
  except Exception:
    import Image

  thumb = _copy_file(recent)
  if thumb:
    img = Image.open(thumb)
    img.thumbnail((size, size))
    img.save(thumb)

  return thumb
