# Blog-pedia

Blog-pedia is a comprehensive blogging platform built with Flask, SQLAlchemy, and Bootstrap 5. It provides a feature-rich environment for content creation, user interaction, and content discovery through categories and tags. The platform offers secure authentication, user profiles, and an intuitive interface for both readers and writers.

## Features

### User Management
- User registration and authentication
- Customizable user profiles with bio
- Profile statistics tracking
- Gravatar integration for profile pictures
- Admin privileges for content moderation

### Content Management
- Create, Read, Update, and Delete (CRUD) operations for blog posts
- Rich text editing with CKEditor
- Category system for content organization
- Tagging functionality for flexible categorization
- Image URL support in posts

### Search and Discovery
- Advanced search functionality across multiple fields:
  - Post titles and subtitles
  - Content body
  - Tags and categories
  - Author names
- Category-based navigation
- Tag-based filtering

### Interaction
- Commenting system on blog posts
- User comment history
- Profile-based content discovery
- Contact form for user inquiries

## Getting Started

1. Clone this repository:
```bash
git clone https://github.com/pushkqr/blog-pedia.git
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables in a .env file:
```bash
EMAIL_USER = "site_owner@gmail.com"
EMAIL_PASSWORD = "your_email_password"
FLASK_KEY = "a_secret_string"
DB_URI = "db_url"
```

4. Run the Flask application:
```bash
python main.py
```

5. Access the application in your web browser at http://localhost:5000

## Usage

### For Bloggers
- Register and customize your profile
- Create and manage blog posts
- Organize content with categories and tags
- Track engagement through comments

### For Readers
- Browse posts by categories and tags
- Use advanced search to find specific content
- Engage through comments
- View author profiles

### For Administrators
- Manage user content
- Moderate comments
- Handle contact form submissions
- Maintain platform quality

## Technologies Used
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, CKEditor
- **Backend**: Python (Flask framework)
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Authentication**: Flask-Login
- **Deployment**: Railway platform

## Credits
- Clean Blog Bootstrap Template by Start Bootstrap
- CKEditor for rich text editing
- Flask and its extensions community

## Contributing
Contributions are welcome! Please feel free to:
- Open issues for bug reports or feature requests
- Submit pull requests for improvements
- Suggest new features or enhancements
- Help with documentation

## Deployment
The application is currently deployed on Railway. Visit [Blog-pedia](https://blog-pedia.up.railway.app) to see it in action.
