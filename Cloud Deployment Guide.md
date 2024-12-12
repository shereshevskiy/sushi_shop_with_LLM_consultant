1. Хостинг:
- адрес https://beget.com/p1023067
- регистрация - выбираем VPS
- скачиваем и устанавливаем Putty: https://putty.org.ru/download
- с помощью PyTTYgen создаем приватный и публичный ключ
- публичный указываем при создании VPS, сохраняем к себе на компьютер
- приватный экспортируем в формате OpenSSH тоже к себе на компьютер
- замена символических ссылок (на примере Python 3.12):
	sudo ln -s /usr/bin/python3.12 /usr/bin/python

2. В VS Code:
- установим расширение "Remote - SSH (разработчик Microsoft)"
- откройте командную палитру (Ctrl+Shift+P)
- выбираем "Add New SSH Host"
- вводим команду для подключения:
	ssh user@hostname
- копируем приватный ключ в папку c:\users\user\.ssh под именем английскими буквами
- отредактируем файл конфигурации в c:\users\user\.ssh\config, например:

Host 5.35.88.248
  HostName 5.35.88.248
  User root
  ForwardAgent yes
  IdentityFile c:\Users\aleks\.ssh\5.35.88.248.private.openssh

3. Установка Jupyter Notebook
- установка docker 1 способ:
	sudo apt install podman-docker
	sudo apt install docker.io 
- установка docker 2 способ:
	sudo apt update
	sudo apt upgrade
	sudo apt install apt-transport-https ca-certificates curl software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	sudo apt update
	sudo apt install docker-ce
- запуск докера:
	docker run --restart always -p 8888:8888  -p 8000:8000 -p 5000:5000 -v /root/python:/home/jovyan -e JUPYTER_ENABLE_LAB=yes -d jupyter/base-notebook