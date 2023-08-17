import pdfplumber
import re
import wordninja
import nltk
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
nltk.download('punkt')

def preprocess_text(text):
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Normalize line breaks
    text = re.sub(r'\n+', '\n', text)
    return text

def extract_paragraphs_from_page(page):
    text = preprocess_text(page.extract_text())
    paragraphs = text.split('\n\n')
    return [paragraph.strip() for paragraph in paragraphs if paragraph.strip()]

def correct_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    corrected_sentences = []

    for sentence in sentences:
        # Tokenize each sentence into words
        words = word_tokenize(sentence)
        
        # Split and correct each word using wordninja
        corrected_words = [wordninja.split(word) if word.isalpha() else [word] for word in words]
        
        # Join the corrected words to reconstruct the sentence
        corrected_sentence = ' '.join(''.join(subword) for subword in corrected_words)
        corrected_sentences.append(corrected_sentence)

    # Join the corrected sentences to reconstruct the text
    corrected_text = ' '.join(corrected_sentences)
    return corrected_text

# Open the PDF file
pdf_path = 'Abraham-Silberschatz-Operating-System-Concepts-10th-2018.pdf'

start_page = int(input("Enter the starting page (0-based): "))
end_page = int(input("Enter the ending page (0-based): "))

with pdfplumber.open(pdf_path) as pdf:
    paragraphs = []

    for page_num in range(start_page, end_page + 1):
        page = pdf.pages[page_num]
        paragraphs.extend(extract_paragraphs_from_page(page))

# Print the extracted paragraphs
for paragraph in paragraphs:
    print(correct_text(paragraph))