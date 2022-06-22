FROM python:3.10
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python3 server.py
CMD [ "python3", "spreadsheet_script.py" ]