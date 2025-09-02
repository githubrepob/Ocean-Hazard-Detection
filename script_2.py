# 3. Build NLP models for hazard detection

import warnings
warnings.filterwarnings('ignore')

# Text preprocessing function
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text

# Apply preprocessing
training_data['processed_text'] = training_data['text'].apply(preprocess_text)

# 3.1 Binary Hazard Detection Model (Is it a hazard or not?)
print("Building binary hazard detection model...")

X_binary = training_data['processed_text']
y_binary = training_data['is_hazard']

# Split data
X_train_bin, X_test_bin, y_train_bin, y_test_bin = train_test_split(
    X_binary, y_binary, test_size=0.2, random_state=42, stratify=y_binary
)

# Create pipeline for binary classification
binary_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
    ('classifier', MultinomialNB(alpha=0.1))
])

# Train the model
binary_pipeline.fit(X_train_bin, y_train_bin)

# Evaluate
y_pred_bin = binary_pipeline.predict(X_test_bin)
print("Binary Classification Results:")
print(classification_report(y_test_bin, y_pred_bin, target_names=['Normal', 'Hazard']))

# 3.2 Multi-class Hazard Type Detection Model
print("\nBuilding multi-class hazard type detection model...")

X_multi = training_data['processed_text']
y_multi = training_data['hazard_type']

# Split data
X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(
    X_multi, y_multi, test_size=0.2, random_state=42, stratify=y_multi
)

# Create pipeline for multi-class classification
multiclass_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
    ('classifier', MultinomialNB(alpha=0.1))
])

# Train the model
multiclass_pipeline.fit(X_train_multi, y_train_multi)

# Evaluate
y_pred_multi = multiclass_pipeline.predict(X_test_multi)
print("Multi-class Classification Results:")
print(classification_report(y_test_multi, y_pred_multi))

print("\nModels trained successfully!")