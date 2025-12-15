#!/usr/bin/env python3
"""
Genera embeddings de la KB usando sentence-transformers.
Produce embeddings compatibles con el modelo MindSpore en Android.
"""

import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
KB_PATH = "app/src/main/assets/agrochat_knowledge_base.json"
OUTPUT_PATH = "app/src/main/assets/kb_embeddings.npy"

# Modelo - el mismo que usa MindSpore
# paraphrase-multilingual-MiniLM-L12-v2 produce 384 dims
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def main():
    print("=== Generando embeddings con sentence-transformers ===")
    print(f"Modelo: {MODEL_NAME}")
    print(f"KB: {KB_PATH}")
    
    # Cargar KB
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        kb_data = json.load(f)
    
    # Extraer todas las preguntas en orden (por ID para consistencia)
    questions = []
    entries = kb_data['entries']
    entries_sorted = sorted(entries, key=lambda x: x['id'])
    
    for entry in entries_sorted:
        for q in entry['questions']:
            questions.append(q)
    
    print(f"Total entradas: {len(entries_sorted)}")
    print(f"Total preguntas: {len(questions)}")
    
    # Mostrar algunas preguntas de muestra
    print("\nPrimeras 10 preguntas:")
    for i, q in enumerate(questions[:10]):
        print(f"  {i}: {q}")
    
    # Buscar preguntas de plagas de papa
    print("\nPreguntas de plagas de papa:")
    for i, q in enumerate(questions):
        if 'papa' in q.lower() and 'plaga' in q.lower():
            print(f"  {i}: {q}")
    
    # Cargar modelo
    print("\nCargando modelo...")
    model = SentenceTransformer(MODEL_NAME)
    
    # Generar embeddings
    print("Generando embeddings...")
    embeddings = model.encode(questions, normalize_embeddings=True, show_progress_bar=True)
    
    print(f"\nEmbeddings shape: {embeddings.shape}")
    print(f"Tipo: {embeddings.dtype}")
    print(f"Norma del primero: {np.linalg.norm(embeddings[0])}")
    
    # Convertir a float32 (MindSpore lo espera así)
    embeddings = embeddings.astype(np.float32)
    
    # Guardar
    np.save(OUTPUT_PATH, embeddings)
    print(f"\nGuardado en: {OUTPUT_PATH}")
    
    # Verificar
    loaded = np.load(OUTPUT_PATH)
    print(f"Verificación - shape: {loaded.shape}")
    print(f"Verificación - dtype: {loaded.dtype}")
    
    # Test de similitud: query de plagas de papa
    print("\n=== Test de similitud ===")
    test_query = "control de plagas en papa"
    query_embedding = model.encode([test_query], normalize_embeddings=True)[0]
    
    # Calcular similitud con todos
    similarities = np.dot(embeddings, query_embedding)
    
    # Top 5 más similares
    top_indices = np.argsort(similarities)[::-1][:5]
    print(f"Query: '{test_query}'")
    print("Top 5 coincidencias:")
    for idx in top_indices:
        print(f"  [{idx}] Score: {similarities[idx]:.4f} - '{questions[idx]}'")

if __name__ == "__main__":
    main()
