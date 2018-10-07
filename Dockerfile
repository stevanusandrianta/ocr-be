from continuumio/miniconda3

COPY requirements.txt /

RUN apt-get update -y
RUN apt-get install -y git
RUN apt-get install -y libgl1-mesa-glx

RUN conda install -c conda-forge opencv

RUN pip install -r /requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \

# copy project module
RUN mkdir /app/
COPY /app/ /app/app/

# copy configs
COPY gunicorn.config.py /app/

# copy project web-app
COPY run.py /app/

EXPOSE 8080
WORKDIR /app/

# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.
ENTRYPOINT ["gunicorn", "-c", "gunicorn.config.py", "run:APP", "--preload"]
