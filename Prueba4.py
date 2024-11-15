import os
import openai
import subprocess

# Configura tu clave API de OpenAI
openai.api_key = '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'

# Función para extraer palabras clave de la retroalimentación, especialmente aquellas marcadas como errores.
def extraer_palabras_clave(mensaje):
    # Define palabras clave de ejemplo o reglas de extracción
    palabras_clave = []
    # Extrae líneas que contienen "[ERROR]" y separa cada palabra para crear una lista de palabras clave
    for linea in mensaje.splitlines():
        if "[ERROR]" in linea:
            palabras_clave.extend(linea.split())
    return palabras_clave

# Función para resaltar errores en el archivo, agregando comentarios "FIXME" en líneas que contengan palabras clave.
def resaltar_errores(archivo, palabras_clave):
    with open(archivo, 'r') as f:
        contenido = f.readlines()
    
    contenido_resaltado = []
    for linea in contenido:
        for palabra in palabras_clave:
            if palabra in linea:
                # Añade un comentario de error antes de la línea con el texto a resaltar
                linea = f"// FIXME: ERROR DETECTADO\n{linea.replace(palabra, f'{palabra}')}"
        contenido_resaltado.append(linea)
    
    with open(archivo, 'w') as f:
        f.writelines(contenido_resaltado)
    print(f"Errores resaltados en {archivo}")

# Función para obtener todos los archivos en el área de preparación de Git, incluyendo su extensión.
def obtener_archivos_proyecto():
    """Obtiene una lista de archivos listos para commit, sin limitar el tipo de archivo."""
    # Agrega todos los cambios al área de preparación
    subprocess.run(["git", "add", "."])
    
    # Elimina archivos específicos del área de preparación si es necesario
    subprocess.run(["git", "reset", "Prueba1.py", "Prueba2.py","Prueba3.py"])
    
    # Verifica los archivos en el área de preparación
    resultado = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True)
    archivos = resultado.stdout.splitlines()
    
    # Devuelve una lista de tuplas con el nombre de archivo y su extensión
    archivos_con_extension = [(archivo, os.path.splitext(archivo)[1]) for archivo in archivos]
    return archivos_con_extension

# Función para enviar el contenido de un archivo a OpenAI y recibir retroalimentación sobre errores críticos.
def revisar_codigo_con_openai(contenido_archivo, extension):
    """Envía el contenido de un archivo a OpenAI para una revisión de errores críticos según el tipo de archivo."""
    # Determina el tipo de archivo y ajusta el mensaje en función de la extensión
    if extension == ".py":
        descripcion = "Eres un asistente que revisa código Python en busca de errores críticos únicamente."
    elif extension == ".html":
        descripcion = "Eres un asistente que revisa código HTML en busca de errores críticos y posibles problemas de estructura."
    elif extension == ".js":
        descripcion = "Eres un asistente que revisa código JavaScript en busca de errores críticos y problemas comunes de funcionamiento."
    else:
        descripcion = "Eres un asistente que revisa código en busca de errores críticos, aunque no reconozco explícitamente la extensión."

    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Usa gpt-4 si tienes acceso
        messages=[
            {"role": "system", "content": descripcion},
            {"role": "user", "content": f"Por favor revisa este código y dime si hay errores críticos o fallas en su funcionamiento:\n{contenido_archivo}"}
        ]
    )
    return respuesta['choices'][0]['message']['content']

# Función para actualizar el archivo README.md con una lista de archivos y los paquetes requeridos.
def actualizar_readme(archivos_proyecto):
    """Actualiza el archivo README.md con la lista de archivos y los paquetes requeridos."""
    contenido_readme = "# Proyecto de Revisión de Código con IA\n\n"
    contenido_readme += "Este proyecto utiliza IA para revisar los archivos en busca de errores críticos antes de hacer un push.\n\n"
    contenido_readme += "## Archivos en el Proyecto\n\n"
    
    for archivo, _ in archivos_proyecto:
        contenido_readme += f"- `{archivo}`\n"
    
    # Agregar una sección de requisitos
    contenido_readme += "\n## Requisitos de Instalación\n\n"
    contenido_readme += "Para ejecutar el código, asegúrate de instalar los siguientes paquetes:\n"
    contenido_readme += "- Python 3.x\n"
    contenido_readme += "- openai (`pip install openai`)\n"
    contenido_readme += "- git\n\n"
    
    with open("README.md", "w") as f:
        f.write(contenido_readme)
    print("README.md actualizado.")


