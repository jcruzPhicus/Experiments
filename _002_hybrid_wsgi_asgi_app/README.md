# Ejecutar

Para ejecutar:
```
sudo systemctl stop nginx
nginx -c whatever_folder_this_is_in/nginx.conf
./start.sh
```

# IMPORTANTE
El script de start no limpia después de ejecutarse; quedan vivos los procesos de Daphne y uWSGI.
