# TicTacToe game with AIs
- On Windows use Powershell
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
4. Create .env file with OpenAI API key (or other LLM API key - then change models in backend/)
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

## Image
<img width="1895" height="953" alt="Image" src="https://github.com/user-attachments/assets/c91430d6-2d01-4c23-bd42-0f4bee332b6c" />
