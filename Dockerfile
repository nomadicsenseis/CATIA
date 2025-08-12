FROM mcr.microsoft.com/devcontainers/anaconda:1-3

WORKDIR /app

# Install conda packages (scientific libraries)
RUN conda install -y \
    pandas>=2.2.0 \
    numpy>=1.26.0 \
    matplotlib>=3.8.0 \
    scikit-learn>=1.4.0 \
    jupyter>=1.0.0 \
    psycopg2>=2.9.9

# Install pip packages (other libraries)
RUN pip install --no-cache-dir \
    boto3>=1.34.0 \
    awscli>=1.32.0 \
    sqlalchemy>=2.0.0 \
    python-dotenv>=1.0.0 \
    langchain>=0.1.0 \
    langchain-community>=0.0.10 \
    langchain-aws>=0.0.1 \
    Pillow>=10.0.0 \
    requests>=2.28.0 \
    msal>=1.32.0 \
    aiohttp>=3.12.0 \
    beautifulsoup4>=4.13.0 \
    pydantic>=2.0.0 \
    langchain-openai>=0.1.0 \
    openai>=1.0.0 \
    pyyaml>=6.0.1 \
    asyncio-mqtt>=0.16.1 \
    websockets>=12.0 \
    aiofiles>=23.2.1

# Set environment variables
ENV PYTHONPATH=/app

# Create a script to load environment variables
RUN echo "#!/bin/bash\n\
set -a\n\
[ -f /app/.devcontainer/.env ] && source /app/.devcontainer/.env\n\
[ -f /app/.env ] && source /app/.env\n\
set +a\n\
exec \"\$@\"" > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "dashboard_analyzer/main.py"] 