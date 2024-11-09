import os
import openai
import subprocess

# Configura tu clave API de OpenAI
openai.api_key = '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'

def extraer_palabras_clave(mensaje):
    # Define palabras clave de ejemplo o reglas de extracción
    palabras_clave = []
    # Aquí puedes implementar lógica para extraer las palabras específicas de la retroalimentación
    for linea in mensaje.splitlines():
        if "[ERROR]" in linea:
            palabras_clave.extend(linea.split())
    return palabras_clave

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

def obtener_archivos_proyecto():
    """Obtiene una lista de archivos listos para commit, sin limitar el tipo de archivo."""
    # Agrega todos los cambios al área de preparación
    subprocess.run(["git", "add", "."])
    
    # Verifica los archivos en el área de preparación
    resultado = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True)
    archivos = resultado.stdout.splitlines()
    
    # Devuelve una lista de tuplas con el nombre de archivo y su extensión
    archivos_con_extension = [(archivo, os.path.splitext(archivo)[1]) for archivo in archivos]
    return archivos_con_extension

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


import subprocess

def configurar_remoto():
    """Configura el remoto 'origin' si no existe."""
    # Verifica si 'origin' está configurado como remoto
    resultado_remoto = subprocess.run(["git", "remote"], capture_output=True, text=True)
    
    if "origin" not in resultado_remoto.stdout:
        print("El remoto 'origin' no está configurado. Añadiéndolo ahora.")
        # Añade el remoto 'origin' con la URL de tu repositorio
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/SebastianMatos/GitHub-con-IA.git"])
    else:
        print("El remoto 'origin' ya está configurado.")

def sincronizar_repositorio():
    """Sincroniza el repositorio local con el remoto antes de hacer un push."""
    configurar_remoto()  # Configura el remoto antes de sincronizar
    # Realiza un fetch para actualizar la información del remoto
    subprocess.run(["git", "fetch", "origin"], check=True)
    
    # Realiza un pull con rebase para evitar conflictos de historial
    resultado_pull = subprocess.run(["git", "pull", "--rebase", "origin", "main"], capture_output=True, text=True)
    
    if "CONFLICT" in resultado_pull.stdout:
        print("Conflicto detectado durante el pull --rebase. Por favor, resuelve el conflicto manualmente antes de continuar.")
        exit(1)
    elif "Already up to date" in resultado_pull.stdout:
        print("El repositorio local ya está actualizado.")
    else:
        print("Repositorio actualizado con cambios remotos usando rebase.")

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
        
        retroalimentacion = revisar_codigo_con_openai(contenido_archivo, extension)
        
        retroalimentacion_filtrada = retroalimentacion.replace("[BIEN]", "").replace("[ERROR]", "")
        print(f"Revisión para {archivo}:\n{retroalimentacion_filtrada}\n")
        
        palabras_clave = extraer_palabras_clave(retroalimentacion)
        
        if "[ERROR]" in retroalimentacion:
            resaltar_errores(archivo, palabras_clave)
            print(f"Push cancelado. Revisa el archivo {archivo} con errores resaltados.")
            exit(1)

    # Realiza el push con --force si es necesario para evitar rechazos
    print("No se detectaron errores críticos. Realizando el commit y el push.")
    subprocess.run(["git", "add", "README.md", "DOCUMENTACION.md"])
    subprocess.run(["git", "commit", "-m", "Commit automático: revisión completada sin errores críticos y documentación actualizada"])
    subprocess.run(["git", "push", "--force", "https://github.com/SebastianMatos/GitHub-con-IA.git", "main"])

if __name__ == "__main__":
    main()
