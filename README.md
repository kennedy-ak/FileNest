# File Server

## Project Title: File Server

### Project Objective

Lizzy runs a business that distributes documents such as wedding cards, admission forms, etc., on behalf of various businesses to different users. To scale her business, Lizzy wants a digital platform where these documents can be easily accessed and downloaded remotely.

### Features

#### User Features:
1. **Signup & Login**: Users can sign up and log in with an email and password. Account verification is required.
2. **Password Reset**: Users can recover lost passwords.
3. **Feed Page**: Users can see a list of files available for download.
4. **File Search**: Users can search for specific files on the server.
5. **Email File**: Users can send a file to an email through the platform.

#### Admin Features:
1. **File Upload**: Admins can upload files with a title and description.
2. **Download & Email Statistics**: Admins can see the number of downloads and emails sent for each file.

### Technologies Used

- **Django**: Backend framework.

- **PostgreSQL**: Database.
- **Crispy Forms**: To style Django forms.

- **Whitenoise**: To serve static files.

### Requirements

- Python 3.x
- PostgreSQL

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/fileserver.git
    cd fileserver
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variables**:
    Create a `.env` file in the root directory and add the following environment variables:
    ```env
    DEBUG=True
    SECRET_KEY=your_secret_key
    DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
    EMAIL_HOST=smtp.example.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_email_password
    EMAIL_USE_TLS=True
    RECAPTCHA_PUBLIC_KEY=your_recaptcha_public_key
    RECAPTCHA_PRIVATE_KEY=your_recaptcha_private_key
    ```

5. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

### Usage

1. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:8000`.

2. **Admin Panel**:
    Go to `http://127.0.0.1:8000/admin` to access the Django admin panel. Log in with the superuser credentials created earlier.

3. **Uploading Files (Admin)**:
    - Log in to the admin panel.
    - Navigate to the file upload section.
    - Upload files with a title and description.

4. **User Interaction**:
    - Sign up or log in with an email and password.
    - Verify your account via the verification email.
    - Reset your password if needed.
    - Browse the feed page to see available files.
    - Search for files using the search feature.
    - Send files to an email through the platform.



### Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.


