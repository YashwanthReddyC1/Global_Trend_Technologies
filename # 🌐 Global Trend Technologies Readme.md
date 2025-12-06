# 🌐 Global Trend Technologies

## **API Integration **

A fully featured Python-based CLI application designed to simplify API data exploration and demonstrate how real-world systems efficiently fetch, filter, and manage external data sources demonstrating **enterprise‑grade API integration**, **data caching**, **robust error handling**, and **interactive data exploration** using the official JSONPlaceholder API.

This assignment showcases production‑level design principles, clean architecture, and a user‑focused command‑line experience.

---

Before diving into the technical breakdown, the following overview provides a high-level understanding of what the application delivers and how it brings together multiple components to create a seamless API‑driven workflow.

# 🚀 Overview

This application integrates with the public JSONPlaceholder REST API to retrieve Posts, Users, Comments, and related resources. It provides:

### ✔ Real API Integration

### ✔ Intelligent Caching (Memory + Persistent File Storage)

### ✔ Interactive Filtering & Search

### ✔ Centralized Error Management

### ✔ Professional CLI UX Design

### ✔ Auto‑dependency installation

Built as part of the **Global Trend Technologies  Program**, it demonstrates backend integration fundamentals and software craftsmanship.

---

# 📦 Features

## ⚡ Performance

### 🔹 **Advanced API Client**

* Uses `requests.Session` for efficient HTTP communication.
* Graceful handling of timeouts, connection issues, and malformed responses.
* Clear user-facing status messages.

### 🔹 **Caching System (Memory + File)**

* Reduces API load and speeds up the application.
* Automatic TTL expiration system.
* Persistent `global_trend_cache.json` created on first run.

## 🎛 User Experience

### 🔹 **Smart Filtering Engine**

Supports filtering posts and users by:

* User ID
* Keyword (searching multiple fields)
* ID Range (min–max)

### 🔹 **Professional CLI Design**

* Clean, structured menu system.
* Color-friendly output.
* Pagination-aware summaries.
* Helpful prompts and validation.

## 🛡 Reliability

### 🔹 **Comprehensive Error Handling**

Handles:

* Network failures

* Timeouts

* Invalid input

* Missing data

* HTTP errors

* JSON parsing issues
  **Advanced API Client**

* Uses `requests.Session` for efficient HTTP communication.

* Graceful handling of timeouts, connection issues, and malformed responses.

* Clear user-facing status messages.

### 🔹 **Caching System (Memory + File)**

* Reduces API load and speeds up the application.
* Automatic TTL expiration system.
* Persistent `global_trend_cache.json` created on first run.

### 🔹 **Smart Filtering Engine**

Supports filtering posts and users by:

* User ID
* Keyword (searching multiple fields)
* ID Range (min–max)

### 🔹 **Professional CLI Design**

* Clean, structured menu system.
* Color‑friendly output.
* Pagination‑aware summaries.
* Helpful prompts and validation.

### 🔹 **Comprehensive Error Handling**

Handles:

* Network failures
* Timeouts
* Invalid input
* Missing data
* HTTP errors
* JSON parsing issues

---

# 🛠 Installation & Setup

### **1. Clone the repository**

```bash
git clone <repository-url>
cd <project-folder>
```

### **2. (Optional) Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate        # Windows
```

### **3. Install requirements**

The script automatically installs `requests` if missing.
You may also install manually:

```bash
pip install requests
```

---

# ▶️ Running the Application

Execute:

```bash
python app.py
```

You will see a professional welcome interface, followed by the main menu:

```
1. List Posts
2. List Users
3. View Post Details
4. View User Details
5. Refresh Data
6. View Cache Information
7. Exit
```

---

# 🔍 Functional Highlights

## 1. **List Posts**

* Filter by user ID
* Filter by keyword
* Filter by ID range
* Display previews of up to 15 posts

## 2. **List Users**

* Search via name/username/email
* Filter by ID range

## 3. **View Post Details**

* Full content with author info
* Optionally load comments

## 4. **View User Details**

* Full user profile: address, company, and contact info
* Optionally list all user posts

## 5. **Refresh Data**

* Force‑fetch posts and/or users
* Immediately updates cache

## 6. **Cache Diagnostics**

Shows:

* Cache age
* Number of cached items
* File size
* TTL configuration

---

# 🧩 Architecture Breakdown

```
+--------------------+
|  User Interface    |
+--------------------+
           |
           v
+--------------------+
|    Application     |
+--------------------+
      /        \
     v          v
+---------+  +---------+
|  API    |  |  Cache  |
| Client  |  | Manager |
+---------+  +---------+

         v
+-----------------------+
|     Data Filters      |
+-----------------------+
```

### Modules

* **APIClient** → Handles all communication with JSONPlaceholder.
* **CacheManager** → Stores, loads, and validates cached data.
* **DataFilter** → Provides modular filtering utilities.
* **UserInterface** → All user input/output interactions.
* **Application** → Business logic orchestrator.

---

# 🧪 Error Handling System

Every error is processed through a centralized handler with descriptive icons and human‑friendly messages.

| Error Type      | Trigger Example    | User Message                  |
| --------------- | ------------------ | ----------------------------- |
| Network Failure | API unreachable    | "Cannot connect to API"       |
| Timeout         | Request >15s       | "Request took too long"       |
| HTTP Error      | 404/500            | "Server returned status X"    |
| JSON Error      | Corrupted response | "Invalid JSON format"         |
| Invalid Input   | Wrong ID value     | "Please enter a valid number" |
| Not Found       | Missing resource   | "Item doesn't exist"          |

---

# 🗃 Cache System Overview

### **Cache TTL:** 300 seconds (5 minutes)

### **Stores:**

* Posts
* Users
* Individual post lookups
* Individual user lookups

Cache file:

```
global_trend_cache.json
```

Automatically created and updated.

---

# 📈 Possible Enhancements

## 🧪 Testing & Code Quality

* Add unit testing with pytest
* Introduce automated CI workflows for testing and style checks

## ⚡ Performance & Architecture

* Implement SQLite-backed persistent caching
* Add asynchronous API requests for faster data loading
* Introduce configuration files for environment-based settings

## 🎨 UI/UX Improvements

* TUI (Rich/Textual) interface
* GUI implementation (Tkinter/PyQt)
* Enhanced color-themed CLI with better navigation cues

## 🔌 Feature Expansion

* Support for additional JSONPlaceholder endpoints (todos, albums, photos)
* Add search across all related resources (posts ↔ comments ↔ users)

---

# 📄 License

This project is provided for educational and professional demonstration purposes. Adapt as needed for internal Global Trend Technologies use.

---

# 📬 Contact

For questions or improvements, contact your HR or supervisor or project coordinator.

---

### ⭐ Thank You for Reviewing This!

A polished demonstration of backend API integration and Python CLI engineering.
