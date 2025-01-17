
# PDF Processor

This script extracts text from PDF files and saves the content in a consolidated JSON file. It is designed to handle multiple PDFs, ensure scalability, and log the processing details for debugging and review.

## Features
- Extracts text from all pages of PDF files.
- Consolidates extracted content into a single JSON file.
- Includes metadata such as file name and total pages.
- Handles errors gracefully and logs them for review.


## Requirements
- Python 3.7+
- Install dependencies using:
  ```bash
  pip install pdfplumber
  ```

## How to Use
1. Place all PDF files to be processed in the `./pdfs` folder.
2. Run the script:
   ```bash
   python pdf_processor.py
   ```
3. Check the consolidated JSON file at `./output/all_pdfs.json`.
4. Review logs in `app.log` for details of the processing.

## Output
The JSON file will have the following structure:
```json
{
    "sample1.pdf": {
        "Page_1": "Text content from page 1...",
        "Page_2": "Text content from page 2...",
        "metadata": {
            "file_name": "sample1.pdf",
            "total_pages": 2
        }
    },
    "sample2.pdf": {
        "Page_1": "Text content from page 1...",
        "metadata": {
            "file_name": "sample2.pdf",
            "total_pages": 1
        }
    }
}
```

## Logging
Logs are saved to `app.log` with details of processed files, warnings, and errors.

## Error Handling
- Handles malformed PDFs gracefully and logs errors.
- Skips files with issues and continues processing the rest.

## Scalability
- The script uses a modular approach and can handle large numbers of files efficiently.
- Additional enhancements like multiprocessing can be added for parallel processing.


# PDF Processor - Testing

This project includes unit tests for the PDF extraction functionality using `pytest`. The tests cover different scenarios, such as valid PDFs, PDFs with no text, malformed PDFs, and corrupted PDFs.

## Running Tests

To run the tests, use `pytest`:

```bash
pytest test_pdf_processor.py
```

### Test Scenarios

1. **Valid Multi-Page PDF**: Verifies that text is correctly extracted from a PDF with multiple pages.
2. **PDF with No Text**: Simulates a PDF with no extractable text and ensures that `"No text found"` is returned.
3. **Malformed PDF**: Simulates a malformed PDF (non-PDF file with `.pdf` extension) and checks proper error handling.
4. **Corrupted PDF**: Tests the handling of corrupted PDFs (using random binary data).
5. **Processing Multiple PDFs**: Verifies that a directory of PDFs is processed and their extracted data is consolidated into a JSON file.

### Test Output

After running the tests, you should see output indicating whether the tests passed or failed. If a test fails, details about the error will be provided.

## Requirements

Ensure you have the following dependencies installed:

- `pytest`
- `pdfplumber`
- `fpdf`
