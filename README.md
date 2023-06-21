# capstone-project-9900w18c777
# How this project was initialised
```
mkdir backend && cd backend
python3 -m venv .venv
touch requirements.txt
echo "fastapi==0.70.0
uvicorn==0.15.0
PyJWT==1.7.1
python-decouple==3.3
numpy==1.24.3
scikit-learn==1.2.2
pandas==2.0.2
jwt==1.3.1
python-decouple==3.8
python-jose==3.3.0" >> requirements.txt
touch .env 
touch main.py
cd .. 
echo backend/.venv/ >> .gitignore
npm create vite@latest
cd frontend
npm install axios bootstrap react-router-dom
```

# Setup Frontend from package root
```
cd frontend
npm start
```

## To format files
npm run format

## From project root, activate python virtual environment and install requirements
```
cd backend
source .venv/bin/activate
pip3 install -r requirements.txt 
uvicorn main:app --reload
```

# Docker Container for backend
```
cd frontend && touch Dockerfile && touch .dockerignore
touch Dockerfile
```

# Docker Container for backend
```
cd backend && touch Dockerfile && touch .dockerignore
```
