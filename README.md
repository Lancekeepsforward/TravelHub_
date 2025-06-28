# TravelHub

A simple web application for sharing resort experiences.

## Setup Instructions

1. Create a MySQL database named `travelhub`

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Update the database configuration in `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/travelhub'
```
Replace `username` and `password` with your MySQL credentials.

4. Create a folder for resort images:
```bash
mkdir static/resort_images
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Features

- User registration and login
- View resorts on the homepage
- User profiles with submitted resorts
- Resort cards with hover effects
- Responsive design using Bootstrap 