# Experiments

Este repo contiene experimentos de código para teorizar como implementar ciertas funciones. Este readme contiene una breve explicación de que intenta probar cada cosa, e iré añadiendo readmes a cada proyecto si es necesario. 

# Instalación y ejecución
```
sudo apt install python3-dev libmysqlclient-dev nginx
pipenv --python /usr/bin/python3
pipenv install
pipenv shell
cd _proyecto_que_quieras_probar
./start.sh
```

# Explicación de cada experimento
- 001_full_asgi_app (02/02/2024): Implementación de websockets con django_channels en una app totalmente ASGI
- 002_hybrid_wsgi_asgi_app (02/02/2024): Implementación de websockets con django_channels en una app hibrida de WSGI y ASGI.

