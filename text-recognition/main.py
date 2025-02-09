from open_image import open_image
from replace_text import replace_text

image = open_image("imgs/chinese.jpg")

replace_text(image, "imgs/output_image.jpg")