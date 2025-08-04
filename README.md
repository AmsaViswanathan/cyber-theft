# Cyber Theft Detection using X-AI (Final Year MCA Project)

Hi! I'm Amsa Viswanathan, and this is my MCA final semester project.  
This project is about detecting cyber theft and phishing messages using a machine learning model with explainable AI (X-AI).

## 🔍 Project Overview

The system helps users identify whether a message is:
- Safe  
- Suspicious  
- Phishing or Spam  

It also provides a confidence score based on the model's prediction.

## 🛠️ Tech Stack Used

- Python  
- Flask (for web interface)  
- SQLite (for storing user data)  
- scikit-learn (for ML model)  
- TF-IDF + Naive Bayes  
- HTML/CSS (frontend)

## 💡 Key Features

- User Registration & Login  
- Upload or input messages for checking  
- Real-time classification  
- Simple UI design  
- Backend connected to trained ML model

## 🗂️ Project Files

| File / Folder     | Description |
|-------------------|-------------|
| `app.py`          | Main application code using Flask |
| `train_model.py`  | ML model training script |
| `model.pkl`       | Trained ML model |
| `templates/`      | HTML files for UI |
| `static/`         | CSS and frontend assets |
| `users.db`        | SQLite DB for users |
| `messages.csv`    | Sample dataset used |
| `requirements.txt`| Python libraries list |

## ⚙️ How to Run

```bash
pip install -r requirements.txt
python app.py
