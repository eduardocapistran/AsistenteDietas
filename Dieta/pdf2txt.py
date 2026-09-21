import PyPDF2
import argparse

def pdf_to_text(pdf_path, output_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Check if the PDF has any pages
        if len(pdf_reader.pages) > 0:
            text = ""
            
            # Loop through each page in the PDF
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
                
            # Write the text to a text file
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            
            print(f"Text extracted from {pdf_path} and saved to {output_path}")
        else:
            print(f"No pages found in {pdf_path}")

def main():
    parser = argparse.ArgumentParser(description='Convert PDF to text')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    parser.add_argument('output_path', type=str, help='Path to the output text file')
    
    args = parser.parse_args()
    
    pdf_to_text(args.pdf_path, args.output_path)

if __name__ == "__main__":
    main()

