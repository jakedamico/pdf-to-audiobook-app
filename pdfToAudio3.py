import fitz
from gtts import gTTS
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QSpinBox, QDoubleSpinBox, QDialog

class PDFViewerWindow(QMainWindow):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.pdf_document = fitz.open(filepath)
        self.current_page_num = 0
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("PDF Viewer")

        layout = QVBoxLayout()
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        prev_button = QPushButton("Previous", self)
        prev_button.clicked.connect(self.show_previous_page)
        layout.addWidget(prev_button)

        next_button = QPushButton("Next", self)
        next_button.clicked.connect(self.show_next_page)
        layout.addWidget(next_button)

        extract_button = QPushButton("Extract Text", self)
        extract_button.clicked.connect(self.extract_text)
        layout.addWidget(extract_button)

        coordinates_button = QPushButton("Add Coordinates", self)
        coordinates_button.clicked.connect(self.show_coordinates_dialog)
        layout.addWidget(coordinates_button)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.show_page()

    def show_coordinates_dialog(self):
        dialog = CoordinatesInputDialog(self)
        dialog.exec_()

    def show_page(self):
        page = self.pdf_document[self.current_page_num]
        image = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        qt_image = QImage(image.samples, image.width, image.height, image.stride, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(pixmap)

    def show_previous_page(self):
        if self.current_page_num > 0:
            self.current_page_num -= 1
            self.show_page()

    def show_next_page(self):
        if self.current_page_num < len(self.pdf_document) - 1:
            self.current_page_num += 1
            self.show_page()

    def extract_text(self):
        coordinates = []
        dialog = CoordinatesInputDialog(self)
        if dialog.exec_():
            coordinates = dialog.get_coordinates()
        
        if coordinates:
            extracted_text = ""
            for coord in coordinates:
                page = self.pdf_document[coord[0]]
                extracted_text += page.get_text("text", clip=coord[1]).strip()

            tts = gTTS(text=extracted_text, lang='en')
            output_audio_path = 'extracted_text_audio.mp3'
            tts.save(output_audio_path)
            print(f"Text-to-speech audio saved as: {output_audio_path}")

    def closeEvent(self, event):
        self.pdf_document.close()
        event.accept()

class CoordinatesInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.coordinates = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Enter Coordinates")
        layout = QVBoxLayout()

        self.page_label = QLabel("Page Number:", self)
        layout.addWidget(self.page_label)

        self.page_input = QSpinBox(self)
        self.page_input.setMinimum(0)
        self.page_input.setMaximum(len(self.parent().pdf_document) - 1)
        layout.addWidget(self.page_input)

        self.x1_label = QLabel("x1 Coordinate:", self)
        layout.addWidget(self.x1_label)
        
        self.x1_input = QDoubleSpinBox(self)
        layout.addWidget(self.x1_input)

        self.y1_label = QLabel("y1 Coordinate:", self)
        layout.addWidget(self.y1_label)

        self.y1_input = QDoubleSpinBox(self)
        layout.addWidget(self.y1_input)

        self.x2_label = QLabel("x2 Coordinate:", self)
        layout.addWidget(self.x2_label)

        self.x2_input = QDoubleSpinBox(self)
        layout.addWidget(self.x2_input)

        self.y2_label = QLabel("y2 Coordinate:", self)
        layout.addWidget(self.y2_label)

        self.y2_input = QDoubleSpinBox(self)
        layout.addWidget(self.y2_input)

        add_button = QPushButton("Add Coordinates", self)
        add_button.clicked.connect(self.add_coordinates)
        layout.addWidget(add_button)

        extract_button = QPushButton("Extract Text", self)
        extract_button.clicked.connect(self.accept)
        layout.addWidget(extract_button)

        self.setLayout(layout)

    def add_coordinates(self):
        page_num = self.page_input.value()
        x1 = self.x1_input.value()
        y1 = self.y1_input.value()
        x2 = self.x2_input.value()
        y2 = self.y2_input.value()

        self.coordinates.append((page_num, (x1, y1, x2, y2)))
        self.x1_input.setValue(0)
        self.y1_input.setValue(0)
        self.x2_input.setValue(0)
        self.y2_input.setValue(0)

    def get_coordinates(self):
        return self.coordinates

def main():
    app = QApplication(sys.argv)
    filepath = 'Fooled-by-Randomness-Role-of-Chance-in-Markets-and-Life-PROPER1.pdf'
    viewer = PDFViewerWindow(filepath)
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
