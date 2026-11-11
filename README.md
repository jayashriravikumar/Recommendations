#  Product Recommendation and Stock Forecasting System

This repository contains a full-stack implementation of a web-based intelligent recommendation and inventory forecasting system. It is developed using **ReactJS** for the frontend and **Flask** for the backend. The system provides personalized product recommendations to users and forecasts stock demand for administrators using machine learning techniques.

---

##  Table of Contents

* [Introduction](#introduction)
* [Project Overview](#project-overview)
* [Features](#features)
* [Technology Stack](#technology-stack)
* [Directory Structure](#directory-structure)
* [Installation and Setup](#installation-and-setup)
* [API Endpoints](#api-endpoints)
* [Future Enhancements](#future-enhancements)


---

## 📖 Introduction

With the growing demand for intelligent product suggestion systems and stock optimization in e-commerce and retail industries, this project introduces a scalable solution integrating recommendation algorithms and forecasting models. The system aids in enhancing user engagement and reducing inventory risks.

---

## 🧾 Project Overview

* **Frontend**: A responsive user interface built using ReactJS and TailwindCSS.
* **Backend**: Flask-based API server for delivering recommendations and stock forecasts.
* **ML Models**: Includes collaborative filtering-based recommendation and FAISS for time-series forecasting.

---

## 🔍 Features

### User Dashboard

* Accepts a User ID input.
* Returns a curated list of personalized product recommendations.

### Admin Dashboard

* Displays real-time stock forecasts for various products.
* Highlights stockout risks based on predicted demand.

---

## 🛠️ Technology Stack

| Component   | Technology                               |
| ----------- | ---------------------------------------- |
| Frontend    | ReactJS, TailwindCSS, Axios              |
| Backend     | Python, Flask, Pandas, NumPy             |
| ML/Forecast | Scikit-learn, FAISS                      |
| Deployment  | Docker                                   |

---

## 📁 Directory Structure

```
jayashriravikumar-recommendations/
├── my-recommender-frontend/
│   ├── src/components/              # HomePage, Recommendations, StockForecast
│   ├── App.jsx, index.js            # Main application files
│   └── tailwind.config.js, etc.     # Styling
├── my-recommender-backend/
│   ├── app.py                       # Flask server
│   ├── model.py                     # ML model training
│   ├── recommender.py               # Recommendation logic
│   └── requirements.txt             # Python dependencies
└── README.md
```

---

## 🧪 Installation and Setup

### Backend (Flask)

```bash
cd my-recommender-backend
python -m venv venv
source venv/bin/activate          # Use venv\Scripts\activate for Windows
pip install -r requirements.txt
python app.py                     # Run server on http://localhost:5000
```

### Frontend (React)

```bash
cd my-recommender-frontend
npm install
npm start                         # Launches app on http://localhost:3000
```

---

##  API Endpoints

| Method | Endpoint                  | Description                      |
| ------ | ------------------------- | -------------------------------- |
| GET    | `/recommend?user_id=<id>` | Fetch recommendations for a user |
| GET    | `/forecast_stock`         | Retrieve 7-day demand forecast   |

---

##  Future Enhancements

* Integration with authentication systems (login/register).
* Migration to a cloud-hosted database (MongoDB, PostgreSQL).
* Continuous feedback-based model re-training.
* Deployment to cloud platforms like Heroku, Vercel, or Render.

---





