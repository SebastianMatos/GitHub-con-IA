# pre_push_check.py

import os
import openai
import subprocess

# Configura tu API Key de OpenAI
openai.api_key = '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'

def get_python_files():
    """Obtiene una lista de archivos Python que están listos para el commit."""
    result = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True)
    files = result.stdout.splitlines()
    python_files = [f for f in files if f.endswith(".py")]
    return python_files

def check_code_with_openai(file_content):
    """Envía el contenido de un archivo Python a ChatGPT para revisión."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente de programación que revisa código Python en busca de errores."},
            {"role": "user", "content": f"Por favor revisa este código y dime si hay errores o mejoras posibles:\n{file_content}"}
        ]
    )
    return response.choices[0].message["content"]

def main():
    # Obtiene los archivos Python a revisar
    python_files = get_python_files()
    
    if not python_files:
        print("No hay archivos Python en el commit actual.")
        return
    
    # Revisa cada archivo
    for file in python_files:
        print(f"Revisando el archivo: {file}")
        with open(file, 'r') as f:
            file_content = f.read()
        
        # Llama a la API de OpenAI para revisar el código
        feedback = check_code_with_openai(file_content)
        print(f"Revisión para {file}:\n{feedback}\n")
        
        # Si hay problemas, cancela el push
        if "error" in feedback.lower() or "mejora" in feedback.lower():
            print(f"Push cancelado. Revisa el archivo {file} y realiza los cambios sugeridos.")
            exit(1)

if __name__ == "__main__":
    main()
