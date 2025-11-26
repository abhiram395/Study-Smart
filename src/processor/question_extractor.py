import re

class QuestionExtractor:
    def __init__(self):
        # Regex patterns for common question numbering
        self.split_patterns = [
            r'(?:\n|^|\s)(Q\.?\s*\d+[\.:\)])',  # Q.1, Q1., Q 1)
            r'(?:\n|^|\s)(\d+[\.:\)])',         # 1., 1)
            r'(?:\n|^|\s)(\([a-zA-Z0-9]+\))',   # (a), (1)
            r'(?:\n|^|\s)([a-zA-Z][\.:\)])'     # a., a)
        ]

    def clean_text(self, text):
        """
        Removes common noise found in question papers.
        """
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove page numbers (e.g., Page 1 of 3, 2 | Page)
        text = re.sub(r'(?:Page\s+\d+\s+of\s+\d+|\d+\s*\|\s*Page)', '', text, flags=re.IGNORECASE)
        
        # Remove paper codes (e.g., [5E1352], 5E1352 at start/end of lines)
        text = re.sub(r'\[\w{4,}\]', '', text)
        
        # Remove common header/footer lines completely
        # Matches lines containing these keywords, replacing the WHOLE line
        header_keywords = r'(Roll\s*No|Total\s*No\.?\s*of\s*Pages|Maximum\s*Marks|Time\s*Allowed|Paper\s*ID|Candidate\s*Name|Semester|B\.Tech|Part\s*-[A-Z]|Section\s*-[A-Z])'
        text = re.sub(r'^.*' + header_keywords + r'.*$', '', text, flags=re.IGNORECASE | re.MULTILINE)
        
        # Remove lines that are just paper codes (e.g. 5E1352) or short garbage
        text = re.sub(r'^\s*\w{4,6}\s*$', '', text, flags=re.MULTILINE)

        return text

    def is_valid_question(self, text):
        """
        Checks if the text looks like a valid question.
        """
        if len(text) < 15: # Too short
            return False
            
        # Check for high density of symbols/garbage
        # If more than 30% of characters are non-alphanumeric (excluding spaces), it's likely garbage
        non_alnum = sum(1 for c in text if not c.isalnum() and not c.isspace())
        if non_alnum / len(text) > 0.3:
            return False
            
        # Must contain at least some vowels (basic language check)
        if not re.search(r'[aeiou]', text, re.IGNORECASE):
            return False
            
        return True

    def extract_questions(self, raw_text):
        """
        Splits raw text into a list of questions.
        Includes heuristics to merge multi-line questions and ignore garbage.
        """
        if not raw_text:
            return []
            
        # 1. Clean the text first
        cleaned_text = self.clean_text(raw_text)
        
        # 2. Split by newlines first to handle structure
        lines = cleaned_text.split('\n')
        questions = []
        current_question = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip short garbage lines
            if len(line) < 3:
                continue

            # Check if this line STARTS with a question pattern
            is_new_question = False
            for pattern in self.split_patterns:
                if re.match(r'^(Q\.?\s*\d+[\.:\)]|\d+[\.:\)]|\([a-zA-Z0-9]+\)|[a-zA-Z][\.:\)])', line):
                    is_new_question = True
                    break
            
            if is_new_question:
                if current_question:
                    q_text = " ".join(current_question).strip()
                    if self.is_valid_question(q_text): 
                        questions.append(q_text)
                current_question = [line]
            else:
                current_question.append(line)
                
        if current_question:
            q_text = " ".join(current_question).strip()
            if self.is_valid_question(q_text):
                questions.append(q_text)
            
        return questions
