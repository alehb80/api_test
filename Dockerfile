FROM python:3.9
ADD . /test_tecnico
ADD requirements.lock /
RUN pip install --upgrade -r /requirements.lock
ENV PYTHONPATH=$PYTHONPATH:/test_tecnico
WORKDIR /test_tecnico/backend/services
EXPOSE 8000
CMD python services.py