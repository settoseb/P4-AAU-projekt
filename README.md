<p align="center">
  <img src="AAU_logo.png">
</p>

# <span style="color:#211a52">AAU P4 - Secure Banking System</span>


This repository contains all the code for our P4 project.

## Development Environment Setup

Clone the repository:

```bash
git clone https://github.com/ViggoGaming/AAU-P4.git
```

### Frontend

1. Navigate to the frontend folder:

```bash
cd frontend-bank
```
*Remember to rename .env.example to .env inside of the frontend folder*

2. Install the necessary packages:

```bash
npm install
```

3. Start the frontend:

```bash
npm start
```

4. Access the frontend at:

[http://localhost:5173](http://localhost:5173)

### Backend

1. Navigate to the backend folder:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
source ./venv/bin/activate
```

4. Install the necessary packages in the virtual environment:

```bash
pip install -r requirements.txt
```

5. Start the backend:

```bash
fastapi dev main.py
```

6. Access the backend documentation at:

[http://localhost:8000/docs](http://localhost:8000/docs)

