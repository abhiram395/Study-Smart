import google.generativeai as genai
import os

class AnswerGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            
            # Priority list of models to try
            preferred_models = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            self.model = None
            
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Try to find a preferred model first
            for preferred in preferred_models:
                # Check if any available model contains the preferred string (e.g. 'models/gemini-1.5-flash-001')
                match = next((m for m in available_models if preferred in m), None)
                if match:
                    self.model = genai.GenerativeModel(match)
                    print(f"Selected preferred model: {match}")
                    break
            
            # Fallback: pick the first available 'gemini' model if no preferred one found
            if not self.model:
                for m in available_models:
                    if 'gemini' in m:
                        self.model = genai.GenerativeModel(m)
                        print(f"Fallback model: {m}")
                        break

    def generate_answer(self, question, subject, marks=10):
        """
        Generates a model answer for a given question.
        """
        if not self.model:
            return "Error: API Key not configured."

        prompt = f"""
        You are an expert academic professor in {subject}.
        Please write a model answer for the following exam question.
        
        Question: "{question}"
        
        Guidelines:
        - Assume this is for a {marks}-mark question.
        - Structure the answer with clear headings and bullet points.
        - Include a brief introduction and conclusion.
        - If applicable, mention key diagrams or examples (describe them in text).
        - Keep the tone academic and precise.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {str(e)}"
