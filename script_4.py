# 4. Create sentiment analysis and location extraction modules (without geocoder)

from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize sentiment analyzer
try:
    sia = SentimentIntensityAnalyzer()
    print("VADER sentiment analyzer loaded")
except:
    print("VADER not available, using TextBlob for sentiment")
    sia = None

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
    # Common location patterns for Indian coastal areas
    location_patterns = [
        r'\b(?:coast|beach|harbor|harbour|port|bay|island|shore|marina|pier|lighthouse)\b',
        r'\b(?:mumbai|chennai|kolkata|kochi|cochin|vishakhapatnam|visakhapatnam|paradip|mangalore|goa|calicut|kozhikode|tuticorin|ennore|kandla|nhava sheva)\b',
        r'\b(?:kerala|tamil nadu|andhra pradesh|telangana|odisha|west bengal|gujarat|maharashtra|karnataka|puducherry)\b',
        r'\b(?:arabian sea|bay of bengal|indian ocean|lakshadweep|andaman|nicobar)\b'
    ]
    
    locations = []
    for pattern in location_patterns:
        matches = re.findall(pattern, text.lower())
        locations.extend(matches)
    
    return list(set(locations))

# Keyword extraction for hazard types
def extract_hazard_keywords(text):
    """Extract hazard-specific keywords"""
    
    hazard_keywords = {
        'tsunami': ['tsunami', 'tidal wave', 'seismic wave', 'underwater earthquake', 'sea withdrawal'],
        'storm_surge': ['storm surge', 'cyclone', 'hurricane', 'typhoon', 'storm tide'],
        'high_waves': ['high waves', 'rough sea', 'choppy waters', 'dangerous waves', 'wave height'],
        'swell_surge': ['swell', 'ground swell', 'ocean swell', 'wave energy'],
        'coastal_flooding': ['coastal flooding', 'inundation', 'sea level rise', 'overflow'],
        'general_hazard': ['emergency', 'alert', 'warning', 'danger', 'evacuate', 'rescue']
    }
    
    found_keywords = {}
    text_lower = text.lower()
    
    for category, keywords in hazard_keywords.items():
        found_keywords[category] = [kw for kw in keywords if kw in text_lower]
    
    return found_keywords

# Urgency assessment function
def assess_urgency(text, hazard_type, sentiment_score):
    """Assess urgency level based on text content and context"""
    
    urgent_keywords = ['alert', 'emergency', 'evacuate', 'immediate', 'danger', 'warning', 'critical', 'urgent', 'sos']
    medium_keywords = ['advisory', 'caution', 'watch', 'monitor', 'observe', 'unusual', 'abnormal']
    
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
    
    # Hazard keyword extraction
    keywords = extract_hazard_keywords(text)
    
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
        'hazard_keywords': keywords,
        'urgency': urgency,
        'confidence': float(confidence),
        'timestamp': datetime.datetime.now().isoformat()
    }

# Test the comprehensive analysis
test_posts = [
    "TSUNAMI ALERT! Massive waves hitting Chennai coast. Immediate evacuation required! #emergency #tsunami",
    "Beautiful day at Marina Beach Mumbai. Perfect weather for a walk!",
    "Storm surge warning issued for Kochi harbor. All vessels advised to return to port immediately",
    "Unusual wave patterns observed near Vishakhapatnam. Fishermen reporting strange sea behavior at Bay of Bengal",
    "High waves and rough sea conditions making navigation dangerous near Paradip port"
]

print("Testing comprehensive hazard analysis:")
print("=" * 60)

for i, post in enumerate(test_posts, 1):
    print(f"\nTest Post {i}: {post[:50]}...")
    analysis = analyze_hazard_post(post)
    print(f"Hazard Detected: {analysis['is_hazard']}")
    print(f"Hazard Type: {analysis['hazard_type']}")
    print(f"Urgency: {analysis['urgency']}")
    print(f"Confidence: {analysis['confidence']:.2f}")
    print(f"Sentiment: {analysis['sentiment']['sentiment_label']}")
    print(f"Locations: {analysis['locations']}")
    print(f"Key Hazard Keywords: {[kw for cat, kws in analysis['hazard_keywords'].items() for kw in kws]}")
    print("-" * 40)

print("\nHazard analysis system ready!")