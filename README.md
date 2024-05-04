# SEC 10K Filing Analyzer

## Overview
This repository contains code for analyzing SEC 10K filings of any company using a Language Model (LM) provided by OpenAI. The main focus of this project is to extract insights from the Business, Risk, and Management's Discussion and Analysis (MDA) sections of the filings. Additionally, the code generates graphs illustrating important financial statements of the company.

## Features
- Downloads sec 10 K data of any company from the Input Box.
- Analyze SEC 10K filings to extract insights on Business, Risk, and MDA sections.
- Generate graphs depicting key financial statements of the company.
- Utilizes OpenAI API for language analysis.
- Utilizes SEC Edgar Downloader to obtain 10K filings.
- Utilizes SEC API for financial data retrieval.

## Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/kaybee128/Sec-10k-analysis.git
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Ensure you have obtained an API key from OpenAI and SEC API.
2. Set up the API keys in the appropriate configuration files.
3. Run the Python scripts to analyze the 10K filings and generate graphs:
   ```bash
   python app.py
   ```
## Demo
https://drive.google.com/file/d/1pD-nq-53WAcgLco8AMfcSF5Tzmch-3FI/view?usp=sharing   

## Tech Stack
1. FrontEnd- HTML + Javascript: They iare one of the most commonly used tech stack for front end development. It is easy to comprehend and is compatible with almost all backend tools.
2. BackEnd- Python + Flask: Chose python due to its succinctness and readability, allowing to accomplish tasks efficiently with minimal code, sometimes just a single line.  Flask is a python based backend which produces websites which are quick-loading and scalable.
3. Other Tools and API: sec-edgar-downloader, sec_api, sec-downloader: used them to download sec 10K filings and easy segregation of sections. Matplotlib for plotting the graph, bs4 for parsing HTML pages and extracting important information from it. Openai library for using the generative AI model for analysing the text.

## Contributing
Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to open an issue or submit a pull request.
