# capstone-project-9900w18c777
Getting this project to work locally requires two terminals: one for backend and one for the frontend.

# Backend
Open a terminal and navigate to `COMP9900` directory. Then run the following commands in order:
```
cd backend
virtualenv -p python3 env
source env/bin/activate
pip3 install --no-cache-dir -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
This final command starts the server.

# Frontend
Open another terminal and navigate to `COMP9900` directory. Then run the following commands:
```
cd frontend
npm install
npm run dev
```
The command should show a url. Go to this url in your browser to use the app.
