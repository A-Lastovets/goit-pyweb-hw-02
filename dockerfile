FROM python:3.12.2-bookworm

WORKDIR /assistant
COPY . .

RUN pip install -r requirements.txt
RUN pip install pipenv
RUN pipenv install

EXPOSE 6000

ENTRYPOINT ["pipenv", "run", "python", "main.py"]
