import os

def rm():
    cmd = 'docker rm ' + os.environ['PSQL_CONTAINER']
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    rm()