import sys
import os

# Add project root to path
sys.path.append(os.path.abspath("C:/Users/Admin/OneDrive/Desktop/question_predictor"))

try:
    print("Testing imports...")
    from src.processor.pdf_loader import PDFLoader
    from src.processor.syllabus_parser import SyllabusParser
    from src.processor.question_extractor import QuestionExtractor
    from src.analyzer.topic_modeler import TopicModeler
    from src.predictor.predictor import Predictor
    print("Imports successful.")

    print("Testing instantiation...")
    loader = PDFLoader()
    parser = SyllabusParser()
    extractor = QuestionExtractor()
    modeler = TopicModeler()
    predictor = Predictor()
    print("Instantiation successful.")
    
    print("All checks passed!")

except Exception as e:
    print(f"Verification failed: {e}")
    sys.exit(1)
