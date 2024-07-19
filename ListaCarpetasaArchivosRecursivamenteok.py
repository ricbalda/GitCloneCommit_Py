import os

def printDirectoryFiles(directory):
   for filename in os.listdir(directory):  
        full_path=os.path.join(directory, filename)
        if not os.path.isdir(full_path): 
            print( full_path + "\n")


def checkFolders(directory):

    dir_list = next(os.walk(directory))[1]

    #print(dir_list)

    for dir in dir_list:           
        print(dir)
        checkFolders(directory +"/"+ dir) 

    printDirectoryFiles(directory)       


def main():
  main_dir="C:\D\GIT_Down_All_Commits"

  checkFolders(main_dir)


  input("Press enter to exit ;")


if __name__ == "__main__":
    main()
# 2024-07-18 Lista Todas los directoruios recrusivamente