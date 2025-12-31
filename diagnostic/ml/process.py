import os
import joblib
import numpy as np
from pathlib import Path

# Chemin du modèle
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / 'diagnostic' / 'ml' / 'model.pkl'

# Mapping des symptômes
SYMPTOM_MAPPING = {
    'fever': 0, 'cough': 1, 'headache': 2, 'fatigue': 3,
    'sore_throat': 4, 'shortness_of_breath': 5, 'chest_pain': 6,
    'nausea': 7, 'vomiting': 8, 'diarrhea': 9
}

# Mapping des maladies
DISEASE_MAPPING = {
    0: 'Grippe (Influenza)',
    1: 'Pneumonie',
    2: 'COVID-19',
    3: 'Rhume commun',
    4: 'Bronchite',
    5: 'Gastro-entérite'
}

def load_model():
    """Charge le modèle ML entraîné"""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Le modèle n'existe pas. Exécutez 'python train_model.py' d'abord."
        )
    return joblib.load(MODEL_PATH)

def prepare_input(symptoms):
    """Convertit les symptômes en vecteur pour le modèle"""
    feature_vector = np.zeros(len(SYMPTOM_MAPPING))
    for symptom in symptoms:
        if symptom in SYMPTOM_MAPPING:
            feature_vector[SYMPTOM_MAPPING[symptom]] = 1
    return feature_vector.reshape(1, -1)

def predict_disease(symptoms):
    """Prédit les maladies possibles avec probabilités"""
    try:
        model = load_model()
        X = prepare_input(symptoms)
        
        # Obtenir les probabilités
        probabilities = model.predict_proba(X)[0]
        
        # Créer la liste des prédictions avec probabilités
        predictions = []
        for idx, prob in enumerate(probabilities):
            if prob > 0.05:  # Seuil de 5%
                predictions.append({
                    'disease': DISEASE_MAPPING.get(idx, 'Inconnu'),
                    'probability': round(prob * 100, 1)
                })
        
        # Trier par probabilité décroissante
        predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        return predictions[:3]  # Top 3 prédictions
        
    except Exception as e:
        raise Exception(f"Erreur de prédiction: {str(e)}")