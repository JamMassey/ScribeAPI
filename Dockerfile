ENV PYTHONUNBUFFERED=1

WORKDIR /api

COPY requirements.txt /api/
RUN pip install -r requirements.txt

COPY setup.py /api/setup.py
COPY setup.cfg /api/setup.cfg
COPY versioneer.py /api/versioneer.py
COPY pyproject.toml /api/pyproject.toml
COPY README.md /api/README.md
COPY src /api/src

RUN pip install .

EXPOSE 5000
ENTRYPOINT [ "python3 src/scribe/__main__.py" ]
