# DataMind-AI

### AI-Powered Customer Intelligence & Personalized Product Recommendation System

DataMind-AI is an end-to-end machine learning application that analyzes customer purchasing behavior, performs RFM-based customer segmentation, groups customers using K-Means clustering, and generates personalized product recommendations.

The project combines **Python, Pandas, Scikit-learn, PostgreSQL, FastAPI, HTML, CSS and JavaScript** into a complete data-to-application pipeline.
---

## 🌐 Live Demo

**DataMind-AI is live and accessible online:**

👉 https://datamind-ai-47y1.onrender.com/

### Live API

- Health Check: https://datamind-ai-47y1.onrender.com/health
- Recommendations: https://datamind-ai-47y1.onrender.com/recommendations/1489
- Customer Insights: https://datamind-ai-47y1.onrender.com/customer/1489/insights
- Swagger API Docs: https://datamind-ai-47y1.onrender.com/docs

---

## 🚀 Project Overview

Modern e-commerce platforms generate large amounts of customer and transaction data, but raw transaction data alone does not directly reveal:

- Which customers are highly valuable?
- Which customers may need re-engagement?
- Which customer groups behave similarly?
- Which products should be recommended to each customer?

DataMind-AI addresses these questions through customer behavioral analysis and a personalized recommendation engine.

---

## 🎯 Business Problem

E-commerce businesses need to understand customer behavior and deliver relevant products instead of treating every customer the same.

DataMind-AI converts transactional data into actionable customer intelligence by combining:

**Transaction Data → RFM Analysis → Customer Segmentation → Behavioral Clustering → Product Recommendations → API → Interactive Dashboard**

---

## 🧠 Machine Learning Pipeline

```text
Raw Customer & Transaction Data
             │
             ▼
      Data Generation
             │
             ▼
     PostgreSQL Database
             │
             ▼
     Customer Feature Engineering
             │
             ▼
        RFM Analysis
     ┌───────┼────────┐
     │       │        │
 Recency  Frequency  Monetary
     │       │        │
     └───────┼────────┘
             ▼
      Customer Segmentation
             │
             ▼
       Feature Scaling
             │
             ▼
      K-Means Clustering
             │
             ▼
   Personalized Recommendation
             │
             ▼
          FastAPI
             │
             ▼
       DataMind Dashboard

## 📊 RFM Analysis

RFM analysis is used to understand customer purchasing behavior through three dimensions:

### Recency
How recently the customer made a purchase.

### Frequency
How frequently the customer places orders.

### Monetary
How much the customer has spent.

Each customer receives:

- `R_score`
- `F_score`
- `M_score`
- `RFM_score`

These scores are used to create behavioral customer segments.

Example segments include:

- Champions
- Loyal Customers
- Potential Loyalists
- New Customers
- At Risk
- At Risk High Value
- Lost Customers

---

## 🤖 Customer Segmentation

DataMind-AI uses **K-Means clustering** to identify groups of customers with similar behavioral characteristics.

The clustering workflow includes:

1. Customer feature preparation
2. Feature scaling
3. Testing different cluster counts
4. Silhouette score evaluation
5. Selection of the tested cluster count with the highest silhouette score
6. Final K-Means clustering
7. Customer cluster assignment

### Current Generated Dataset

The tested clustering configuration selected **2 clusters** based on the highest silhouette score among the evaluated values.

| Cluster | Avg. Recency (Days) | Avg. Orders | Avg. Spend |
|--------:|--------------------:|------------:|-----------:|
| 0 | 119.30 | 4.27 | ₹142,889.38 |
| 1 | 287.47 | 1.88 | ₹49,911.91 |

---

## 🛍️ Personalized Recommendation Engine

The recommendation engine combines multiple behavioral signals to rank products for each customer.

### Recommendation Signals

- Customer category preferences
- Customer behavioral cluster
- Product popularity
- Purchase history

Each recommendation contains:

- Product ID
- Product name
- Category
- Price
- Recommendation score
- Rank
- Customer cluster

The system produces a ranked list of personalized products for each customer.

---

## ⚡ FastAPI Backend

FastAPI exposes the recommendation system through REST API endpoints.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "recommendations_loaded": true
}
```

### Customer Recommendations

```http
GET /recommendations/{customer_id}
```

Example:

```http
GET /recommendations/1489
```

### Customer Insights

```http
GET /customer/{customer_id}/insights
```

