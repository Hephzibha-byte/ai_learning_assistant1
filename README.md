# 🤖 AI Learning & Study Assistant

An AI-powered personalized learning assistant that helps students learn from their own study materials, generate quizzes, create study plans, track performance, and receive personalized recommendations.

## 📌 Project Overview

The AI Learning & Study Assistant is an intelligent educational application built using Python, Streamlit, RAG, and local Large Language Models.

The system acts as a personal AI tutor that can answer student questions, retrieve information from uploaded PDFs, generate quizzes, evaluate performance, create study plans, and maintain student learning progress.

By combining Retrieval-Augmented Generation (RAG), Agentic AI tools, and student memory, the application provides a personalized and adaptive learning experience.

## 🎯 Objectives

- Provide personalized AI-based learning assistance.
- Allow students to learn from their own PDF study materials.
- Retrieve relevant information using RAG.
- Generate topic-based quizzes automatically.
- Evaluate quiz performance and store scores.
- Identify strong and weak learning topics.
- Generate personalized study recommendations.
- Create customized study plans.
- Provide voice input and text-to-speech support.
- Display student learning progress through a dashboard.

## ⭐ Key Features

### 💬 AI Chat
Students can ask questions and receive AI-generated explanations.

### 📄 PDF Upload & RAG
Students can upload study PDFs and ask questions based on their uploaded content.

### 🧠 Student Memory
The system stores learning progress and quiz performance for personalization.

### 📝 AI Quiz Generation
Automatically generates quizzes based on selected topics.

### 📊 Quiz Evaluation
Evaluates student answers and calculates the score.

### 🎯 Personalized Recommendations
Analyzes quiz performance and recommends topics that need more attention.

### 📅 Study Plan Generator
Creates customized study plans based on subject, number of days, and study hours.

### 📊 Progress Dashboard
Displays:
- Number of quizzes taken
- Average score
- Best score
- Topics studied
- Strong topics
- Weak topics
- Quiz history
- Personalized recommendations

### 🎤 Voice Input
Allows students to ask questions using voice.

### 🔊 Read Aloud
Converts AI-generated answers into speech.

## 🏗️ System Architecture

```text
                 👨‍🎓 Student
                     |
                     v
              Streamlit Interface
                     |
                     v
               🤖 AI Agent
                     |
        +------------+-------------+
        |            |             |
        v            v             v
      📄 RAG      🧠 Memory      🛠️ Tools
        |            |             |
        v            v             v
   PDF Retrieval  Progress     Quiz / Plan
        |          Tracking      Generator
        |            |             |
        +------------+-------------+
                     |
                     v
               🤖 AI Response
                     |
                     v
              👨‍🎓 Student
                     |
                     v
              📊 Progress Update
