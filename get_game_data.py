import sys
import os
import shutil
import json
import subprocess

GAME_DIR_PATTERN = "game"
GO_EXTENSION = "go"
COMPILE_COMMAND = ["go", "build"]

def fullPath(path):
    cwd = os.getcwd()
    full_path = os.path.join(cwd, path)
    return full_path

def findGamePaths(source):
    game_paths = []
    for root,dirs,files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source,directory)
                game_paths.append(path)
        break
    return game_paths

def createDir(target):
    if not os.path.exists(target):
        os.mkdir(target) 

def cleanupNames(game_paths):
    clean_names = []
    for path in game_paths:
        _,dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(GAME_DIR_PATTERN,"")
        clean_names.append(new_dir_name)
    
    return clean_names

def copyToTarget(game_path, target_path):
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    shutil.copytree(game_path,target_path)

def makeJsonFile(file_name, game_paths):
    data = {
        "game_names":game_paths,
        "number_of_games":len(game_paths)
    }
    with open(file_name,"w") as f:
        json.dump(data,f)

def compileAndRun(target_path):
    code_file_name = None
    for root,dir,files in os.walk(target_path):
        for file in files:
            if file.endswith(GO_EXTENSION):
                code_file_name = file
                break
        break

    if code_file_name is None:
        return

    command = COMPILE_COMMAND + [code_file_name]
    runCommand(command,target_path)

def runCommand(command, target_path):
    cwd =os.getcwd()
    os.chdir(target_path)
    result = subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    print(result)
    os.chdir(cwd)


if __name__ == "__main__":
    args = sys.argv
    if len(args)!=3:
        raise Exception("Source / Target directory not provided ")
    source, target = args[1:]
    source =fullPath(source)
    target = fullPath(target)
    game_paths = findGamePaths(source)
    clean_names = cleanupNames(game_paths)
    
    createDir(target)

    for game_path, clean_name in zip(game_paths,clean_names):
        target_path = os.path.join(target,clean_name)
        copyToTarget(game_path,target_path)
        compileAndRun(target_path)
    
    json_path = os.path.join(target,"metadata.json")
    makeJsonFile(json_path,game_paths)

