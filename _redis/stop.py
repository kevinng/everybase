import os

def stop():
    cmd = 'docker stop ' + os.environ['REDIS_CONTAINER']
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    stop()