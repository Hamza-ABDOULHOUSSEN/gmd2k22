import os
import sys
import subprocess

BASE_PATH = os.getcwd()   #python folder

def omim_search(query):
    content = []

    os.chdir("./../java_lucene_index")

    #process = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen("./launch.sh omim "+query, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")

    lines = stdout.splitlines()

    for line in lines:
        table = line.split('#-#')
        content.append(table)

    os.chdir(BASE_PATH)

    return content

def main():
    #default query
    query = "\"omim_id : 100300\""

    argc = len(sys.argv)
    if (argc > 1):
        query = sys.argv[1]
        query = f'"{query}"'

    content = omim_search(query)
    n = len(content)

    print(f"result : {n}")

    if (n>0):
        elem = content[0]
        print(f"omim_id : {elem[0]}")
        print(f"field0 : {elem[1]}")
        print(f"field1 : {elem[2]}")
        print(f"symptoms : {elem[3]}")

if __name__ == '__main__':
    main()
