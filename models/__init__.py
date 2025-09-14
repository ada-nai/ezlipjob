"""
Pydantic models for structured outputs in the job application assistant
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from enum import Enum

class ToneType(str, Enum):
    """Available tone options for content generation"""
    PROFESSIONAL = "Professional"
    WARM = "Warm" 
    CONCISE = "Concise"

class PersonalizationMatch(BaseModel):
    """Represents a match between resume experience and job requirement"""
    resume_point: str = Field(description="Specific experience or skill from resume")
    job_requirement: str = Field(description="Matching job requirement")
    relevance_score: float = Field(description="Relevance score from 0-1")
    explanation: str = Field(description="Why this is a good match")

    @field_validator('relevance_score')
    @classmethod
    def validate_relevance_score(cls, v):
        """Ensure relevance score is between 0 and 1"""
        if v < 0:
            return 0.0
        elif v > 1:
            return 1.0
        return v

class CompanyInsight(BaseModel):
    """Company research insights from web search"""
    company_name: str = Field(description="Company name")
    industry: str = Field(description="Company industry")
    values: List[str] = Field(description="Company values and culture")
    recent_news: List[str] = Field(description="Recent company news or achievements")
    size: Optional[str] = Field(description="Company size category")
    culture_keywords: List[str] = Field(description="Keywords describing company culture")

class CoverLetterContent(BaseModel):
    """Structured cover letter output"""
    salutation: str = Field(description="Personalized greeting using hiring manager name")
    opening_paragraph: str = Field(description="Introduction paragraph with position interest")
    body_paragraph_1: str = Field(description="First body paragraph highlighting relevant experience")
    body_paragraph_2: str = Field(description="Second body paragraph with specific achievements")
    closing_paragraph: str = Field(description="Closing paragraph with call to action")
    signature_line: str = Field(description="Professional closing with candidate name")
    word_count: int = Field(description="Total word count")
    personalization_elements: List[str] = Field(description="List of personalized elements included")

class EmailDraft(BaseModel):
    """Structured email draft output"""
    to_email: str = Field(description="Recipient email address")
    subject_line: str = Field(description="Professional subject line")
    greeting: str = Field(description="Professional greeting")
    body_paragraph_1: str = Field(description="Opening paragraph with position interest")
    body_paragraph_2: str = Field(description="Brief qualifications highlight")
    closing_paragraph: str = Field(description="Call to action and availability")
    signature: str = Field(description="Professional signature block")
    word_count: int = Field(description="Body word count (excluding greeting and signature)")

class ContentQualityMetrics(BaseModel):
    """Quality assessment metrics for generated content"""
    personalization_score: float = Field(description="How well content matches candidate to job (0-1)")
    company_alignment_score: float = Field(description="How well content aligns with company culture (0-1)")
    tone_consistency_score: float = Field(description="How well content matches requested tone (0-1)")
    professional_standard_score: float = Field(description="Professional communication quality (0-1)")
    specific_examples_count: int = Field(description="Number of specific examples included")
    achievement_mentions: int = Field(description="Number of quantified achievements mentioned")

class GenerationResult(BaseModel):
    """Complete result from content generation process"""
    success: bool = Field(description="Whether generation was successful")
    cover_letter: Optional[CoverLetterContent] = Field(default=None, description="Generated cover letter")
    email_draft: Optional[EmailDraft] = Field(default=None, description="Generated email draft")
    personalization_matches: List[PersonalizationMatch] = Field(default=[], description="Experience-job matches found")
    company_insights: Optional[CompanyInsight] = Field(default=None, description="Company research results")
    quality_metrics: Optional[ContentQualityMetrics] = Field(default=None, description="Content quality assessment")
    generation_time: float = Field(default=0.0, description="Time taken for generation in seconds")
    error_message: Optional[str] = Field(default=None, description="Error message if generation failed")
    warnings: List[str] = Field(default=[], description="Any warnings during generation")
    tone_used: ToneType = Field(default=ToneType.PROFESSIONAL, description="Tone style applied to content")

class WebSearchResult(BaseModel):
    """Structured web search result for company research"""
    query: str = Field(description="Search query used")
    results: List[Dict[str, Any]] = Field(description="Raw search results")
    insights: CompanyInsight = Field(description="Extracted company insights")
    search_success: bool = Field(description="Whether search was successful")

class ResumeJobAlignment(BaseModel):
    """Analysis of how well resume aligns with job requirements"""
    overall_match_score: float = Field(description="Overall alignment score (0-1)")
    matching_skills: List[str] = Field(description="Skills that match job requirements")
    missing_skills: List[str] = Field(description="Skills mentioned in job but not in resume")
    relevant_experiences: List[str] = Field(description="Most relevant work experiences")
    education_relevance: str = Field(description="How education aligns with job")
    experience_level_match: str = Field(description="Whether experience level matches job requirements")
    recommendations: List[str] = Field(description="Recommendations for highlighting strengths")

class ContentGenerationRequest(BaseModel):
    """Input request for content generation"""
    resume_data: Dict[str, Any] = Field(description="Parsed resume data")
    job_data: Dict[str, Any] = Field(description="Scraped job data") 
    tone: ToneType = Field(default=ToneType.PROFESSIONAL, description="Desired tone")
    include_company_research: bool = Field(default=True, description="Whether to research company")
    custom_instructions: Optional[str] = Field(default=None, description="Additional custom instructions")
    focus_areas: List[str] = Field(default=[], description="Specific areas to emphasize")