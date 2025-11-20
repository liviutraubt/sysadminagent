FROM python:3

WORKDIR /app

RUN pip install google-adk mcp litellm

COPY my_agent /app/my_agent
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]