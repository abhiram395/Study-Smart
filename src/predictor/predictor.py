import random
from collections import Counter

class Predictor:
    def __init__(self):
        pass

    def generate_study_plan(self, processed_data):
        """
        Generates a study plan based on topic frequency.
        processed_data: list of dicts, where each dict has 'questions' list.
                        Each item in 'questions' is {'question': q, 'topic': t}
        """
        # 1. Aggregate Topic Counts
        topic_counts = Counter()
        topic_questions = {} # Store questions for each topic to show examples
        
        for paper in processed_data:
            for item in paper['questions']:
                topic = item['topic']
                topic_counts[topic] += 1
                
                if topic not in topic_questions:
                    topic_questions[topic] = []
                topic_questions[topic].append(item['question'])

        # 2. Rank Topics
        total_questions = sum(topic_counts.values())
        ranked_topics = []
        
        for topic, count in topic_counts.most_common():
            weightage = (count / total_questions) * 100 if total_questions > 0 else 0
            
            # Determine Priority
            if weightage >= 15:
                priority = "High"
            elif weightage >= 5:
                priority = "Medium"
            else:
                priority = "Low"
                
            ranked_topics.append({
                'topic': topic,
                'count': count,
                'weightage': round(weightage, 1),
                'priority': priority,
                'example_questions': random.sample(topic_questions[topic], min(3, len(topic_questions[topic])))
            })
            
        return ranked_topics
