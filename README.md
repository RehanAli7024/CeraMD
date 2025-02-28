# CeraMD - Medical Transcription Application

CeraMD is a modern web application designed to assist medical professionals with transcription services. The application features a React-based frontend for audio recording and a FastAPI backend for processing and managing transcriptions.

## 🌟 Features

- Audio recording and transcription
- Real-time audio processing
- Secure data storage
- Modern, responsive UI
- Dockerized deployment
- RESTful API endpoints

## 🚀 Live Demo

- Frontend Application: [Coming Soon](#)
- API Documentation: [Coming Soon](#) (Swagger UI)
- API Base URL: [Coming Soon](#)

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- TypeScript
- Tailwind CSS

### Backend
- FastAPI (Python)
- SQLAlchemy
- PostgreSQL
- Docker

## 📋 Prerequisites

Before running the application, make sure you have the following installed:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/downloads)

## 🔧 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/RehanAli7024/CeraMD.git
cd CeraMD
```

### 2. Environment Variables
Create `.env` files in both backend and frontend directories:

Backend `.env`:
```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

Frontend `.env`:
```env
VITE_API_URL=http://localhost:8000
```

### 3. Running with Docker (Recommended)
```bash
# Build and start all services
docker compose up --build

# Stop services
docker compose down
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 4. Manual Setup (Alternative)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd project
npm install
npm run dev
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login`: User login
- `POST /api/auth/register`: User registration

### Transcription
- `POST /api/transcribe`: Upload audio for transcription
- `GET /api/transcriptions`: Get all transcriptions
- `GET /api/transcriptions/{id}`: Get specific transcription

For detailed API documentation, visit http://localhost:8000/docs when the backend is running.

## 🧪 Testing

### API Testing with Curl

1. Test the health check endpoint:
```bash
curl http://localhost:8000/health
```

2. Upload an audio file:
```bash
curl -X POST http://localhost:8000/api/transcribe \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.mp3"
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd project
npm test
```

## 📦 Deployment

The application is containerized using Docker, making it easy to deploy to any cloud platform that supports Docker containers.

### Build Images
```bash
docker compose build
```

### Push to Registry
```bash
docker compose push
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contact

Rehan Ali - [GitHub](https://github.com/RehanAli7024)

Project Link: [https://github.com/RehanAli7024/CeraMD](https://github.com/RehanAli7024/CeraMD)
