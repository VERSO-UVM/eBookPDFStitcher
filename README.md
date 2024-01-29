# eBookPDFStitcher

## Overview

This repository contains a simple application, initially developed as a Python script, designed to address the specific need of stitching together PDFs. The primary use case is to facilitate the creation of lendable digital copies of books for libraries. Publishers often release books with chapters in separate PDF documents, and this tool aims to provide an easy and cost-effective solution for combining them into a single PDF.

The project started as a basic Python script with a simple user interface. Users can select a folder containing PDFs (assuming file names are in descending order) and specify a location to save the combined file. The initial version served its purpose and received positive feedback during a demonstration to the primary user. Subsequently, there was a request to explore options such as turning it into a Chrome extension or a standalone application for more convenient use.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Installation
**Clone the repository**
git clone [https://github.com/yourusername/yourproject.git](https://github.com/VERSO-UVM/eBookPDFStitcher.git)

**Navigate to the project directory**
pdf_files contain sample pdfs for testing scripts

**Install dependencies**
You will need to install the following Python Packages
* PySimpleGUI
* PyPDF2 
* fitz
* os
* tempfile
* shutil

# Usage

This project is for general use in stitching together sequencial PDFs while following the copyright for those documents. 

## Contributing

There are several ways you can contribute to this project:

1. **Bug Reports:**
   - If you find a bug or issue, please [open a new issue](../../issues) with a detailed description.
   - Include steps to reproduce the bug if possible.
   - Mention the version of the project where the issue occurred.

2. **Feature Requests:**
   - If you have a feature in mind that you'd like to see, [open a new issue](../../issues) and describe the proposed feature.
   - Include any relevant use cases or scenarios.

3. **Pull Requests:**
   - Feel free to submit pull requests for bug fixes or new features.
   - Before submitting, ensure your code follows the project's coding standards.
   - Clearly describe the purpose of your pull request.

4. **Documentation:**
   - Help improve the project's documentation.
   - Fix typos, clarify explanations, or add missing information.

### Getting Started

1. Fork the project repository.
2. Create a new branch for your contributions (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request explaining your changes.

## Code of Conduct

Please note that we have a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.


## License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Acknowledgements

This project would not be possible without the contributions of Tamunotonye Harry

## Answered FAQ
Do the books tend to stick to a similar layout, or does it vary from one book to another? For instance, do they typically include elements like title pages and page numbers in consistent locations, or is it more diverse?
*Layouts vary some, but almost all books will have a title page and page numbers in consistent locations.*

Do the dimensions of the pdfs often vary between chapters (so from a letter to a legal size) in a set of scans?
*All books are consistent chapter to chapter.*

Is there a max number of individual PDF chapters for a given book the tool will need to handle and merge?
*Rare to see an academic book with more than 50 chapters*
