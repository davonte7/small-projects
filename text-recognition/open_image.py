from PIL import Image, ImageFile

def open_image(file: str) -> ImageFile:
  
  # Load the image
  image = Image.open(file)
  return image