FROM hdgigante/python-opencv:4.8.1-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY . /ains/

WORKDIR /ains/ains_devenv
RUN pip install --no-cache-dir --upgrade -r requirements-devenv.txt

WORKDIR /ains/map_storage
CMD ["uvicorn", "hub_api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]