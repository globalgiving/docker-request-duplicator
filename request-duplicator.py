import os,sys,threading,socket
import time
import docker

BACKLOG = 500            # how many pending connections queue will hold
MAX_DATA_RECV = 999999  # max number of bytes we receive at once
DEBUG = True            # set to True to see the debug msgs
BLOCKED = []            # just an example. Remove with [""] for no blocking at all.
backends = []
docker_client = docker.DockerClient(base_url='unix://var/run/docker.sock')
SERVICE_NAME = os.environ['SERVICE_NAME']
SERVICE_PORT = int(os.environ['SERVICE_PORT'])

def main():
    # host and port info.
    host = ''               # blank for localhost

    print("Starting up on {}:{}".format(host,8080))

    updater = threading.Thread(target=backend_updater)
    updater.start()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, 8080))
        s.listen(BACKLOG)

    except socket.error as e:
        if s:
            s.close()
        print("Could not open socket: {}".format(e))
        sys.exit(1)

    while 1:
        conn, client_addr = s.accept()
        t = threading.Thread(target=proxy_thread, args=(conn, client_addr))
        t.start()

    s.close()

def backend_updater():
    while 1:
        print("Updating backend list")
        new_backends = []
        for service in docker_client.services.list(filters={"name":SERVICE_NAME}):
            for task in service.tasks():
                task_name = "{}.{}.{}".format(SERVICE_NAME, task['Slot'], task['ID'])
                print("Found service task: {}".format(task_name))
                new_backends.append(task_name)
        backends[:] = new_backends[:]
        time.sleep(60)

# A thread to handle request from browser
def proxy_thread(conn, client_addr):
    request = conn.recv(MAX_DATA_RECV)
    response = None

    try:
        for backend in backends:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((backend, SERVICE_PORT))
            s.send(request)

            save_data = False
            if response == None:
                response = []
                save_data = True

            while 1:
                data = s.recv(MAX_DATA_RECV)

                if len(data) <= 0:
                    break

                if save_data:
                    response.append(data)

            s.close()
        conn.send(response.join(""))
        conn.close()
    except socket.error:
        if s:
            s.close()
        if conn:
            conn.close()
        print("{}\t{}\t{}".format(client_addr[0], "Peer Reset", first_line))
        sys.exit(1)

if __name__ == '__main__':
    main()

