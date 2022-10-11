FROM python:3.9
ARG user
ARG password
ADD . /test_tecnico
ENV PYTHONPATH=$PYTHONPATH:/test_tecnico
WORKDIR /test_tecnico/backend/services
CMD python services.py