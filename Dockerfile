FROM python:3.12-bullseye

WORKDIR /app

RUN groupadd --system app && useradd --system --gid app --create-home app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-cache

COPY . .

RUN chown -R app:app /app

ENV PATH="/app/.venv/bin:$PATH"

USER app
