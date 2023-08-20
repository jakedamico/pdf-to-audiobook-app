# import fitz

# def get_text(filepath: str, start_page: int, end_page: int) -> str:
#     with fitz.open(filepath) as doc:
#         text = ""
#         for page_num in range(start_page, end_page + 1):
#             page = doc[page_num]
#             text += page.get_text().strip()
#         return text

# # Get user input for file path and page range
# filepath = 'Abraham-Silberschatz-Operating-System-Concepts-10th-2018.pdf'
# start_page = int(input("Enter the starting page (0-based): "))
# end_page = int(input("Enter the ending page (0-based): "))

# # Call the function to extract text within the specified page range
# extracted_text = get_text(filepath, start_page, end_page)

# # Print the extracted text
# print(extracted_text)

import fitz
from gtts import gTTS
import os
import re

def extract_text_by_area(page, x0, y0, x1, y1):
    return page.get_text("text", clip=(x0, y0, x1, y1))

def get_text_with_area_extraction(filepath: str, start_page: int, end_page: int, x0, y0, x1, y1) -> str:
    with fitz.open(filepath) as doc:
        extracted_text = ""
        for page_num in range(start_page, end_page + 1):
            page = doc[page_num]
            #extracted_text += extract_text_by_area(page, x0, y0, x1, y1).replace('\n', ' ').strip()
            extracted_text += page.get_text().replace('\n', ' ').strip()
        
        standardized_text = re.sub(r'\s+', ' ', extracted_text)
        return standardized_text
    
def get_pdf_dimensions(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    
    page = doc[page_num]
    page_width = str(page.rect.width)
    page_height = str(page.rect.height)
    
    doc.close()
    print(f"{page_width}, {page_height}")

# Get user input for file path, page range, and text area coordinates
filepath = 'Fooled-by-Randomness-Role-of-Chance-in-Markets-and-Life-PROPER1.pdf'
get_pdf_dimensions(filepath, 27)
start_page = int(input("Enter the starting page: ")) - 1
end_page = int(input("Enter the ending page: ")) - 1

# x0 = float(input("Enter the x-coordinate of the top-left corner: "))
# y0 = float(input("Enter the y-coordinate of the top-left corner: "))
# x1 = float(input("Enter the x-coordinate of the bottom-right corner: "))
# y1 = float(input("Enter the y-coordinate of the bottom-right corner: "))

x0, y0, x1, y1 = 0, 419.5, 595.25, 0

# Call the function to extract text within the specified page range and area
extracted_text = get_text_with_area_extraction(filepath, start_page, end_page, x0, y0, x1, y1)

print(extracted_text)

# Create a gTTS object to convert text to speech
tts = gTTS(text=extracted_text, lang='en')

# Save the speech as an audio file
output_audio_path = 'extracted_text_audio.mp3'
tts.save(output_audio_path)

# Print a message indicating where the audio file was saved
print(f"Text-to-speech audio saved as: {output_audio_path}")
