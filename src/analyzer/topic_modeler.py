from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TopicModeler:
    def __init__(self, n_topics=10):
        self.n_topics = n_topics
        self.vectorizer = CountVectorizer(stop_words='english', max_df=0.95, min_df=2)
        self.lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        self.feature_names = None

    def fit_transform(self, questions):
        """
        Fits LDA model to the questions and returns the topic distribution.
        """
        if not questions:
            return None, None
            
        dtm = self.vectorizer.fit_transform(questions)
        self.lda.fit(dtm)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        # Get dominant topic for each question
        topic_results = self.lda.transform(dtm)
        return topic_results

    def get_topic_keywords(self, topic_idx, n_words=5):
        """
        Returns top keywords for a given topic.
        """
        topic = self.lda.components_[topic_idx]
        top_indices = topic.argsort()[:-n_words - 1:-1]
        return [self.feature_names[i] for i in top_indices]

    def filter_by_syllabus(self, questions, syllabus_topics, threshold=0.1):
        """
        Filters questions that don't match syllabus topics using TF-IDF similarity.
        """
        if not syllabus_topics:
            return questions # Return all if no syllabus provided
            
        tfidf = TfidfVectorizer(stop_words='english')
        # Fit on combined corpus to ensure same vocabulary
        all_text = questions + syllabus_topics
        tfidf_matrix = tfidf.fit_transform(all_text)
        
        question_vectors = tfidf_matrix[:len(questions)]
        syllabus_vectors = tfidf_matrix[len(questions):]
        
        valid_questions = []
        
        # Calculate max similarity of each question to ANY syllabus topic
        similarities = cosine_similarity(question_vectors, syllabus_vectors)
        max_sims = similarities.max(axis=1)
        
        for i, sim in enumerate(max_sims):
            if sim >= threshold:
                valid_questions.append(questions[i])
                
        return valid_questions
