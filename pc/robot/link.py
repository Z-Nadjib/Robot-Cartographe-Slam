# link.py — communication UDP avec le robot
import socket

class Link:
    def __init__(self, robot_ip, port_rx=5005, port_tx=5006):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", port_rx))
        self.sock.setblocking(False)
        self.robot = (robot_ip, port_tx)

    def send(self, msg):
        self.sock.sendto(msg.encode(), self.robot)

    def poll(self):
        """Renvoie la liste des messages reçus depuis le dernier appel (listes de champs)."""
        msgs = []
        while True:
            try:
                data, _ = self.sock.recvfrom(2048)
            except BlockingIOError:
                break
            except ConnectionResetError:        # Windows : robot pas encore à l'écoute
                continue
            msgs.append(data.decode(errors="ignore").strip().split(","))
        return msgs
