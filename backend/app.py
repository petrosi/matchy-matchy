from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import PyPDF2
import io
from dotenv import load_dotenv
import json
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

# Hugging Face API configuration
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
# HUGGINGFACE_API_KEY = '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'
# Using a more accessible model that doesn't require special permissions
API_URL = "https://api-inference.huggingface.co/models/gpt2"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def create_analysis_prompt(cv_text, job_description):
    """Create a structured prompt for CV analysis"""
    return f"""
    <|prompter|>\n
    Here are the CV of a candidate and a job description:

    CV: {cv_text[:1000]}

    Job: {job_description[:1000]}
    
    Perform an analysis of the follwing: 
        Does the candidate has relevant experience and skills?
        How much does the profile match?
        What are the strengths? 
        What are the weaknesses?
        What are the suggestions?

    Return the analysis in a structured format like:
    {{
        "general_analysis": "The candidate has relevant experience and skills. Match: 75%. Strengths: Technical background, relevant experience. Weaknesses: Could use more specific examples. Suggestions: Add project examples, include certifications.",
        "match_percentage": "75",
        "strengths": ["Technical background", "relevant experience"],
        "weaknesses": ["Could use more specific examples"],
        "suggestions": ["Add project examples", "include certifications"]
    }}
    <|endoftext|><|assistant|>
    """

def analyze_with_llm(cv_text, job_description):
    """Analyze CV against job description using Hugging Face InferenceClient"""
    from huggingface_hub import InferenceClient

    prompt = create_analysis_prompt(cv_text, job_description)

    try:
        print(f"Connecting to Hugging Face with token: {HUGGINGFACE_API_KEY[:10]}...")

        # Use instruction-tuned model
        client = InferenceClient(
            provider="novita", 
            api_key=HUGGINGFACE_API_KEY
        )

        parameters = {
            "max_new_tokens": 300,
            "temperature": 0.7,
            "do_sample": True,
            "top_p": 0.9,
            "stream": False,
        }

        print("Calling text_generation...")
        result = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        # ✅ Robust handling of all result types (generator or plain string)
        try:
            generated_text = ''.join(part.token.text for part in result)
        except (AttributeError, TypeError):
            generated_text = result.choices[0].message['content']

        print(f"Generated text: {generated_text}")

        # Try to extract structured analysis
        if generated_text and any(kw in generated_text.lower() for kw in ["match", "strength", "weakness"]):
            analysis_result = format_response(generated_text)
            analysis_result["is_fallback"] = False
            return analysis_result
        else:
            return {
                **create_fallback_analysis(cv_text, job_description),
                "is_fallback": True,
                "fallback_reason": "LLM response was not structured properly"
            }

    except Exception as e:
        error_msg = str(e) or f"Unknown error: {type(e).__name__}"
        print(f"LLM Analysis Error: {error_msg}")
        return {
            **create_fallback_analysis(cv_text, job_description),
            "is_fallback": True,
            "fallback_reason": f"Connection error: {error_msg}"
        }

