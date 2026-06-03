# Inventory & Order Management System

## 🚀 Project Overview
A full-stack Inventory & Order Management System built using FastAPI, React (Vite), PostgreSQL, and Docker. It manages products, customers, and orders with real-time inventory tracking.

---

## 🛠️ Tech Stack
- Backend: FastAPI (Python)
- Frontend: React (Vite)
- Database: PostgreSQL
- Deployment: Render (Backend), Vercel (Frontend)
- Containerization: Docker

---

## 🌐 Live Links

### Frontend
https://inventory-order-management-gray.vercel.app/

### Backend API
https://inventory-order-management-nhmh.onrender.com/

### Docker Image
https://hub.docker.com/r/sonupravin/inventory-backend

---

## 📦 Features

- Add / View Products
- Add / View Customers
- Create Orders
- Inventory Stock Management
- Automatic stock reduction on order
- Prevent order if stock is insufficient
- Unique SKU validation
- Unique email validation

---

## 📡 API Endpoints

- GET /products
- POST /products
- GET /customers
- POST /customers
- GET /orders
- POST /orders

---

## ⚙️ Setup Instructions

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload