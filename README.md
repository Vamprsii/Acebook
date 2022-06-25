# Acebook
,
git clone 
cd Acebook
python -m venv env   #create a virtual environment
.\env\Scripts\activate  #activate your virtual environment
cd backend
pip install -r .\requirements.txt
uvicorn main:app --reload     #start server
visit  127.0.0.1:8000/
