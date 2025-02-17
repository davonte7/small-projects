from PIL import ImageDraw, ImageFont, ImageFile
import pytesseract
from typing import Dict, Any
from collections import defaultdict
from translate_text import detect_language
from translate_text import translate_text

# Group words by line using block_num and line_num
def group_lines(data: Dict) -> defaultdict[Any, dict[str, float | int | str]]:
  
  lines = defaultdict(lambda: {"x": float("inf"), "y": float("inf"), "w": 0, "h": 0, "text": "", "font_size": 0})

  for i in range(len(data['text'])):
      if data['text'][i].strip():  # Ignore empty entries
          block, line = data['block_num'][i], data['line_num'][i]
          key = (block, line)

          x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

          # Update bounding box for the entire line
          lines[key]["x"] = min(lines[key]["x"], x)
          lines[key]["y"] = min(lines[key]["y"], y)
          lines[key]["w"] = ( lines[key]["w"] + (x + w) - lines[key]["x"] ) /2
          lines[key]["h"] = max(lines[key]["h"], y + h - lines[key]["y"])
          lines[key]["text"] += " " + data['text'][i]  # Concatenate words
          lines[key]["font_size"] = (lines[key]["font_size"] + h)/2
  
  return lines

# Replace Text in image
def draw_text(
      lines: defaultdict[Any, dict[str, float | int | str]], 
      image: ImageFile,
      font: str
      ) -> ImageFile:
  
  draw = ImageDraw.Draw(image)

  # Process each detected line
  for _, line in lines.items():
      
      lang = detect_language(line["text"])
      
      if lang == "en":
          continue

      translated_text = translate_text(line["text"])
    #   translated_text = "Contentment is the key to happiness"
      
      x, y, w, h = line["x"], line["y"], line["w"], line["h"]
      
      new_font = ImageFont.truetype(font, size=10)

    # text_length = (draw.textlength(translated_text, font=new_font))
    # x1,y1,w1,h1 = draw.textbbox((x,y), translated_text, new_font)
      
      draw.rectangle(((x, y), (x + w, y + h)), fill="white")
      
      # Replace the full line with translated text
      draw.multiline_text((x, y), translated_text, fill="black", font=new_font, align='center')
  
  return image

def replace_text(image: ImageFile, output_file: str) -> None:

  font ="arial.ttf"

  # Get bounding box data for detected text (word-level detection)
  data = pytesseract.image_to_data(image, lang="eng+chi_sim", output_type=pytesseract.Output.DICT)

  lines = group_lines(data)
  image = draw_text(lines, image, font)
  
  # Save the modified image
  image.save(output_file)