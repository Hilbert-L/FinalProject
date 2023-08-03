# capstone-project-9900w18c777
Getting this project to work locally requires two terminals: one for backend and one for the frontend.

# Backend
Open a terminal and navigate to project root directory (`capstone-project-9900w18c777`). Then run the following commands in order:
```
cd backend
virtualenv -p python3 env
source env/bin/activate
pip3 install --no-cache-dir -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
This final command starts the server.

# Frontend
First we need to install the latest version of `node`. We will use `nvm` to do this. Open another terminal and run these commands:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
nvm install node
```
Close the terminal and reopen it to effect changes. Now navigate to project root directory (`capstone-project-9900w18c777`) and run the following commands in order:
```
cd frontend
npm install
npm run dev
```
This final command should show a url. Go to this url in your browser to start using the app.
