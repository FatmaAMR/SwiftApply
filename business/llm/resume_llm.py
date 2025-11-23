from groq import Groq
import json
from utils import get_settings

class resume_llm:
    def __init__(self):
        # Initialize the Groq client
        self.client = Groq(api_key=get_settings().GROQ_KEY)
        self.model_name=get_settings().GROQ_MODEL_NAME
    
    
    async def parse_cv(self, cv_text: str) -> dict:
        messages = [
            {"role": "system", "content": """You are a CV parsing assistant. 
            Return valid JSON with personal_info, education, skills, experience,
            achievements, certifications, extra information if exist."""},
            {"role": "user", "content": cv_text}
        ]

        response = self.client.chat.completions.create(
            model=self.model_name, 
            messages=messages,
            temperature=0.0,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )

        try:
            parsed_json = json.loads(response.choices[0].message.content)
        except Exception:
            parsed_json = {"raw_text": cv_text, "raw_llm_output": response.content}

        return parsed_json


    async def analyze_cv(self, parsed_cv: dict, job_description_text: str, notes: str, company_info: str) -> dict:
        """
        Analyze a candidate CV against a job description and company notes.
        Returns structured JSON with match_score, missing skills, recommended keywords, etc.
        """
        prompt = f"""
        You are an HR expert. Analyze the candidate CV below against the Job Description and Company Notes. 
        Identify missing skills, recommended improvements, and calculate an overall match score (0-100).

Candidate CV JSON:
{json.dumps(parsed_cv)}

Job Description:
{job_description_text}

Company Notes:
{company_info}

Consider the following:
{notes}

Return ONLY valid JSON (no markdown, no explanation) with these exact keys:
- match_score (integer 0-100)
- missing_skills (list of strings)
- recommended_keywords (list of strings)
- sections_to_improve (list of strings)
- strengths (list of strings)
- overall_feedback (string, 2-3 sentences)
"""
        messages = [
            {"role": "system", "content": "You are an expert HR evaluator. Always respond with clean JSON only."},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat.completions.create(
    model=self.model_name,  
    messages=messages,
    temperature=0.0,
    max_tokens=3000,
    response_format={"type": "json_object"}
)
            analysis_json = json.loads(response.choices[0].message.content)
        except Exception:
            analysis_json = {
                "raw_analysis": getattr(response, 'content', None),
                "error": "Failed to parse JSON from LLM"
            }
        return analysis_json

    async def generate_cv(self, parsed_cv: dict, analysis: dict, job_description_text:str, company_info:str) -> dict:
        """
        Generate a final CV JSON using the parsed CV and analysis.
        """
        prompt = f"""
            Generate:
            1. Parsed, customized to the job description used to get the analysis results, CV structured into clear sections.
            2. A professional cover letter tailored to the CV.
            3. A professional email template for sending the CV and cover letter.
            4. Recommended sections for improving the CV based on gaps.
            5. Detect missing or incomplete sections and list them.
            6. If some sections in the CV text are empty or unclear, return empty arrays or empty strings — do NOT invent content.
            7. The JSON MUST be strictly valid and follow this exact structure:

            {{
            "cv": {{
                "header": {{}},
                "summary": "",
                "skills": [],
                "experience": [],
                "education": [],
                "projects": [],
                "certifications": [],
                "languages": [],
                "tools": [],
                "additional_sections": {{}}
            }},
            "cover_letter": {{
                "content": "",
                "tone": "",
                "length": ""
            }},
            "email_template": {{
                "subject": "",
                "body": ""
            }},
            "metadata": {{
                "recommended_sections": [],
                "missing_sections": [],
                "warnings": []
            }}
            }}

            Return ONLY the JSON.

            Consider and use the following:

            Candidate original data:
            {json.dumps(parsed_cv)}

            Analysis and recommendations:
            {json.dumps(analysis)}
            
            Job description:
            {job_description_text}
            
            Comapny kind of business and priorities:
            {company_info}
            
            whaen writting all of CV, Coverletter, and Email content.

            """

        messages = [
            {"role": "system", "content": """You are a senior ATS-optimized CV writer. 
            Always return CLEAN, VALID JSON ONLY. No explanations, no markdown, no notes."""},
            {"role": "user", "content": prompt}
        ]

        try:
            response = self.client.chat.completions.create(
    model=self.model_name,  # or llama3-70b-8192, etc.
    messages=messages,
    temperature=0.0,
    max_tokens=3000,
    response_format={"type": "json_object"}
)
            final_cv_json = json.loads(response.choices[0].message.content)
        except Exception:
            final_cv_json = {
                "raw_cv_output": getattr(response, 'content', None),
                "error": "Failed to parse JSON from LLM",
                "original_parsed_cv": parsed_cv,
                "analysis": analysis
            }
        return final_cv_json
