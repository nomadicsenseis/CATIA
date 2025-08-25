FROM continuumio/miniconda3:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements if they exist
COPY requirements.txt* ./

# Install Python dependencies
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Install additional packages that might be needed
RUN conda install -c conda-forge -y \
    pandas \
    numpy \
    matplotlib \
    scikit-learn \
    jupyter \
    && conda clean -afy

# Set the default command
CMD ["/bin/bash"]

