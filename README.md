# 🏖️ TravelHub

A modern web application for sharing and discovering resort experiences with images, ratings, and community features.

## 📹 Demo

<!-- Drag and drop your Introduction.mov file here when editing on GitHub -->
<!-- The video will be automatically embedded as a playable video -->
[Introduction_Video](Introduction.mov)
Need to Download

## 📷 Screenshots

### Home Page
![Home Page](project_pics/HomePage.png)

### Login Page
![Login Page](project_pics/Login.png)

### Personal Page
![Personal Page](project_pics/PersonalPage.png)

### Resort Detail (Without Login)
![Resort Detail Without Login](project_pics/ResortDetailWithoutLogin.png)
![Resort Detail Without Login 2](project_pics/ResortDetailWithoutLogin2.png)

### Resort Detail (With Login)
![Resort Detail With Login](project_pics/ResortDetailWithLogin.png)

## ✨ Features

### 🎯 Core Functionality
- **User Authentication**: Secure registration and login system
- **Resort Sharing**: Upload and share resort experiences with images
- **Community Features**: Vote, comment, and interact with other users' posts
- **User Profiles**: Personal dashboard showing your submitted resorts

### 🖼️ Media & Content
- **Image Upload**: Support for multiple image formats
- **Interactive Images**: Hover effects and clickable resort cards
- **Resort Details**: Comprehensive resort information pages

### 📊 Analytics & Statistics
- **Cost Tracking**: Track and display resort expenses
- **Recommendation System**: Rate resorts on a 1-10 scale
- **Community Stats**: View average costs and recommendations
- **Voting System**: Upvote/downvote resorts

### 🎨 User Experience
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Modern UI**: Clean, intuitive interface using Bootstrap
- **Real-time Updates**: Dynamic content loading and updates

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- MySQL 5.7+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/TravelHub.git
   cd TravelHub
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**
   ```sql
   CREATE DATABASE travelhub;
   ```

5. **Configure database connection**
   
   Edit `app.py` and update the database URI:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/travelhub'
   ```
   Replace `username` and `password` with your MySQL credentials.

6. **Create required directories**
   ```bash
   mkdir -p static/pics
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the application**
   
   Open your browser and navigate to: `http://localhost:5000`

## 👤 Default Admin Account

After first run, you can log in with:
- **Username**: `admin`
- **Password**: `123`

## 📁 Project Structure

```
TravelHub/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   └── pics/             # Resort images storage
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── profile.html      # User profile
│   ├── add_resort.html   # Add resort form
│   └── resort_detail.html # Resort details page
└── venv/                 # Virtual environment
```

## 🛠️ Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **File Handling**: Flask file uploads
- **Authentication**: Flask-Login

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:
- Create an issue on GitHub
- Check the existing issues for solutions
- Review the setup instructions above

---

**Happy Traveling! 🌴✈️** 