from PIL import Image
import pytesseract
  
img = Image.open('222.png')
text = pytesseract.image_to_string(img, lang='chi_sim')
print(text)