import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from pathlib import Path

# Créer le dossier ml s'il n'existe pas
ml_dir = Path('diagnostic/ml')
ml_dir.mkdir(parents=True, exist_ok=True)

# Génération de données synthétiques d'entraînement
np.random.seed(42)

# Définir les symptômes (10 symptômes)
symptoms = ['fever', 'cough', 'headache', 'fatigue', 'sore_throat',
            'shortness_of_breath', 'chest_pain', 'nausea', 'vomiting', 'diarrhea']

# Définir les maladies (6 maladies)
diseases = {
    0: 'Grippe',
    1: 'Pneumonie', 
    2: 'COVID-19',
    3: 'Rhume',
    4: 'Bronchite',
    5: 'Gastro-entérite'
}

# Profils de symptômes par maladie
disease_profiles = {
    0: [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],  # Grippe
    1: [1, 1, 0, 1, 0, 1, 1, 0, 0, 0],  # Pneumonie
    2: [1, 1, 1, 1, 0, 1, 0, 0, 0, 0],  # COVID-19
    3: [0, 1, 0, 1, 1, 0, 0, 0, 0, 0],  # Rhume
    4: [1, 1, 0, 1, 0, 1, 0, 0, 0, 0],  # Bronchite
    5: [1, 0, 1, 1, 0, 0, 0, 1, 1, 1],  # Gastro-entérite
}

# Générer 1000 échantillons
n_samples = 1000
data = []
labels = []

for _ in range(n_samples):
    disease_id = np.random.randint(0, 6)
    profile = disease_profiles[disease_id].copy()
    
    # Ajouter du bruit (variation)
    for i in range(len(profile)):
        if np.random.random() < 0.2:  # 20% de chance de variation
            profile[i] = 1 - profile[i]
    
    data.append(profile)
    labels.append(disease_id)

X = np.array(data)
y = np.array(labels)

# Diviser les données
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entraîner le modèle
print("🚀 Entraînement du modèle...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Évaluer le modèle
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Précision du modèle: {accuracy * 100:.2f}%")
print("\n📊 Rapport de classification:")
print(classification_report(y_test, y_pred, target_names=list(diseases.values())))

# Sauvegarder le modèle
model_path = ml_dir / 'model.pkl'
joblib.dump(model, model_path)
print(f"\n💾 Modèle sauvegardé dans: {model_path}")