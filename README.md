# blog-pedia

Blog-pedia is a simple blog web application built with Flask, SQLAlchemy, and Bootstrap. It allows users to register, log in and create, edit, and delete blog posts for admin only. Users can also leave comments on posts and contact the site owner through a contact form.

## Features

- User Registration and Authentication
- Create, Read, Update, and Delete (CRUD) Operations for Blog Posts
- Comments on Blog Posts
- Contact Form for User Inquiries
- Admin Panel with Exclusive Privileges

## Getting Started

1. Clone this repository:

```bash
git clone https://github.com/pushkqr/blog-pedia.git
```

2.Install the required dependencies:

```bash
pip install -r requirements.txt
```

3.Set up your email credentials in the main.py file:

```bash
EMAIL_USER = "site_owner@gmail.com"
EMAIL_PASSWORD = "your_email_password"
```

4.Run the Flask application:

```bash
python main.py
```

5.Access the application in your web browser at http://localhost:5000.

## Usage
- Register a new account or log in with existing credentials.
- Create new blog posts by navigating to the "New Post" page.
- View all existing posts on the homepage.
- Click on a post to view its details, leave comments, and edit or delete it if you're the author or an admin.
- Use the contact form to send inquiries to the site owner.

## Credits
This project is based on the Clean Blog Bootstrap Template by Start Bootstrap.

## Contributing

Contributions are welcome! Please open an issue or pull request for any improvements or bug fixes.
