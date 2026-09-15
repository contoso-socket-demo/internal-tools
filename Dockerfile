# Reporting box image. Deliberately behind, so the container scanner has real
# OS-package CVEs to report rather than a clean image.
#
# python:3.9.7-slim-bullseye is from Sept 2021 and carries a large number of
# OS-level CVEs on its own. That is the point.
#
# Do NOT add `apt-get update && apt-get install` here. Debian bullseye is
# EOL, so security.debian.org 404s on the package versions in this image's
# stale apt index and the build fails with exit 100. The base layers already
# supply more than enough for the container scan.
FROM python:3.9.7-slim-bullseye

# Runs as root: no USER directive anywhere in this file.
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 8081
CMD ["python", "-m", "reporting.dashboard"]
