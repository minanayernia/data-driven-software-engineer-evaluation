import os
import json
import logging
import pdfplumber

# Set up logging
logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

import pdfplumber
import logging
import os

import pdfplumber
import logging

import pdfplumber
import logging

import pdfplumber
import logging

def extract_text_from_pdf(pdf_path):
    extracted_data = {}
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if len(pdf.pages) == 0:
                raise ValueError("PDF has no pages")
            
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text is None:
                    extracted_data[f"Page_{i}"] = "No text found"
                else:
                    extracted_data[f"Page_{i}"] = text

        logging.info(f"Successfully extracted text from: {pdf_path}")
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path}: {e}")
        extracted_data["error"] = "Error extracting text from PDF"
    return extracted_data



def process_pdfs(input_dir, output_file):
    """
    Processes all PDF files in the input directory and consolidates their content into a single JSON file.
    """
    all_pdfs_data = {}

    # Get list of PDF files
    pdf_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.pdf')]

    if not pdf_files:
        logging.warning("No PDF files found in the input directory.")
        return

    logging.info(f"Found {len(pdf_files)} PDF files to process.")

    # Process each PDF
    for file_path in pdf_files:
        try:
            logging.info(f"Processing: {file_path}")
            pdf_name = os.path.basename(file_path)
            pdf_content = extract_text_from_pdf(file_path)

            # Add metadata
            metadata = {
                "file_name": pdf_name,
                "total_pages": len(pdf_content)
            }
            pdf_content["metadata"] = metadata

            # Add to consolidated data
            all_pdfs_data[pdf_name] = pdf_content
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            continue

    # Save all data to a single JSON file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_pdfs_data, f, ensure_ascii=False, indent=4)
        logging.info(f"Saved all PDF data to: {output_file}")
    except Exception as e:
        logging.error(f"Error saving JSON file: {e}")

def main():
    # Define directories
    input_dir = "./pdfs"
    output_file = "./output/all_pdfs.json"

    # Create output directory if it doesn't exist
    if not os.path.exists("./output"):
        os.makedirs("./output")

    process_pdfs(input_dir, output_file)

if __name__ == "__main__":
    main()
