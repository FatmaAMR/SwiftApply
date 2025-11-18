import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from utils import get_settings


class CVChatbot:
    def __init__(self, temperature: float = 0.3, settings=None):
        if settings is None:
            settings = get_settings()
        self.llm = ChatOpenAI(model=settings.OPENAI_MODEL_NAME, temperature=temperature)

    
    async def parse_cv(self, cv_text: str) -> dict:
        messages = [
            SystemMessage(content="You are a CV parsing assistant. Extract all relevant sections into a structured JSON."),
            HumanMessage(
                content=f"""
Candidate CV:
{cv_text}

Return JSON with:
- personal_info
- education
- skills
- experience
- achievements
- certifications
"""
            )
        ]

        response = await self.llm.ainvoke(messages)
        try:
            parsed_json = json.loads(response.content)
        except Exception:
            parsed_json = {"raw_text": cv_text, "raw_llm_output": response.content}  # fallback if JSON invalid
        return parsed_json

  
  
    async def analyze_cv(self, parsed_cv: dict, jd_text: str, notes: str, company_info: str) -> dict:
        prompt = f"""
You are an HR expert. Analyze the candidate CV below against the Job Description and Company Notes. 
Identify missing skills, recommended improvements, and calculate an overall match score (0-100).

Candidate CV JSON:
{json.dumps(parsed_cv)}

Job Description:
{jd_text}

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
            SystemMessage(content="You are an expert HR evaluator. Always respond with clean JSON only."),
            HumanMessage(content=prompt)
        ]

        response = await self.llm.ainvoke(messages)
        try:
            analysis_json = json.loads(response.content)
        except Exception:
            analysis_json = {"raw_analysis": response.content, "error": "Failed to parse JSON from LLM"}
        return analysis_json




    async def generate_cv(self, parsed_cv: dict, analysis: dict, template_id: str) -> dict:
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
            SystemMessage(content="You are a senior CV writer. Respond with clean, valid JSON only - nothing else."),
            HumanMessage(content=prompt)
        ]

        response = await self.llm.ainvoke(messages)
        try:
            final_cv_json = json.loads(response.content)
        except Exception:
            final_cv_json = {
                "raw_cv_output": response.content,
                "error": "Failed to parse JSON from LLM",
                "original_parsed_cv": parsed_cv,
                "analysis": analysis
            }
        return final_cv_json