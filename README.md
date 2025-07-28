## Overview
This project is designed for document analysis and processing of PDFs. It extracts meaningful content from scientific, technical, and financial documents and outputs structured JSON data. 
It was developed as part of the Adobe Hackathon.
## Project Structure
├── process_pdfs.py # Core script to process and extract content from PDFs
├── requirements.txt # List of Python dependencies
├── Dockerfile # Container configuration for deployment
└── sample_dataset/
├── pdfs/ # Sample PDF files
│ ├── *.pdf # Example documents
│ └── generate_50page_pdf.py # Script to generate large PDFs for testing
└── outputs/ # Extracted JSON outputs from the PDFs
