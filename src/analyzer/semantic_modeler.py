from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticModeler:
    def __init__(self, model_name='all-MiniLM-L6-v2', n_topics=5):
        self.n_topics = n_topics
        # Load a pre-trained model (small and fast)
        self.model = SentenceTransformer(model_name)
        self.kmeans = KMeans(n_clusters=n_topics, random_state=42, n_init=10)
        self.cluster_centers_ = None

    def fit_transform(self, questions):
        """
        Encodes questions and clusters them into topics.
        Returns a one-hot like distribution (hard clustering for now).
        """
        if not questions:
            return None
            
        # 1. Encode questions to vectors
        embeddings = self.model.encode(questions)
        
        # 2. Cluster embeddings
        # Adjust n_clusters if we have fewer questions than topics
        actual_n_topics = min(self.n_topics, len(questions))
        if actual_n_topics < self.n_topics:
            self.kmeans = KMeans(n_clusters=actual_n_topics, random_state=42, n_init=10)
            
        self.kmeans.fit(embeddings)
        self.cluster_centers_ = self.kmeans.cluster_centers_
        
        # 3. Assign labels
        labels = self.kmeans.labels_
        
        # Convert to format expected by Predictor (one-hot-ish)
        # Predictor expects: list of arrays where array[i] is prob of topic i
        # Since KMeans is hard clustering, we'll give 1.0 to the assigned topic
        topic_distributions = np.zeros((len(questions), self.n_topics))
        for i, label in enumerate(labels):
            topic_distributions[i][label] = 1.0
            
        return topic_distributions

    def filter_by_syllabus(self, questions, syllabus_topics, threshold=0.25):
        """
        Filters questions using semantic similarity to syllabus topics.
        Returns a list of dicts: {'question': q, 'topic': t, 'similarity': s}
        """
        if not syllabus_topics:
            # If no syllabus, return questions with unknown topic
            return [{'question': q, 'topic': 'Unknown', 'similarity': 0.0} for q in questions]
            
        # Encode everything
        q_embeddings = self.model.encode(questions)
        s_embeddings = self.model.encode(syllabus_topics)
        
        # Calculate similarity matrix (Questions x Syllabus)
        similarities = cosine_similarity(q_embeddings, s_embeddings)
        
        # For each question, find its max similarity and the corresponding topic index
        max_sims = similarities.max(axis=1)
        topic_indices = similarities.argmax(axis=1)
        
        valid_data = []
        for i, sim in enumerate(max_sims):
            if sim >= threshold:
                valid_data.append({
                    'question': questions[i],
                    'topic': syllabus_topics[topic_indices[i]],
                    'similarity': float(sim)
                })
                
        print(f"Semantic Filter: Kept {len(valid_data)}/{len(questions)} questions (Threshold: {threshold})")
        return valid_data
