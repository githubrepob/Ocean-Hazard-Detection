# 5. Create hotspot generation and geospatial analysis

import math
from collections import Counter, defaultdict

# Hotspot generation functions
def generate_hotspots(reports, radius_km=50):
    """Generate hotspots based on report density and severity"""
    
    # Define approximate coordinates for major Indian coastal cities
    location_coordinates = {
        'mumbai': (19.0760, 72.8777),
        'chennai': (13.0827, 80.2707),
        'kolkata': (22.5726, 88.3639),
        'kochi': (9.9312, 76.2673),
        'cochin': (9.9312, 76.2673),
        'vishakhapatnam': (17.6868, 83.2185),
        'visakhapatnam': (17.6868, 83.2185),
        'paradip': (20.2648, 86.6989),
        'mangalore': (12.9141, 74.8560),
        'goa': (15.2993, 74.1240),
        'calicut': (11.2588, 75.7804),
        'kozhikode': (11.2588, 75.7804),
        'tuticorin': (8.7642, 78.1348),
        'coast': (15.0000, 77.0000),  # Generic coastal location
        'beach': (15.0000, 77.0000),
        'harbor': (15.0000, 77.0000),
        'harbour': (15.0000, 77.0000),
        'port': (15.0000, 77.0000),
        'bay': (15.0000, 77.0000),
        'shore': (15.0000, 77.0000)
    }
    
    hotspots = []
    location_reports = defaultdict(list)
    
    # Group reports by location
    for report in reports:
        for location in report.get('locations', []):
            if location in location_coordinates:
                location_reports[location].append(report)
    
    # Generate hotspots for each location with multiple reports
    for location, loc_reports in location_reports.items():
        if len(loc_reports) > 1:  # Only create hotspot if multiple reports
            
            # Calculate hotspot metrics
            total_reports = len(loc_reports)
            hazard_reports = sum(1 for r in loc_reports if r['is_hazard'])
            avg_confidence = sum(r['confidence'] for r in loc_reports) / total_reports
            
            # Count urgency levels
            urgency_counts = Counter(r['urgency'] for r in loc_reports)
            
            # Calculate severity score
            severity_score = (
                urgency_counts['high'] * 3 + 
                urgency_counts['medium'] * 2 + 
                urgency_counts['low'] * 1
            ) / total_reports
            
            # Count hazard types
            hazard_types = Counter(r['hazard_type'] for r in loc_reports if r['is_hazard'])
            
            hotspot = {
                'location': location,
                'coordinates': location_coordinates[location],
                'total_reports': total_reports,
                'hazard_reports': hazard_reports,
                'hazard_ratio': hazard_reports / total_reports,
                'avg_confidence': avg_confidence,
                'severity_score': severity_score,
                'urgency_distribution': dict(urgency_counts),
                'hazard_types': dict(hazard_types),
                'risk_level': 'high' if severity_score >= 2.5 else 'medium' if severity_score >= 1.5 else 'low'
            }
            
            hotspots.append(hotspot)
    
    # Sort hotspots by severity score
    hotspots.sort(key=lambda x: x['severity_score'], reverse=True)
    
    return hotspots

# Time series analysis for trend detection
def analyze_trends(reports, time_window_hours=24):
    """Analyze trends in hazard reports over time"""
    
    current_time = datetime.datetime.now()
    time_buckets = defaultdict(list)
    
    # Group reports by hour
    for report in reports:
        report_time = datetime.datetime.fromisoformat(report['timestamp'])
        hours_ago = (current_time - report_time).total_seconds() / 3600
        
        if hours_ago <= time_window_hours:
            hour_bucket = int(hours_ago)
            time_buckets[hour_bucket].append(report)
    
    trends = []
    for hour, hour_reports in sorted(time_buckets.items()):
        hazard_count = sum(1 for r in hour_reports if r['is_hazard'])
        avg_severity = sum(
            3 if r['urgency'] == 'high' else 2 if r['urgency'] == 'medium' else 1 
            for r in hour_reports
        ) / len(hour_reports) if hour_reports else 0
        
        trends.append({
            'hours_ago': hour,
            'total_reports': len(hour_reports),
            'hazard_reports': hazard_count,
            'avg_severity': avg_severity
        })
    
    return trends

