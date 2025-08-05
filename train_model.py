import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. Load the CSV file
data = pd.read_csv("messages.csv")
print("✅ Data loaded:", data.shape)

# 2. Make sure required columns exist
if 'text' not in data.columns or 'label' not in data.columns:
    raise ValueError("CSV must contain 'text' and 'label' columns")

# 3. Split into features and labels
X = data['text']
y = data['label']

# 4. Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Create the model pipeline
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# 6. Train the model
model.fit(X_train, y_train)

# 7. Test the model
y_pred = model.predict(X_test)

# 8. Show the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy:.2%}")  # Example: 92.50%

# 9. Show precision, recall, F1 score
print("📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Original", "Fake"]))

# 10. Save model
joblib.dump(model, 'model.pkl')
print("💾 Model saved as model.pkl")

