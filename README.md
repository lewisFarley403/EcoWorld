# Gamification Of Sustainability

## ECM2434 - Group Software Engineering Project - University Of Exeter

### Project Overview
This project focuses on the development of a gamified platform aimed at 
promoting sustainable behaviors. The goal is to engage users through 
interactive challenges, rewards, and  educational content that fosters
awareness and actionable steps towards environmental sustainability.

### Link to the deployed website
**https://whniecm2434.pythonanywhere.com/**

### Team Members
- Ethan Sweeney
- Lewis Farley
- Sam Gates
- Theo Armes
- Johnny Say
- Chris lynch
- Charlie Shortman

### Project Structure

### Technologies Used
- Django
- HTML
- CSS
- JavaScript
- sqlite3

### Installation and Setup

1. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Set up the database by running the appropriate script for your system:
   - Windows: Run `setup_windows.bat`
   - macOS/Linux: Run `./setup_mac_linux.sh`

   Or manually run the following commands:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py loaddata initialDb.json
   ```
   
3. Next, create a superuser account to access the gamekeeper panel for the first time:
   ```sh
   python manage.py createsuperuser
   ```

4. Run the django server ```python manage.py runserver```

### How to test
1. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Run the following command:
- On windows, run: `test_windows.bat`
- On macOS/Linux, run: `./test_mac_linux.sh`

### Privacy Policy
Template from https://app.privacypolicies.com/wizard/privacy-policy

### License
MIT License

Copyright (c) [2025] [Ethan Sweeney, Lewis Farley, Sam Gates, Theo Armes, Johnny Say, Chris lynch, Charlie Shortman]

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
