# Reporting box image. Deliberately behind, so the container scanner has
# real OS-package CVEs to report rather than a clean image.
FROM python:3.9.7-slim-bullseye

# Runs as root: no USER directive anywhere in this file.
WORKDIR /app

RUN apt-get update && apt-get install -y \
      curl \
      git \
      openssl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 8081
CMD ["python", "-m", "reporting.dashboard"]
