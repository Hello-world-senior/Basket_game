import socket
import asyncio
import pyray
import raylib
from raylib import colors

class Settings:
    WIDTH = 800
    HEIGHT = 600
    bg_color = raylib.WHITE
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Wpressed = False
    Spressed = False
    UPpressed = False
    DOWNpressed = False
class Object:
    def __init__(self, pos: list):
        self.pos = pos

    def event(self):
        pass

    def logic(self):
        pass

    def draw(self):
        pass

class Wall(Object):
    def __init__(self, pos: list, wasd: bool, stlk: bool):
        super().__init__(pos)
        self.speed = [0, 0]
        self.wasd = wasd
        self.stlk = stlk
    def event(self):
        if Settings.Wpressed:
            self.speed[1] = -6
            Settings.Wpressed = False
        if Settings.Spressed:
            self.speed[1] = -6
            Settings.Spressed = False
        if Settings.UPpressed:
            self.speed[1] = -6
            Settings.UPpressed = False
        if Settings.DOWNpressed:
            self.speed[1] = 6
            Settings.DOWNpressed = False
        if self.wasd:
            if pyray.is_key_down(raylib.KEY_S):
                self.speed[1] = 6
                set("S")
                print("SSSSSSSSSS")
            if pyray.is_key_down(raylib.KEY_W) :
                self.speed[1] = -6
                set("W")
                print("WWWWWWWWWWW")
        if self.stlk:
            if pyray.is_key_down(raylib.KEY_UP):
                self.speed[1] = -6
                set("UP")
                print("UUUUUUUUUPPPPPP")
            if pyray.is_key_down(raylib.KEY_DOWN):
                self.speed[1] = 6
                set("DOWN")
                print("DOOOOOOOOWN")

    def servevent(self):
        if self.wasd:
            if pyray.is_key_down(raylib.KEY_S):
                set("S")
                print("SSSSSSSSSS")
            if pyray.is_key_down(raylib.KEY_W) :
                set("W")
                print("WWWWWWWWWWW")
        if self.stlk:
            if pyray.is_key_down(raylib.KEY_UP):
                set("UP")
                print("UUUUUUUUUPPPPPP")
            if pyray.is_key_down(raylib.KEY_DOWN):
                set("DOWN")
                print("DOOOOOOOOWN")
    def logic(self):
        if self.pos[1] >= Settings.HEIGHT-145 and self.speed[1] > 0:
           self.pos[1] = self.pos[1]
        elif self.pos[1] < 5 and self.speed[1] < 0:
            self.pos[1] = self.pos[1]
        else:
            self.pos[1] += self.speed[1]

    def draw(self):
        pyray.draw_rectangle(self.pos[0], self.pos[1], 25, 145, colors.BLACK)


class Ball(Object):
    def __init__(self, pos: list, path: str, dxy: list):
        super().__init__(pos)
        self.pos = pos
        self.path = path
        self.speed = [0, 0]
        self.dx = dxy[0]
        self.dy = dxy[1]
        image = pyray.load_image(path)
        # pyray.image_resize(image, 10, 10)
        self.texture = pyray.load_texture_from_image(image)
        pyray.unload_image(image)

    def event(self):
        self.pos[0] += self.dx
        self.pos[1] += self.dy

    def logic(self):
        if self.pos[0] >= Settings.WIDTH - 90:
            self.dx = -5
        if self.pos[0] <= 0:
            self.dx = 5
        if self.pos[1] >= Settings.HEIGHT - 90:
            self.dy = -5
        if self.pos[1] <= 0:
            self.dy = 5


    def draw(self):
        pyray.draw_texture(self.texture, *self.pos, colors.WHITE)

async def udp_listener():
    print("Starting UDP listener...")
    loop = asyncio.get_event_loop()
    print("Task 3 is running")
    # Создаем UDP-сервер и привязываем его к адресу и порту
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPProtocol(),
        local_addr=(server_ip, server_port)
    )

    try:
        while True:
             pass
    finally:
        transport.close()


# Протокол для обработки пакетов (UDP)
class UDPProtocol:
    def datagram_received(self, data, addr):
        asyncio.create_task(get(data, addr))
async def get(data, addr):
    #while True:
        #data, server_address = Settings.client_socket.recvfrom(max_buffer)
    print(data.decode())
    if data.decode() == "W":
        Settings.Wpressed = True
        print("YEEEEEEEEEEEES")
    if data.decode() == "S":
        Settings.Spressed = True
    if data.decode() == "DOWN":
        print("YEEEEEEEEEEEES")
        Settings.DOWNpressed = True
    if data.decode() == "UP":
        Settings.UPpressed = True
        print("YEEEEEEEEEEEES")
    print("Task 1 is running")


def set(info: str):
    Settings.client_socket.sendto(info.encode(), (server_ip, server_port))


async def main():
    message = input("Введите никнейм:")
    Settings.client_socket.sendto(message.encode(), (server_ip, server_port))
    while True:
        data, server_address = Settings.client_socket.recvfrom(max_buffer)
        if data.decode() == "READY":
            print("READY")
            pyray.set_target_fps(30)
            w, h = Settings.WIDTH, Settings.HEIGHT
            left_goal = 0
            right_goal = 0
            pyray.init_window(w, h, f'Tennis I {left_goal} : II {right_goal}')
            b = Ball([400, 300], "basketball.png", [5, 5])
            objects = [
                Wall([5, 190], True, False),
                Wall([770,  190], False, True)
            ]
            await asyncio.gather(
                method_name(b, left_goal, objects, right_goal),
                udp_listener()
            )



async def method_name(b, left_goal, objects, right_goal):
    while not pyray.window_should_close():

        for obj in objects:  # Event
            obj.event()
        b.event()
        for obj in objects:  # Logic
            obj.logic()
        if b.pos[0] - 30 == objects[0].pos[0] and b.pos[1] >= objects[0].pos[1] and b.pos[1] <= objects[0].pos[1] + 145:
            b.dx = 10
            left_goal += 1

        if b.pos[0] + 90 == 770 and b.pos[1] >= objects[1].pos[1] and b.pos[1] <= objects[1].pos[1] + 145:
            b.dx = -10
            right_goal += 1
        b.logic()

        pyray.begin_drawing()  # Drawing
        pyray.clear_background(Settings.bg_color)
        pyray.set_window_title(f'Tennis I {left_goal} : II {right_goal}')
        for obj in objects:
            obj.draw()
        b.draw()
        pyray.end_drawing()
        print("Task 2 is running")
    pyray.close_window()


if __name__ == "__main__":
    asyncio.run(main())
