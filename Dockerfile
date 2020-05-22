# Install dependencies
FROM python:3-slim AS build
WORKDIR /app
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install --user pipenv
RUN /root/.local/bin/pipenv install --system

# Copy application
COPY server.py .

# Build production image
FROM gcr.io/distroless/python3-debian10
COPY --from=build /usr/local/lib/python3.8/site-packages /app/site-packages
COPY --from=build /app /app
WORKDIR /app
ENV PYTHONPATH /app/site-packages
CMD ["server.py"]