Example:

```http
GET /customer/1489/insights
```

### Available Customers

```http
GET /customers
```

### API Documentation

FastAPI automatically provides interactive Swagger documentation at:

```text
/docs
```

---

## 💻 Interactive Dashboard

The DataMind-AI dashboard provides an interactive customer intelligence experience.

### Customer Profile

Displays:

- Customer ID
- Customer cluster
- Total orders
- Total spent
- Recency
- Customer segment

### RFM Intelligence

Displays:

- Recency score
- Frequency score
- Monetary score
- Overall RFM score

### Recommendation Engine

Displays:

- Recommendation logic
- Product category
- Product name
- Product price
- Recommendation score
- Recommendation rank

The interface uses a modern dark AI-inspired design with gradient accents, glass-style cards, responsive layouts and interactive states.

---

## 🧠 DataMind Insight

The dashboard generates a customer-specific intelligence summary using the customer's actual behavioral and RFM data.

For example, customer `1489` is presented with:

- Customer ID: `1489`
- Cluster: `0`
- Total Orders: `3`
- Total Spent: `₹197,128.71`
- Recency: `194 days`
- RFM Score: `11/15`
- Customer Segment: `Potential Loyalists`

The dashboard combines these signals with the recommendation engine to provide a more transparent view of how personalized recommendations are generated.

---

## 📈 Example Customer

For customer `1489`, the application currently returns:

```text
Customer ID       1489
Cluster           0
Total Orders      3
Total Spent       ₹197,128.71
Recency           194 days
Customer Segment  Potential Loyalists
RFM Score         11 / 15
```

Example recommendations include:

```text
1. Formal Shirt 161
2. Jeans 40
3. Hoodie 171
4. Formal Shirt 25
5. Jacket 132
```

---

## 🗂️ Project Structure

```text
DataMind-AI/
│
├── api/
│   └── main.py
│
├── data/
│   ├── customers.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   ├── generate_data.py
│   ├── load_to_postgres.py
│   ├── customer_features.py
│   ├── rfm_features.py
│   ├── customer_clustering.py
│   ├── product_recommender.py
│   ├── customer_features.csv
│   ├── customer_rfm.csv
│   ├── customer_clusters.csv
│   └── product_recommendations.csv
│
├── frontend/
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   │
│   └── templates/
│       └── index.html
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

### Programming

- Python
- SQL
- HTML
- CSS
- JavaScript

### Data Science & Machine Learning

- Pandas
- NumPy
- Scikit-learn
- K-Means Clustering
- Feature Scaling
- Silhouette Analysis
- RFM Analysis

### Database

- PostgreSQL
- SQLAlchemy
- Psycopg2

### Backend

- FastAPI
- Uvicorn

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript

---

## ⚙️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/siddharthgupta-afk/DataMind-AI.git
cd DataMind-AI
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a local `.env` file:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=datamind
```

Do not commit `.env` to GitHub.

### 5. Start PostgreSQL

Make sure PostgreSQL is running and the `datamind` database is available.

### 6. Start the FastAPI Application

```powershell
uvicorn api.main:app --reload
```

Open the dashboard:

```text
http://127.0.0.1:8000/
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Testing

The application was tested for:

- Valid customer IDs
- Multiple customer IDs
- Invalid customer IDs
- Empty customer input
- Negative customer IDs
- API unavailable state
- API recovery after restart

---

## 🔐 Security

Sensitive and development-only files are excluded using `.gitignore`.

Examples:

```text
.env
.venv/
.venv-*/
__pycache__/
.vscode/
*.pyc
```

---

## 🔮 Future Improvements

Potential future improvements include:

- Product image integration
- Customer behavior visualizations
- Recommendation history
- Recommendation feedback tracking
- Collaborative filtering
- Hybrid recommendation models
- Model monitoring
- Cloud database integration
- Docker deployment
- Authentication and role-based access

---

## 👨‍💻 Author

**Siddharth Gupta**

Data Analyst | Python • SQL • Power BI

GitHub:  
https://github.com/siddharthgupta-afk

Portfolio:  
https://siddharth-data-ai.vercel.app/

---

## ⭐ Project Summary

DataMind-AI demonstrates an end-to-end approach to transforming raw transactional data into:

**Customer Intelligence + Behavioral Segmentation + Personalized Recommendations + FastAPI + Interactive Dashboard**