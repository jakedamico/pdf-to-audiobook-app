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

def get_text(filepath: str, start_page: int, end_page: int) -> str:
    with fitz.open(filepath) as doc:
        text = ""
        for page_num in range(start_page, end_page + 1):
            page = doc[page_num]
            text += page.get_text().strip()
        return text

# Get user input for file path and page range
filepath = 'Fooled-by-Randomness-Role-of-Chance-in-Markets-and-Life-PROPER1.pdf'
start_page = int(input("Enter the starting page (0-based): "))
end_page = int(input("Enter the ending page (0-based): "))

# Call the function to extract text within the specified page range
extracted_text = get_text(filepath, start_page, end_page)

# Create a gTTS object to convert text to speech
tts = gTTS(text=extracted_text, lang='en')

# Save the speech as an audio file
output_audio_path = 'extracted_text_audio.mp3'
tts.save(output_audio_path)

# Print a message indicating where the audio file was saved
print(f"Text-to-speech audio saved as: {output_audio_path}")