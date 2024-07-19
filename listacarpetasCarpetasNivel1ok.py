import os

def listar_carpetas(ruta_actual):
  """
  Función que lista solo las carpetas del directorio especificado.

  Argumentos:
    ruta_actual: La ruta del directorio a listar.

  Retorno:
    Una lista con los nombres de las carpetas.
  """
  carpetas = []
  for archivo in os.listdir(ruta_actual):
    if os.path.isdir(os.path.join(ruta_actual, archivo)):
      carpetas.append(archivo)
  return carpetas

# Obtiene la ruta del directorio actual
ruta_actual = os.getcwd()

# Lista las carpetas del directorio actual
carpetas = listar_carpetas(ruta_actual)

# Imprime la lista de carpetas
print("Carpetas en el directorio actual:")
for carpeta in carpetas:
  print(carpeta)
