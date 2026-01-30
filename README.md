# TicTacToe game with AIs

### Setup:
1. Declare virtual env (if needed)
```
python -m venv venv
```
2. Start virtual env
```
.\\venv\\Scripts\\activate
```
3. or 1. Instal requirements (to the virtual env if it is activated)
```
pip install -r requirements.txt
```
4. Create .env file with OpenAI API key
```
OPENAI_API_KEY=sk-1234abcd
```

### Start virtual env:
```
.\\venv\\Scripts\\activate
```


### Start frontend:
```
python -m http.server 5500
```
- v adresáři ./frontend/

### Start backend:
```
uvicorn backend.main:app --reload
```
- v adresáři projektu, nemusí být v ./backend/

### Navigate to:
```
http://localhost:5500/
```
