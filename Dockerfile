FROM nvidia/cuda:11.8.0-base-ubuntu22.04
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends gcc g++ make git python3 python3-dev python3-pip python3-venv python3-wheel espeak-ng libsndfile1-dev && rm -rf /var/lib/apt/lists/*
RUN pip3 install llvmlite --ignore-installed


# Install Dependencies:
RUN pip3 install torch torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
RUN rm -rf /root/.cache/pip

RUN git clone https://github.com/coqui-ai/TTS

#Install, specify extras here - could also do make install
RUN pip3 install -e TTS/. 

RUN rm -rf TTS

WORKDIR /api

COPY requirements.txt /api/
RUN pip install -r requirements.txt

COPY setup.py /api/setup.py
COPY setup.cfg /api/setup.cfg
COPY versioneer.py /api/versioneer.py
COPY pyproject.toml /api/pyproject.toml
COPY README.md /api/README.md
COPY src /api/src

RUN pip3 install .

EXPOSE 5000
ENTRYPOINT [ "python3 src/scribe/__main__.py" ]
