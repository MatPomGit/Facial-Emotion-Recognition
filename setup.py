"""
Setup configuration for Facial Emotion Recognition System
Konfiguracja instalacji dla Systemu Rozpoznawania Emocji
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='facial-emotion-recognition',
    version='1.0.0',
    author='MatPomGit',
    description='Real-time facial emotion recognition system using MediaPipe and SVM',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/MatPomGit/Facial-Emotion-Recognition',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='facial-recognition emotion-recognition machine-learning computer-vision mediapipe svm',
    python_requires='>=3.7',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
        'dlib': [
            'dlib>=19.22.0',
        ],
        'tensorflow': [
            'tensorflow>=2.8.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'facial-emotion-recognition=main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
    project_urls={
        'Bug Reports': 'https://github.com/MatPomGit/Facial-Emotion-Recognition/issues',
        'Source': 'https://github.com/MatPomGit/Facial-Emotion-Recognition',
        'Documentation': 'https://github.com/MatPomGit/Facial-Emotion-Recognition#readme',
    },
)
