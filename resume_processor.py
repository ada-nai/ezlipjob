"""
Resume Processing Module
Handles resume text extraction and parsing of key information
"""

import re
import PyPDF2
from docx import Document
from typing import Dict, List, Optional, Tuple
import io

class ResumeProcessor:
    """Main class for processing resumes and extracting key information"""
    
    def __init__(self):
        self.contact_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'[\+]?[1-9]?[\d\s\-\(\)]{8,15}',
            'linkedin': r'linkedin\.com\/in\/[\w\-]+',
            'github': r'github\.com\/[\w\-]+'
        }
        
    def extract_pdf_text(self, file_buffer) -> str:
        """
        Extract text from PDF file
        Abstract implementation - returns placeholder for now
        """
        try:
            # TODO: Implement full PDF extraction with PyPDF2
            # For now, return placeholder indicating PDF was uploaded
            return "[PDF content extraction - implement with PyPDF2 when needed]"
        except Exception as e:
            raise ValueError(f"Error extracting PDF text: {str(e)}")
    
    def extract_docx_text(self, file_buffer) -> str:
        """
        Extract text from DOCX file
        Abstract implementation - returns placeholder for now
        """
        try:
            # TODO: Implement full DOCX extraction
            # For now, return placeholder indicating DOCX was uploaded
            return "[DOCX content extraction - implement with python-docx when needed]"
        except Exception as e:
            raise ValueError(f"Error extracting DOCX text: {str(e)}")
    
    def extract_file_text(self, uploaded_file) -> str:
        """
        Extract text from uploaded file based on type
        """
        if uploaded_file.type == "application/pdf":
            return self.extract_pdf_text(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return self.extract_docx_text(uploaded_file)
        else:
            raise ValueError(f"Unsupported file type: {uploaded_file.type}")
    
    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from resume text"""
        contact_info = {}
        
        # Extract email
        email_match = re.search(self.contact_patterns['email'], text, re.IGNORECASE)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Extract phone
        phone_match = re.search(self.contact_patterns['phone'], text)
        if phone_match:
            contact_info['phone'] = phone_match.group().strip()
        
        # Extract LinkedIn
        linkedin_match = re.search(self.contact_patterns['linkedin'], text, re.IGNORECASE)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group()
        
        # Extract GitHub
        github_match = re.search(self.contact_patterns['github'], text, re.IGNORECASE)
        if github_match:
            contact_info['github'] = github_match.group()
        
        return contact_info
    
    def extract_name(self, text: str) -> str:
        """Extract candidate name from resume text"""
        lines = text.strip().split('\n')
        
        # Usually name is in the first few lines
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            if line and len(line.split()) <= 4 and len(line) > 2:
                # Check if it looks like a name (not email, phone, etc.)
                if not re.search(r'[@\d\(\)\+\-]', line):
                    return line
        
        return "Candidate Name"
    
    def extract_experience_section(self, text: str) -> List[str]:
        """Extract work experience entries from resume"""
        experience_keywords = [
            'experience', 'employment', 'work history', 'professional experience',
            'career', 'positions', 'roles'
        ]
        
        lines = text.split('\n')
        experience_entries = []
        in_experience_section = False
        current_entry = []
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_entry and in_experience_section:
                    experience_entries.append(' '.join(current_entry))
                    current_entry = []
                continue
            
            # Check if we're entering experience section
            if any(keyword in line.lower() for keyword in experience_keywords):
                in_experience_section = True
                continue
            
            # Check if we're leaving experience section (hit another major section)
            if in_experience_section and any(section in line.lower() for section in 
                                           ['education', 'skills', 'projects', 'certifications']):
                if current_entry:
                    experience_entries.append(' '.join(current_entry))
                break
            
            if in_experience_section:
                # Check if this looks like a new job entry (company/title)
                if (line.isupper() or 
                    any(indicator in line.lower() for indicator in ['company', 'inc', 'corp', 'ltd']) or
                    re.search(r'\d{4}\s*[-–]\s*\d{4}|\d{4}\s*[-–]\s*present', line.lower())):
                    
                    if current_entry:
                        experience_entries.append(' '.join(current_entry))
                    current_entry = [line]
                else:
                    current_entry.append(line)
        
        # Add last entry
        if current_entry and in_experience_section:
            experience_entries.append(' '.join(current_entry))
        
        return experience_entries[:5]  # Return top 5 experiences
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        skills_keywords = ['skills', 'technologies', 'technical skills', 'competencies']
        
        lines = text.split('\n')
        skills = []
        in_skills_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in skills section
            if any(keyword in line.lower() for keyword in skills_keywords):
                in_skills_section = True
                # Check if skills are on the same line
                if ':' in line:
                    skills_text = line.split(':', 1)[1].strip()
                    skills.extend([s.strip() for s in skills_text.split(',') if s.strip()])
                continue
            
            # Check if we're leaving skills section
            if in_skills_section and any(section in line.lower() for section in 
                                       ['experience', 'education', 'projects', 'certifications']):
                break
            
            if in_skills_section:
                # Parse skills from line
                if ',' in line:
                    skills.extend([s.strip() for s in line.split(',') if s.strip()])
                elif '•' in line or '·' in line:
                    skill = re.sub(r'[•·]\s*', '', line).strip()
                    if skill:
                        skills.append(skill)
                else:
                    skills.append(line)
        
        # Clean and filter skills
        cleaned_skills = []
        for skill in skills:
            skill = re.sub(r'[^\w\s\+\#\.]', '', skill).strip()
            if skill and len(skill) > 1:
                cleaned_skills.append(skill)
        
        return cleaned_skills[:15]  # Return top 15 skills
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information from resume"""
        education_keywords = ['education', 'academic', 'university', 'college', 'degree']
        degree_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'certificate']
        
        lines = text.split('\n')
        education_entries = []
        in_education_section = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in education section
            if any(keyword in line.lower() for keyword in education_keywords):
                in_education_section = True
                continue
            
            # Check if we're leaving education section
            if in_education_section and any(section in line.lower() for section in 
                                          ['experience', 'skills', 'projects', 'certifications']):
                break
            
            if in_education_section:
                education_entries.append(line)
            
            # Also catch degree mentions anywhere in resume
            if any(degree in line.lower() for degree in degree_keywords):
                if line not in education_entries:
                    education_entries.append(line)
        
        return education_entries[:3]  # Return top 3 education entries
    
    def parse_resume(self, resume_text: str) -> Dict:
        """
        Main function to parse resume text and extract all key information
        """
        if not resume_text or len(resume_text.strip()) < 50:
            raise ValueError("Resume text is too short or empty")
        
        # Extract all information
        parsed_data = {
            'name': self.extract_name(resume_text),
            'contact_info': self.extract_contact_info(resume_text),
            'experience': self.extract_experience_section(resume_text),
            'skills': self.extract_skills(resume_text),
            'education': self.extract_education(resume_text),
            'raw_text': resume_text,
            'text_length': len(resume_text)
        }
        
        return parsed_data
    
    def validate_resume_data(self, parsed_data: Dict) -> Tuple[bool, List[str]]:
        """Validate parsed resume data and return warnings"""
        warnings = []
        is_valid = True
        
        if not parsed_data.get('name') or parsed_data['name'] == "Candidate Name":
            warnings.append("Could not extract candidate name")
        
        if not parsed_data.get('contact_info', {}).get('email'):
            warnings.append("Could not extract email address")
        
        if not parsed_data.get('experience'):
            warnings.append("Could not extract work experience")
            is_valid = False
        
        if not parsed_data.get('skills'):
            warnings.append("Could not extract skills")
        
        if parsed_data.get('text_length', 0) < 100:
            warnings.append("Resume text seems too short")
            is_valid = False
        
        return is_valid, warnings


def process_resume_input(uploaded_file=None, manual_text=None):
    """
    Convenience function to process resume from either file upload or manual text
    """
    processor = ResumeProcessor()
    
    try:
        if uploaded_file is not None:
            # Handle file upload
            resume_text = processor.extract_file_text(uploaded_file)
        elif manual_text:
            # Handle manual text input
            resume_text = manual_text.strip()
        else:
            raise ValueError("Either file upload or manual text must be provided")
        
        # Parse the resume
        parsed_data = processor.parse_resume(resume_text)
        
        # Validate the data
        is_valid, warnings = processor.validate_resume_data(parsed_data)
        
        return {
            'success': True,
            'data': parsed_data,
            'is_valid': is_valid,
            'warnings': warnings
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': None,
            'is_valid': False,
            'warnings': []
        }