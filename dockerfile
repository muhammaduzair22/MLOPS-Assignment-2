FROM apache/airflow:2.5.1

USER root

# Install NLTK dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    python3-nltk && \
    rm -rf /var/lib/apt/lists/*

USER airflow

# Install NLTK and download required packages
RUN python3 -m pip install --no-cache-dir nltk && \
    python3 -m nltk.downloader all
