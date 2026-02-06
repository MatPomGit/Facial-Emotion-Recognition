"""
Facial Emotion Recognition System

A real-time facial emotion recognition system using MediaPipe and SVM.
System rozpoznawania emocji na twarzy w czasie rzeczywistym wykorzystujący MediaPipe i SVM.
"""

__version__ = "1.0.0"
__author__ = "MatPomGit"
__license__ = "MIT"

from modules.svm import SVM
from modules.fps import FPS

__all__ = ["SVM", "FPS"]
