#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

def incoming_connections():
    """Configuration des clients entrant - connection"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s connected." % client_address)
        client.send(bytes("Greeting from the cave!Now type your name and press enter!","utf8"))
        addresses[client]=client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    """manip de la config de la connection d'un seul client""" 

    name = client.recv(BUFSIZ).decode('utf8')
    welcome = 'Welcome %s! If you want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = '%s has joined the chat!' % name
    broadcast(bytes(msg,"utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}","utf8"):
            broadcast(msg,name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del client[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def broadcast(msg, prefix=""):
    """envoie des msg au clients"""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5) #nous allons faire un max de 5 connections
    print("Waiting for connection...")
    ACCEPT_THREAD= Thread(target=incoming_connections)
    ACCEPT_THREAD.start() #boucle infinir pour laisser le serveur en arriere-plan
    ACCEPT_THREAD.join()
    SERVER.close()