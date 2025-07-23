### Setup:
1. Declare virtual env (if needed)
```
python -m venv venv
```
3. Start virtual env
```
.\\venv\\Scripts\\activate
```
3. or 1. Instal requirements (to the virtual env if it is activated)
```
pip install -r requirements.txt
```


### Start virtual env:
```
.\\venv\\Scripts\\activate
```


### Start frontend:
```
python -m http.server 5500
```

### Start backend:
```
uvicorn backend.main:app --reload
```
- v adresáři projektu, nemusí být v ./backend/

### Navigate to:
```
http://localhost:5500/
```
