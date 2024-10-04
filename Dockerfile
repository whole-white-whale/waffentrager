FROM python:3.12-slim
WORKDIR /app
RUN pip install pipx && pipx install poetry
ENV PATH="/root/.local/bin:$PATH"
COPY ./poetry.lock .
COPY ./pyproject.toml .
RUN poetry install --no-root
COPY ./README.md .
COPY ./waffentrager ./waffentrager
RUN poetry install
ENTRYPOINT ["poetry", "run", "python", "waffentrager/telegram_bot.py"]