# Social media engagement metrics
def calculate_engagement_metrics(reports):
    """Calculate engagement and virality metrics"""
    
    total_reports = len(reports)
    hazard_reports = sum(1 for r in reports if r['is_hazard'])
    
    # Sentiment distribution
    sentiment_dist = Counter(r['sentiment']['sentiment_label'] for r in reports)
    
    # Urgency distribution
    urgency_dist = Counter(r['urgency'] for r in reports)
    
    # Location coverage
    all_locations = []
    for r in reports:
        all_locations.extend(r['locations'])
    location_coverage = len(set(all_locations))
    
    # Average confidence
    avg_confidence = sum(r['confidence'] for r in reports) / total_reports if total_reports > 0 else 0
    
    return {
        'total_reports': total_reports,
        'hazard_reports': hazard_reports,
        'hazard_percentage': (hazard_reports / total_reports * 100) if total_reports > 0 else 0,
        'sentiment_distribution': dict(sentiment_dist),
        'urgency_distribution': dict(urgency_dist),
        'location_coverage': location_coverage,
        'average_confidence': avg_confidence,
        'engagement_score': min(100, total_reports * 2 + location_coverage * 5)  # Simple engagement score
    }

# Generate sample reports for testing
def generate_sample_reports():
    """Generate sample reports for testing hotspot generation"""
    
    sample_texts = [
        "TSUNAMI WARNING! Massive waves approaching Chennai coast. All residents evacuate immediately!",
        "Unusual sea behavior observed near Chennai Marina Beach. Water receding rapidly.",
        "High waves and storm surge affecting Mumbai harbor operations. Fishing boats returning early.",
        "Dangerous wave conditions reported near Mumbai coast. Small craft advisory in effect.",
        "Cyclone approaching Kochi harbor. All vessels advised to seek shelter immediately.",
        "Storm surge causing flooding in low-lying areas of Kochi. Emergency services responding.",
        "Normal beach conditions at Goa. Tourists enjoying calm weather and clear waters.",
        "Perfect surfing conditions at Mangalore beach today. Light winds and moderate waves."
    ]
    
    reports = []
    for text in sample_texts:
        analysis = analyze_hazard_post(text)
        reports.append(analysis)
    
    return reports

# Test the hotspot generation system
print("Testing hotspot generation and analytics...")
print("=" * 50)

# Generate sample reports
sample_reports = generate_sample_reports()
print(f"Generated {len(sample_reports)} sample reports")

# Generate hotspots
hotspots = generate_hotspots(sample_reports)
print(f"\nIdentified {len(hotspots)} hotspots:")

for i, hotspot in enumerate(hotspots, 1):
    print(f"\nHotspot {i}: {hotspot['location'].upper()}")
    print(f"  Coordinates: {hotspot['coordinates']}")
    print(f"  Total Reports: {hotspot['total_reports']}")
    print(f"  Hazard Reports: {hotspot['hazard_reports']}")
    print(f"  Risk Level: {hotspot['risk_level']}")
    print(f"  Severity Score: {hotspot['severity_score']:.2f}")
    print(f"  Hazard Types: {hotspot['hazard_types']}")

# Calculate engagement metrics
engagement = calculate_engagement_metrics(sample_reports)
print(f"\n\nEngagement Metrics:")
print(f"Total Reports: {engagement['total_reports']}")
print(f"Hazard Reports: {engagement['hazard_reports']} ({engagement['hazard_percentage']:.1f}%)")
print(f"Location Coverage: {engagement['location_coverage']} unique locations")
print(f"Average Confidence: {engagement['average_confidence']:.2f}")
print(f"Engagement Score: {engagement['engagement_score']}")
print(f"Sentiment Distribution: {engagement['sentiment_distribution']}")
print(f"Urgency Distribution: {engagement['urgency_distribution']}")

print("\nHotspot generation and analytics system ready!")