def format_response(llm_response):
    """
    Parse and enhance the LLM response for CV/job analysis.
    This function uses the LLM's output to extract and supplement analysis details.
    """
    import re

    # Try to extract structured fields from the LLM response using regex
    def extract_field(pattern, text, default=None):
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return default

    # Extract fields from LLM response - improved patterns
    # Look for match percentage in various formats
    match_patterns = [
        r"match\s*[:\-]?\s*(\d{1,3})\%?",
        r"(\d{1,3})\%\s*match",
        r"matches?\s*(\d{1,3})\%",
        r"profile\s*match[:\-]?\s*(\d{1,3})\%?"
    ]
    
    match_pct = None
    for pattern in match_patterns:
        match_pct = extract_field(pattern, llm_response)
        if match_pct:
            break
    
    strengths = extract_field(r"strengths?\s*[:\-]?\s*(.*?)(?:weakness|suggestion|$)", llm_response)
    weaknesses = extract_field(r"weaknesses?\s*[:\-]?\s*(.*?)(?:suggestion|$)", llm_response)
    suggestions = extract_field(r"suggestions?\s*[:\-]?\s*(.*)", llm_response)

    # Helper to split comma/semicolon lists - preserve case for suggestions
    def split_items(s, preserve_case=False):
        if not s:
            return []
        items = re.split(r"[,;\n]", s)
        if preserve_case:
            return [item.strip() for item in items if item.strip()]
        else:
            return [item.strip().capitalize() for item in items if item.strip()]

    strengths_list = split_items(strengths)
    weaknesses_list = split_items(weaknesses)
    suggestions_list = split_items(suggestions, preserve_case=True)  # Preserve case for suggestions

    # Limit to top 3 for each
    return {
        "match_percentage": match_pct,
        "strengths": strengths_list[:3],
        "weaknesses": weaknesses_list[:3],
        "suggestions": suggestions_list[:3]
    }

def create_fallback_analysis(cv_text, job_description):
    """Create a basic analysis when LLM fails"""
    
    # Simple keyword matching
    cv_lower = cv_text.lower()
    job_lower = job_description.lower()
    
    # Common technical skills
    tech_skills = ['python', 'javascript', 'java', 'react', 'node.js', 'aws', 'docker', 'kubernetes', 'sql', 'mongodb']
    soft_skills = ['leadership', 'communication', 'teamwork', 'problem solving', 'project management']
    
    # Count matches
    tech_matches = sum(1 for skill in tech_skills if skill in cv_lower and skill in job_lower)
    soft_matches = sum(1 for skill in soft_skills if skill in cv_lower and skill in job_lower)
    
    # Calculate match percentage
    total_skills = len(tech_skills) + len(soft_skills)
    match_percentage = min(95, max(40, int((tech_matches + soft_matches) / total_skills * 100 + 30)))
    
    # Generate strengths and weaknesses based on content
    strengths = []
    weaknesses = []
    suggestions = []
    
    if 'experience' in cv_lower:
        strengths.append("Has relevant work experience")
    else:
        weaknesses.append("Limited work experience")
        suggestions.append("Add relevant work experience or internships")
    
    if any(skill in cv_lower for skill in tech_skills):
        strengths.append("Technical skills present")
    else:
        weaknesses.append("Missing technical skills")
        suggestions.append("Add relevant technical skills")
    
    if 'education' in cv_lower or 'degree' in cv_lower:
        strengths.append("Educational background present")
    else:
        weaknesses.append("Education information missing")
        suggestions.append("Include educational background")
    
    if 'project' in cv_lower:
        strengths.append("Project experience mentioned")
    else:
        suggestions.append("Add specific project examples")
    
    if not strengths:
        strengths = ["Good foundation for the role"]
    if not weaknesses:
        weaknesses = ["Could use more specific examples"]
    if not suggestions:
        suggestions = ["Add quantifiable achievements", "Include relevant certifications"]
    
    return {
        "match_percentage": str(match_percentage),
        "strengths": strengths[:3],
        "weaknesses": weaknesses[:3],
        "suggestions": suggestions[:3]
    }

@app.route('/api/analyze', methods=['POST'])
def analyze_cv():
    """Main endpoint for CV analysis"""
    try:
        if 'cv_file' not in request.files:
            return jsonify({'error': 'No CV file uploaded'}), 400
        
        cv_file = request.files['cv_file']
        job_description = request.form.get('job_description', '')
        
        if cv_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not job_description.strip():
            return jsonify({'error': 'Job description is required'}), 400
        
        # Extract text from PDF
        cv_text = extract_text_from_pdf(cv_file)
        
        if cv_text.startswith('Error'):
            return jsonify({'error': cv_text}), 400
        
        # Analyze with LLM
        analysis = analyze_with_llm(cv_text, job_description)
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'CV Analysis API is running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)