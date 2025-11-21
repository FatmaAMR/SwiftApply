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

    async def generate_cv(self, parsed_cv: dict, analysis: dict, template_id: str) -> dict:
        """
        Generate a final CV JSON using the parsed CV and analysis.
        """
        prompt = f"""
You are a professional CV writer.
Rewrite the candidate's CV to be perfectly tailored to the job, incorporating all recommendations from the analysis.
Use template ID: {template_id}.

Output ONLY valid JSON with these exact keys (no markdown, no extra text):
- header (dict with name, title, contact info, linkedin, etc.)
- summary (string - professional summary)
- skills (list of strings or categorized dict)
- experience (list of job dicts with company, role, dates, bullets)
- education (list of education dicts)
- additional_sections (dict with certifications, projects, languages, etc.)

Candidate original data:
{json.dumps(parsed_cv)}

Analysis and recommendations:
{json.dumps(analysis)}
"""
        messages = [
            {"role": "system", "content": "You are a senior CV writer. Respond with clean, valid JSON only - nothing else."},
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
