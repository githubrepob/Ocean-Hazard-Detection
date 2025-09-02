// Application Data
// const appData = {
//     sample_posts: [
//         {
//             text: "TSUNAMI ALERT! Massive waves hitting Chennai coast. Immediate evacuation required!",
//             is_hazard: true,
//             hazard_type: "tsunami",
//             urgency: "high",
//             confidence: 0.95,
//             locations: ["chennai", "coast"],
//             timestamp: "2025-08-31T14:30:00"
//         },
//         {
//             text: "Beautiful day at Marina Beach Mumbai. Perfect weather for a walk!",
//             is_hazard: false,
//             hazard_type: "normal",
//             urgency: "low",
//             confidence: 0.92,
//             locations: ["mumbai", "beach"],
//             timestamp: "2025-08-31T13:15:00"
//         },
//         {
//             text: "Storm surge warning issued for Kochi harbor. All vessels return to port immediately",
//             is_hazard: true,
//             hazard_type: "storm_surge",
//             urgency: "high",
//             confidence: 0.88,
//             locations: ["kochi", "harbor"],
//             timestamp: "2025-08-31T12:45:00"
//         },
//         {
//             text: "High waves and rough sea conditions near Paradip port making navigation dangerous",
//             is_hazard: true,
//             hazard_type: "high_waves",
//             urgency: "medium",
//             confidence: 0.83,
//             locations: ["paradip", "port"],
//             timestamp: "2025-08-31T11:20:00"
//         }
//     ],
//     hotspots: [
//         {
//             location: "Chennai",
//             coordinates: [13.0827, 80.2707],
//             risk_level: "high",
//             total_reports: 5,
//             hazard_reports: 4,
//             severity_score: 2.8,
//             dominant_hazard: "Tsunami"
//         },
//         {
//             location: "Mumbai",
//             coordinates: [19.0760, 72.8777],
//             risk_level: "medium",
//             total_reports: 3,
//             hazard_reports: 2,
//             severity_score: 1.9,
//             dominant_hazard: "Storm Surge"
//         },
//         {
//             location: "Kochi",
//             coordinates: [9.9312, 76.2673],
//             risk_level: "high",
//             total_reports: 4,
//             hazard_reports: 3,
//             severity_score: 2.5,
//             dominant_hazard: "High Waves"
//         },
//         {
//             location: "Paradip",
//             coordinates: [21.3099, 87.5286],
//             risk_level: "medium",
//             total_reports: 3,
//             hazard_reports: 2,
//             severity_score: 1.7,
//             dominant_hazard: "High Waves"
//         }
//     ],
//     alerts: [
//         {
//             id: 1,
//             timestamp: "2025-08-31T14:30:00",
//             location: "Chennai Coast",
//             hazard_type: "Tsunami",
//             urgency: "high",
//             confidence: 0.95,
//             message: "Massive waves hitting Chennai coast. Immediate evacuation required!"
//         },
//         {
//             id: 2,
//             timestamp: "2025-08-31T12:45:00",
//             location: "Kochi Harbor",
//             hazard_type: "Storm Surge",
//             urgency: "high",
//             confidence: 0.88,
//             message: "Storm surge warning issued. All vessels return to port immediately"
//         },
//         {
//             id: 3,
//             timestamp: "2025-08-31T11:20:00",
//             location: "Paradip Port",
//             hazard_type: "High Waves",
//             urgency: "medium",
//             confidence: 0.83,
//             message: "High waves making navigation dangerous"
//         }
//     ],
//     metrics: {
//         total_reports: 156,
//         active_hazards: 23,
//         active_hotspots: 8,
//         system_confidence: 0.89,
//         hazard_distribution: {
//             tsunami: 15,
//             storm_surge: 28,
//             high_waves: 34,
//             swell_surge: 12,
//             normal: 67
//         }
//     }
// };

// Global variables
let analysisHistory = [];
let charts = {};
let selectedHotspot = null;

