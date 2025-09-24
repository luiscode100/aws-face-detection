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
