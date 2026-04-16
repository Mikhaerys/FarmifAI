#!/usr/bin/env python3
"""
Generate black and white architecture diagrams for FarmifAI paper.
Creates publication-quality diagrams using matplotlib.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Set up style for academic papers
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.linewidth'] = 0.5


def draw_box(ax, x, y, width, height, text, fontsize=8, bold=False, fill='white', linewidth=1):
    """Draw a rounded rectangle with centered text."""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor=fill,
        edgecolor='black',
        linewidth=linewidth
    )
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, weight=weight)


def draw_arrow(ax, start, end, style='->', color='black'):
    """Draw an arrow between two points."""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle=style, color=color, lw=0.8))


def create_system_architecture():
    """Create the on-device system architecture diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(5, 11.5, 'FarmifAI System Architecture (On-Device)', 
            ha='center', va='center', fontsize=12, weight='bold')
    
    # Main container - Android Device
    outer_box = FancyBboxPatch(
        (0.5, 0.5), 9, 10.5,
        boxstyle="round,pad=0.02,rounding_size=0.2",
        facecolor='white',
        edgecolor='black',
        linewidth=2
    )
    ax.add_patch(outer_box)
    ax.text(5, 10.7, 'Android Device', ha='center', va='center', fontsize=10, weight='bold')
    
    # App container
    app_box = FancyBboxPatch(
        (1, 1), 8, 9,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        facecolor='#f5f5f5',
        edgecolor='black',
        linewidth=1.5
    )
    ax.add_patch(app_box)
    ax.text(5, 9.7, 'FarmifAI Application', ha='center', va='center', fontsize=9, weight='bold')
    
    # Input layer - User Interface Components
    draw_box(ax, 2.5, 8.5, 2.2, 0.8, 'VoiceHelper\n(Vosk + TTS)', fontsize=7)
    draw_box(ax, 5, 8.5, 2.2, 0.8, 'ChatInterface\n(Compose UI)', fontsize=7)
    draw_box(ax, 7.5, 8.5, 2.2, 0.8, 'CameraHelper\n(CameraX)', fontsize=7)
    
    # Processing layer
    draw_box(ax, 2.5, 6.8, 2.2, 0.8, 'model-es-small\n(Vosk ASR)', fontsize=7, fill='#e8e8e8')
    draw_box(ax, 5, 6.8, 2.2, 0.8, 'SemanticSearch\nHelper', fontsize=7)
    draw_box(ax, 7.5, 6.8, 2.2, 0.8, 'PlantDisease\nClassifier', fontsize=7)
    
    # Model layer
    draw_box(ax, 5, 5.2, 2.5, 0.8, 'sentence_encoder.ms\n(MiniLM 384-dim)', fontsize=7, fill='#e8e8e8')
    draw_box(ax, 7.5, 5.2, 2.2, 0.8, 'plant_disease\n_model.ms', fontsize=7, fill='#e8e8e8')
    
    # Knowledge base
    draw_box(ax, 5, 3.8, 2.5, 0.7, 'kb_embeddings.npy\n(517 × 384 float32)', fontsize=7, fill='#d8d8d8')
    
    # LLM layer
    draw_box(ax, 5, 2.6, 2.2, 0.7, 'LlamaService\n(llama.cpp)', fontsize=7)
    draw_box(ax, 5, 1.6, 2.8, 0.7, 'Llama-3.2-1B-Q4_K_M.gguf\n(~750MB)', fontsize=7, fill='#e8e8e8')
    
    # Arrows - Voice path
    draw_arrow(ax, (2.5, 8.1), (2.5, 7.2))
    
    # Arrows - Chat path
    draw_arrow(ax, (5, 8.1), (5, 7.2))
    draw_arrow(ax, (5, 6.4), (5, 5.6))
    draw_arrow(ax, (5, 4.8), (5, 4.15))
    draw_arrow(ax, (5, 3.45), (5, 2.95))
    draw_arrow(ax, (5, 2.25), (5, 1.95))
    
    # Arrows - Camera path
    draw_arrow(ax, (7.5, 8.1), (7.5, 7.2))
    draw_arrow(ax, (7.5, 6.4), (7.5, 5.6))
    
    # Cross connections
    draw_arrow(ax, (3.6, 6.8), (3.9, 6.8))  # Voice to Semantic
    draw_arrow(ax, (6.1, 5.2), (6.4, 5.2))  # Semantic to Vision context
    
    # Legend
    ax.text(1.3, 0.3, 'Gray boxes = ML Models', fontsize=7, style='italic')
    
    plt.tight_layout()
    plt.savefig('docs/fig_system_architecture.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.savefig('docs/fig_system_architecture.pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: fig_system_architecture.png/pdf")


def create_training_architecture():
    """Create the training pipeline architecture diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(6, 9.5, 'FarmifAI Training Architecture', 
            ha='center', va='center', fontsize=12, weight='bold')
    
    # Training Environment container
    env_box = FancyBboxPatch(
        (0.5, 0.5), 11, 8.5,
        boxstyle="round,pad=0.02,rounding_size=0.2",
        facecolor='white',
        edgecolor='black',
        linewidth=2
    )
    ax.add_patch(env_box)
    ax.text(6, 8.7, 'Training Environment (Google Colab / Azure ML)', 
            ha='center', va='center', fontsize=9, weight='bold')
    
    # === LEFT SIDE: Vision Model Training ===
    ax.text(3, 8.2, 'Vision Model Pipeline', ha='center', fontsize=9, weight='bold')
    
    # Datasets
    draw_box(ax, 2, 7.2, 2.2, 0.7, 'PlantVillage DS\n(38 classes)', fontsize=7, fill='#e8e8e8')
    draw_box(ax, 4, 7.2, 2.2, 0.7, 'Colombia Crops\n(Coffee, etc.)', fontsize=7, fill='#e8e8e8')
    
    # Training phases
    draw_box(ax, 3, 5.8, 3.5, 1.0, 'MobileNetV2 Fine-tuning\nPhase 1: Feature Extraction (25 ep)\nPhase 2: Full Fine-tuning (35 ep)', fontsize=6)
    
    # Output
    draw_box(ax, 3, 4.3, 2.2, 0.6, 'SavedModel (TF)', fontsize=7)
    draw_box(ax, 3, 3.4, 2.5, 0.6, 'MindSpore Converter\n(TF → .ms)', fontsize=7, fill='#d8d8d8')
    draw_box(ax, 3, 2.4, 2.5, 0.6, 'plant_disease_model.ms', fontsize=7, fill='#c8c8c8')
    
    # Arrows vision
    draw_arrow(ax, (2, 6.85), (2.5, 6.3))
    draw_arrow(ax, (4, 6.85), (3.5, 6.3))
    draw_arrow(ax, (3, 5.3), (3, 4.6))
    draw_arrow(ax, (3, 4.0), (3, 3.7))
    draw_arrow(ax, (3, 3.1), (3, 2.7))
    
    # === RIGHT SIDE: NLP Model Pipeline ===
    ax.text(9, 8.2, 'NLP Model Pipeline', ha='center', fontsize=9, weight='bold')
    
    # Knowledge base
    draw_box(ax, 9, 7.2, 2.8, 0.7, 'agrochat_knowledge\n_base.json (517 Q&A)', fontsize=7, fill='#e8e8e8')
    
    # Encoder
    draw_box(ax, 9, 5.8, 3.2, 0.9, 'paraphrase-multilingual\n-MiniLM-L12-v2\n(Sentence Transformers)', fontsize=6)
    
    # Processing
    draw_box(ax, 9, 4.5, 2.8, 0.7, 'Mean Pooling +\nL2 Normalization', fontsize=7)
    
    # Output
    draw_box(ax, 9, 3.4, 2.5, 0.6, 'sentence_encoder.ms', fontsize=7, fill='#c8c8c8')
    draw_box(ax, 9, 2.4, 2.5, 0.6, 'kb_embeddings.npy\n(517 × 384)', fontsize=7, fill='#c8c8c8')
    
    # Arrows NLP
    draw_arrow(ax, (9, 6.85), (9, 6.25))
    draw_arrow(ax, (9, 5.35), (9, 4.85))
    draw_arrow(ax, (9, 4.15), (9, 3.7))
    draw_arrow(ax, (9, 4.15), (9, 2.7))
    
    # === BOTTOM: Deployment ===
    deploy_box = FancyBboxPatch(
        (1.5, 1.0), 9, 1.0,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor='#f0f0f0',
        edgecolor='black',
        linewidth=1,
        linestyle='--'
    )
    ax.add_patch(deploy_box)
    ax.text(6, 1.5, 'Deployment: Copy models to app/src/main/assets/ → Build APK → Install on device', 
            ha='center', va='center', fontsize=8)
    
    # Arrows to deployment
    draw_arrow(ax, (3, 2.1), (3, 1.7), style='->')
    draw_arrow(ax, (9, 2.1), (9, 1.7), style='->')
    
    plt.tight_layout()
    plt.savefig('docs/fig_training_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('docs/fig_training_architecture.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: fig_training_architecture.png/pdf")


def create_rag_pipeline():
    """Create the RAG inference pipeline diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Title
    ax.text(6, 4.6, 'RAG (Retrieval-Augmented Generation) Pipeline', 
            ha='center', va='center', fontsize=11, weight='bold')
    
    # Pipeline boxes
    draw_box(ax, 1.2, 2.5, 1.8, 1.0, 'User Query\n(Text/Voice)', fontsize=7, fill='#e8e8e8')
    draw_box(ax, 3.2, 2.5, 1.6, 1.0, 'Tokenize\n(128 tokens)', fontsize=7)
    draw_box(ax, 5.2, 2.5, 1.8, 1.0, 'Encode\n(MiniLM\n384-dim)', fontsize=7)
    draw_box(ax, 7.2, 2.5, 1.8, 1.0, 'Cosine\nSimilarity\nSearch', fontsize=7)
    draw_box(ax, 9.2, 2.5, 1.6, 1.0, 'Top-K\nContexts', fontsize=7)
    draw_box(ax, 11, 2.5, 1.4, 1.0, 'LLM\nResponse', fontsize=7, fill='#e8e8e8')
    
    # Knowledge base (below)
    draw_box(ax, 7.2, 0.9, 2.5, 0.7, 'KB Embeddings\n(517 × 384 float32)', fontsize=7, fill='#d8d8d8')
    
    # Arrows
    draw_arrow(ax, (2.1, 2.5), (2.4, 2.5))
    draw_arrow(ax, (4.0, 2.5), (4.3, 2.5))
    draw_arrow(ax, (6.1, 2.5), (6.3, 2.5))
    draw_arrow(ax, (8.1, 2.5), (8.4, 2.5))
    draw_arrow(ax, (10.0, 2.5), (10.3, 2.5))
    
    # Arrow from KB to similarity
    draw_arrow(ax, (7.2, 1.25), (7.2, 2.0))
    
    # Timing annotations
    ax.text(3.2, 1.5, '~10ms', ha='center', fontsize=6, style='italic')
    ax.text(5.2, 1.5, '50-100ms', ha='center', fontsize=6, style='italic')
    ax.text(7.2, 3.3, '10-30ms', ha='center', fontsize=6, style='italic')
    ax.text(11, 1.5, '2-5s', ha='center', fontsize=6, style='italic')
    
    plt.tight_layout()
    plt.savefig('docs/fig_rag_pipeline.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('docs/fig_rag_pipeline.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: fig_rag_pipeline.png/pdf")


def create_vision_inference():
    """Create the vision model inference pipeline diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 3.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Title
    ax.text(6, 3.6, 'Vision Model Inference Pipeline', 
            ha='center', va='center', fontsize=11, weight='bold')
    
    # Pipeline boxes
    draw_box(ax, 1.2, 2, 1.6, 1.2, 'Camera\nCapture\n(RGB)', fontsize=7, fill='#e8e8e8')
    draw_box(ax, 3.2, 2, 1.8, 1.2, 'Preprocess\nResize 224×224\nNormalize [-1,1]', fontsize=6)
    draw_box(ax, 5.5, 2, 2.2, 1.2, 'MindSpore Lite\nInference\n(MobileNetV2)', fontsize=6, fill='#d8d8d8')
    draw_box(ax, 8, 2, 1.8, 1.2, 'Softmax\n21 classes\nTop-K', fontsize=7)
    draw_box(ax, 10.5, 2, 2.0, 1.2, 'Disease Result\n+ Confidence\n+ Treatment', fontsize=6, fill='#e8e8e8')
    
    # Arrows
    draw_arrow(ax, (2.0, 2), (2.3, 2))
    draw_arrow(ax, (4.1, 2), (4.4, 2))
    draw_arrow(ax, (6.6, 2), (7.1, 2))
    draw_arrow(ax, (8.9, 2), (9.5, 2))
    
    # Timing
    ax.text(3.2, 0.8, '~20ms', ha='center', fontsize=6, style='italic')
    ax.text(5.5, 0.8, '200-400ms', ha='center', fontsize=6, style='italic')
    ax.text(8, 0.8, '~5ms', ha='center', fontsize=6, style='italic')
    
    plt.tight_layout()
    plt.savefig('docs/fig_vision_inference.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('docs/fig_vision_inference.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: fig_vision_inference.png/pdf")


def create_two_phase_training():
    """Create the two-phase training diagram for MobileNetV2."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(6, 5.6, 'Two-Phase Transfer Learning Strategy', 
            ha='center', va='center', fontsize=11, weight='bold')
    
    # Phase 1 container
    phase1_box = FancyBboxPatch(
        (0.5, 2.5), 5, 2.7,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        facecolor='#f5f5f5',
        edgecolor='black',
        linewidth=1.5
    )
    ax.add_patch(phase1_box)
    ax.text(3, 5.0, 'Phase 1: Feature Extraction (25 epochs)', 
            ha='center', va='center', fontsize=9, weight='bold')
    
    # Phase 1 content
    draw_box(ax, 2, 4.0, 2.5, 0.8, 'MobileNetV2\nBackbone\n(FROZEN)', fontsize=6, fill='#d0d0d0')
    draw_box(ax, 4.5, 4.0, 2.0, 0.8, 'Classification\nHead\n(trainable)', fontsize=6)
    draw_arrow(ax, (3.25, 4.0), (3.5, 4.0))
    ax.text(3, 2.9, 'LR: 1e-3 | Adam | Dropout 0.4', ha='center', fontsize=7, style='italic')
    
    # Phase 2 container
    phase2_box = FancyBboxPatch(
        (6.5, 2.5), 5, 2.7,
        boxstyle="round,pad=0.02,rounding_size=0.15",
        facecolor='#f5f5f5',
        edgecolor='black',
        linewidth=1.5
    )
    ax.add_patch(phase2_box)
    ax.text(9, 5.0, 'Phase 2: Fine-tuning (35 epochs)', 
            ha='center', va='center', fontsize=9, weight='bold')
    
    # Phase 2 content
    draw_box(ax, 8, 4.0, 2.5, 0.8, 'MobileNetV2\nBackbone\n(trainable)', fontsize=6)
    draw_box(ax, 10.5, 4.0, 2.0, 0.8, 'Classification\nHead\n(trainable)', fontsize=6)
    draw_arrow(ax, (9.25, 4.0), (9.5, 4.0))
    ax.text(9, 2.9, 'LR: 1e-5 | Label Smoothing 0.1', ha='center', fontsize=7, style='italic')
    
    # Arrow between phases
    draw_arrow(ax, (5.5, 3.8), (6.5, 3.8), style='->')
    ax.text(6, 4.2, 'weights\ntransfer', ha='center', fontsize=6)
    
    # Data augmentation box
    aug_box = FancyBboxPatch(
        (2, 0.8), 8, 1.3,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor='white',
        edgecolor='black',
        linewidth=1,
        linestyle='--'
    )
    ax.add_patch(aug_box)
    ax.text(6, 1.8, 'Data Augmentation (Both Phases)', ha='center', fontsize=8, weight='bold')
    ax.text(6, 1.2, 'Rotation 40° | Shift 0.3 | Zoom 0.3 | Flip H/V | Brightness [0.6, 1.4]', 
            ha='center', fontsize=7)
    
    plt.tight_layout()
    plt.savefig('docs/fig_two_phase_training.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('docs/fig_two_phase_training.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: fig_two_phase_training.png/pdf")


def create_deployment_workflow():
    """Create the deployment workflow diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')
    
    # Title
    ax.text(6, 4.6, 'Model Deployment Workflow', 
            ha='center', va='center', fontsize=11, weight='bold')
    
    # Row 1: Model preparation
    draw_box(ax, 1.5, 3.3, 2.2, 0.9, 'Train Model\n(TF/PyTorch)', fontsize=7, fill='#e8e8e8')
    draw_box(ax, 4, 3.3, 2.2, 0.9, 'Export Model\n(SavedModel/\nONNX)', fontsize=6)
    draw_box(ax, 6.5, 3.3, 2.2, 0.9, 'Convert to\nMindSpore\n(.ms)', fontsize=7)
    draw_box(ax, 9, 3.3, 2.0, 0.9, 'Validate\nModel', fontsize=7)
    draw_box(ax, 11, 3.3, 1.5, 0.9, 'Copy to\nassets/', fontsize=7, fill='#d8d8d8')
    
    # Arrows row 1
    draw_arrow(ax, (2.6, 3.3), (2.9, 3.3))
    draw_arrow(ax, (5.1, 3.3), (5.4, 3.3))
    draw_arrow(ax, (7.6, 3.3), (8.0, 3.3))
    draw_arrow(ax, (10.0, 3.3), (10.25, 3.3))
    
    # Row 2: App build
    draw_box(ax, 2, 1.7, 2.0, 0.9, 'Build APK\n(Gradle)', fontsize=7)
    draw_box(ax, 4.5, 1.7, 2.0, 0.9, 'Sign APK\n(Release)', fontsize=7)
    draw_box(ax, 7, 1.7, 2.2, 0.9, 'Install via\nADB/Store', fontsize=7, fill='#d8d8d8')
    draw_box(ax, 10, 1.7, 2.5, 0.9, 'Push LLM\n(adb push)', fontsize=7, fill='#e8e8e8')
    
    # Arrows row 2
    draw_arrow(ax, (11, 2.85), (11, 2.6), style='->')  # From assets to build
    draw_arrow(ax, (11, 2.4), (3, 2.2), style='->')  # Curved to build
    draw_arrow(ax, (3.0, 1.7), (3.5, 1.7))
    draw_arrow(ax, (5.5, 1.7), (5.9, 1.7))
    draw_arrow(ax, (8.1, 1.7), (8.75, 1.7))
    
    # Annotation
    ax.text(6, 0.7, 'LLM (~750MB) deployed separately due to size constraints', 
            ha='center', fontsize=7, style='italic')
    
    plt.tight_layout()
    plt.savefig('docs/fig_deployment_workflow.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.savefig('docs/fig_deployment_workflow.pdf', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: fig_deployment_workflow.png/pdf")


if __name__ == "__main__":
    import os
    os.makedirs('docs', exist_ok=True)
    
    print("Generating diagrams...")
    create_system_architecture()
    create_training_architecture()
    create_rag_pipeline()
    create_vision_inference()
    create_two_phase_training()
    create_deployment_workflow()
    print("\nAll diagrams generated successfully!")
    print("Output files in: docs/")
