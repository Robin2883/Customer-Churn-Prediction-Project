from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, recall_score

def evaluate_model(model, threshold, X, y):
    
    proba = model.predict_proba(X)[:, 1]
    preds= (proba >= threshold).astype(int)
    acc = accuracy_score(y, preds)
    rec = recall_score(y, preds)
    print("Classification Report:\n", classification_report(y, preds))
    print("Confusion Matrix:\n", confusion_matrix(y, preds))
    print(f"Model trained. Accuracy: {acc:.4f}, Recall: {rec:.4f}")