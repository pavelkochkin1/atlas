FROM python:3.11-slim

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY /backend/requirements /backend/requirements

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements/prod.txt

COPY ./backend /backend
COPY ./backend/.env /backend/.env

EXPOSE 80

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8073"]
