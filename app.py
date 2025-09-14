import streamlit as st
import time
from datetime import datetime
from typing import Optional, Dict, Any

# Import our backend modules
from resume_processor import process_resume_input
from job_scraper import scrape_linkedin_job, create_manual_job_data
from content_generator import generate_application_content
from models import ToneType, GenerationResult

# Page configuration
st.set_page_config(
    page_title="LinkedIn Job Application Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'job_data' not in st.session_state:
    st.session_state.job_data = None
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'processing_step' not in st.session_state:
    st.session_state.processing_step = 0

def check_api_key():
    """Check if OpenAI API key is configured"""
    try:
        api_key = st.secrets["general"]["OPENAI_API_KEY"]
        if not api_key or api_key == "your-openai-api-key-here":
            st.error("⚠️ OpenAI API key not configured. Please add your API key to deploy the application.")
            st.info("💡 Add your OpenAI API key to `.streamlit/secrets.toml` for local development or Streamlit Cloud secrets for deployment.")
            st.stop()
        return True
    except KeyError:
        st.error("⚠️ OpenAI API key not found in secrets. Please configure your API key.")
        st.info("� Create `.streamlit/secrets.toml` file with your OpenAI API key.")
        st.stop()

def create_copy_button(text: str, label: str, key: str):
    """Create a copy button for text content"""
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_area(label, value=text, height=100, key=f"display_{key}")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
        if st.button("📋 Copy", key=f"copy_{key}", help="Click to select text for copying"):
            st.code(text, language=None)
            st.success("✅ Text ready to copy!")

def display_progress_bar(step: int, total_steps: int, status_text: str):
    """Display progress bar with current status"""
    progress = step / total_steps
    progress_bar = st.progress(progress)
    st.write(f"**Step {step}/{total_steps}:** {status_text}")
    return progress_bar

def display_quality_metrics(result: GenerationResult):
    """Display content quality metrics"""
    if result.quality_metrics:
        st.subheader("📊 Content Quality Assessment")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Personalization Score",
                f"{result.quality_metrics.personalization_score:.0%}",
                help="How well the content matches your background to the job"
            )
        
        with col2:
            st.metric(
                "Professional Standard",
                f"{result.quality_metrics.professional_standard_score:.0%}",
                help="Quality of professional communication"
            )
        
        with col3:
            st.metric(
                "Generation Time",
                f"{result.generation_time:.1f}s",
                help="Time taken to generate content"
            )
        
        # Additional metrics
        if result.quality_metrics.specific_examples_count > 0:
            st.success(f"✅ {result.quality_metrics.specific_examples_count} specific examples included")
        
        if result.quality_metrics.achievement_mentions > 0:
            st.success(f"✅ {result.quality_metrics.achievement_mentions} achievements highlighted")

def display_personalization_matches(result: GenerationResult):
    """Display personalization matches found"""
    if result.personalization_matches:
        st.subheader("🎯 Experience Matches Found")
        
        for i, match in enumerate(result.personalization_matches[:3], 1):
            with st.expander(f"Match {i}: {match.relevance_score:.0%} relevance"):
                st.write(f"**Your Experience:** {match.resume_point}")
                st.write(f"**Job Requirement:** {match.job_requirement}")
                st.write(f"**Why it's relevant:** {match.explanation}")

def process_application_pipeline(resume_text: str = None, uploaded_file = None, 
                               linkedin_url: str = None, job_title: str = None, 
                               company_name: str = None, job_description: str = None,
                               tone: str = "Professional"):
    """Main processing pipeline with progress tracking"""
    
    # Create progress container
    progress_container = st.container()
    
    with progress_container:
        # Step 1: Process Resume
        st.write("### 🔄 Processing Pipeline")
        progress_bar = display_progress_bar(1, 4, "Processing resume...")
        
        try:
            resume_result = process_resume_input(
                uploaded_file=uploaded_file,
                manual_text=resume_text
            )
            
            if not resume_result['success']:
                st.error(f"❌ Resume processing failed: {resume_result['error']}")
                return None
                
            st.session_state.resume_data = resume_result['data']
            time.sleep(0.5)  # Small delay for user experience
            
            # Step 2: Process Job Information
            progress_bar.progress(0.5)
            st.write("**Step 2/4:** Extracting job details...")
            
            if linkedin_url:
                job_result = scrape_linkedin_job(linkedin_url)
            else:
                job_result = create_manual_job_data(job_title, company_name, job_description)
            
            if not job_result['success']:
                st.error(f"❌ Job processing failed: {job_result['error']}")
                return None
                
            st.session_state.job_data = job_result['data']
            time.sleep(0.5)
            
            # Step 3: Generate Content
            progress_bar.progress(0.75)
            st.write("**Step 3/4:** Generating personalized content with AI...")
            
            content_result = generate_application_content(
                resume_data=st.session_state.resume_data,
                job_data=st.session_state.job_data,
                tone=tone,
                include_company_research=True
            )
            
            if not content_result.success:
                st.error(f"❌ Content generation failed: {content_result.error_message}")
                return None
            
            st.session_state.generated_content = content_result
            time.sleep(0.5)
            
            # Step 4: Complete
            progress_bar.progress(1.0)
            st.write("**Step 4/4:** Complete! ✅")
            
            return content_result
            
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return None

