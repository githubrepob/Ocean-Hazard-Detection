# 2. Create realistic training data for ocean hazard detection from social media

# Ocean hazard keywords and patterns
tsunami_keywords = ["tsunami", "tidal wave", "sea level rising", "ocean wave", "coastal flooding", "seismic wave"]
storm_surge_keywords = ["storm surge", "high tide", "coastal flooding", "sea wall breach", "water level rise"]
high_wave_keywords = ["high waves", "rough sea", "big waves", "dangerous waves", "wave height", "choppy waters"]
coastal_hazard_keywords = ["coastal erosion", "beach damage", "pier damage", "harbor damage", "coastal infrastructure"]
swell_surge_keywords = ["swell", "ocean swell", "wave energy", "surf conditions", "marine conditions"]

# Generate synthetic training data
def generate_training_data():
    # Tsunami-related posts
    tsunami_posts = [
        "Massive waves hitting the coast! Water rising rapidly #tsunami #emergency",
        "Unusual sea behavior observed. Water receding dramatically from beach",
        "ALERT: Large waves approaching coastal areas. Evacuate immediately!",
        "Seismic activity detected offshore. Tsunami warning in effect",
        "Water levels rising unusually fast at the harbor",
        "Unprecedented tidal wave seen from lighthouse. Seeking higher ground",
        "Ocean behaving strangely. Waves much larger than normal",
        "Coastal flooding in progress. Multiple areas affected",
        "Sea wall breached by massive waves. Emergency response needed",
        "Tsunami sirens activated. Moving to evacuation centers"
    ]
    
    # Storm surge posts
    storm_surge_posts = [
        "Hurricane approaching! Storm surge warning issued for coastal areas",
        "High winds and rising water levels. Coastal flooding expected",
        "Storm surge barriers activated. Water levels critical",
        "Cyclone impact: Severe coastal flooding in multiple districts",
        "Emergency: Storm surge causing widespread flooding",
        "Harbor facilities underwater due to storm surge",
        "Extreme weather causing dangerous sea conditions",
        "Coastal evacuation ordered due to incoming storm surge",
        "Pier completely submerged by storm waters",
        "Fishing boats damaged by storm surge and high waves"
    ]
    
    # High waves posts
    high_wave_posts = [
        "Dangerous wave conditions observed. Small craft advisory in effect",
        "10-foot waves reported near coast. Swimming prohibited",
        "Rough sea conditions making navigation hazardous",
        "Large waves damaging coastal properties",
        "Surfing cancelled due to dangerous wave heights",
        "Fishing vessels returning early due to high waves",
        "Wave height exceeding safe limits for marine activities",
        "Choppy waters making ferry operations dangerous",
        "Massive swells creating hazardous conditions",
        "Wave energy causing coastal infrastructure damage"
    ]
    
    # Normal/Non-hazardous posts
    normal_posts = [
        "Beautiful sunset at the beach today. Perfect weather!",
        "Enjoying a peaceful walk along the shore",
        "Great day for fishing. Calm waters and good catch",
        "Beach volleyball tournament going well. Nice conditions",
        "Ferry service running on schedule today",
        "Port operations normal. Ships arriving and departing safely",
        "Lighthouse tour was amazing. Clear visibility",
        "Coastal cleanup drive successful. Community participation excellent",
        "Marine research expedition launched successfully",
        "Harbor festival celebrating maritime heritage"
    ]
    
    # Swell surge posts
    swell_posts = [
        "Long-period swells reaching coast. Unusual wave patterns",
        "Ocean swell causing minor flooding in low-lying areas",
        "Swell surge affecting boat moorings at marina",
        "Unexpectedly large swells from distant storm system",
        "Swell conditions making port entry challenging",
        "Ground swell causing periodic coastal flooding",
        "Marine advisory: Significant swell activity predicted",
        "Swell-induced waves affecting coastal infrastructure",
        "Long-range swell impacting navigation channels",
        "Periodic swell surges observed at tide monitoring stations"
    ]
    
    # Create labeled dataset
    data = []
    
    # Add tsunami posts
    for post in tsunami_posts:
        data.append({'text': post, 'hazard_type': 'tsunami', 'is_hazard': 1, 'urgency': 'high'})
    
    # Add storm surge posts
    for post in storm_surge_posts:
        data.append({'text': post, 'hazard_type': 'storm_surge', 'is_hazard': 1, 'urgency': 'high'})
    
    # Add high waves posts
    for post in high_wave_posts:
        data.append({'text': post, 'hazard_type': 'high_waves', 'is_hazard': 1, 'urgency': 'medium'})
    
    # Add swell posts
    for post in swell_posts:
        data.append({'text': post, 'hazard_type': 'swell_surge', 'is_hazard': 1, 'urgency': 'medium'})
    
    # Add normal posts
    for post in normal_posts:
        data.append({'text': post, 'hazard_type': 'normal', 'is_hazard': 0, 'urgency': 'low'})
    
    return pd.DataFrame(data)

# Generate training data
training_data = generate_training_data()
print(f"Generated {len(training_data)} training samples")
print("\nSample data:")
print(training_data.head())
print(f"\nHazard type distribution:")
print(training_data['hazard_type'].value_counts())