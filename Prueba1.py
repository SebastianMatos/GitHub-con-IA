[import os
import openai
import subprocess

# Configura tu clave API de OpenAI
openai.api_key = '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'

def obtener_archivos_python():
    """Obtiene una lista de archivos Python listos para commit, excluyendo Prueba1.py."""
    # Agrega todos los cambios al área de preparación
    subprocess.run(["git", "add", "."])
    
    # Elimina Prueba1.py del área de preparación si está presente
    subprocess.run(["git", "reset", "Prueba1.py"])
    
    # Verifica los archivos en el área de preparación
    resultado = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True)
    archivos = resultado.stdout.splitlines()
    archivos_python = [archivo for archivo in archivos if archivo.endswith(".py") and archivo != "Prueba1.py"]
    return archivos_python

def revisar_codigo_con_openai(contenido_archivo):
    """Envía el contenido de un archivo Python a OpenAI para una revisión de errores críticos."""
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Usa gpt-4 si tienes acceso
        messages=[
            {"role": "system", "content": "Eres un asistente que revisa código Python en busca de errores críticos únicamente."},
            {"role": "user", "content": f"Por favor revisa este código y dime si hay errores críticos o fallas en su funcionamiento:\n{contenido_archivo}"}
        ]
    )
    return respuesta['choices'][0]['message']['content']

def main():
    # Obtiene los archivos Python a revisar
    archivos_python = obtener_archivos_python()
    
    if not archivos_python:
        print("No hay archivos Python en el commit actual.")
        return
    
    # Revisa cada archivo
    for archivo in archivos_python:
        print(f"Revisando el archivo: {archivo}")
        with open(archivo, 'r') as f:
            contenido_archivo = f.read()
        
        # Llama a la API de OpenAI para revisar el código
        retroalimentacion = revisar_codigo_con_openai(contenido_archivo)
        print(f"Revisión para {archivo}:\n{retroalimentacion}\n")
        
        # Si se detectan errores críticos, cancela el push
        if any(palabra in retroalimentacion.lower() for palabra in ["error crítico", "falla", "problema grave"]):
            print(f"Push cancelado. Revisa el archivo {archivo} y realiza los cambios sugeridos.")
            exit(1)
    
    # Si no se detectaron errores críticos, realiza el commit y el push
    print("No se detectaron errores críticos. Realizando el commit y el push.")
    subprocess.run(["git", "commit", "-m", "Commit automático: revisión completada sin errores críticos"])
    subprocess.run(["git", "push", "--set-upstream", "https://github.com/SebastianMatos/GitHub-con-IA.git", "main"])

if __name__ == "__main__":
    main()
]