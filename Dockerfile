FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync
COPY . .
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["pytest", "--alluredir=allure-results", "-v"]