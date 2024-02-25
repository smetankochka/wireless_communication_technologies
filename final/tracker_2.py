from client2server import client2server
import math


def parce_status(status, required):
    """required =   dx - смещение спутника на камере радара
                    status - состояние радара
                    position - положение радара
                    time - точное время на радаре в милисекундах с начала работы
                    all - все вышеперечисленное
    Возращает либо число либо словарь со значениями по ключам"""
    if isinstance(status, str):
        status = int(status)
    if required == "dx":
        dx = int(status) & 0x0fff
        return dx
    elif required == "status":
        status = (int(status) >> 12) & 0xf
        return status
    elif required == "position":
        position = (int(status) >> 16) & 0xf
        return position
    elif required == "time":
        time = (int(status) >> 20) & 0x1fff
        return time
    elif required == "radar_pos":
        radar_pos = int(status) >> 76 & 0x1fff
        return radar_pos
    elif required == "all":
        dx = status & 0x0fff
        status = (int(status) >> 12) & 0xf
        position = (int(status) >> 16) & 0xf
        time = (int(status) >> 20) & 0x1fff
        radar_pos = (int(status) >> 76) & 0x1fff
        all = {"dx": dx,
               "status": status,
               "position": position,
               "time": time,
               'radar_pos': radar_pos}
        return all


class tracker:
    def run(tracklog):

        try:

            tracklog.write(b"[0] Starting...")

            c2s = client2server()

            last_dx = 0
            last_time = 0

            radar_vel = 0

            tek_vel = 0

            sat_vel = 0

            tracklog.write(b"[+] Starting main loop...\n")

            while True:

                try:
                    status = parce_status(c2s.getStatus(), required='all')

                    dx = status['dx']
                    if dx > 2048:
                        dx -= 4096
                    stat = status['status']
                    pol = status['position']
                    time = status['time']
                    abs_cor = status['radar_pos']
                except:
                    tracklog.write(b"parcer_error. Sorry Max daun")
                    status = parce_status(c2s.getStatus())

                    dx = int(status) & 0x0fff
                    if dx > 2048:
                        dx -= 4096
                    stat = (int(status) >> 12) & 0xf
                    pol = (int(status) >> 16) & 0xf
                    time = int(status) >> 20
                if dx == -1536:
                    if pol == 4:
                        c2s.moveLeft(10)
                    elif pol == 3:
                        c2s.moveRight(10)
                    continue
                if time == last_time:
                    continue

                log = f"[{time}] dx={dx} sat_vel={sat_vel} radar_vel={radar_vel} tek_vel={tek_vel} pol={pol}\n"
                tracklog.write(log.encode())

                sat_vel += (dx - last_dx) / (time - last_time)

                radar_vel = dx / 2 + sat_vel / 3  # ПРИ / 5 ПОЛУЧАЕТСЯ 68%

                radar_vel = min(100, max(-100, radar_vel))

                if math.floor(radar_vel) != tek_vel:
                    tek_vel = min(100, max(-100, math.floor(radar_vel)))

                    if tek_vel > 0:
                        c2s.moveLeft(abs(tek_vel))
                    elif tek_vel < 0:
                        c2s.moveRight(abs(tek_vel))

                # if pol == 4:
                # 	tdx = 1000
                # 	while tdx > 500:
                # 		tdx = int(c2s.getStatus()) & 0x0fff
                # 		c2s.moveLeft(abs(tek_vel))
                # elif pol == 3:
                # 	tdx = 1000
                # 	while tdx > 500:
                # 		tdx = int(c2s.getStatus()) & 0x0fff
                # 		c2s.moveRight(abs(tek_vel))

                last_time = time
                last_dx = dx
        except Exception as e:
            import traceback
            exc = traceback.format_exc().encode()
            tracklog.write(exc)
