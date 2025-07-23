Setup:
1. Declare virtual env (if needed)
python -m venv venv
2. Start virtual env
.\\venv\\Scripts\\activate
1. or 3. Instal requirements (to the virtual env if it is activated)
pip install -r requirements.txt


start virtual env:
.\\venv\\Scripts\\activate


start frontend:

1. cd ./frontend/
2. python -m http.server 5500



start backend:

1. uvicorn backend.main:app --reload

(v adresáři projektu, nemusí být v ./backend/)

