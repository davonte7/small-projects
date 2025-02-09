from PIL import ImageDraw, ImageFont, ImageFile
import pytesseract
from typing import Dict, Any
from collections import defaultdict
from translate_text import detect_language
from translate_text import translate_text

# Group words by line using block_num and line_num
def group_lines(data: Dict) -> defaultdict[Any, dict[str, float | int | str]]:
  
  lines = defaultdict(lambda: {"x": float("inf"), "y": float("inf"), "w": 0, "h": 0, "text": ""})

  for i in range(len(data['text'])):
      if data['text'][i].strip():  # Ignore empty entries
          block, line = data['block_num'][i], data['line_num'][i]
          key = (block, line)

          x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

          # Update bounding box for the entire line
          lines[key]["x"] = min(lines[key]["x"], x)
          lines[key]["y"] = min(lines[key]["y"], y)
          lines[key]["w"] = max(lines[key]["w"], x + w - lines[key]["x"])
          lines[key]["h"] = max(lines[key]["h"], y + h - lines[key]["y"])
          lines[key]["text"] += " " + data['text'][i]  # Concatenate words
  
  return lines

# Replace Text in image
def draw_text(
      lines: defaultdict[Any, dict[str, float | int | str]], 
      image: ImageFile,
      font: ImageFont
      ) -> ImageFile:
  
  draw = ImageDraw.Draw(image)

  # Process each detected line
  for _, line in lines.items():
      
      lang = detect_language(line["text"])
      
      if lang == "en":
          continue

      translated_text = translate_text(line["text"])
      # translated_text = "RED"    
      
      x, y, w, h = line["x"], line["y"], line["w"], line["h"]

      # Draw a white rectangle to erase the original text
      draw.rectangle(((x, y), (x + w, y + h)), fill="white")

      # Replace the full line with translated text
      draw.text((x, y), translated_text, fill="black", font=font)
  
  return image

def replace_text(image: ImageFile, output_file: str) -> None:

  font = ImageFont.truetype("arial.ttf", size=20)

  # Get bounding box data for detected text (word-level detection)
  data = pytesseract.image_to_data(image, lang="eng+chi_sim", output_type=pytesseract.Output.DICT)

  lines = group_lines(data)
  image = draw_text(lines, image, font)
  
  # Save the modified image
  image.save(output_file)