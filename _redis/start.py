import os

def start():
    cmd = """
        docker run --name %s \\
            -p %s:%s \\
            -d redis
        """ % (os.environ['REDIS_CONTAINER'],
            os.environ['REDIS_PORT'],
            os.environ['REDIS_PORT'])
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    start()