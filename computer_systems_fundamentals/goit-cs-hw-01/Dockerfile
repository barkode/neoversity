FROM ubuntu:26.04

# Оновлення пакетів та встановлення DOSBox
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y dosbox && \
    rm -rf /var/lib/apt/lists/*

# Створення непривілейованого користувача
RUN useradd -m -s /bin/bash dosuser

USER dosuser
WORKDIR /home/dosuser

# Запуск DOSBox
ENTRYPOINT ["dosbox"]