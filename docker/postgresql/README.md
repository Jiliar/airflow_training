# 🐳 Configuración de Red y Contenedores para Airflow con PostgreSQL

## 🔄 Paso 1: Detener servicios existentes
```bash
docker-compose -p postgresql -f docker/airflow/docker-compose.yml down
```
> 🛑 **Detiene** los contenedores de Airflow si estaban corriendo

## � Paso 2: Iniciar PostgreSQL
```bash
docker-compose -p postgresql -f docker/postgresql/docker-compose.yml up -d
```
> ✅ **Inicia** PostgreSQL en modo detached (segundo plano)

## 🌐 Paso 3: Crear red personalizada
```bash
docker network create airflow_network
```
> 🔗 Crea una red llamada `airflow_network` para conectar todos los servicios

## 📋 Paso 4: Verificar contenedores activos
```bash
docker ps --format "table {{.Names}}\t{{.Image}}"
```
> 👀 Muestra tabla con los contenedores y sus imágenes:

| NAMES                                      | IMAGE                     |
|--------------------------------------------|---------------------------|
| pgadmin                                    | dpage/pgadmin4            |
| postgresql                                 | postgres:14               |
| airflow_training-airflow-worker-1          | apache/airflow:3.0.1      |
| airflow_training-airflow-dag-processor-1   | apache/airflow:3.0.1      |
| airflow_training-airflow-triggerer-1       | apache/airflow:3.0.1      |
| airflow_training-airflow-scheduler-1       | apache/airflow:3.0.1      |
| airflow_training-airflow-apiserver-1       | apache/airflow:3.0.1      |
| airflow_training-postgres-1                | postgres:13               |
| airflow_training-redis-1                   | redis:7.2-bookworm        |

## 🔌 Paso 5: Conectar todos los contenedores a la red
```bash
docker network connect airflow_network pgadmin
docker network connect airflow_network postgresql
docker network connect airflow_network airflow_training-airflow-worker-1
docker network connect airflow_network airflow_training-airflow-dag-processor-1
docker network connect airflow_network airflow_training-airflow-triggerer-1
docker network connect airflow_network airflow_training-airflow-scheduler-1
docker network connect airflow_network airflow_training-airflow-apiserver-1
docker network connect airflow_network airflow_training-postgres-1
docker network connect airflow_network airflow_training-redis-1
```
> 🤝 Conecta **todos los servicios** a la red `airflow_network` para permitir comunicación entre ellos

## 🧪 Paso 6: Verificar conectividad
```bash
docker exec -it airflow_training-airflow-scheduler-1 curl -v postgresql:5432
```
> 🔍 Prueba de conexión desde el scheduler de Airflow al PostgreSQL (puerto 5432)

## 💡 Notas importantes:
1. Todos los contenedores deben estar en la **misma red** para resolverse por nombre
2. PostgreSQL usa el puerto estándar **5432**
3. La red personalizada permite comunicación segura entre servicios
4. 🐳 Usa `docker network inspect airflow_network` para verificar conexiones
5. Los servicios clave conectados son:
   - PostgreSQL (2 instancias)
   - PgAdmin
   - Redis
   - Todos los componentes de Airflow:
     - Worker
     - DAG Processor
     - Triggerer
     - Scheduler
     - API Server
```