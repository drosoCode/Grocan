FROM python:3
WORKDIR /home/grocan
ADD requirements.txt requirements.txt
RUN \
  apt-get update && apt-get install -y ffmpeg \
  && pip install --no-cache-dir -r requirements.txt   

ADD grocan.py grocan.py
RUN chmod +x grocan.py

CMD ["./grocan.py"]