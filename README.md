# doc-processing-agent-final
🧠 Agentic Resume Parser with OpenAI (GPT-3.5)
This project is an intelligent resume parsing tool that uses agentic flow with OpenAI's GPT-3.5 model to extract structured data from unstructured PDF resumes. It extracts key information such as name, email, phone number, education, experience, and skills, and exports everything to a clean CSV file.

🚀 Features
✅ PDF text extraction using PyMuPDF (fitz)

✅ Agentic flow with step-by-step extraction and validation

✅ Uses OpenAI’s gpt-3.5-turbo for fast and cost-effective parsing

✅ Retry mechanism if JSON format fails

✅ Data refinement for more accurate results

✅ Output saved to output.csv

🧠 What Is Agentic Flow?
Instead of relying on a single prompt, agentic flow breaks down the parsing process into smaller “agents” or steps:

Agent 1: Extracts contact details (name, email, phone)

Agent 2: Extracts education information

Agent 3: Extracts work experience

Agent 4: Extracts skills

Agent 5 (Validator): Validates and refines all the combined data using full resume context

This modular approach improves robustness, accuracy, and interpretability.

📂 Folder Structure
bash
Copy
Edit
resume_agentic_project/
│
├── main.py               # Main Python script
├── .env                  # Your OpenAI API key (not committed)
├── output.csv            # Final extracted data
└── resumes/              # Folder to place your input PDF resumes
🛠️ Installation
Clone the repo:

bash
Copy
Edit
git clone https://github.com/yourusername/resume-agentic-parser.git
cd resume-agentic-parser
Set up virtual environment:

bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Add your OpenAI key:

Create a .env file with:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_key_here
📄 Usage
Put your resumes (PDFs) inside the resumes/ folder.

Run the script:

bash
Copy
Edit
python main.py
