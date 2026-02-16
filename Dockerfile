############################
# Base image
############################
FROM python:3.13-slim

############################
# Environment
############################
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

############################
# System dependencies
############################
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
 && rm -rf /var/lib/apt/lists/*

############################
# Non-root user
############################
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid ${USER_GID} ${USERNAME} \
 && useradd  --uid ${USER_UID} --gid ${USER_GID} \
             --create-home --shell /bin/bash ${USERNAME}

############################
# uv + virtualenv
############################
RUN pip install --no-cache-dir --upgrade pip uv \
 && uv venv ${VIRTUAL_ENV} \
 && chown -R ${USERNAME}:${USERNAME} ${VIRTUAL_ENV}

############################
# Switch to non-root
############################
USER ${USERNAME}
WORKDIR /workspace

############################
# Python dependencies
############################
COPY --chown=${USERNAME}:${USERNAME} pyproject.toml uv.lock* ./

RUN uv sync --locked

############################
# Jupyter kernel
############################
RUN uv pip install --no-cache-dir ipykernel \
 && python -m ipykernel install --user \
    --name graph-cookbook \
    --display-name "Python (graph-cookbook)"

############################
# Runtime
############################
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
