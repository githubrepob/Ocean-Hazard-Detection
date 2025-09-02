# 6. Save models and create helper functions for the web application

# Save trained models
print("Saving trained models...")

# Save binary classification model
with open('binary_hazard_model.pkl', 'wb') as f:
    pickle.dump(binary_pipeline, f)

# Save multiclass classification model  
with open('multiclass_hazard_model.pkl', 'wb') as f:
    pickle.dump(multiclass_pipeline, f)

# Save training data for reference
training_data.to_csv('training_data.csv', index=False)

print("Models saved successfully!")

# Create a comprehensive analysis class
class OceanHazardDetector:
    """Comprehensive Ocean Hazard Detection and Social Media Analytics System"""
    
    def __init__(self):
        self.binary_model = binary_pipeline
        self.multiclass_model = multiclass_pipeline
        self.reports_database = []
        
    def analyze_single_post(self, text):
        """Analyze a single social media post"""
        return analyze_hazard_post(text)
    
    def analyze_batch_posts(self, posts):
        """Analyze multiple social media posts"""
        results = []
        for post in posts:
            analysis = self.analyze_single_post(post)
            results.append(analysis)
        return results
    
    def add_report(self, analysis):
        """Add analysis result to database"""
        self.reports_database.append(analysis)
    
    def get_active_hotspots(self):
        """Get current active hotspots"""
        return generate_hotspots(self.reports_database)
    
    def get_dashboard_metrics(self):
        """Get metrics for dashboard display"""
        if not self.reports_database:
            return {
                'total_reports': 0,
                'active_hazards': 0,
                'hotspots': 0,
                'avg_confidence': 0
            }
        
        total_reports = len(self.reports_database)
        active_hazards = sum(1 for r in self.reports_database if r['is_hazard'])
        hotspots = len(self.get_active_hotspots())
        avg_confidence = sum(r['confidence'] for r in self.reports_database) / total_reports
        
        return {
            'total_reports': total_reports,
            'active_hazards': active_hazards,
            'hotspots': hotspots,
            'avg_confidence': avg_confidence
        }
    
    def get_recent_alerts(self, hours=24):
        """Get recent high-priority alerts"""
        current_time = datetime.datetime.now()
        recent_alerts = []
        
        for report in self.reports_database:
            report_time = datetime.datetime.fromisoformat(report['timestamp'])
            hours_diff = (current_time - report_time).total_seconds() / 3600
            
            if (hours_diff <= hours and 
                report['is_hazard'] and 
                report['urgency'] in ['high', 'medium']):
                recent_alerts.append(report)
        
        # Sort by urgency and confidence
        recent_alerts.sort(key=lambda x: (
            3 if x['urgency'] == 'high' else 2 if x['urgency'] == 'medium' else 1,
            x['confidence']
        ), reverse=True)
        
        return recent_alerts[:10]  # Return top 10 recent alerts

# Initialize the detector
detector = OceanHazardDetector()

# Add sample reports to the system
for report in sample_reports:
    detector.add_report(report)

# Test the detector class
print(f"\nTesting OceanHazardDetector class:")
metrics = detector.get_dashboard_metrics()
print(f"Dashboard Metrics: {metrics}")

recent_alerts = detector.get_recent_alerts()
print(f"Recent Alerts: {len(recent_alerts)}")

hotspots = detector.get_active_hotspots()
print(f"Active Hotspots: {len(hotspots)}")

print("\nOcean Hazard Detection System fully initialized!")