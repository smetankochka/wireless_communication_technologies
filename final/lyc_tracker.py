from client2server import client2server
from math import sqrt


class tracker:
    prev_error = 0
    tracklog = None
    prev_t = 0
    I = 0
    prev_speed = 0
    prev_dur = 1

    def pid(value, target, coefs, dt=1, constrains=(-100, 100)):
        kp, ki, kd = coefs
        P = target - value
        I = (tracker.I + P)
        D = (P - tracker.prev_error)

        tracker.I = I
        tracker.prev_error = P

        P *= kp
        I *= ki
        D *= kd

        out = P + I + D
        out = round(out)
        tracker.tracklog.write(f'{P=} {I=} {D=} {out=}\n'.encode())
        out = min(out, constrains[1])
        out = max(out, constrains[0])

        return out

    def parse_status(status: int):
        # dx = status & 0x0FFF
        # if dx > 2048:
        #     dx = dx - 4096
        # return dx, 0

        status = bin(status + 2 ** 90)[3:][::-1]
        dx_bin = status[:12]
        radar_status_bin = status[12:16]
        radar_position_bin = status[16:20]
        time_bin = status[20:37]
        coordinate_bin = status[76:89]

        dx = int(dx_bin[::-1], 2)
        if dx > 2048:
            dx = dx - 4096
        radar_status = int(radar_status_bin[::-1], 2)
        radar_position = int(radar_position_bin[::-1], 2)
        time = int(time_bin[::-1], 2)
        coordinate = int(coordinate_bin[::-1], 2)

        return dx, radar_status, radar_position, time, coordinate

    def move(c2s, speed: int):
        if tracker.prev_speed < 0 and speed > 0:
            speed *= 1.1
        if tracker.prev_speed > 0 and speed < 0:
            speed *= 1.1
        speed = round(speed)

        if speed > 0:
            c2s.moveRight(speed)
        elif speed < 0:
            c2s.moveLeft(-speed)
        else:
            c2s.moveStop()

    def tick(c2s, tracklog):
        status = int(c2s.getStatus())
        dx, radar_status, radar_position, time, coordinate = tracker.parse_status(status)
        if time == tracker.prev_t:
            return
        dt = time - tracker.prev_t
        tracker.prev_t = time
        tracklog.write(f"{dx=} {dt=} {radar_status=} {radar_position=} {time=} {coordinate=}\n".encode())
        if abs(dx) > 500:
            c2s.moveStop()
            tracker.I = 0
            return
        # P = 0.27
        # I = 0.00675
        # D = 0.027
        #
        target = 0
        if tracker.prev_dur == -1:
            if dx <= 10:
                target = 10
            else:
                tracker.prev_dur = 1
        else:
            if dx >= -10:
                target = -10
            else:
                tracker.prev_dur = -1
        # target = -dx / 10

        speed = tracker.pid(dx, target, (0.67, 0.000730, 1.3), dt) * 1.3
        tracklog.write(f"speed: {speed}\n".encode())

        tracker.move(c2s, speed)

    def run(tracklog, c2s=None):
        tracklog.write(f'Atempt 4. Team 6\n'.encode())
        is_simulation = True
        if c2s is None:
            is_simulation = False
            c2s = client2server()
        tracker.tracklog = tracklog
        i = 0
        if is_simulation:
            tracker.tick(c2s, tracklog)
            return
        while i == 0:
            tracker.tick(c2s, tracklog)
