import os

def stop():
    cmd = 'docker stop ' + os.environ['PSQL_CONTAINER']
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    stop()