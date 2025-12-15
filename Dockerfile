FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
# Fix permissions for libraries that write to home
RUN mkdir -p /tmp/home
ENV HOME=/tmp/home
# Start the FastAPI server on port 7860 (required by Hugging Face)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