# Función para crear DOCUMENTACION.md que detalla el propósito y la funcionalidad de cada archivo.
def crear_documentacion(archivos_proyecto):
    """Crea el archivo DOCUMENTACION.md que detalla el propósito y la funcionalidad de cada archivo."""
    contenido_doc = "# Documentación del Proyecto\n\n"
    contenido_doc += "Este documento describe la estructura del proyecto.\n\n"
    contenido_doc += "## Descripción del Proyecto\n\n"
    contenido_doc += "El objetivo de este proyecto es utilizar IA para revisar automáticamente los archivos en busca de errores críticos antes de realizar un push al repositorio.\n\n"
    contenido_doc += "## Archivos en el Proyecto\n\n"

    for archivo, _ in archivos_proyecto:
        contenido_doc += f"### {archivo}\n"
        contenido_doc += f"- Descripción: Este archivo es parte del sistema de revisión automatizada de código.\n\n"

    # Agregar sección sobre dependencias
    contenido_doc += "## Dependencias del Proyecto\n\n"
    contenido_doc += "Asegúrate de tener instaladas las siguientes herramientas para ejecutar el proyecto:\n"
    contenido_doc += "- Python 3.x\n"
    contenido_doc += "- openai (`pip install openai`)\n"
    contenido_doc += "- git\n\n"
    
    with open("DOCUMENTACION.md", "w") as f:
        f.write(contenido_doc)
    print("DOCUMENTACION.md creado y actualizado.")

# Función para sincronizar el repositorio local con el remoto antes de hacer un push.
def sincronizar_repositorio():
    """Sincroniza el repositorio local con el remoto antes de hacer un push."""
    resultado_pull = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
    if "Already up to date" in resultado_pull.stdout:
        print("El repositorio local ya está actualizado.")
    else:
        print("Repositorio actualizado con cambios remotos.")

# Función principal que coordina la sincronización, revisión de archivos, actualización de documentación, y push al repositorio.
def main():
    # Sincroniza el repositorio antes de realizar cambios
    sincronizar_repositorio()
    
    # Obtiene todos los archivos a revisar (sin filtrar por tipo), incluyendo su extensión
    archivos_proyecto = obtener_archivos_proyecto()
    
    if not archivos_proyecto:
        print("No hay archivos en el commit actual.")
        return
    
    # Actualiza el README.md y crea DOCUMENTACION.md
    actualizar_readme(archivos_proyecto)
    crear_documentacion(archivos_proyecto)
    
    # Revisa cada archivo
    for archivo, extension in archivos_proyecto:
        print(f"Revisando el archivo: {archivo} (Tipo: {extension})")
        with open(archivo, 'r') as f:
            contenido_archivo = f.read()
        
        # Llama a la API de OpenAI para revisar el código según el tipo de archivo
        retroalimentacion = revisar_codigo_con_openai(contenido_archivo, extension)
        
        # Filtra "[BIEN]" y "[ERROR]" de la retroalimentación antes de imprimir
        retroalimentacion_filtrada = retroalimentacion.replace("[BIEN]", "").replace("[ERROR]", "")
        print(f"Revisión para {archivo}:\n{retroalimentacion_filtrada}\n")
        
        palabras_clave = extraer_palabras_clave(retroalimentacion)
        
        # Si se detectan errores críticos, cancela el push
        if "[ERROR]" in retroalimentacion:
            resaltar_errores(archivo, palabras_clave)
            print(f"Push cancelado. Revisa el archivo {archivo} con errores resaltados.")
            exit(1)

    # Si no se detectaron errores críticos, realiza el commit y el push
    print("No se detectaron errores críticos. Realizando el commit y el push.")
    subprocess.run(["git", "add", "README.md", "DOCUMENTACION.md"])
    subprocess.run(["git", "commit", "-m", "Commit automático: revisión completada sin errores críticos y documentación actualizada"])
    subprocess.run(["git", "push", "--set-upstream", "https://github.com/SebastianMatos/GitHub-con-IA.git", "main"])

if __name__ == "__main__":
    main()
