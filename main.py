import streamlit as st
import os
import tempfile
from src.processor.pdf_loader import PDFLoader
from src.processor.syllabus_parser import SyllabusParser
from src.processor.question_extractor import QuestionExtractor
from src.analyzer.semantic_modeler import SemanticModeler
from src.predictor.predictor import Predictor
from src.collector.web_scraper import WebScraper

from src.generator.answer_generator import AnswerGenerator

def save_uploaded_file(uploaded_file):
    try:
        suffix = os.path.splitext(uploaded_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def main():
    st.set_page_config(page_title="Question Paper Predictor", layout="wide")
    
    st.title("📚 Exam Question Predictor")
    st.markdown("""
    Upload your **Syllabus** and **Previous Year Question Papers** to generate predictions.
    Supports **PDFs** and **Images**. Can also **Auto-Fetch** papers from the web.
    """)

    with st.sidebar:
        st.header("Configuration")
        subject_name = st.text_input("Subject Name", "General")
        university_name = st.text_input("University / Board", "", placeholder="e.g. RTU, Mumbai University, CBSE")
        
        st.divider()
        st.header("🤖 AI Features")
        api_key = st.text_input("Gemini API Key", type="password", help="Get your free key from aistudio.google.com")
        
        with st.expander("Advanced Settings"):
            tesseract_path = st.text_input("Tesseract Path (Optional)", value="", placeholder="C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
            
        if st.button("🔄 Reset App"):
            st.session_state.clear()
            st.rerun()
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Upload Syllabus")
        syllabus_file = st.file_uploader("Upload Syllabus (PDF/Image)", type=['pdf', 'jpg', 'jpeg', 'png'], key="syllabus")
        
    with col2:
        st.subheader("2. Question Papers")
        input_method = st.radio("Choose Input Method:", ["Upload Files", "Auto-Fetch from Web"])
        
        paper_files = []
        if input_method == "Upload Files":
            paper_files = st.file_uploader("Upload Papers (PDF/JPG/PNG)", type=['pdf', 'jpg', 'jpeg', 'png'], accept_multiple_files=True, key="papers")
        else:
            st.info(f"Will search for '{subject_name}' papers post-2020.")

    # Initialize session state for data persistence
    if 'study_plan' not in st.session_state:
        st.session_state['study_plan'] = None
    if 'processed_data' not in st.session_state:
        st.session_state['processed_data'] = None
    if 'paper_paths' not in st.session_state:
        st.session_state['paper_paths'] = []

    if st.button("Analyze & Predict", type="primary"):
        if not syllabus_file:
            st.error("Please upload a syllabus file.")
            return
            
        if input_method == "Upload Files" and not paper_files:
            st.error("Please upload at least one question paper.")
            return

        with st.spinner("Initializing modules..."):
            loader = PDFLoader(tesseract_cmd=tesseract_path if tesseract_path else None)
            syllabus_parser = SyllabusParser()
            extractor = QuestionExtractor()
            modeler = SemanticModeler(n_topics=5)
            predictor = Predictor()
            scraper = WebScraper()

        # 1. Process Syllabus
        with st.spinner("Processing Syllabus..."):
            syl_path = save_uploaded_file(syllabus_file)
            syllabus_topics = syllabus_parser.parse_syllabus(syl_path)
            st.success(f"Extracted {len(syllabus_topics)} topics from syllabus.")
            with st.expander("View Syllabus Topics"):
                st.write(syllabus_topics)

        # 2. Acquire Papers
        paper_paths = []
        if input_method == "Upload Files":
            for p_file in paper_files:
                p_path = save_uploaded_file(p_file)
                if p_path:
                    paper_paths.append(p_path)
        else:
            with st.spinner("Searching and downloading papers..."):
                paper_paths = scraper.find_papers(subject_name, university_name)
                if not paper_paths:
                    st.error("No papers found online. Please upload manually.")
                    return
                st.success(f"Downloaded {len(paper_paths)} papers.")
        
        st.session_state['paper_paths'] = paper_paths

        # 3. Process Papers
        processed_data = []
        
        progress_bar = st.progress(0)
        for i, p_path in enumerate(paper_paths):
            with st.spinner(f"Processing paper {i+1}..."):
                raw_text = loader.extract_text(p_path)
                
                if raw_text:
                    questions = extractor.extract_questions(raw_text)
                    valid_data = modeler.filter_by_syllabus(questions, syllabus_topics)
                    
                    processed_data.append({
                        'filename': os.path.basename(p_path),
                        'questions': valid_data
                    })
            
            progress_bar.progress((i + 1) / len(paper_paths))

        if not processed_data:
            st.error("No valid data processed.")
            return
            
        st.session_state['processed_data'] = processed_data

        # 4. Generate Study Plan
        with st.spinner("Generating Study Strategy..."):
            study_plan = predictor.generate_study_plan(processed_data)
            st.session_state['study_plan'] = study_plan

    # --- Display Dashboard if data exists ---
    if st.session_state['study_plan']:
        study_plan = st.session_state['study_plan']
        paper_paths = st.session_state['paper_paths']
        
        # Re-initialize modules for interaction if needed (like scraper/answer_gen)
        # We need these for the buttons to work
        scraper = WebScraper()
        answer_gen = AnswerGenerator(api_key) if api_key else None
            
        st.divider()
        st.header("📈 Smart Study Plan")
        st.markdown(f"**Subject:** {subject_name} | **Based on:** {len(paper_paths)} papers")
        
        # Dashboard Metrics
        col1, col2, col3 = st.columns(3)
        high_pri = len([t for t in study_plan if t['priority'] == 'High'])
        med_pri = len([t for t in study_plan if t['priority'] == 'Medium'])
        
        col1.metric("High Priority Topics", high_pri)
        col2.metric("Medium Priority Topics", med_pri)
        col3.metric("Total Topics Found", len(study_plan))
        
        st.subheader("Topic Priority List")
        
        for item in study_plan:
            priority_color = "red" if item['priority'] == "High" else "orange" if item['priority'] == "Medium" else "green"
            
            with st.expander(f"**{item['topic']}**  [{item['priority']}] - {item['weightage']}% Weightage"):
                col_a, col_b = st.columns([3, 1])
                
                with col_a:
                    st.markdown(f"**Frequency:** Appeared {item['count']} times")
                    st.markdown(f"**Priority:** :{priority_color}[{item['priority']}]")
                    st.markdown("---")
                    st.markdown("**Example Questions:**")
                    for idx, q in enumerate(item['example_questions']):
                        st.markdown(f"- {q}")
                        if api_key:
                            # Create a unique key for this question
                            q_key = f"ans_{item['topic']}_{idx}"
                            
                            # Initialize session state for answers if needed
                            if 'generated_answers' not in st.session_state:
                                st.session_state['generated_answers'] = {}
                            
                            # Check if we already have an answer
                            existing_ans = st.session_state['generated_answers'].get(q_key)
                            
                            if existing_ans:
                                st.markdown("### Model Answer")
                                st.info(existing_ans)
                            else:
                                if st.button(f"✨ Generate Answer", key=f"btn_{q_key}"):
                                    with st.spinner("Writing answer..."):
                                        ans = answer_gen.generate_answer(q, subject_name)
                                        st.session_state['generated_answers'][q_key] = ans
                                        st.rerun()
                        
                with col_b:
                    if item['priority'] == "High":
                        if st.button(f"📚 Study Materials", key=f"btn_{item['topic']}"):
                            with st.spinner("Fetching resources..."):
                                links = scraper.find_study_material(item['topic'])
                                if links:
                                    for title, url in links:
                                        st.markdown(f"[{title}]({url})")
                                else:
                                    st.info("No specific links found.")

        st.success("Analysis Complete! Focus on the High Priority topics first.")

if __name__ == "__main__":
    main()
