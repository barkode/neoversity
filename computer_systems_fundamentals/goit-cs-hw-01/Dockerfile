FROM ubuntu:26.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Встановлюємо пакети
RUN apt-get update && \
    apt-get install -y dosbox nasm xvfb x11vnc novnc websockify && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# 2. Копіюємо ваш файл в образ (файл має бути в тій самій папці, що й Dockerfile)
COPY task1.asm /workspace/

# 3. Компілюємо програму прямо під час збірки образу
RUN nasm -f bin task1.asm -o task1.com

# 4. Створюємо скрипт для запуску екрану та DOSBox
RUN echo '#!/bin/bash\n\
export DISPLAY=:0\n\
Xvfb :0 -screen 0 800x600x16 &\n\
sleep 1\n\
x11vnc -display :0 -nopw -forever -bg -quiet\n\
websockify --web /usr/share/novnc/ 8080 localhost:5900 &\n\
dosbox -c "mount c /workspace" -c "c:" -c "task1.com"\n\
' > /start.sh && chmod +x /start.sh

EXPOSE 8080

CMD ["/start.sh"]