import sys
import os

def worker(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)
    print("source path: ",source_path)
    print("target path: ",target_path)

if __name__ == "__main__":
    args = sys.argv
    if len(args)!=3:
        raise Exception("Source / Target directory not provided ")

    
    source, target = args[1:]
    worker(source, target)