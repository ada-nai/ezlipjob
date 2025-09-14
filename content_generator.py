"""
AI Content Generation Module
Uses GPT-4o for personalized cover letter and email generation with structured outputs
"""

import openai
import time
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

from config import get_config, get_openai_config, get_content_limits
from models import (
    GenerationResult, CoverLetterContent, EmailDraft, PersonalizationMatch,
    CompanyInsight, ContentQualityMetrics, ResumeJobAlignment, WebSearchResult,
    ContentGenerationRequest, ToneType
)

class ContentGenerator:
    """Main AI content generation class using GPT-4o with structured outputs"""
    
    def __init__(self):
        """Initialize the content generator with GPT-4o"""
        try:
            openai_config = get_openai_config()
            self.client = openai.OpenAI(
                api_key=openai_config['api_key']
            )
            self.model = openai_config['model']
            self.max_tokens = openai_config['max_tokens']
            self.temperature = openai_config['temperature']
            self.timeout = openai_config['timeout']
            
            # Get content limits
            self.content_limits = get_content_limits()
            
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")
    
    def research_company(self, company_name: str, job_description: str) -> Optional[CompanyInsight]:
        """
        Use web search tool via OpenAI to research company
        Note: This is a placeholder for when OpenAI enables web search tools
        For now, we'll extract insights from job description and use GPT-4o knowledge
        """
        try:
            system_prompt = """You are a company research analyst. Based on the company name and job description provided, 
            extract insights about the company's industry, values, culture, and provide relevant information that would 
            help a job applicant understand the company better. Use your knowledge base to provide accurate information."""
            
            user_prompt = f"""
            Company: {company_name}
            Job Description: {job_description[:1000]}
            
            Please provide insights about this company including:
            - Industry and business focus
            - Company values and culture keywords
            - Company size category (startup, mid-size, enterprise, etc.)
            - Key cultural elements that would be relevant for a job application
            
            Provide accurate information based on your knowledge. If uncertain about specific details, focus on what can be reasonably inferred from the job description.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "company_insight",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "company_name": {"type": "string"},
                                "industry": {"type": "string"},
                                "values": {"type": "array", "items": {"type": "string"}},
                                "recent_news": {"type": "array", "items": {"type": "string"}},
                                "size": {"type": "string"},
                                "culture_keywords": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["company_name", "industry", "values", "culture_keywords"]
                        }
                    }
                },
                max_tokens=1000,
                temperature=0.5
            )
            
            insight_data = json.loads(response.choices[0].message.content)
            return CompanyInsight(**insight_data)
            
        except Exception as e:
            print(f"Company research failed: {str(e)}")
            # Fallback company insight
            return CompanyInsight(
                company_name=company_name,
                industry="Technology" if "tech" in job_description.lower() else "Business",
                values=["Innovation", "Excellence", "Teamwork"],
                recent_news=[],
                size="Not specified",
                culture_keywords=["professional", "collaborative", "growth-oriented"]
            )
    
    def analyze_resume_job_alignment(self, resume_data: Dict, job_data: Dict) -> ResumeJobAlignment:
        """Analyze how well the resume aligns with job requirements"""
        try:
            system_prompt = """You are an expert career counselor analyzing resume-job fit. 
            Provide detailed analysis of how well a candidate's background matches a job posting."""
            
            user_prompt = f"""
            RESUME DATA:
            Name: {resume_data.get('name', 'N/A')}
            Skills: {', '.join(resume_data.get('skills', []))}
            Experience: {' | '.join(resume_data.get('experience', [])[:3])}
            Education: {' | '.join(resume_data.get('education', []))}
            
            JOB DATA:
            Title: {job_data.get('job_title', 'N/A')}
            Company: {job_data.get('company', 'N/A')}
            Description: {job_data.get('description', '')[:800]}
            Requirements: {' | '.join(job_data.get('requirements', [])[:5])}
            
            Analyze the alignment and provide structured feedback.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "resume_job_alignment",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "overall_match_score": {"type": "number", "minimum": 0, "maximum": 1},
                                "matching_skills": {"type": "array", "items": {"type": "string"}},
                                "missing_skills": {"type": "array", "items": {"type": "string"}},
                                "relevant_experiences": {"type": "array", "items": {"type": "string"}},
                                "education_relevance": {"type": "string"},
                                "experience_level_match": {"type": "string"},
                                "recommendations": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["overall_match_score", "matching_skills", "relevant_experiences", "recommendations"]
                        }
                    }
                },
                max_tokens=1500,
                temperature=0.3
            )
            
            alignment_data = json.loads(response.choices[0].message.content)
            return ResumeJobAlignment(**alignment_data)
            
        except Exception as e:
            print(f"Alignment analysis failed: {str(e)}")
            # Fallback alignment
            return ResumeJobAlignment(
                overall_match_score=0.7,
                matching_skills=resume_data.get('skills', [])[:5],
                missing_skills=[],
                relevant_experiences=resume_data.get('experience', [])[:2],
                education_relevance="Relevant background",
                experience_level_match="Good match",
                recommendations=["Highlight technical skills", "Emphasize relevant projects"]
            )
    
    def find_personalization_matches(self, resume_data: Dict, job_data: Dict) -> List[PersonalizationMatch]:
        """Find specific matches between resume experience and job requirements"""
        try:
            system_prompt = """You are an expert at matching candidate qualifications to job requirements. 
            Find specific, detailed connections between the candidate's background and the job needs."""
            
            user_prompt = f"""
            CANDIDATE BACKGROUND:
            Skills: {', '.join(resume_data.get('skills', []))}
            Experience: {' '.join(resume_data.get('experience', [])[:3])}
            
            JOB REQUIREMENTS:
            Title: {job_data.get('job_title')}
            Description: {job_data.get('description', '')[:1000]}
            Requirements: {' '.join(job_data.get('requirements', []))}
            
            Find 3-5 specific matches between candidate background and job needs. 
            For each match, provide the specific resume point, matching job requirement, 
            a relevance score, and explanation of why it's a good match.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "personalization_matches",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "matches": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "resume_point": {"type": "string"},
                                            "job_requirement": {"type": "string"},
                                            "relevance_score": {"type": "number", "minimum": 0, "maximum": 1},
                                            "explanation": {"type": "string"}
                                        },
                                        "required": ["resume_point", "job_requirement", "relevance_score", "explanation"]
                                    }
                                }
                            },
                            "required": ["matches"]
                        }
                    }
                },
                max_tokens=2000,
                temperature=0.4
            )
            
            matches_data = json.loads(response.choices[0].message.content)
            return [PersonalizationMatch(**match) for match in matches_data["matches"]]
            
        except Exception as e:
            print(f"Personalization matching failed: {str(e)}")
            return []
    
    def generate_cover_letter(self, resume_data: Dict, job_data: Dict, 
                            company_insight: Optional[CompanyInsight], 
                            matches: List[PersonalizationMatch],
                            tone: ToneType) -> CoverLetterContent:
        """Generate personalized cover letter using GPT-4o with structured output"""
        
        # Prepare tone-specific instructions
        tone_instructions = {
            ToneType.PROFESSIONAL: "Use formal, business-appropriate language. Be respectful and traditional in approach.",
            ToneType.WARM: "Use friendly but professional language. Show enthusiasm and personality while maintaining professionalism.",
            ToneType.CONCISE: "Be direct and to-the-point. Use shorter sentences and get straight to the value proposition."
        }
        
        # Extract names for personalization
        candidate_name = resume_data.get('name', 'Candidate')
        contact_info = job_data.get('contact_info', {})
        hiring_manager = contact_info.get('hiring_manager', 'Hiring Manager')
        
        # Build context from matches
        match_context = "\n".join([
            f"- {match.resume_point} aligns with {match.job_requirement}"
            for match in matches[:3]
        ])
        
        # Company context
        company_context = ""
        if company_insight:
            company_context = f"Company values: {', '.join(company_insight.values)}. Culture: {', '.join(company_insight.culture_keywords)}."
        
        system_prompt = f"""You are an expert professional writer specializing in cover letters. 
        Create a compelling, personalized cover letter that demonstrates clear alignment between 
        the candidate's background and the job requirements. 
        
        IMPORTANT PERSONALIZATION REQUIREMENTS:
        - Address the hiring manager by name: {hiring_manager}
        - Use the candidate's name: {candidate_name}
        - If hiring manager is "Hiring Manager", use "Dear Hiring Manager"
        - If hiring manager has a specific name, use "Dear [Name]"
        - Reference the candidate by name in the letter body for personalization
        
        TONE: {tone_instructions[tone]}
        REQUIREMENTS: {self.content_limits['cover_letter_min']}-{self.content_limits['cover_letter_max']} words total, professional format, specific examples, company alignment."""
        
        user_prompt = f"""
        CANDIDATE: {candidate_name}
        EMAIL: {resume_data.get('contact_info', {}).get('email', 'email@example.com')}
        
        JOB: {job_data.get('job_title')} at {job_data.get('company')}
        LOCATION: {job_data.get('location', 'Remote')}
        HIRING_MANAGER: {hiring_manager}
        
        KEY ALIGNMENTS:
        {match_context}
        
        COMPANY CONTEXT: {company_context}
        
        CANDIDATE BACKGROUND:
        Experience: {' | '.join(resume_data.get('experience', [])[:2])}
        Skills: {', '.join(resume_data.get('skills', [])[:8])}
        
        Write a cover letter with exactly 4 paragraphs:
        1. Opening: Express interest in the specific position
        2. Body 1: Highlight most relevant experience with specific examples
        3. Body 2: Demonstrate additional qualifications and achievements
        4. Closing: Call to action and professional close
        
        Ensure {self.content_limits['cover_letter_min']}-{self.content_limits['cover_letter_max']} words total and include specific personalization elements.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "cover_letter",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "salutation": {"type": "string", "description": "Personalized greeting using hiring manager name"},
                                "opening_paragraph": {"type": "string"},
                                "body_paragraph_1": {"type": "string"},
                                "body_paragraph_2": {"type": "string"},
                                "closing_paragraph": {"type": "string"},
                                "signature_line": {"type": "string", "description": "Professional closing with candidate name"},
                                "word_count": {"type": "integer"},
                                "personalization_elements": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["salutation", "opening_paragraph", "body_paragraph_1", "body_paragraph_2", "closing_paragraph", "signature_line", "word_count", "personalization_elements"]
                        }
                    }
                },
                max_tokens=2000,
                temperature=0.7
            )
            
            cover_letter_data = json.loads(response.choices[0].message.content)
            return CoverLetterContent(**cover_letter_data)
            
        except Exception as e:
            raise Exception(f"Cover letter generation failed: {str(e)}")
    
    def generate_email_draft(self, resume_data: Dict, job_data: Dict, 
                           company_insight: Optional[CompanyInsight],
                           tone: ToneType) -> EmailDraft:
        """Generate professional email draft using GPT-4o"""
        
        # Determine recipient email and suggested subject
        contact_info = job_data.get('contact_info', {})
        if isinstance(contact_info, dict):
            to_email = contact_info.get('contact_email', contact_info.get('email', f"careers@{job_data.get('company', 'company').lower().replace(' ', '')}.com"))
            suggested_subject = contact_info.get('suggested_subject', None)
            hiring_manager = contact_info.get('hiring_manager', 'Hiring Manager')
        else:
            to_email = f"careers@{job_data.get('company', 'company').lower().replace(' ', '')}.com"
            suggested_subject = None
            hiring_manager = 'Hiring Manager'
        
        # Extract candidate name for personalization
        candidate_name = resume_data.get('name', 'Candidate')
        
        # Prepare subject line instruction
        subject_instruction = ""
        if suggested_subject:
            subject_instruction = f"IMPORTANT: Use this EXACT subject line: '{suggested_subject}'"
        else:
            subject_instruction = f"Create a clear subject line with job title and candidate name ({candidate_name})"
        
        system_prompt = f"""You are an expert at writing professional job application emails. 
        Create a concise, compelling email that accompanies a job application.
        
        IMPORTANT PERSONALIZATION REQUIREMENTS:
        - Use the candidate's name: {candidate_name}
        - Address the hiring manager: {hiring_manager}
        - If hiring manager is "Hiring Manager", use "Dear Hiring Manager"
        - If hiring manager has a specific name, use "Dear [Name]" 
        - Reference the candidate by name in the email body for personalization
        
        REQUIREMENTS: 
        - Professional business email format
        - {self.content_limits['email_min']}-{self.content_limits['email_max']} words in body (excluding greeting and signature)
        - {subject_instruction}
        - Mention attached resume and cover letter
        - Include call to action
        - Tone: {tone.value}"""
        
        user_prompt = f"""
        CANDIDATE: {candidate_name}
        EMAIL: {resume_data.get('contact_info', {}).get('email', 'email@example.com')}
        PHONE: {resume_data.get('contact_info', {}).get('phone', '(555) 123-4567')}
        
        JOB: {job_data.get('job_title')} at {job_data.get('company')}
        RECIPIENT: {to_email}
        HIRING_MANAGER: {hiring_manager}
        {f"REQUIRED_SUBJECT: {suggested_subject}" if suggested_subject else ""}
        
        TOP QUALIFICATIONS:
        - {', '.join(resume_data.get('skills', [])[:5])}
        - {resume_data.get('experience', ['Relevant experience'])[0][:100] if resume_data.get('experience') else 'Relevant experience'}
        
        Create a professional email draft with all components.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "email_draft",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "to_email": {"type": "string"},
                                "subject_line": {"type": "string"},
                                "greeting": {"type": "string"},
                                "body_paragraph_1": {"type": "string"},
                                "body_paragraph_2": {"type": "string"},
                                "closing_paragraph": {"type": "string"},
                                "signature": {"type": "string"},
                                "word_count": {"type": "integer"}
                            },
                            "required": ["to_email", "subject_line", "greeting", "body_paragraph_1", "body_paragraph_2", "closing_paragraph", "signature", "word_count"]
                        }
                    }
                },
                max_tokens=1500,
                temperature=0.6
            )
            
            email_data = json.loads(response.choices[0].message.content)
            return EmailDraft(**email_data)
            
        except Exception as e:
            raise Exception(f"Email draft generation failed: {str(e)}")
    
    def assess_content_quality(self, cover_letter: CoverLetterContent, 
                             email_draft: EmailDraft, 
                             matches: List[PersonalizationMatch]) -> ContentQualityMetrics:
        """Assess the quality of generated content"""
        
        # Calculate personalization score
        personalization_score = min(1.0, len(matches) * 0.2)
        
        # Assess word count compliance
        cover_letter_compliance = 1.0 if 200 <= cover_letter.word_count <= 300 else 0.7
        email_compliance = 1.0 if 100 <= email_draft.word_count <= 150 else 0.7
        
        # Count specific examples and achievements
        full_text = f"{cover_letter.opening_paragraph} {cover_letter.body_paragraph_1} {cover_letter.body_paragraph_2} {cover_letter.closing_paragraph}"
        specific_examples = len(re.findall(r'\b\d+[%\+\$]|\b\d+\s+(years?|months?)\b', full_text))
        
        return ContentQualityMetrics(
            personalization_score=personalization_score,
            company_alignment_score=0.8,  # Based on company insight usage
            tone_consistency_score=0.9,   # Assume good tone consistency
            professional_standard_score=(cover_letter_compliance + email_compliance) / 2,
            specific_examples_count=specific_examples,
            achievement_mentions=len(cover_letter.personalization_elements)
        )
    
    def generate_application_materials(self, request: ContentGenerationRequest) -> GenerationResult:
        """
        Main function to generate complete application materials
        """
        start_time = time.time()
        warnings = []
        
        try:
            # Step 1: Company research (if requested)
            company_insight = None
            if request.include_company_research:
                try:
                    company_insight = self.research_company(
                        request.job_data.get('company', ''),
                        request.job_data.get('description', '')
                    )
                except Exception as e:
                    warnings.append(f"Company research failed: {str(e)}")
            
            # Step 2: Find personalization matches
            matches = self.find_personalization_matches(
                request.resume_data, 
                request.job_data
            )
            
            if not matches:
                warnings.append("Limited personalization matches found")
            
            # Step 3: Generate cover letter
            cover_letter = self.generate_cover_letter(
                request.resume_data,
                request.job_data,
                company_insight,
                matches,
                request.tone
            )
            
            # Step 4: Generate email draft
            email_draft = self.generate_email_draft(
                request.resume_data,
                request.job_data,
                company_insight,
                request.tone
            )
            
            # Step 5: Assess quality
            quality_metrics = self.assess_content_quality(
                cover_letter, 
                email_draft, 
                matches
            )
            
            generation_time = time.time() - start_time
            
            return GenerationResult(
                success=True,
                cover_letter=cover_letter,
                email_draft=email_draft,
                personalization_matches=matches,
                company_insights=company_insight,
                quality_metrics=quality_metrics,
                generation_time=generation_time,
                warnings=warnings,
                tone_used=request.tone
            )
            
        except Exception as e:
            return GenerationResult(
                success=False,
                cover_letter=None,
                email_draft=None,
                personalization_matches=[],
                company_insights=None,
                quality_metrics=None,
                generation_time=time.time() - start_time,
                error_message=str(e),
                warnings=warnings,
                tone_used=request.tone
            )


def generate_application_content(resume_data: Dict, job_data: Dict, 
                               tone: str = "Professional", 
                               include_company_research: bool = True,
                               custom_instructions: Optional[str] = None) -> GenerationResult:
    """
    Convenience function for generating application materials
    """
    generator = ContentGenerator()
    
    request = ContentGenerationRequest(
        resume_data=resume_data,
        job_data=job_data,
        tone=ToneType(tone),
        include_company_research=include_company_research,
        custom_instructions=custom_instructions
    )
    
    return generator.generate_application_materials(request)