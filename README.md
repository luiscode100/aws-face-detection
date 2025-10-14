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
![Creación Lambda](./docs/1.png)

### Configuración básica de AWS Lambda

Se muestra la configuración base utilizada en la función **`detection_faces`**.

![Configuración básica de Lambda](./docs/3.png)

## Parámetros principales

- **Memoria asignada:** 1280 MB  
- **Almacenamiento temporal (/tmp):** 512 MB  
- **Timeout:** 1 min 3 s  
- **Rol IAM asociado:** `service-role/detection_faces-role-pkf5xv9u`


