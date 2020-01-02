import os

def start():
    cmd = """
        docker run --name %s \\
            -e POSTGRES_USER=%s \\
            -e POSTGRES_PASSWORD=%s \\
            -e POSTGRES_DB=%s \\
            -p %s:%s \\
            -d postgres
        """ % (os.environ['PSQL_CONTAINER'],
            os.environ['PSQL_USER'],
            os.environ['PSQL_PASSWORD'],
            os.environ['PSQL_NAME'],
            os.environ['PSQL_PORT'],
            os.environ['PSQL_PORT'])
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    start()