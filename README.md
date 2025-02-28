# CeraMD - Medical Transcription Application

CeraMD is a modern web application designed to assist medical professionals with transcription services. The application features a React-based frontend for audio recording and a FastAPI backend for processing and managing transcriptions.

## 🌟 Features

- Audio recording and transcription
- Real-time audio processing 
- Secure data storage
- Modern, responsive UI
- Dockerized deployment
- RESTful API endpoints

## LLMs Used 
- "writer/palmyra-med-70b" for SOAP note generation and differential diagnosis.
- "meta-llama/llama-3-8b-instruct" for transcript processing.

## 🚀 Live Demo

- Frontend Application: [https://cera-md-zeta.vercel.app/](#)
- API Base URL: [https://ceramd-1.onrender.com](#)

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- TypeScript
- Tailwind CSS

### Backend
- FastAPI (Python)
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

### 2. Running with Docker (Recommended)
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

### 3. Manual Setup (Alternative)

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

### Transcription
- speech to text transcription is directly achieved using Deepgram API with React.
- `POST /api/process-transcript`: Transcribed audio processed and diaterized
- `POST /api/generate-soap`: Generate Soap Note
- `POST /api/generate-differential-diagnosis`: Get a differntial diagnosis

For detailed API documentation, visit http://localhost:8000/docs when the backend is running.

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

## 👥 Contact

Rehan Ali - [GitHub](https://github.com/RehanAli7024)

Project Link: [https://github.com/RehanAli7024/CeraMD](https://github.com/RehanAli7024/CeraMD)
