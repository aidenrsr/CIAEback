# CIAE Backend Service

This repository contains the backend service for the CIAE project application. It is a lightweight Flask app designed to manage API endpoints for the React-based frontend.

## Project Links
- **Application Website**: [ciaeproject.com](https://ciaeproject.com)
- **GitHub Repository**: [github.com/aidenrsr/CIAEback](https://github.com/aidenrsr/CIAEback)

## Features
- **API Management**: Provides RESTful API endpoints to support frontend functionality.
- **Database**: Integrated with PostgreSQL
- **Deployment**: Uses Docker for containerization and is deployed via Google Cloud Platform (GCP).

## Getting Started

### Prerequisites
- **Python**: Version 3.8 or higher
- **PostgreSQL**: Installed and running
- **Docker**: Installed and configured
- **Google Cloud SDK**: For deployment on GCP

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aidenrsr/CIAEback.git
   cd CIAEback
   ```

2. Create a virtual environment and activate it:
   ```bash
   pip install pipenv
   pipenv shell
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
   ```

5. Run database migrations:
   ```bash
   flask db upgrade
   ```

6. Start the development server:
   ```bash
   flask run
   ```

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t ciae-backend .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:808
   ```


## Contributing

Contributions are welcome! Please follow the steps below to contribute:

1. Fork the repository and create a feature branch.
2. Commit your changes with clear messages.
3. Open a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
