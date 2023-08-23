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
from TTS.api import TTS
import nextTextToAudio

def extract_text_by_area(page, rect):
    return page.get_text("text", clip=rect)

def get_text_with_area_extraction(filepath: str, start_page: int, end_page: int, rect) -> str:
    with fitz.open(filepath) as doc:
        extracted_text = ""
        for page_num in range(start_page, end_page + 1):
            page = doc[page_num]
            extracted_text += extract_text_by_area(page, rect).replace('\n', ' ').strip()
        
        standardized_text = re.sub(r'\s+', ' ', extracted_text)
        return standardized_text
    
def get_pdf_dimensions(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    
    page = doc[page_num]
    page_width = page.rect.width
    page_height = page.rect.height
    
    doc.close()
    return page_width, page_height

def calculate_text_area_full_border(page_width, page_height, border_size):
    # border_x = page_width * percentage
    # border_y = page_height * percentage

    # x0 = border_x
    # y0 = page_height - border_y
    # x1 = page_width - border_x
    # y1 = border_y
    
    rect = (
        border_size,        # left
        border_size,        # top
        page_width - border_size,   # right
        page_height - border_size  # bottom
    )
    
    return rect

def count_characters(input_string):
    return len(input_string)

def calculate_text_area_top_border(page_width, page_height, border_size):
    
    rect = (
        0,        # left
        border_size,  # top
        page_width,   # right
        page_height  # bottom
    )
    
    return rect

filepath = 'Fooled-by-Randomness-Role-of-Chance-in-Markets-and-Life-PROPER1.pdf'
start_page = int(input("Enter the starting page: ")) - 1
end_page = int(input("Enter the ending page: ")) - 1

page_num = start_page
page_width, page_height = get_pdf_dimensions(filepath, page_num)

percentage = float(input("Enter the percentage of the border to remove (e.g., 0.1 for 10%): "))
rect = calculate_text_area_top_border(page_width, page_height, percentage)

extracted_text = get_text_with_area_extraction(filepath, start_page, end_page, rect)
print(count_characters(extracted_text))
print(extracted_text)

#coqui tts
# tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=True, gpu=False)

# output_audio_path = 'extracted_text_audio_tts.mp3'
# tts.tts_to_file(text=extracted_text, file_path=output_audio_path)

nextTextToAudio.text_to_speech(extracted_text)

print(f"Text-to-speech audio finished processing")

