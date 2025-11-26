# PracticaPruebaDockerWecSokets


Una empresa de seguridad necesita un sistema de procesamiento de datos distribuido y aislado. Se requiere una arquitectura de anillo cerrado compuesta por 3 nodos (contenedores). Un mensaje de seguridad entra en el sistema, es transformado secuencialmente por cada nodo y regresa al origen para su validación final.

El sistema debe desplegarse con un solo comando docker-compose up.

1. La Arquitectura (Topología de Anillo)
Debe implementar tres servicios independientes (puedes usar el lenguaje que prefieras: Node, Python, Go, etc., incluso mezclarlos).

Nodo A (The Initiator):

Inicia el proceso.

Expone el puerto 8080 al host (tu navegador/cliente externo) para recibir un "disparo" inicial.

Se conecta vía WebSocket al Nodo B.

Nodo B (The Transformer):

No expone puertos al host.

Recibe datos del Nodo A.

Se conecta vía WebSocket al Nodo C.

Nodo C (The Auditor):

No expone puertos al host.

Recibe datos del Nodo B.

Se conecta vía WebSocket de vuelta al Nodo A (cerrando el anillo).

2. Reglas de Negocio (La Lógica Anti-IA)
Para evitar soluciones genéricas, se deben cumplir estrictamente las siguientes reglas de transformación de datos. El incumplimiento de cualquier variable anula el punto.

El Objeto Mensaje (JSON):

El mensaje que viaja por el anillo debe tener estrictamente esta estructura JSON. No se permite agregar campos extra:


JSON

{
  "_id": "UUID-generado-en-A",
  "power_level": 10,
  "audit_trail": []
}

El Flujo:

Disparo: Usted envía una petición (HTTP o WS) al Nodo A con un valor numérico inicial (ej: 50).

Paso 1 (Nodo A -> Nodo B): El Nodo A crea el JSON, asigna el power_level recibido y lo envía al Nodo B.

Paso 2 (Nodo B):

Recibe el JSON.

Lógica: Debe comprobar si el power_level es par o impar.

Si es PAR: Multiplica por 2.

Si es IMPAR: Suma 1.

Agrega el string "B_processed" al array audit_trail.

Envía el JSON modificado al Nodo C.

Paso 3 (Nodo C):

Recibe el JSON.

Lógica: Resta 5 al power_level.

Agrega el string "C_verified" al array audit_trail.

Envía el JSON de vuelta al Nodo A.

Cierre (Nodo A):

Recibe el mensaje del Nodo C.

Imprime en la consola de Docker (STDOUT): "CICLO COMPLETADO: [Valor Final]".

3. Requisitos Técnicos de Docker (Docker-Compose)
Los contenedores NO deben usar "localhost" para comunicarse entre sí. Deben usar los alias de servicio definidos en el compose (ej: ws://nodo-b:3000).

Debe haber al menos un Dockerfile personalizado. (No puede usar solo imágenes pre-construidas como node:alpine ejecutando comandos en línea; debe copiar el código fuente y construir la imagen).

Entregables
Repositorio de git con el código fuente de los 3 nodos.

Archivo Dockerfile (al menos uno).

Archivo docker-compose.yaml.

Captura de pantalla de los logs de la terminal donde se vea al Nodo A imprimiendo el mensaje final "CICLO COMPLETADO".

Documento PDF como informe de funcionamiento con una descripción de lo realizado y justificación de la arquitectura seguida.   Incluir detalle de lo alcanzado y/o errores obtenidos 
