"""
LinkedIn Job Scraping Module
Handles extraction of job details from LinkedIn URLs and posts
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional, Tuple
import time
from urllib.parse import urlparse, parse_qs

class LinkedInJobScraper:
    """Main class for scraping LinkedIn job postings"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.timeout = 10
        
    def validate_linkedin_url(self, url: str) -> Tuple[bool, str]:
        """Validate if URL is a LinkedIn job posting"""
        if not url:
            return False, "URL is empty"
        
        try:
            parsed = urlparse(url)
            if 'linkedin.com' not in parsed.netloc:
                return False, "URL is not from LinkedIn"
            
            # Check for job posting patterns
            job_patterns = [
                '/jobs/view/',
                '/jobs/collections/',
                '/feed/update/',  # LinkedIn posts
                '/posts/'
            ]
            
            if not any(pattern in url for pattern in job_patterns):
                return False, "URL doesn't appear to be a LinkedIn job posting or post"
            
            return True, "Valid LinkedIn URL"
            
        except Exception as e:
            return False, f"Invalid URL format: {str(e)}"
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\$\%]', '', text)
        
        return text
    
    def extract_job_id(self, url: str) -> Optional[str]:
        """Extract job ID from LinkedIn URL"""
        try:
            # Pattern for /jobs/view/jobid
            match = re.search(r'/jobs/view/(\d+)', url)
            if match:
                return match.group(1)
            
            # Pattern for query parameters
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            if 'currentJobId' in query_params:
                return query_params['currentJobId'][0]
            
            return None
        except:
            return None
    
    def scrape_job_posting(self, url: str) -> Dict:
        """Scrape job details from LinkedIn job posting URL"""
        try:
            # Add delay to avoid rate limiting
            time.sleep(1)
            
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_data = {
                'job_title': self.extract_job_title(soup),
                'company': self.extract_company_name(soup),
                'location': self.extract_location(soup),
                'description': self.extract_job_description(soup),
                'requirements': self.extract_requirements(soup),
                'employment_type': self.extract_employment_type(soup),
                'experience_level': self.extract_experience_level(soup),
                'contact_info': self.extract_contact_info(soup),
                'url': url
            }
            
            return job_data
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch job posting: {str(e)}")
        except Exception as e:
            raise Exception(f"Error scraping job posting: {str(e)}")
    
    def extract_job_title(self, soup: BeautifulSoup) -> str:
        """Extract job title from page"""
        selectors = [
            'h1[data-test-id="job-title"]',
            'h1.jobs-unified-top-card__job-title',
            'h1.topcard__title',
            'h1',
            '.job-title',
            '.jobs-details-top-card__job-title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                title = self.clean_text(element.get_text())
                if title and len(title) > 3:
                    return title
        
        return "Job Title Not Found"
    
    def extract_company_name(self, soup: BeautifulSoup) -> str:
        """Extract company name from page"""
        selectors = [
            'a[data-test-id="job-detail-company-name"]',
            '.jobs-unified-top-card__company-name',
            '.topcard__org-name-link',
            '.job-details-company-name',
            '.jobs-details-top-card__company-url'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                company = self.clean_text(element.get_text())
                if company and len(company) > 1:
                    return company
        
        return "Company Not Found"
    
    def extract_location(self, soup: BeautifulSoup) -> str:
        """Extract job location from page"""
        selectors = [
            '[data-test-id="job-location"]',
            '.jobs-unified-top-card__bullet',
            '.topcard__flavor--bullet',
            '.job-location'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                location = self.clean_text(element.get_text())
                if location and len(location) > 2:
                    return location
        
        return "Location Not Specified"
    
    def extract_job_description(self, soup: BeautifulSoup) -> str:
        """Extract job description from page"""
        selectors = [
            '.jobs-description__content',
            '.jobs-box__html-content',
            '.job-description',
            '[data-test-id="job-description"]',
            '.description__text'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                description = self.clean_text(element.get_text())
                if description and len(description) > 50:
                    return description[:2000]  # Limit length
        
        return "Job description not available"
    
    def extract_requirements(self, soup: BeautifulSoup) -> List[str]:
        """Extract job requirements from description"""
        description = self.extract_job_description(soup)
        
        requirements = []
        requirement_keywords = [
            'requirements', 'qualifications', 'must have', 'required',
            'experience', 'skills', 'education', 'preferred'
        ]
        
        # Split description into sentences/bullet points
        sentences = re.split(r'[.•\n]', description)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in requirement_keywords):
                if len(sentence) > 20 and len(sentence) < 200:
                    requirements.append(sentence)
        
        return requirements[:10]  # Return top 10 requirements
    
    def extract_employment_type(self, soup: BeautifulSoup) -> str:
        """Extract employment type (Full-time, Part-time, etc.)"""
        selectors = [
            '[data-test-id="job-employment-type"]',
            '.jobs-unified-top-card__job-insight',
            '.job-criteria__text'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                text = self.clean_text(element.get_text()).lower()
                if any(job_type in text for job_type in ['full-time', 'part-time', 'contract', 'internship']):
                    return text.title()
        
        return "Not Specified"
    
    def extract_experience_level(self, soup: BeautifulSoup) -> str:
        """Extract experience level requirements"""
        description = self.extract_job_description(soup)
        description_lower = description.lower()
        
        if any(term in description_lower for term in ['entry level', 'junior', '0-1 year', 'new grad']):
            return "Entry Level"
        elif any(term in description_lower for term in ['senior', '5+ years', 'lead', 'principal']):
            return "Senior Level"
        elif any(term in description_lower for term in ['mid level', '2-4 years', 'experienced']):
            return "Mid Level"
        else:
            return "Not Specified"
    
    def extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract contact information if available"""
        contact_info = {}
        
        # Look for hiring manager or HR contact
        text_content = soup.get_text().lower()
        
        # Extract email patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, soup.get_text())
        
        if emails:
            contact_info['email'] = emails[0]
        
        # Common hiring patterns
        hiring_patterns = [
            r'contact\s+([A-Za-z\s]+)\s+at',
            r'reach out to\s+([A-Za-z\s]+)',
            r'hiring manager[:\s]*([A-Za-z\s]+)'
        ]
        
        for pattern in hiring_patterns:
            match = re.search(pattern, text_content, re.IGNORECASE)
            if match:
                contact_info['hiring_manager'] = match.group(1).strip()
                break
        
        return contact_info
    
    def generate_fallback_contact(self, company_name: str) -> Dict[str, str]:
        """Generate fallback contact information"""
        if company_name and company_name != "Company Not Found":
            # Generate common email patterns
            company_clean = re.sub(r'[^\w]', '', company_name.lower())
            fallback_emails = [
                f"careers@{company_clean}.com",
                f"hr@{company_clean}.com",
                f"jobs@{company_clean}.com"
            ]
            
            return {
                'suggested_emails': fallback_emails,
                'hiring_manager': "Hiring Manager",
                'note': f"Contact information not found. Try these common {company_name} email patterns."
            }
        
        return {
            'hiring_manager': "Hiring Manager",
            'suggested_emails': ["careers@company.com"],
            'note': "Contact information not available. Use general hiring manager title."
        }


def scrape_linkedin_job(url: str) -> Dict:
    """
    Convenience function to scrape LinkedIn job posting
    """
    scraper = LinkedInJobScraper()
    
    try:
        # Validate URL
        is_valid, message = scraper.validate_linkedin_url(url)
        if not is_valid:
            return {
                'success': False,
                'error': message,
                'data': None
            }
        
        # Scrape job data
        job_data = scraper.scrape_job_posting(url)
        
        # Add fallback contact if no contact info found
        if not job_data.get('contact_info'):
            job_data['contact_info'] = scraper.generate_fallback_contact(job_data['company'])
        
        # Validate extracted data
        if not job_data['job_title'] or job_data['job_title'] == "Job Title Not Found":
            return {
                'success': False,
                'error': "Could not extract job title. Please check the URL or try manual entry.",
                'data': job_data
            }
        
        return {
            'success': True,
            'data': job_data,
            'message': "Job details extracted successfully"
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'data': None
        }


def create_manual_job_data(job_title: str, company_name: str, job_description: str) -> Dict:
    """
    Create job data structure from manual input with enhanced parsing
    """
    if not job_title or not company_name:
        return {
            'success': False,
            'error': "Job title and company name are required",
            'data': None
        }
    
    # Parse hiring person information
    hiring_person = extract_hiring_person(job_description)
    contact_email = extract_contact_email(job_description)
    subject_line = extract_subject_line(job_description)
    organization = extract_organization(job_description, company_name)
    
    job_data = {
        'job_title': job_title.strip(),
        'company': organization,
        'location': extract_location(job_description),
        'description': job_description.strip() if job_description else "No description provided",
        'requirements': extract_enhanced_requirements(job_description),
        'employment_type': extract_employment_type(job_description),
        'experience_level': extract_experience_level(job_description),
        'contact_info': {
            'hiring_manager': hiring_person,
            'contact_email': contact_email,
            'suggested_subject': subject_line,
            'suggested_emails': [contact_email] if contact_email else generate_suggested_emails(organization),
            'note': "Extracted from job posting"
        },
        'url': "Manual Entry"
    }
    
    return {
        'success': True,
        'data': job_data,
        'message': "Manual job data created successfully"
    }

def extract_hiring_person(description: str) -> str:
    """Extract hiring person name from job description"""
    if not description:
        return None
    
    # Look for patterns like "Contact John Doe", "Reach out to Jane Smith", email signatures
    patterns = [
        r'contact\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'reach\s+out\s+to\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'hiring\s+manager[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+)',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+)@[a-zA-Z0-9.-]+',  # Name before email
        r'^([A-Z][a-z]+\s+[A-Z][a-z]+)$',  # Name on its own line
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            # Validate it looks like a real name
            if len(match.split()) == 2 and all(part.isalpha() for part in match.split()):
                return match.title()
    
    return None

def extract_contact_email(description: str) -> str:
    """Extract contact email from job description"""
    if not description:
        return None
    
    # Find email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, description)
    
    if emails:
        # Prefer non-generic emails
        for email in emails:
            if not any(generic in email.lower() for generic in ['noreply', 'donotreply', 'no-reply']):
                return email
        return emails[0]  # Fallback to first email
    
    return None

def extract_subject_line(description: str) -> str:
    """Extract suggested subject line from job description"""
    if not description:
        return None
    
    # Look for patterns like "Keep subject: ...", "Subject: ...", "Use subject: ..."
    patterns = [
        r'keep\s+subject\s*[:\-]\s*(.+?)(?:\n|$)',
        r'subject\s*[:\-]\s*(.+?)(?:\n|$)',
        r'use\s+subject\s*[:\-]\s*(.+?)(?:\n|$)',
        r'email\s+subject\s*[:\-]\s*(.+?)(?:\n|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description, re.IGNORECASE | re.MULTILINE)
        if matches:
            subject = matches[0].strip().strip('"\'')
            if 5 < len(subject) < 100:  # Reasonable subject length
                return subject
    
    return None

def extract_organization(description: str, company_name: str) -> str:
    """Extract organization name, with fallback to company_name"""
    if not description:
        return company_name
    
    # Look for specific organization mentions
    patterns = [
        r'(?:at|in|for)\s+([A-Z][a-zA-Z\s]+(?:Team|Department|Division))',
        r'([A-Z][a-zA-Z\s]+(?:Inc|Corp|Ltd|LLC|Company))',
        r'join\s+([A-Z][a-zA-Z\s]+)(?:\s+team)?',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description)
        for match in matches:
            if 3 < len(match.strip()) < 50:
                return match.strip()
    
    return company_name

def extract_location(description: str) -> str:
    """Extract work location from description"""
    if not description:
        return "Not Specified"
    
    # Look for location patterns
    patterns = [
        r'work\s+from\s+([A-Za-z\s,]+?)(?:\s+office|\.|$)',
        r'location[:\s]+([A-Za-z\s,]+?)(?:\.|$)',
        r'office[:\s]+([A-Za-z\s,]+?)(?:\.|$)',
        r'based\s+in\s+([A-Za-z\s,]+?)(?:\.|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description, re.IGNORECASE)
        if matches:
            location = matches[0].strip().strip(',')
            if 3 < len(location) < 50:
                return location
    
    return "Not Specified"

def extract_enhanced_requirements(description: str) -> List[str]:
    """Extract job requirements with better parsing"""
    if not description:
        return []
    
    requirements = []
    
    # Split by common delimiters
    sentences = re.split(r'[.•\n\-]', description)
    
    for sentence in sentences:
        sentence = sentence.strip()
        # Look for requirement indicators
        if any(keyword in sentence.lower() for keyword in 
               ['required', 'must have', 'experience', 'skill', 'knowledge', 'years', 'minimum']):
            if 10 < len(sentence) < 200:  # Reasonable length
                requirements.append(sentence.strip())
    
    return requirements[:8]  # Limit to top 8

def extract_employment_type(description: str) -> str:
    """Extract employment type from description"""
    if not description:
        return "Not Specified"
    
    types = {
        'full-time': ['full time', 'full-time', 'permanent'],
        'part-time': ['part time', 'part-time'],
        'contract': ['contract', 'contractor', 'freelance'],
        'internship': ['intern', 'internship', 'trainee']
    }
    
    description_lower = description.lower()
    for emp_type, keywords in types.items():
        if any(keyword in description_lower for keyword in keywords):
            return emp_type.title()
    
    return "Full-time"  # Default assumption

def extract_experience_level(description: str) -> str:
    """Extract experience level from description"""
    if not description:
        return "Not Specified"
    
    # Look for year patterns
    year_patterns = [
        r'(\d+)[\+\-]*\s*years?\s+(?:of\s+)?(?:minimum\s+)?experience',
        r'(\d+)[\+\-]*\s*years?\s+(?:minimum|min)',
        r'minimum\s+(\d+)\s*years?',
        r'(\d+)[\+\-]*\s*yrs?\s+experience',
    ]
    
    for pattern in year_patterns:
        matches = re.findall(pattern, description.lower())
        if matches:
            years = int(matches[0])
            if years <= 2:
                return f"{years}+ years (Entry Level)"
            elif years <= 5:
                return f"{years}+ years (Mid Level)"
            else:
                return f"{years}+ years (Senior Level)"
    
    return "Not Specified"

def generate_suggested_emails(company: str) -> List[str]:
    """Generate suggested email addresses based on company name"""
    if not company:
        return ["careers@company.com"]
    
    clean_company = re.sub(r'[^\w\s]', '', company.lower()).replace(' ', '')
    suggestions = [
        f"careers@{clean_company}.com",
        f"hr@{clean_company}.com", 
        f"jobs@{clean_company}.com",
        f"hiring@{clean_company}.com"
    ]
    
    return suggestions