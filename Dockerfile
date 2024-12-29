# Utilizamos la imagen oficial de Python
FROM python:3.9.21-alpine3.20
# Dentro del contendor instalamos python, pip y flask con run, alpine utiliza el administrador de paquetes apk
RUN pip install flask mysql-connector flask-cors
# Le decimos al contenedor que se ponga en el directorio app
WORKDIR /app
# copiamos nuestro proyecto a la carpta /app
COPY . .
# exponemos el puerto en el contenedor
EXPOSE 3000
#ejecutamos el servidor
CMD ["python", "main.py"]

#Comandos
#para construir el contenedor: docker build -t agenda .
#Para sopar dentro de el: docker run --rm -it agenda /bin/sh
#Para correr: docker run -it --rm --name mi-contenedor -p 3000:3000 -v "$PWD":/app -w /app agenda
