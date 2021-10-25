# Suite AAGE
La Suite AAGE es un Sistema perteneciente a la Agencia de Acompañamiento a la Gestión Educativa,
departamento perteneciente a la Universidad Adventista de Chile.

Este sistema se divide en distintos módulos, los que se enlistan a continuación:
* Recursos Humanos (En desarrollo)
* Carga Horaria
* Evaluación Docente 
* Ciclos de Calidad (De momento externo a este sistema)
* Entre otros en desarrollo

## Tecnologías aplicadas
Para este sistema, se utilizan:

* Lenguaje de programación Python (v3)
* FrameWork de desarrollo Django (v2.2)
* Base da datos PostgreSQL (superior a v9.4)
* Sistema de Contenedores Docker (versión actual) 

## Entorno de desarrollo
Ahora se explicará como poder configurar y levantar el proyecto en el servidor local

### Configuración
Para la puesta en desarrollo, primero se debe clonar el proyecto
```
git clone https://gitlab.unach.cl/aage/aagesuite.git
```

Luego copia a la carpeta raíz del proyecto, los archivos ```.env_development``` con nombre ```.env```
y ```development.yml``` con nombre ```docker-compose.yml```

### Creación del contenedor Docker
Para levantar el contenedor Docker, se utilizará el archivo ```docker-compose.yml```
que fue copiado a la raíz previamente. En este archivo se especifican dos servicios:

1. db: Es el servicio de Base de Datos del sistema y está configurado para una versión actual de PostgreSQL
y su información básica para funcionar, se encuentra en el archivo ```.env``` del mismo directorio.
Como dato anexo, este servicio está configurado para recibir conecciones por el ```pueto 5532```

2. web: Es el servicio web del sistema, donde se especifican las reglas de construcción del sistema,
comandos para el momento de iniciar el contenedor, volúmenes de conección entre el directorio raíz
y contenedor, especificación de las variables de entorno por medio del archivo ```.env```
y el o los puertos de salida

Una vez verificado que los puertos de salida de ambos servicios (db y web) no tengan conflicto,
se procede a levantar el sistema mediante el comando
```
docker-compose up
```

La primera vez que se ejecute, Docker descargará e instalará en el contenedor,
los paquetes especificados en el archivo ```requirements.txt```

Cuando termine la instalación, comenzará a aparecer en consola la información de cada uno
de los servicios especificados en el archivo ```docker-compose.yml```

Para mantener el contenedor en ejecución, cada vez que se inicie la máquina,
se debe levantar el sistema en modo background
```
docker-compose up -d
```

Para poder ver los registros de los servicios, se debe ingresar al log del contenedor
```
docker-compose logs --tail="50" -f
```
en donde:
* ```--tail="50"``` permitirá que el log muestre solo las últimas 50 líneas
* ```-f``` permitirá seguir viendo los registros de los servicios

Si desea solo ver los registros de un servicio en específico, agréguelo al comando
```
docker-compose logs -f web
```
en este caso, solo veríamos los registros del servicio web

### Migración de base de datos

Una vez creado y en ejecución el contenedor del proyecto,
se debe iniciar la creación de la base de datos, en dos sencillos pasos:

1. Ingresar al contenedor del sistema
```
docker exec -it aagesuite bash
```

2. Ejecutar las migraciones de las apps del sistema
```
python manage.py migrate
```

Esto creará las tablas y campos necesarios para el sistema,
tanto de la base de Django como lo creado para cada app

### Ingresar al sistema
Para el ingreso al sistema, primero se debe crear un usuario administrador,
que pueda ingresar al sitio de administración de Django y comenzar a cargar la información
necesaria para cada aplicación, también en dos sencillos pasos:

1. Ingresar al contenedor del sistema
```
docker exec -it aagesuite bash
```
2. Crear usuario administrador
```
python manage.py createsuperuser
```

Una vez creado el usuario, se ingresa desde el navegador a la ruta http://127.0.0.1:8001
en donde se estará mostrando el sistema (siempre que 8001 sea el puerto de salida del servicio web)