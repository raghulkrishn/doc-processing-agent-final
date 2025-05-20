import os
import fitz  # PyMuPDF
import openai
import pandas as pd
from dotenv import load_dotenv
import json
import time

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Extract text from PDF
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Wrapper to call OpenAI Chat API
def call_openai(messages, temperature=0.2):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

# Parse JSON safely from model output
def parse_json_safe(json_string):
    try:
        start = json_string.find('{')
        end = json_string.rfind('}') + 1
        json_str = json_string[start:end]
        return json.loads(json_str)
    except Exception as e:
        print(f"⚠️ JSON parse error: {e}")
        return None

# Agent for extracting a specific part
def extract_part(text, part_name, json_schema, retries=2):
    prompt = f"""
Extract the {part_name} from the resume text below.
Respond ONLY in this JSON format exactly as shown:
{json.dumps(json_schema, indent=2)}

Resume text:
{text}
"""
    for attempt in range(retries):
        output = call_openai([
            {"role": "system", "content": "You are a helpful assistant for parsing resumes."},
            {"role": "user", "content": prompt}
        ])
        data = parse_json_safe(output)
        if data and all(k in data for k in json_schema.keys()):
            return data
        else:
            print(f"❌ Attempt {attempt + 1} failed to extract {part_name}. Retrying...")
            time.sleep(1)

    print(f"❌ Failed to extract {part_name} after {retries} attempts.")
    return {k: "" for k in json_schema.keys()}

# Agent to validate and refine all extracted parts
def validate_and_refine(data, text):
    prompt = f"""
Given the extracted resume data below:

{json.dumps(data, indent=2)}

And the resume text:

{text}

Fix or add any missing or incorrect fields.
Respond ONLY in the same JSON format — no extra comments.
"""
    output = call_openai([
        {"role": "system", "content": "You are a helpful assistant for refining parsed resume data."},
        {"role": "user", "content": prompt}
    ])
    refined = parse_json_safe(output)
    return refined if refined else data

# Main agentic function combining all steps
def agentic_resume_parser(text):
    contact_schema = {"full_name": "", "email": "", "phone": ""}
    education_schema = {"education": ""}
    work_schema = {"work_experience": ""}
    skills_schema = {"skills": ""}

    contact = extract_part(text, "contact info (full name, email, phone)", contact_schema)
    education = extract_part(text, "education details", education_schema)
    work = extract_part(text, "work experience", work_schema)
    skills = extract_part(text, "skills", skills_schema)

    combined = {**contact, **education, **work, **skills}
    final_data = validate_and_refine(combined, text)
    return final_data

# Process all resumes in the folder
def process_resumes(folder_path):
    results = []

    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return results

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            print(f"\n📄 Processing: {file_name}")
            try:
                text = extract_text_from_pdf(file_path)
                if not text.strip():
                    print(f"⚠️ Empty PDF text in: {file_name}")
                    continue
                data = agentic_resume_parser(text)
                data["file_name"] = file_name
                results.append(data)
            except Exception as e:
                print(f"❌ Error processing {file_name}: {e}")

    return results

# Run the agentic resume parser
if __name__ == "__main__":
    folder = "resumes"
    output_file = "output.csv"
    all_data = process_resumes(folder)

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(output_file, index=False)
        print(f"\n✅ Done! Extracted data saved to: {output_file}")
    else:
        print("⚠️ No valid data extracted.")
