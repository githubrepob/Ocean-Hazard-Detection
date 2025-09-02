# 4. Create sentiment analysis and location extraction modules

from nltk.sentiment import SentimentIntensityAnalyzer
import geocoder
from geopy.geocoders import Nominatim

# Initialize sentiment analyzer
try:
    sia = SentimentIntensityAnalyzer()
except:
    print("VADER not available, using TextBlob for sentiment")
    sia = None

# Initialize geocoder
geolocator = Nominatim(user_agent="ocean_hazard_detector")

# Sentiment analysis function
def analyze_sentiment(text):
    """Analyze sentiment of text"""
    if sia:
        scores = sia.polarity_scores(text)
        return {
            'compound': scores['compound'],
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'sentiment_label': 'positive' if scores['compound'] > 0.05 else 'negative' if scores['compound'] < -0.05 else 'neutral'
        }
    else:
        # Fallback to TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        return {
            'compound': polarity,
            'sentiment_label': 'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
        }

# Location extraction function
def extract_location(text):
    """Extract location mentions from text"""
    # Common location patterns
    location_patterns = [
        r'\b(?:coast|beach|harbor|port|bay|island|shore|marina|pier|lighthouse)\b',
        r'\b(?:mumbai|chennai|kolkata|kochi|vishakhapatnam|paradip|mangalore|goa)\b',
        r'\b(?:kerala|tamil nadu|andhra pradesh|odisha|west bengal|gujarat|maharashtra|karnataka)\b',
        r'\b(?:arabian sea|bay of bengal|indian ocean)\b'
    ]
    
    locations = []
    for pattern in location_patterns:
        matches = re.findall(pattern, text.lower())
        locations.extend(matches)
    
    return list(set(locations))

# Urgency assessment function
def assess_urgency(text, hazard_type, sentiment_score):
    """Assess urgency level based on text content and context"""
    
    urgent_keywords = ['alert', 'emergency', 'evacuate', 'immediate', 'danger', 'warning', 'critical']
    medium_keywords = ['advisory', 'caution', 'watch', 'monitor', 'observe']
    
    urgency_score = 0
    
    # Check for urgent keywords
    for keyword in urgent_keywords:
        if keyword in text.lower():
            urgency_score += 3
    
    # Check for medium urgency keywords
    for keyword in medium_keywords:
        if keyword in text.lower():
            urgency_score += 1
    
    # Factor in hazard type
    if hazard_type in ['tsunami', 'storm_surge']:
        urgency_score += 2
    elif hazard_type in ['high_waves', 'swell_surge']:
        urgency_score += 1
    
    # Factor in sentiment (negative sentiment might indicate urgency)
    if sentiment_score < -0.3:
        urgency_score += 1
    
    # Determine urgency level
    if urgency_score >= 4:
        return 'high'
    elif urgency_score >= 2:
        return 'medium'
    else:
        return 'low'

# Comprehensive hazard analysis function
def analyze_hazard_post(text):
    """Comprehensive analysis of a social media post for ocean hazards"""
    
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Binary hazard detection
    is_hazard = binary_pipeline.predict([processed_text])[0]
    hazard_probability = binary_pipeline.predict_proba([processed_text])[0][1]
    
    # Multi-class hazard type detection
    hazard_type = multiclass_pipeline.predict([processed_text])[0]
    hazard_type_probs = multiclass_pipeline.predict_proba([processed_text])[0]
    hazard_classes = multiclass_pipeline.classes_
    
    # Sentiment analysis
    sentiment = analyze_sentiment(text)
    
    # Location extraction
    locations = extract_location(text)
    
    # Urgency assessment
    urgency = assess_urgency(text, hazard_type, sentiment.get('compound', 0))
    
    # Confidence score
    confidence = hazard_probability if is_hazard else (1 - hazard_probability)
    
    return {
        'original_text': text,
        'is_hazard': bool(is_hazard),
        'hazard_probability': float(hazard_probability),
        'hazard_type': hazard_type,
        'hazard_type_probabilities': {cls: float(prob) for cls, prob in zip(hazard_classes, hazard_type_probs)},
        'sentiment': sentiment,
        'locations': locations,
        'urgency': urgency,
        'confidence': float(confidence),
        'timestamp': datetime.datetime.now().isoformat()
    }

# Test the comprehensive analysis
test_posts = [
    "TSUNAMI ALERT! Massive waves hitting Chennai coast. Immediate evacuation required! #emergency #tsunami",
    "Beautiful day at Marina Beach. Perfect weather for a walk!",
    "Storm surge warning issued for Mumbai harbor. All vessels advised to return to port immediately",
    "Unusual wave patterns observed near Vishakhapatnam. Fishermen reporting strange sea behavior"
]

print("Testing comprehensive hazard analysis:")
print("=" * 50)

for i, post in enumerate(test_posts, 1):
    print(f"\nTest Post {i}: {post[:50]}...")
    analysis = analyze_hazard_post(post)
    print(f"Hazard Detected: {analysis['is_hazard']}")
    print(f"Hazard Type: {analysis['hazard_type']}")
    print(f"Urgency: {analysis['urgency']}")
    print(f"Confidence: {analysis['confidence']:.2f}")
    print(f"Sentiment: {analysis['sentiment']['sentiment_label']}")
    print(f"Locations: {analysis['locations']}")
    print("-" * 30)

print("\nHazard analysis system ready!")