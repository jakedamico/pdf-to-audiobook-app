import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

pdfName = 'Fooled-by-Randomness-Role-of-Chance-in-Markets-and-Life-PROPER1.pdf'
page_width = 419.5
page_height = 595.25

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.navigation_layout = QHBoxLayout()

        self.view_button = QPushButton("Open PDF", self)
        self.view_button.clicked.connect(self.open_pdf)
        self.navigation_layout.addWidget(self.view_button)

        self.previous_button = QPushButton("Previous", self)
        self.previous_button.clicked.connect(self.show_previous_page)
        self.navigation_layout.addWidget(self.previous_button)

        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.show_next_page)
        self.navigation_layout.addWidget(self.next_button)

        self.page_number_label = QLabel("Page:")
        self.navigation_layout.addWidget(self.page_number_label)

        self.page_number_input = QLineEdit()
        self.page_number_input.returnPressed.connect(self.go_to_page)
        self.navigation_layout.addWidget(self.page_number_input)

        self.layout.addLayout(self.navigation_layout)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.pdf_document = None
        self.current_page_num = 0

    def open_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        pdf_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if pdf_path:
            self.pdf_document = fitz.open(pdf_path)
            self.current_page_num = 0
            self.show_page()

    def show_previous_page(self):
        if self.pdf_document is None:
            return

        if self.current_page_num > 0:
            self.current_page_num -= 1
            self.show_page()

    def show_next_page(self):
        if self.pdf_document is None:
            return

        if self.current_page_num < len(self.pdf_document) - 1:
            self.current_page_num += 1
            self.show_page()

    def go_to_page(self):
        if self.pdf_document is None:
            return

        try:
            new_page_num = int(self.page_number_input.text()) - 1
            if 0 <= new_page_num < len(self.pdf_document):
                self.current_page_num = new_page_num
                self.show_page()
        except ValueError:
            pass

    def show_page(self):
        if self.pdf_document is None:
            return

        page = self.pdf_document[self.current_page_num]
        image = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        qt_image = QImage(image.samples, image.width, image.height, image.stride, QImage.Format_RGB888)

        # Scale down the image by a factor (e.g., 0.5) to make it slightly smaller
        scale_factor = 0.5
        new_width = int(qt_image.width() * scale_factor)
        new_height = int(qt_image.height() * scale_factor)
        scaled_image = qt_image.scaled(new_width, new_height, Qt.KeepAspectRatio)

        pixmap = QPixmap.fromImage(scaled_image)
        self.image_label.setPixmap(pixmap)

        self.page_number_input.setText(str(self.current_page_num + 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec_())