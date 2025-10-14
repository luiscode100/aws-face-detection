# 🖼️ Detector de Caras en AWS

Este proyecto implementa un sistema **serverless de detección de caras** usando **AWS Lambda**, **API Gateway**, **S3** y **DynamoDB**, junto con la librería **OpenCV**.  
Permite enviar imágenes a través de una API REST, detectar rostros y almacenar tanto las imágenes como las coordenadas de los rostros detectados en la nube.

## 📊 Arquitectura
![Arquitectura del proyecto](docs/diagram.png)

**Flujo de datos:**
1. El usuario envía una imagen mediante **API Gateway**.  
2. **Lambda** procesa la imagen con **OpenCV** y detecta los rostros.  
3. Los resultados se guardan en **DynamoDB** (coordenadas) y la imagen en **S3**.  
4. Los logs y errores se registran en **CloudWatch**.  
5. **IAM** y **EC2** se usan como soporte para permisos y generación de layers.

---

## 🛠️ Tecnologías utilizadas

- **AWS Lambda**  
- **Amazon API Gateway**  
- **Amazon S3**  
- **Amazon DynamoDB**  
- **AWS IAM** (gestión de roles y permisos)  
- **Amazon EC2** (para generar el layer de OpenCV)  
- **Python 3.12**  
- **OpenCV**  

---

## ✨ Características

- API REST para enviar imágenes.  
- Procesamiento serverless en Lambda.  
- Detección de rostros con **OpenCV (Haar Cascade)**.  
- Almacenamiento seguro de imágenes en S3.  
- Guardado de coordenadas en DynamoDB.  
- Monitoreo de ejecución con CloudWatch.  

---

## 🧩 Paso 1 — Crear la función Lambda

### 📘 Descripción
En este paso se crea una función **AWS Lambda** desde cero dentro del entorno educativo de **AWS Educate / AWS Academy**.  
Dado que las cuentas *Student Lab* no poseen privilegios para crear o gestionar roles de IAM, se utiliza un **rol preasignado** denominado *LabRole* (o equivalente).

---

### 🧠 Configuración en la consola

1. Accede al servicio **AWS Lambda**.
2. Haz clic en **Create function**.
3. Selecciona la opción **Author from scratch**.
4. Completa los campos de la sección **Basic information**:
   - **Function name:** `detection_faces`
   - **Runtime:** `Python 3.12`
   - **Architecture:** `x86_64`
5. En la sección **Permissions**, selecciona:
   - **Create a new role with basic Lambda permissions**

---  
### 🖼️ Referencia visual
<p><img src="docs/01.png" alt="Creación Lambda" width="80%"></p>    
---

## Paso 2 — Configurar los parámetros básicos de la función Lambda

### 🧩 Descripción
En este paso se ajustan los **parámetros básicos de ejecución** de la función Lambda para optimizar el rendimiento y evitar interrupciones por falta de memoria o tiempo de ejecución.  
La configuración se realiza desde la sección **Edit basic settings** de la consola AWS Lambda.

---

### ⚙️ Configuración en la consola

1. Accede a la función **`detection_faces`** previamente creada.  
2. Haz clic en **Configuration → General configuration → Edit**.  
3. Ajusta los siguientes parámetros:
   - **Memory (MB)**`1280 mb`
   - **Ephemeral storage (/tmp)** `512 mb`
   - **Timeout** `1 min`
   -  **Execution role** `service-role/detection_faces-role-pkf5xv9u`

---
### 🖼️ Referencia visual
<p><img src="docs/02.png" alt="Configuración básica de Lambda" width="80%"></p>    

## Paso 3 — Desplegar la API REST en AWS API Gateway

### 🧩 Descripción
En este paso se crea una **API REST** en **AWS API Gateway** para exponer la función Lambda `detection_faces` como un endpoint accesible vía HTTP.  
Esta API permite enviar peticiones **POST** con datos de imagen para ser procesados mediante OpenCV dentro del entorno serverless.

---
### ⚙️ Configuración en la consola

#### 1. Crear la API REST
Configura los detalles iniciales de la API:  

1. Accede a **API Gateway** y selecciona la opción **Build** dentro de **REST API** (no HTTP API ni WebSocket API).  
2. Configura los detalles iniciales de la API:
   - **API name** `face_detection_api`
3. Haz clic en **Create API**.
  
### 🖼️ Referencia visual
<p><img src="docs/05.png" alt="Crear API REST" width="80%"></p>    

---  

#### 2. Crear el método de integración

1. En los recursos de la API, crea un nuevo **método** y configura lo siguiente:
   - **Method type** `POST`
   - **Integration type** `Lambda Function`
   - **Lambda function** `arn...:detection_faces`
   - **Integration timeout** `29000 ms`

2. Una vez creado el método, la consola mostrará el flujo de integración entre el cliente y Lambda:
   - **Client → Method Request → Integration Request → Lambda → Integration Response → Method Response**

### 🖼️ Referencia visual 
<p><img src="docs/06.png" alt="Crear método POST" width="80%"></p>   

---

#### 3. Desplegar la API

1. Selecciona **Deploy API** para crear un entorno (`stage`) donde se habilitará la API.
   - **Stage** `New Stage`
   - **Stage name** `development`

2. Haz clic en **Deploy**.

### 🖼️ Referencia visual 
<p><img src="docs/8.png" alt="Desplegar API" width="40%"></p>

---

### ✅ Resultado esperado
Una API REST pública en AWS API Gateway vinculada a la función Lambda `detection_faces`, accesible mediante solicitudes POST para procesar imágenes.

---

### ☁️ Paso 4 — Configurar almacenamiento en S3 y DynamoDB
### 🧩 Descripción
En este paso se preparan los servicios de almacenamiento del sistema. El objetivo es disponer de un espacio seguro para guardar las **imágenes procesadas** y una base de datos **NoSQL** para almacenar los **coordenadas de la detección facial**

- **Amazon S3** se utiliza como repositorio de imágenes detectadas.  
- **Amazon DynamoDB** almacena la información estructurada asociada a cada rostro detectado.    

#### 1. Crear S3 Bucket
- **Bucket:** `face-detection-s3-lusber`  
- **Región:** `eu-west-3`  
- **Acceso público:** bloqueado  
- **Cifrado:** SSE-S3
  
---  

### 🖼️ Referencia visual
<p><img src="docs/9.png" alt="Crear Bucket" width="80%"></p>   

#### 2. Crear DynamoDB
- **Tabla:** `faces`  
- **Partition key:** `face_id (String)`  
- **Modo:** On-demand

### 🖼️ Referencia visual   
<p><img src="docs/12.png" alt="Crear tabla DynamoDB" width="80%"></p>   

<p><img src="docs/13.png" alt="Tabla Activa" width="80%"></p>    


---

