FROM prefecthq/prefect:2-python3.10

ARG CODE_PATH

COPY ${CODE_PATH}/* /opt/prefect/flows/

RUN pip install prefect
RUN pip install -r requirements.txt