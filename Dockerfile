FROM python:3.12-slim

# Set environment variables
ENV LANG='ru_RU.UTF-8' \
    LANGUAGE='ru_RU:ru' \
    LC_ALL='ru_RU.UTF-8' \
    LC_MESSAGES='en_US.UTF-8' \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Europe/Moscow

# Install system dependencies, configure locales and timezone in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    locales \
    tzdata && \
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && \
    echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen en_US.UTF-8 ru_RU.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .