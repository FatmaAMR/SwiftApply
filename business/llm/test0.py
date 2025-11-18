from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

from utils import get_settings

class CVChatbot:
    def __init__(self, temperature=0.3, settings=get_settings()):
        self.llm = ChatOpenAI(model=settings.OPENAI_MODEL_NAME, temperature=temperature)

    # Step 1: Extract structured JSON from CV text
    async def parse_cv(self, cv_text: str) -> dict:
        system_prompt = SystemMessage.from_template(
            "You are a CV parsing assistant. Extract all relevant sections into a structured JSON."
        )

        human_prompt = HumanMessage.from_template(
            """Candidate CV:
{cv_text}

Return JSON with:
- personal_info
- education
- skills
- experience
- achievements
- certifications"""
        )

        chat_prompt = AIMessage.from_messages([system_prompt, human_prompt])
        response = await self.llm.ainvoke(chat_prompt.format_messages(cv_text=cv_text))
        return response.content  # parse JSON if needed

    # Step 2: Analyze and score
    async def analyze_cv(self, parsed_cv: dict, jd_text: str, notes: str, company_info: str) -> dict:
        prompt = f"""
You are an HR expert. Analyze the candidate CV below against the Job Description and Company Notes. 
Identify missing skills, recommended improvements, and calculate an overall match score (0-100).

Candidate CV JSON:
{parsed_cv}

Job Description:
{jd_text}

Company Notes:
{company_info}

and consider the follwing:
{notes}

Return JSON with:
- match_score
- missing_skills
- recommended_keywords
- sections_to_improve
"""
        response = await self.llm.ainvoke(prompt)
        return response.content  # parse JSON

    # Step 3: Generate final CV JSON for templating
    async def generate_cv(self, parsed_cv: dict, analysis: dict, template_id: str) -> dict:
        prompt = f"""
You are a professional CV rewriting assistant.
Take the candidate CV JSON and the analysis JSON to generate a fully optimized CV.
Use template ID: {template_id}.
Output JSON with sections:
- header
- summary
- skills
- experience
- education
- additional_sections
"""
        response = await self.llm.ainvoke(prompt)
        return response.content  