// Navigation function
function showPage(pageId) {
    console.log('Navigating to page:', pageId);
    
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => page.classList.remove('active'));
    
    // Remove active class from all nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    
    // Show target page
    const targetPage = document.getElementById(pageId);
    if (targetPage) {
        targetPage.classList.add('active');
        
        // Add active class to corresponding nav link
        const activeLink = document.querySelector(`[onclick="showPage('${pageId}')"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
        
        // Initialize page-specific content
        switch(pageId) {
            case 'dashboard':
                initializeDashboard();
                break;
            case 'monitoring':
                initializeMonitoring();
                break;
            case 'social-media':
                initializeSocialMediaAnalysis();
                break;
            case 'hotspots':
                initializeHotspots();
                break;
            case 'alerts':
                initializeAlerts();
                break;
            case 'analytics':
                initializeAnalytics();
                break;
        }
    } else {
        console.error('Page not found:', pageId);
    }
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing INCOIS Platform...');
    initializeDashboard();
    addSampleAnalysis();
});

// Dashboard functions
function initializeDashboard() {
    updateMetrics();
    renderRecentAlerts();
    setTimeout(() => {
        createHazardChart();
    }, 100);
}

function updateMetrics() {
    const elements = {
        totalReports: document.getElementById('totalReports'),
        activeHazards: document.getElementById('activeHazards'),
        activeHotspots: document.getElementById('activeHotspots'),
        systemConfidence: document.getElementById('systemConfidence')
    };

    if (elements.totalReports) elements.totalReports.textContent = appData.metrics.total_reports;
    if (elements.activeHazards) elements.activeHazards.textContent = appData.metrics.active_hazards;
    if (elements.activeHotspots) elements.activeHotspots.textContent = appData.metrics.active_hotspots;
    if (elements.systemConfidence) elements.systemConfidence.textContent = Math.round(appData.metrics.system_confidence * 100) + '%';
}

function renderRecentAlerts() {
    const alertsContainer = document.getElementById('recentAlerts');
    if (!alertsContainer) return;
    
    const recentAlerts = appData.alerts.slice(0, 3);
    
    alertsContainer.innerHTML = recentAlerts.map(alert => `
        <div class="alert-item">
            <div class="alert-info">
                <h4>${alert.hazard_type} - ${alert.location}</h4>
                <p>${alert.message}</p>
            </div>
            <div class="alert-time">${formatTime(alert.timestamp)}</div>
        </div>
    `).join('');
}

function createHazardChart() {
    const canvas = document.getElementById('hazardChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const data = appData.metrics.hazard_distribution;
    
    if (charts.hazardChart) {
        charts.hazardChart.destroy();
    }
    
    charts.hazardChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Tsunami', 'Storm Surge', 'High Waves', 'Swell Surge', 'Normal'],
            datasets: [{
                data: [data.tsunami, data.storm_surge, data.high_waves, data.swell_surge, data.normal],
                backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Real-time Monitoring functions
function initializeMonitoring() {
    updateAnalysisHistory();
}

function performAnalysis() {
    const analysisInput = document.getElementById('analysisInput');
    if (!analysisInput) return;
    
    const text = analysisInput.value.trim();
    if (!text) {
        alert('Please enter some text to analyze');
        return;
    }
    
    console.log('Starting analysis for:', text);
    showLoadingModal();
    
    // Simulate AI processing delay
    setTimeout(() => {
        const result = simulateAIAnalysis(text);
        displayAnalysisResult(result);
        
        // Add to history
        analysisHistory.unshift({
            text: text,
            result: result,
            timestamp: new Date().toISOString()
        });
        
        updateAnalysisHistory();
        hideLoadingModal();
        
        // Clear input
        analysisInput.value = '';
    }, 1500);
}

function simulateAIAnalysis(text) {
    const hazardKeywords = {
        tsunami: ['tsunami', 'massive waves', 'evacuation', 'sea level rising'],
        storm_surge: ['storm surge', 'storm', 'surge', 'vessels', 'harbor'],
        high_waves: ['high waves', 'rough sea', 'dangerous', 'navigation'],
        swell_surge: ['swell', 'unusual tide', 'tide surge'],
        coastal_flooding: ['flooding', 'water level', 'inundation']
    };
    
    const urgencyKeywords = {
        high: ['alert', 'immediate', 'emergency', 'danger', 'warning', 'massive'],
        medium: ['caution', 'advisory', 'monitor', 'watch', 'rough'],
        low: ['normal', 'calm', 'beautiful', 'perfect']
    };
    
    let detectedType = 'normal';
    let isHazard = false;
    let urgency = 'low';
    let confidence = Math.random() * 0.3 + 0.7;
    
    const lowerText = text.toLowerCase();
    
    // Check for hazard types
    for (const [type, keywords] of Object.entries(hazardKeywords)) {
        if (keywords.some(keyword => lowerText.includes(keyword))) {
            detectedType = type;
            isHazard = true;
            confidence = Math.random() * 0.2 + 0.8;
            break;
        }
    }
    
    // Check urgency
    for (const [level, keywords] of Object.entries(urgencyKeywords)) {
        if (keywords.some(keyword => lowerText.includes(keyword))) {
            urgency = level;
            break;
        }
    }
    
    if (isHazard && urgency === 'low') {
        urgency = 'medium';
    }
    
    // Extract locations
    const locationKeywords = ['chennai', 'mumbai', 'kochi', 'kolkata', 'paradip', 'goa', 'mangalore', 'calicut', 'vishakhapatnam', 'tuticorin', 'coast', 'beach', 'harbor', 'port'];
    const detectedLocations = locationKeywords.filter(loc => lowerText.includes(loc));
    
    // Extract keywords
    const importantWords = text.toLowerCase()
        .replace(/[^\w\s]/g, ' ')
        .split(' ')
        .filter(word => word.length > 3)
        .slice(0, 5);
    
    return {
        is_hazard: isHazard,
        hazard_type: detectedType,
        urgency: urgency,
        confidence: confidence,
        locations: detectedLocations,
        keywords: importantWords,
        sentiment: isHazard ? 'negative' : 'positive'
    };
}

function displayAnalysisResult(result) {
    const resultsContainer = document.getElementById('analysisResults');
    if (!resultsContainer) return;
    
    resultsContainer.innerHTML = `
        <div class="result-item">
            <span class="result-label">Hazard Detected:</span>
            <span class="result-value ${result.is_hazard ? 'positive' : 'negative'}">
                ${result.is_hazard ? 'YES' : 'NO'}
            </span>
        </div>
        <div class="result-item">
            <span class="result-label">Hazard Type:</span>
            <span class="result-value">${result.hazard_type.replace('_', ' ').toUpperCase()}</span>
        </div>
        <div class="result-item">
            <span class="result-label">Urgency Level:</span>
            <span class="result-value ${result.urgency}">${result.urgency.toUpperCase()}</span>
        </div>
        <div class="result-item">
            <span class="result-label">Confidence Score:</span>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${result.confidence * 100}%"></div>
                </div>
                <span class="result-value">${Math.round(result.confidence * 100)}%</span>
            </div>
        </div>
        <div class="result-item">
            <span class="result-label">Detected Locations:</span>
            <span class="result-value">${result.locations.length > 0 ? result.locations.join(', ') : 'None detected'}</span>
        </div>
        <div class="result-item">
            <span class="result-label">Key Terms:</span>
            <div class="keywords-list">
                ${result.keywords.map(keyword => `<span class="keyword-tag">${keyword}</span>`).join('')}
            </div>
        </div>
    `;
}

function updateAnalysisHistory() {
    const historyContainer = document.getElementById('analysisHistory');
    if (!historyContainer) return;
    
    const recentHistory = analysisHistory.slice(0, 5);
    
    if (recentHistory.length === 0) {
        historyContainer.innerHTML = '<p class="text-muted">No analysis history yet. Try analyzing some text!</p>';
        return;
    }
    
    historyContainer.innerHTML = recentHistory.map(item => `
        <div class="history-item">
            <div class="post-text">"${item.text}"</div>
            <div class="analysis-summary">
                <span class="status status--${item.result.is_hazard ? 'error' : 'success'}">${item.result.is_hazard ? 'Hazard' : 'Normal'}</span>
                <span class="status status--${item.result.urgency === 'high' ? 'error' : item.result.urgency === 'medium' ? 'warning' : 'success'}">${item.result.urgency}</span>
                <span>${Math.round(item.result.confidence * 100)}% confident</span>
                <span class="alert-time">${formatTime(item.timestamp)}</span>
            </div>
        </div>
    `).join('');
}

// Social Media Analysis functions
function initializeSocialMediaAnalysis() {
    // Nothing specific needed here
}

function performBatchAnalysis() {
    const batchInput = document.getElementById('batchInput');
    if (!batchInput) return;
    
    const posts = batchInput.value.trim().split('\n').filter(post => post.trim());
    
    if (posts.length === 0) {
        alert('Please enter at least one post for analysis');
        return;
    }
    
    console.log('Performing batch analysis on', posts.length, 'posts');
    showLoadingModal();
    
    setTimeout(() => {
        const results = posts.map(post => ({
            text: post,
            analysis: simulateAIAnalysis(post)
        }));
        
        displayBatchResults(results);
        hideLoadingModal();
        
        // Clear input
        batchInput.value = '';
    }, 2000);
}

function displayBatchResults(results) {
    const resultsContainer = document.getElementById('batchResults');
    if (!resultsContainer) return;
    
    const hazardCount = results.filter(r => r.analysis.is_hazard).length;
    const highUrgency = results.filter(r => r.analysis.urgency === 'high').length;
    const avgConfidence = results.reduce((sum, r) => sum + r.analysis.confidence, 0) / results.length;
    
    resultsContainer.innerHTML = `
        <div class="batch-summary">
            <h4>Analysis Summary</h4>
            <p><strong>Total Posts:</strong> ${results.length} | 
               <strong>Hazards Detected:</strong> ${hazardCount} | 
               <strong>High Urgency:</strong> ${highUrgency} | 
               <strong>Avg Confidence:</strong> ${Math.round(avgConfidence * 100)}%</p>
        </div>
        
        <table class="results-table">
            <thead>
                <tr>
                    <th>Post Text</th>
                    <th>Hazard</th>
                    <th>Type</th>
                    <th>Urgency</th>
                    <th>Confidence</th>
                    <th>Locations</th>
                </tr>
            </thead>
            <tbody>
                ${results.map(result => `
                    <tr>
                        <td class="post-preview" title="${result.text}">${result.text.length > 50 ? result.text.substring(0, 50) + '...' : result.text}</td>
                        <td><span class="status status--${result.analysis.is_hazard ? 'error' : 'success'}">${result.analysis.is_hazard ? 'Yes' : 'No'}</span></td>
                        <td>${result.analysis.hazard_type.replace('_', ' ')}</td>
                        <td><span class="urgency-badge ${result.analysis.urgency}">${result.analysis.urgency}</span></td>
                        <td>${Math.round(result.analysis.confidence * 100)}%</td>
                        <td>${result.analysis.locations.join(', ') || '-'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function exportResults() {
    alert('Results exported successfully! (This is a simulation)');
}

// Hotspot Visualization functions
function initializeHotspots() {
    renderHotspotMap();
}

function renderHotspotMap() {
    const mapContainer = document.getElementById('hotspotMap');
    if (!mapContainer) return;
    
    mapContainer.innerHTML = '';
    
    appData.hotspots.forEach((hotspot, index) => {
        const marker = document.createElement('div');
        marker.className = `hotspot-marker ${hotspot.risk_level}-risk`;
        marker.textContent = hotspot.total_reports;
        marker.title = `${hotspot.location} - ${hotspot.risk_level} risk`;
        
        const positions = [
            {left: '15%', top: '20%'}, // Chennai
            {left: '25%', top: '65%'}, // Mumbai
            {left: '10%', top: '85%'}, // Kochi
            {left: '70%', top: '30%'}  // Paradip
        ];
        
        if (positions[index]) {
            marker.style.left = positions[index].left;
            marker.style.top = positions[index].top;
        }
        
        marker.addEventListener('click', () => {
            selectHotspot(hotspot);
        });
        
        mapContainer.appendChild(marker);
    });
}

function selectHotspot(hotspot) {
    selectedHotspot = hotspot;
    displayHotspotDetails(hotspot);
    
    // Update marker selection
    document.querySelectorAll('.hotspot-marker').forEach(marker => {
        marker.classList.remove('selected');
    });
    
    event.target.classList.add('selected');
}

function displayHotspotDetails(hotspot) {
    const detailsContainer = document.getElementById('hotspotDetails');
    if (!detailsContainer) return;
    
    detailsContainer.innerHTML = `
        <h4>📍 ${hotspot.location}</h4>
        <div class="detail-item">
            <span class="detail-label">Risk Level:</span>
            <span class="detail-value">
                <span class="status status--${hotspot.risk_level === 'high' ? 'error' : hotspot.risk_level === 'medium' ? 'warning' : 'success'}">
                    ${hotspot.risk_level.toUpperCase()}
                </span>
            </span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Total Reports:</span>
            <span class="detail-value">${hotspot.total_reports}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Hazard Reports:</span>
            <span class="detail-value">${hotspot.hazard_reports}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Dominant Hazard:</span>
            <span class="detail-value">${hotspot.dominant_hazard}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Severity Score:</span>
            <span class="detail-value">${hotspot.severity_score}/3.0</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Last Activity:</span>
            <span class="detail-value">2 hours ago</span>
        </div>
    `;
}

// Alert System functions
function initializeAlerts() {
    renderAlerts();
}

function renderAlerts(filteredAlerts = null) {
    const alertsContainer = document.getElementById('alertsList');
    if (!alertsContainer) return;
    
    const alerts = filteredAlerts || appData.alerts;
    
    if (alerts.length === 0) {
        alertsContainer.innerHTML = '<p class="text-muted">No alerts match the current filters</p>';
        return;
    }
    
    alertsContainer.innerHTML = alerts.map(alert => `
        <div class="alert-card ${alert.urgency}">
            <div class="alert-header">
                <h3 class="alert-title">${alert.hazard_type}</h3>
                <span class="urgency-badge ${alert.urgency}">${alert.urgency}</span>
            </div>
            <div class="alert-meta">
                <span>📍 ${alert.location}</span>
                <span>🕒 ${formatTime(alert.timestamp)}</span>
                <span>🎯 ${Math.round(alert.confidence * 100)}% confidence</span>
            </div>
            <p class="alert-message">${alert.message}</p>
        </div>
    `).join('');
}

function applyAlertFilters() {
    const urgencyFilter = document.getElementById('urgencyFilter');
    const hazardFilter = document.getElementById('hazardFilter');
    
    if (!urgencyFilter || !hazardFilter) return;
    
    const urgencyValue = urgencyFilter.value;
    const hazardValue = hazardFilter.value;
    
    let filteredAlerts = appData.alerts;
    
    if (urgencyValue) {
        filteredAlerts = filteredAlerts.filter(alert => alert.urgency === urgencyValue);
    }
    
    if (hazardValue) {
        filteredAlerts = filteredAlerts.filter(alert => 
            alert.hazard_type.toLowerCase().replace(' ', '_') === hazardValue
        );
    }
    
    renderAlerts(filteredAlerts);
}

// Analytics functions
function initializeAnalytics() {
    setTimeout(() => {
        createTrendsChart();
        createLocationChart();
    }, 200);
}

function createTrendsChart() {
    const canvas = document.getElementById('trendsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'];
    const tsunamiData = [2, 4, 1, 8, 3, 2, 4, 15];
    const stormSurgeData = [5, 8, 12, 15, 18, 20, 25, 28];
    const highWavesData = [10, 15, 18, 22, 28, 30, 32, 34];
    
    if (charts.trendsChart) {
        charts.trendsChart.destroy();
    }
    
    charts.trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Tsunami',
                    data: tsunamiData,
                    borderColor: '#1FB8CD',
                    backgroundColor: 'rgba(31, 184, 205, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Storm Surge',
                    data: stormSurgeData,
                    borderColor: '#FFC185',
                    backgroundColor: 'rgba(255, 193, 133, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'High Waves',
                    data: highWavesData,
                    borderColor: '#B4413C',
                    backgroundColor: 'rgba(180, 65, 60, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function createLocationChart() {
    const canvas = document.getElementById('locationChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    const locations = ['Chennai', 'Mumbai', 'Kochi', 'Kolkata', 'Paradip', 'Goa'];
    const frequencies = [23, 18, 15, 12, 10, 8];
    
    if (charts.locationChart) {
        charts.locationChart.destroy();
    }
    
    charts.locationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: locations,
            datasets: [{
                label: 'Hazard Reports',
                data: frequencies,
                backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F', '#DB4545']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Utility functions
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showLoadingModal() {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function hideLoadingModal() {
    const modal = document.getElementById('loadingModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

function addSampleAnalysis() {
    const sampleTexts = [
        "Massive waves hitting Chennai coast. Water levels rising rapidly!",
        "Beautiful sunset at Goa beach today. Perfect weather conditions.",
        "Storm warning for Mumbai harbor. All fishing boats advised to return.",
        "High tide alert for Kochi backwaters. Monitoring situation closely."
    ];
    
    sampleTexts.forEach((text, index) => {
        setTimeout(() => {
            const result = simulateAIAnalysis(text);
            analysisHistory.push({
                text: text,
                result: result,
                timestamp: new Date(Date.now() - (index * 3600000)).toISOString()
            });
        }, index * 100);
    });
}