def main():
    """Main application function"""
    
    # Check API key first
    check_api_key()
    
    # Header
    st.title("📧 LinkedIn Job Application Assistant")
    st.markdown("### Generate personalized cover letters and emails powered by GPT-4o")
    
    # Progress indicator
    if st.session_state.resume_data and st.session_state.job_data and st.session_state.generated_content:
        st.success("🎉 **Status:** Resume ✅ | Job Details ✅ | AI Generation ✅ | Ready to Copy!")
    elif st.session_state.resume_data and st.session_state.job_data:
        st.info("📊 **Status:** Resume ✅ | Job Details ✅ | Ready to Generate")
    elif st.session_state.resume_data:
        st.info("📊 **Status:** Resume ✅ | Add Job Details")
    else:
        st.info("📊 **Status:** Add Resume & Job Details to Begin")
    
    st.markdown("---")
    
    # Create two columns for input
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📄 Resume Input")
        
        # Resume input options
        input_method = st.radio(
            "Choose input method:",
            ["Upload File (PDF/DOCX)", "Paste Resume Text"],
            key="resume_input_method"
        )
        
        resume_text = ""
        uploaded_file = None
        
        if input_method == "Upload File (PDF/DOCX)":
            uploaded_file = st.file_uploader(
                "Upload your resume",
                type=["pdf", "docx"],
                help="Upload your resume in PDF or Word format"
            )
            if uploaded_file:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                st.info("💡 File will be processed when you click Generate")
        else:
            resume_text = st.text_area(
                "Paste your resume text here:",
                height=300,
                placeholder="Copy and paste your resume content here...\n\nInclude:\n• Contact information\n• Work experience\n• Skills and education\n• Key achievements",
                help="Include all relevant sections: contact info, experience, skills, education"
            )
            
        if resume_text:
            st.info(f"📊 Resume length: {len(resume_text)} characters")
            if len(resume_text) < 100:
                st.warning("⚠️ Resume seems short. Add more details for better personalization.")
    
    with col2:
        st.subheader("🔗 Job Information")
        
        # LinkedIn URL input
        linkedin_url = st.text_input(
            "LinkedIn Job Posting URL:",
            placeholder="https://www.linkedin.com/jobs/view/...",
            help="Paste the LinkedIn job posting URL here"
        )
        
        if linkedin_url:
            if "linkedin.com" not in linkedin_url:
                st.warning("⚠️ Please enter a valid LinkedIn URL")
            else:
                st.success("✅ LinkedIn URL provided")
        
        # Manual job details fallback
        st.markdown("**OR enter job details manually:**")
        job_title = st.text_input("Job Title:", placeholder="e.g., Software Engineer")
        company_name = st.text_input("Company Name:", placeholder="e.g., Google")
        job_description = st.text_area(
            "Job Description:",
            height=200,
            placeholder="Paste job description and requirements here...",
            help="Include key requirements, responsibilities, and qualifications"
        )
        
        if job_title and company_name:
            st.success("✅ Manual job details provided")
    
    # Generation options
    st.markdown("---")
    st.subheader("⚙️ Generation Options")
    
    col3, col4 = st.columns([1, 3])
    
    with col3:
        tone = st.selectbox(
            "Select tone:",
            ["Professional", "Warm", "Concise"],
            help="Choose the tone for your cover letter and email"
        )
    
    with col4:
        tone_descriptions = {
            "Professional": "🏢 Formal, business-appropriate language. Best for corporate roles.",
            "Warm": "😊 Friendly but professional. Great for startups and creative roles.",
            "Concise": "⚡ Direct and to-the-point. Perfect for technical positions."
        }
        st.info(f"**{tone} tone:** {tone_descriptions[tone]}")
    
    # Generate button
    st.markdown("---")
    
    # Validation
    has_resume = bool(resume_text or uploaded_file)
    has_job = bool(linkedin_url or (job_title and company_name))
    
    if not has_resume:
        st.warning("📄 Please provide your resume (upload file or paste text)")
    
    if not has_job:
        st.warning("🔗 Please provide job information (LinkedIn URL or manual entry)")
    
    # Generate button
    if st.button("🚀 Generate Application Materials", 
                type="primary", 
                use_container_width=True,
                disabled=not (has_resume and has_job)):
        
        # Process the application
        result = process_application_pipeline(
            resume_text=resume_text,
            uploaded_file=uploaded_file,
            linkedin_url=linkedin_url,
            job_title=job_title,
            company_name=company_name,
            job_description=job_description,
            tone=tone
        )
        
        if result:
            st.success("🎉 Application materials generated successfully!")
    
    # Display results if available
    if st.session_state.generated_content:
        result = st.session_state.generated_content
        
        st.markdown("---")
        st.header("📋 Generated Application Materials")
        
        # Display quality metrics
        display_quality_metrics(result)
        
        # Display personalization matches
        display_personalization_matches(result)
        
        st.markdown("---")
        
        # Cover Letter and Email in columns
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 Cover Letter")
            
            if result.cover_letter:
                # Combine all paragraphs
                full_cover_letter = "\n\n".join([
                    result.cover_letter.opening_paragraph,
                    result.cover_letter.body_paragraph_1,
                    result.cover_letter.body_paragraph_2,
                    result.cover_letter.closing_paragraph
                ])
                
                st.text_area(
                    f"Cover Letter ({result.cover_letter.word_count} words):",
                    value=full_cover_letter,
                    height=300,
                    key="cover_letter_display"
                )
                
                if st.button("📋 Copy Cover Letter", key="copy_cover_letter"):
                    st.code(full_cover_letter, language=None)
                    st.success("✅ Cover letter ready to copy!")
                
                # Show personalization elements
                if result.cover_letter.personalization_elements:
                    with st.expander("🎯 Personalization Elements"):
                        for element in result.cover_letter.personalization_elements:
                            st.write(f"• {element}")
        
        with col2:
            st.subheader("📧 Email Draft")
            
            if result.email_draft:
                # Email components
                st.text_input("To:", value=result.email_draft.to_email, key="email_to_display")
                st.text_input("Subject:", value=result.email_draft.subject_line, key="email_subject_display")
                
                # Full email body
                full_email = "\n\n".join([
                    result.email_draft.greeting,
                    result.email_draft.body_paragraph_1,
                    result.email_draft.body_paragraph_2,
                    result.email_draft.closing_paragraph,
                    result.email_draft.signature
                ])
                
                st.text_area(
                    f"Email Body ({result.email_draft.word_count} words):",
                    value=full_email,
                    height=300,
                    key="email_body_display"
                )
                
                if st.button("📋 Copy Email", key="copy_email"):
                    email_with_subject = f"Subject: {result.email_draft.subject_line}\n\n{full_email}"
                    st.code(email_with_subject, language=None)
                    st.success("✅ Email ready to copy!")
        
        # Regeneration options
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🔄 Regenerate with Different Tone", use_container_width=True):
                st.session_state.generated_content = None
                st.rerun()
        
        with col2:
            if st.button("✏️ Edit Inputs", use_container_width=True):
                st.session_state.resume_data = None
                st.session_state.job_data = None
                st.session_state.generated_content = None
                st.rerun()
        
        with col3:
            if st.button("💾 Start New Application", use_container_width=True):
                # Clear all session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🤖 Powered by OpenAI GPT-4o | Built with Streamlit</p>
            <p>⚠️ Review all generated content before sending</p>
            <p>💡 Generated in {:.1f}s | Professional quality assured</p>
        </div>
        """.format(st.session_state.generated_content.generation_time if st.session_state.generated_content else 0),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()