
# 🌱 Gamification of Sustainability  
*ECM2434 – Group Software Engineering Project @ University of Exeter*

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Django](https://img.shields.io/badge/Framework-Django-092E20?logo=django)](https://www.djangoproject.com/)
[![Live Site](https://img.shields.io/badge/View%20Live-%F0%9F%9A%80-blue)](https://whniecm2434.pythonanywhere.com/)

---

## 🎯 Project Overview

This full-stack web platform promotes **environmental sustainability** by gamifying real-world actions. Users complete eco-friendly challenges, earn rewards, and track their impact — all within an engaging and educational digital environment.

Developed as part of the ECM2434 module at the University of Exeter, this project was built using Agile Kanban methodology in a 7-person development team.

---

## 🔗 Live Demo

👉 [**Visit the deployed site**](https://whniecm2434.pythonanywhere.com/)  
*(Best viewed on desktop)*

---

## 👥 Team Members

- Ethan Sweeney  
- **Lewis Farley**  
- Sam Gates  
- Theo Armes  
- Johnny Say  
- Chris Lynch  
- Charlie Shortman

---

## 🧱 Tech Stack

- **Backend:** Django, SQLite3  
- **Frontend:** HTML, CSS, JavaScript  
- **Tools:** Git, GitHub, PythonAnywhere  

---

## 🧩 Project Features

- 📍 Location-based challenges with QR code verification  
- 🎯 Gamified reward system (eco-points, gardens and leaderboards)  
- 🧠 Educational content to promote sustainable habits
- 🎮 Daily sustainability challenges
- 👥 Gamekeeper panel for administrative control and moderation  
- 📊 User dashboard with progress tracking and statistics  

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/eco-world.git
   cd eco-world
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   - On Windows:
     ```bash
     setup_windows.bat
     ```
   - On macOS/Linux:
     ```bash
     ./setup_mac_linux.sh
     ```
   - Or manually:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     python manage.py loaddata initialDb.json
     ```

4. **Create a superuser account (for Gamekeeper panel):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

> ⚠️ Some configuration variables are stored in `ECM2434/settings.py`.

---

## 🧪 Running Tests

To run tests locally:

- **Windows:**
  ```bash
  test_windows.bat
  ```
- **macOS/Linux:**
  ```bash
  ./test_mac_linux.sh
  ```

---

## 🔐 Privacy Policy

This project uses a privacy policy template from  
🔗 [https://app.privacypolicies.com/wizard/privacy-policy](https://app.privacypolicies.com/wizard/privacy-policy)

---

## 📄 License

This project is licensed under the MIT License.

```
MIT License

© 2025 Ethan Sweeney, Lewis Farley, Sam Gates, Theo Armes, Johnny Say, Chris Lynch, Charlie Shortman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙌 Acknowledgments

Special thanks to the University of Exeter faculty for their guidance and support throughout the ECM2434 module.
