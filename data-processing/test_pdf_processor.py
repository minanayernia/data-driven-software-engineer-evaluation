import os
import pytest
import json
from pdf_processor import extract_text_from_pdf, process_pdfs
from fpdf import FPDF

from fpdf import FPDF

def create_valid_pdf(pdf_path):
    """Creates a simple multi-page PDF for testing."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add first page
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is the first page.", ln=True)
    
    # Add second page
    pdf.add_page()
    pdf.cell(200, 10, txt="This is the second page.", ln=True)
    
    # Save the PDF to the specified path
    pdf.output(pdf_path)

def create_no_text_pdf(pdf_path):
    """Creates an empty PDF with no extractable text."""
    pdf = FPDF()
    pdf.add_page()
    pdf.output(pdf_path)


@pytest.fixture
def mock_pdf_files(tmpdir):
    """Fixture to create test PDFs in a temporary directory."""
    pdf_dir = tmpdir.mkdir("pdfs")

    # Create a valid multi-page PDF
    create_valid_pdf(pdf_dir.join("multi_page.pdf"))

    # Create a PDF with no text content (you could create an empty PDF or one with no extractable text)
    with open(pdf_dir.join("no_text.pdf"), "w") as f:
        f.write("")  # Empty content

    # Create a malformed PDF (simulate by saving a non-PDF file with .pdf extension)
    with open(pdf_dir.join("malformed.pdf"), "w") as f:
        f.write("This is not a valid PDF file.")

    # Create a corrupted PDF (you could simulate a corrupted file by truncating an actual PDF)
    with open(pdf_dir.join("corrupted.pdf"), "wb") as f:
        f.write(b'\x00\x01\x02\x03')  # Random binary data

    return pdf_dir

def test_no_text_pdf(mock_pdf_files):
    """Test a PDF with no text content."""
    pdf_path = mock_pdf_files.join("no_text.pdf")
    result = extract_text_from_pdf(str(pdf_path))
    assert "Page_1" in result
    assert result["Page_1"] == "No text found"


def test_malformed_pdf(mock_pdf_files):
    """Test handling of a malformed PDF."""
    pdf_path = mock_pdf_files.join("malformed.pdf")
    result = extract_text_from_pdf(str(pdf_path))
    assert "error" in result
    assert result["error"] == "Error extracting text from PDF"

def test_corrupted_pdf(mock_pdf_files):
    """Test handling of a corrupted PDF."""
    pdf_path = mock_pdf_files.join("corrupted.pdf")
    result = extract_text_from_pdf(str(pdf_path))
    assert "error" in result
    assert result["error"] == "Error extracting text from PDF"

def test_process_pdfs(mock_pdf_files, tmpdir):
    """Test the process_pdfs function."""
    output_file = tmpdir.join("output.json")
    process_pdfs(str(mock_pdf_files), str(output_file))
    assert os.path.exists(output_file)
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert "multi_page.pdf" in data
    assert "no_text.pdf" in data  # Ensure no_text.pdf is processed correctly
    assert "malformed.pdf" in data
    assert "corrupted.pdf" in data
