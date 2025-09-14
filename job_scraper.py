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
    Create job data structure from manual input
    """
    if not job_title or not company_name:
        return {
            'success': False,
            'error': "Job title and company name are required",
            'data': None
        }
    
    job_data = {
        'job_title': job_title.strip(),
        'company': company_name.strip(),
        'location': "Not Specified",
        'description': job_description.strip() if job_description else "No description provided",
        'requirements': [],
        'employment_type': "Not Specified",
        'experience_level': "Not Specified",
        'contact_info': {
            'hiring_manager': "Hiring Manager",
            'suggested_emails': [f"careers@{re.sub(r'[^\w]', '', company_name.lower())}.com"],
            'note': "Manual entry - contact information estimated"
        },
        'url': "Manual Entry"
    }
    
    # Extract requirements from description if provided
    if job_description:
        sentences = re.split(r'[.•\n]', job_description)
        requirements = []
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in ['required', 'must', 'experience', 'skill']):
                if 20 < len(sentence) < 150:
                    requirements.append(sentence)
        job_data['requirements'] = requirements[:5]
    
    return {
        'success': True,
        'data': job_data,
        'message': "Manual job data created successfully"
    }