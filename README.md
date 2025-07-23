Setup:
1. Declare virtual env (if needed)
```python -m venv venv```
3. Start virtual env
4. 
```.\\venv\\Scripts\\activate```
5. or 1. Instal requirements (to the virtual env if it is activated)
6. 
```pip install -r requirements.txt```


start virtual env:

```.\\venv\\Scripts\\activate```


Start frontend:
1. python -m http.server 5500


Start backend:
1. uvicorn backend.main:app --reload
- v adresáři projektu, nemusí být v ./backend/

Navigate to:

```http://localhost:5500/```
