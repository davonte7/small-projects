from google.cloud import translate_v2 as translate
from langid import classify

def translate_text(text: str) -> str:
  translate_client = translate.Client()
  result = translate_client.translate(text, target_language="en")
  translated_text = result["translatedText"]

  return translated_text

def detect_language(text: str) -> str:

  detected_lang, confidence = classify(text)
  print(f"Detected Language: {detected_lang} (Confidence: {confidence})")
  
  return detected_lang