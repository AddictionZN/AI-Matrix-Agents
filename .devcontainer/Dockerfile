FROM mcr.microsoft.com/devcontainers/miniconda

RUN pip install --upgrade pip setuptools wheel

COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then \
    umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; \
    fi && rm -rf /tmp/conda-tmp
