import streamlit as st
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="LinkedIn Job Application Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Main application function"""
    
    # Header
    st.title("📧 LinkedIn Job Application Assistant")
    st.markdown("### Generate personalized cover letters and emails for your job applications")
    st.markdown("---")
    
    # Check for API key
    try:
        api_key = st.secrets["general"]["OPENAI_API_KEY"]
        if not api_key or api_key == "your-openai-api-key-here":
            st.error("⚠️ OpenAI API key not configured. Please add your API key to deploy the application.")
            st.stop()
    except KeyError:
        st.error("⚠️ OpenAI API key not found in secrets. Please configure your API key.")
        st.stop()
    
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
        
        if input_method == "Upload File (PDF/DOCX)":
            uploaded_file = st.file_uploader(
                "Upload your resume",
                type=["pdf", "docx"],
                help="Upload your resume in PDF or Word format"
            )
            if uploaded_file:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                # TODO: Extract text from file
                resume_text = f"[File uploaded: {uploaded_file.name}]"
        else:
            resume_text = st.text_area(
                "Paste your resume text here:",
                height=300,
                placeholder="Copy and paste your resume content here...",
                help="Include all relevant sections: contact info, experience, skills, education"
            )
            
        if resume_text:
            st.info(f"📊 Resume length: {len(resume_text)} characters")
    
    with col2:
        st.subheader("🔗 Job Information")
        
        # LinkedIn URL input
        linkedin_url = st.text_input(
            "LinkedIn Job Posting URL:",
            placeholder="https://www.linkedin.com/jobs/view/...",
            help="Paste the LinkedIn job posting URL here"
        )
        
        # Manual job details fallback
        with st.expander("💡 Or enter job details manually (fallback option)"):
            job_title = st.text_input("Job Title:", placeholder="e.g., Software Engineer")
            company_name = st.text_input("Company Name:", placeholder="e.g., Google")
            job_description = st.text_area(
                "Job Description:",
                height=200,
                placeholder="Paste job description and requirements here..."
            )
    
    # Generation options
    st.subheader("⚙️ Generation Options")
    
    col3, col4 = st.columns([1, 3])
    
    with col3:
        tone = st.selectbox(
            "Select tone:",
            ["Professional", "Warm", "Concise"],
            help="Choose the tone for your cover letter and email"
        )
    
    with col4:
        st.info("💡 **Tip:** Professional tone is recommended for corporate roles, Warm for startups, and Concise for technical positions.")
    
    # Generate button
    st.markdown("---")
    
    if st.button("🚀 Generate Application Materials", type="primary", use_container_width=True):
        if not resume_text:
            st.error("❌ Please provide your resume (upload file or paste text)")
            return
        
        if not linkedin_url and not (job_title and company_name):
            st.error("❌ Please provide either a LinkedIn URL or manual job details")
            return
        
        # Processing placeholder
        with st.spinner("🔄 Processing your application materials..."):
            # TODO: Implement actual processing
            st.success("✅ Processing completed!")
            
            # Placeholder outputs
            st.subheader("📝 Generated Cover Letter")
            st.text_area(
                "Cover Letter:",
                value="[Generated cover letter will appear here...]",
                height=200,
                key="cover_letter_output"
            )
            
            st.subheader("📧 Email Draft")
            
            col5, col6, col7 = st.columns([1, 2, 3])
            
            with col5:
                st.text_input("To:", value="hiring.manager@company.com", key="email_to")
            
            with col6:
                st.text_input("Subject:", value="Software Engineer Application - John Doe", key="email_subject")
            
            with col7:
                st.text_area(
                    "Email Body:",
                    value="[Generated email body will appear here...]",
                    height=150,
                    key="email_body"
                )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🤖 Powered by OpenAI GPT | Built with Streamlit</p>
            <p>⚠️ Review all generated content before sending</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()