# 🚀 Social Media Aggregator

<div align="center">

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Aggregate and analyze data from GitHub and Reddit in one place.

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-endpoints)

</div>

---

## 📸 Demo

<div align="center">

<table>
  <tr>
    <td align="center">
      <strong>Home Page</strong><br><br>
      <a href="https://github.com/user-attachments/assets/59df991c-23d4-40e9-96cd-978eecc8bf4b">
        <img src="https://github.com/user-attachments/assets/59df991c-23d4-40e9-96cd-978eecc8bf4b" alt="Home Page" width="300">
      </a>
    </td>
    <td align="center">
      <strong>Analytics Output</strong><br><br>
      <a href="https://github.com/user-attachments/assets/31ae4ea9-8d88-4a31-8a51-ecab0c18e469">
        <img src="https://github.com/user-attachments/assets/31ae4ea9-8d88-4a31-8a51-ecab0c18e469" alt="Analytics Output" width="300">
      </a>
    </td>
  </tr>
</table>

<p><i>Click on the images to view full-size screenshots</i></p>

</div>

---


## ✨ Features

### 📊 GitHub Analytics
- 🔥 **Top 5 Issues by Comments**  
- 👤 **Author with Most Issues Across All Repos**  
- 📦 **Repo with the Most Open Issues**

### 🔴 Reddit Analytics
- ⬆️ **Top 5 Posts by Upvotes**  
- 👥 **Author with the Highest Total Upvotes Across Posts**  
- 📈 **Real-time Subreddit Analytics**

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Backend  | Python, Flask |
| APIs     | GitHub REST API, Reddit JSON API |
| Frontend | HTML, CSS, JavaScript |
| HTTP Client | requests |

---

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip

### Quick Setup

```bash
# Clone repository
git clone https://github.com/yourusername/social-media-aggregator.git
cd social-media-aggregator

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
