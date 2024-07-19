""" 
  Nombre  : PushLocalRepo
  Desc.   : De un repositorio local recien creado actualiza ( git add/commit/push ) al repositorio remoto
            Hay que cambiar algunas rutas y nombres para que pueda funcionar bien.
  Creado  : 2024-07-19
  Autor   : Ricardo Balda
  Email   : ricbalda@hotmail.com 

 """
import pathlib
import pdb
import getopt
import json
import os
import shutil
import subprocess
import sys
import string
import time
from urllib.request import urlopen


def Usage():
  print("Usage: %s -u <github user> -r <repo> -d <sourcedirectory> -h<help>" % sys.argv[0])
  print("  -u <github user>  github user name")
  print("  -d <directory>    local directory for repos commits")
  print("  -r <repo>         specific repo")

def copytree_overwrite(src, dst, exclude_dirs=[]):
    def should_copy(src_path):
        # Get the directory name from the source path
        dir_name = os.path.basename(src_path)

        # Check if the directory name is in the exclude list
        return dir_name not in exclude_dirs

    if os.path.exists(dst):
        # Check if the destination is a directory
        if os.path.isdir(dst):
            for src_filename in os.listdir(src):
                src_path = os.path.join(src, src_filename)
                dst_path = os.path.join(dst, src_filename)

                # Check if the file exists in the destination
                if os.path.exists(dst_path):
                    # Overwrite the existing file
                    print(f"Overwriting existing file: {dst_path}")
                    os.remove(dst_path)

                # Check if the current source path is a directory
                if os.path.isdir(src_path):
                    # Check if the directory should be copied
                    if should_copy(src_path):
                        # Copy the directory using shutil.copytree
                        shutil.copytree(src_path, dst_path)
                else:
                    # Copy the file using shutil.copyfile
                    shutil.copyfile(src_path, dst_path)

        else:
            raise OSError(f"Destination '{dst}' is not a directory")
    else:
        # Create the destination directory if it doesn't exist
        os.makedirs(dst)

        # Copy the entire directory tree using shutil.copytree
        shutil.copytree(src, dst, ignore=should_copy)  # Use ignore function with should_copy


def filtro_directorio(directorio, contenidos):
  # Lista de carpetas a ignorar
  carpetas_a_ignorar = [".git"]

  # Filtrar elementos
  elementos_a_copiar = []
  for elemento in contenidos:
    if elemento in carpetas_a_ignorar:
      # Ignorar la carpeta
      pass
    else:
      # Añadir el elemento a la lista de copia
      elementos_a_copiar.append(elemento)

  return elementos_a_copiar


def eliminar_carpetas_excepto(ruta_directorio, carpeta_a_excluir):
  """
  Elimina todas las carpetas dentro de un directorio, excepto una específica.

  Args:
    ruta_directorio: Ruta del directorio donde se eliminarán las carpetas.
    carpeta_a_excluir: Ruta de la carpeta que se desea excluir de la eliminación.

  """

  print('rmdir')

  for root, directories, archivos in os.walk(ruta_directorio):
    if carpeta_a_excluir in directories:
      # print('salta')
      continue

    for archivo in archivos:

            ruta_archivo = os.path.join(root, archivo)
            if carpeta_a_excluir in ruta_archivo:
                # print('salta archivo')
                continue

            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
                # print(f"Archivo {ruta_archivo} eliminado.")


  for directorio, subdirectorios, archivos in os.walk(ruta_directorio):
    # print(f'carpeta_a_excluir={carpeta_a_excluir}  directorio={directorio}')
    if carpeta_a_excluir in directorio:
      # print('salta')
      continue

    # print(f'directorio={directorio}  subdirectorios={subdirectorios}')

    for subdirectorio in subdirectorios:
      ruta_subdirectorio = os.path.join(directorio, subdirectorio)
      if carpeta_a_excluir in ruta_subdirectorio:
       # print('salta2')
       continue

      try:
        # print(f'rmdir={ruta_subdirectorio}')
        # os.rmdir(ruta_subdirectorio)
        shutil.rmtree(ruta_subdirectorio)
      except OSError:
        pass


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


def leer_nota_txt(ruta_archivo):
    """
    Función que lee el contenido del archivo `note.txt` en la ruta especificada.

    Argumentos:
        ruta_archivo: La ruta del archivo `note.txt`.

    Retorno:
        El contenido del archivo `note.txt` como una cadena de texto.
    """
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
        return contenido
    else:
        print(f"Archivo no encontrado: {ruta_archivo}")
        return ""


def main():

  githubUser  = ''
  currentRepo = ''
  mensajecommit = ''

  directorio_origen = ''
  # Directorio destino
  directorio_destino = "C:\\D\\GIT_Down_All_Commits\\atmp"
  carpeta_a_excluir = "C:\\D\\GIT_Down_All_Commits\\atmp\\.git"

  sourceDirectory = ''


  try:
    # process command arguments
    ouropts, args = getopt.getopt(sys.argv[1:],"u:r:d:h")
    for o, a in ouropts:
      if   o == '-u':
        githubUser = a
      if   o == '-d':
        sourceDirectory = a
      if   o == '-r':
        currentRepo = a
      elif o == '-h':
        Usage()
        sys.exit(0)
  except getopt.GetoptError as e:
    print(str(e))
    Usage()
    sys.exit(2)


  # Lista las carpetas del directorio actual
  carpetas = listar_carpetas(sourceDirectory)

  # Imprime la lista de carpetas
  for i, carpeta in enumerate(carpetas):
    txtFile = carpeta + '.txt'
    note_txt_path = os.path.join(sourceDirectory, txtFile)

    # Rs1 carpeta[25:33]
    # Prueba3 carpeta[8:18]
    note_content = leer_nota_txt(note_txt_path)
    if note_content:
        # mensajecommit = carpeta[23:33] + ' - ' + note_content
        mensajecommit = note_content


    print(" ")
    directorio_origen = sourceDirectory + "\\" + carpeta
    print(f"{i+1}. Directorio={directorio_origen}")

    eliminar_carpetas_excepto(directorio_destino, carpeta_a_excluir)
    input("Presiona Enter para continuar...")

    # Copiar el directorio, ignorando la carpeta especificada
    # shutil.copytree(directorio_origen, directorio_destino, ignore=filtro_directorio)

    exclude_dirs = [".git"]  
    copytree_overwrite(directorio_origen, directorio_destino, exclude_dirs)
    input("Presiona Enter para continuar...")


    os.chdir(directorio_destino)
    ruta_actual = os.getcwd()
    print(f'ruta_actual={ruta_actual}')

    print(f"local repo={carpeta}")
    print('Git Add .')
    subprocess.call(['git', 'add', '.'])
    time.sleep(5)
    # input("Presiona Enter para continuar...")

    print(f'Git commit -m "{mensajecommit}"')
    subprocess.call(['git', 'commit', '-m', mensajecommit])
    time.sleep(2)
    # input("Presiona Enter para continuar...")

    print(f'Git push')
    subprocess.call(['git', 'push'])
    time.sleep(3)
    # input("Presiona Enter para continuar...")


if __name__ == "__main__":
  print(" ")
  print('Inicio **')
  main()
  print('Fin **')