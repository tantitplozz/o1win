FROM ollama/ollama:latest

RUN ollama pull thebloke/mythomax-l2-13b

CMD ["serve"] 