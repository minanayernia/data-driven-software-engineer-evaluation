import os
import multiprocessing
import pdfplumber
import csv


def extract_data_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''.join(page.extract_text() for page in pdf.pages)
        return text
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def save_to_csv(data, output_path):
    try:
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving data: {e}")

def process_pdf(file_path, output_dir):
    print(f"Processing: {file_path}")
    data = extract_data_from_pdf(file_path)
    if data:
        # For this example, splitting data into lines and saving as rows
        structured_data = [line.split() for line in data.split('\n') if line.strip()]
        output_file = os.path.join(output_dir, os.path.basename(file_path).replace('.pdf', '.csv'))
        save_to_csv(structured_data, output_file)

def main():
    input_dir = "./pdfs"
    output_dir = "./output"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.pdf')]

    if not pdf_files:
        print("No PDF files found in the input directory.")
        return

    print(f"Found {len(pdf_files)} PDF files.")

    # Using multiprocessing for scalability
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.starmap(process_pdf, [(file, output_dir) for file in pdf_files])

if __name__ == "__main__":
    main()
