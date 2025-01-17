import os
import json
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extracts the text content from the PDF file, structured by pages.
    Returns a dictionary with page numbers as keys.
    """
    extracted_data = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            extracted_data[f"Page_{i}"] = page.extract_text() or ""
    return extracted_data

def process_pdfs(input_dir, output_file):
    """
    Processes all PDFs in the input directory and consolidates their data into a single JSON file.
    """
    all_pdfs_data = {}

    pdf_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the input directory.")
        return

    print(f"Found {len(pdf_files)} PDF files.")

    for file_path in pdf_files:
        print(f"Processing: {file_path}")
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

    # Save all data to a single JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_pdfs_data, f, ensure_ascii=False, indent=4)

    print(f"Saved all PDF data to: {output_file}")

def main():
    input_dir = "./pdfs"
    output_file = "./output/all_pdfs.json"

    if not os.path.exists("./output"):
        os.makedirs("./output")

    process_pdfs(input_dir, output_file)

if __name__ == "__main__":
    main()
