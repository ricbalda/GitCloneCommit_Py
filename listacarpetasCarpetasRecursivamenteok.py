import os
import sys

def listar_carpetas_sin_recursividad(ruta_carpeta):
    """
    Función que lista solo las carpetas del directorio especificado **y sus subdirectorios inmediatos**.

    Argumentos:
        ruta_carpeta: La ruta del directorio a listar.

    Retorno:
        Una lista con los nombres de las carpetas.
    """
    carpetas = []
    for entry in os.scandir(ruta_carpeta):
        if entry.is_dir():
            carpetas.append(entry.name)

    # Itera sobre las carpetas encontradas y busca subdirectorios inmediatos
    for carpeta in carpetas:
        subdirectorio = os.path.join(ruta_carpeta, carpeta)
        for sub_entry in os.scandir(subdirectorio):
            if sub_entry.is_dir():
                carpetas.append(os.path.join(carpeta, sub_entry.name))

    return carpetas

def main():
    """
    Función principal para ejecutar el programa.
    """
    # Obtiene el argumento del directorio a listar
    if len(sys.argv) < 2:
        print("Uso: listadocarpetas -d <directorio>")
        return

    ruta_carpeta = sys.argv[1]

    # Verifica si el directorio existe
    if not os.path.exists(ruta_carpeta):
        print(f"Error: El directorio '{ruta_carpeta}' no existe.")
        return

    # Lista las carpetas del directorio sin recursión
    carpetas = listar_carpetas_sin_recursividad(ruta_carpeta)

    # Imprime la lista de carpetas con formato mejorado
    print(f"Carpetas en el directorio '{ruta_carpeta}':")
    for i, carpeta in enumerate(carpetas):
        # Agrega numeración y alineación a la izquierda
        print(f"{i+1:2}. {carpeta:<30}")

if __name__ == "__main__":
    main()
