import streamlit as st
import ollama
import requests
import logging
from datetime import datetime
import os
import json

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Set up logging
log_file = os.path.join('logs', 'converter.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_installed_models():
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Ollama API response: {json.dumps(data)}")
            models = [model['name'] for model in data['models']]
            logger.info(f"Found models: {models}")
            return models
        else:
            logger.error(f"Failed to fetch models: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error fetching models: {str(e)}")
        return []

def get_log_contents(max_lines=100):
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()[-max_lines:]
                return ''.join(lines)
        return "No logs available yet."
    except Exception as e:
        logger.error(f"Error reading logs: {str(e)}")
        return f"Error reading log file: {str(e)}"

def save_markdown_file(content, filename):
    try:
        file_path = os.path.join('output', filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    except Exception as e:
        logger.error(f"Error saving markdown file: {str(e)}")
        raise

def convert_url_to_markdown(url, selected_model):
    logger.info(f"Starting conversion for URL: {url} using model: {selected_model}")
    
    jina_url = f"https://r.jina.ai/{url}"
    logger.info(f"Processed URL: {jina_url}")
    
    try:
        response = requests.get(jina_url)
        if response.status_code == 200:
            chat_response = ollama.chat(
                model=selected_model,
                messages=[{
                    'role': 'user',
                    'content': f'Convert this HTML to markdown: {response.text}'
                }]
            )
            markdown_content = chat_response['message']['content']
            logger.info(f"Successfully converted URL: {url}")
            return markdown_content
        else:
            error_msg = f"Failed to fetch URL: {response.status_code}"
            logger.error(error_msg)
            raise Exception(error_msg)
                
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        raise

def get_source_code():
    try:
        with open(__file__, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading source code: {str(e)}"

def main():
    st.set_page_config(page_title="Website to Markdown Converter", layout="wide")
    
    # Create tabs
    tab_converter, tab_logs, tab_help, tab_code = st.tabs(["Converter", "Logs", "Help", "Code"])
    
    with tab_converter:
        st.title("Website to Markdown Converter")
        
        url = st.text_input("Enter the website URL:", value="https://ollama.com/")
        
        # Model selection
        models = get_installed_models()
        if not models:
            st.warning("No Ollama models found. Please ensure Ollama is running and models are installed.")
            st.info("To get started:")
            st.code("""
1. Install Ollama from https://ollama.com/download
2. Start the Ollama service
3. Install a model using: ollama pull mistral or your preferred model
            """)
            return
            
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_model = st.selectbox(
                "Select an Ollama model:",
                options=models
            )
        
        with col2:
            save_locally = st.checkbox("Save .md file locally", value=True)
        
        if st.button("Convert to Markdown"):
            if not url:
                st.error("Please enter a URL")
                logger.warning("Conversion attempted without URL")
                return
                
            try:
                with st.spinner("Converting..."):
                    markdown_content = convert_url_to_markdown(url, selected_model)
                    st.markdown(markdown_content)
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"converted_{timestamp}.md"
                    
                    if save_locally:
                        file_path = save_markdown_file(markdown_content, filename)
                        st.success(f"File saved locally: {file_path}")
                    
                    st.download_button(
                        "Download Markdown",
                        markdown_content,
                        file_name=filename
                    )
            except Exception as e:
                st.error(f"Error processing request: {str(e)}")
    
    with tab_logs:
        st.title("Conversion Logs")
        logs = get_log_contents()
        st.text_area("Recent Logs", value=logs, height=400)
        if st.button("Refresh Logs"):
            st.experimental_rerun()
    
    with tab_help:
        st.title("Help & Instructions")
        st.markdown("""
        # Website to Markdown Converter - Help Guide

        ## Important Note
        ⚠️ This application runs locally and requires Ollama to be installed and running on your machine. It is not a cloud service.

        ## About the Service

        This local converter uses two components:
        1. **r.jina.ai**: A service that helps fetch and clean web content
        2. **Ollama**: A local AI model running on your machine that converts the content to Markdown

        ### System Requirements
        - A computer running Windows, macOS, or Linux
        - At least 8GB RAM (16GB recommended)
        - Sufficient disk space for Ollama models (typically 4-8GB per model)
        - Active internet connection for fetching web content
        
        ### How It Works
        - The app runs on your local machine
        - Web content is fetched through r.jina.ai
        - Conversion is performed locally using your installed Ollama model
        - No data is sent to external AI services
        
        ### How r.jina.ai Works
        - When you enter a URL like `example.com`, it's processed as `https://r.jina.ai/example.com`
        - This service helps bypass CORS issues and cleans the HTML content
        - It makes web content more accessible for conversion

        ## Getting Started

        ### Prerequisites
        1. **Install Ollama**
           - Download from [ollama.com/download](https://ollama.com/download)
           - Follow installation instructions for your operating system
           - Verify installation by running `ollama --version` in terminal

        2. **Install a Language Model**
           - Open terminal
           - Run: `ollama pull mistral` (recommended)
           - Or choose another model: `ollama pull llama2`

        3. **Start Ollama Service**
           - Ensure Ollama is running in the background
           - On most systems, it starts automatically
           - If needed, start manually: `ollama serve`

        ## Using the Converter

        ### Basic Usage
        1. Enter the website URL (without https://r.jina.ai/)
        2. Select your installed Ollama model
        3. Choose whether to save the .md file locally
        4. Click "Convert to Markdown"
        5. Use the "Download Markdown" button or find the file in the 'output' folder

        ### Output Options
        - **Download Button**: Directly download the converted markdown
        - **Local Save**: Files are saved in the 'output' directory if enabled
        - **Preview**: See the converted markdown directly in the app

        ### Tips for Best Results
        - Enter complete URLs (including https://)
        - Start with simple web pages
        - Check the logs if conversion fails
        - Ensure stable internet connection

        ## Troubleshooting

        ### Common Issues and Solutions

        1. **No Models Available**
           - Verify Ollama is running (`ollama list`)
           - Install at least one model (`ollama pull mistral`)
           - Restart the application

        2. **Conversion Fails**
           - Check URL accessibility
           - Verify internet connection
           - Check logs for specific errors
           - Try a different model

        3. **Slow Conversion**
           - Large websites take longer
           - Complex pages need more processing
           - Consider using a faster model

        ### Need More Help?
        - Check the Logs tab for detailed error messages
        - Visit [Ollama's documentation](https://github.com/ollama/ollama)
        - Review the source code in the Code tab
        - Ensure your system meets minimum requirements
        """)

    with tab_code:
        st.title("Source Code")
        st.markdown("""
        This tab contains the complete source code for this application. 
        You can copy and modify it for your own use.
        """)
        st.code(get_source_code(), language="python")

if __name__ == "__main__":
    main()