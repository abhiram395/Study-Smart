from .pdf_loader import PDFLoader
import re

class SyllabusParser:
    def __init__(self):
        self.loader = PDFLoader()

    def parse_syllabus(self, file_path):
        """
        Parses the syllabus PDF and extracts a list of topics.
        This is a simplified implementation. A real one would need
        complex NLP to distinguish 'topics' from 'instructions'.
        """
        raw_text = self.loader.extract_text(file_path)
        if not raw_text:
            return []

        # Naive topic extraction: assume lines that are not too long and not too short are topics
        # In a real scenario, we'd use the user's input or specific formatting (bold, headers)
        
        lines = raw_text.split('\n')
        topics = []
        
        for line in lines:
            cleaned = line.strip()
            # Filter out page numbers, short headers, etc.
            if len(cleaned) > 5 and len(cleaned) < 100:
                # Remove bullet points
                cleaned = re.sub(r'^[\d\.\-\•\●]+\s*', '', cleaned)
                topics.append(cleaned)
                
        return topics

    def validate_topic(self, question_text, syllabus_topics):
        """
        Checks if a question is relevant to the syllabus.
        Returns True/False and a score.
        """
        # TODO: Implement semantic similarity here using embeddings
        # For now, simple keyword matching
        
        question_lower = question_text.lower()
        for topic in syllabus_topics:
            topic_lower = topic.lower()
            # Check if significant words from topic appear in question
            topic_words = set(topic_lower.split())
            question_words = set(question_lower.split())
            
            common = topic_words.intersection(question_words)
            if len(common) >= 1: # Very loose matching
                return True
                
        return False
