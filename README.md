# AI Document Analysis App

## Overview

AI Document Analysis App is an AI-powered tool designed to help undergraduate students quickly analyze and summarize academic documents. This application uses advanced natural language processing techniques to extract key information from PDF and Word documents, providing summaries and topic-specific notes to aid in studying and research.

## Features

- 📤 Upload PDF or Word documents for analysis
- 🔑 Specify key topics for focused note-taking
- 📚 Generate concise summaries of document content
- 🧠 Extract key points from the entire document
- 📝 Create topic-specific notes based on user input
- 🤖 Utilizes GPT-4o for intelligent text analysis
- 🎓 Explanations tailored for easy understanding (ELI5 style)

## Intended Use Case

This app is primarily designed for:
- Undergraduate students looking to quickly grasp main concepts from academic papers or textbooks
- Researchers needing to efficiently process and summarize large volumes of text
- Anyone seeking to extract key information from lengthy documents without reading them in full

## Setup Process

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/document-analysis-app.git
   cd document-analysis-app
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Running the App

1. Start the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Usage

1. Upload a PDF or Word document using the file uploader.
2. Enter topics you want to explore in the text area (one per line).
3. Click the "Analyze Document" button.
4. Review the generated summary, key points, and topic-specific notes.

## Contributing

We welcome contributions to improve Zahra's Document Analysis App! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with clear, descriptive messages.
4. Push your changes to your fork.
5. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the GPT-4o model
- Streamlit for the web app framework
- Langchain for document processing utilities

## Disclaimer

This tool is designed to assist with studying and research, not to replace thorough reading and critical thinking. Always verify important information and use this app as a supplement to your academic work, not a substitute.