# Gamification Of Sustainability

## ECM2434 - Group Software Engineering Project - University Of Exeter

### Project Overview
This project focuses on the development of a gamified platform aimed at 
promoting sustainable behaviors. The goal is to engage users through 
interactive challenges, rewards, and  educational content that fosters
awareness and actionable steps towards environmental sustainability.

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
   - Windows: Run `setup.bat`
   - macOS/Linux: Run `./setup.sh`

   Or manually run the following commands:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py loaddata initialDb.json
   ```
3. Run the django server ```python manage.py runserver```


### 

### License