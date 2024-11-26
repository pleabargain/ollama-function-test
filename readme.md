# Website to Markdown Converter

A local Streamlit application that converts web pages to Markdown format using Ollama's local AI models and r.jina.ai for content fetching.

## ⚠️ Important Note
This is a local application that requires Ollama to be installed and running on your machine. It is not a cloud service.

## System Requirements

- A computer running Windows, macOS, or Linux
- Python 3.8 or higher
- At least 8GB RAM (16GB recommended)
- Sufficient disk space for Ollama models (typically 4-8GB per model)
- Active internet connection for fetching web content

## Features

- Convert any website to Markdown format using local AI processing
- Uses Ollama's local AI models for secure, private conversions
- Clean web content fetching via r.jina.ai
- Save converted files locally
- Download converted Markdown files
- Detailed logging system
- User-friendly interface with help documentation

## Prerequisites

1. **Python 3.8+**
2. **Ollama (Required)**
   - Download from [ollama.com/download](https://ollama.com/download)
   - Install following the instructions for your OS
   - Verify installation: `ollama --version`
   - Must be running locally on your machine

3. **Required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

## Installation

1. Clone this repository:
   ```bash
   git clone [your-repository-url]
   cd website-to-markdown-converter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install an Ollama model locally:
   ```bash
   ollama pull mistral  # recommended model
   ```

## Usage

1. Start the local Ollama service:
   ```bash
   ollama serve
   ```

2. Run the Streamlit app locally:
   ```bash
   streamlit run main.py
   ```

3. Open your browser and navigate to the local URL (typically http://localhost:8501)

## Application Structure

