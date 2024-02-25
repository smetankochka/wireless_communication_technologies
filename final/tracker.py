from client2server import client2server


def parce_status(status):
    dx = int(status) & 0x0fff
    sost = (int(status) >> 12) & 0xf
    position = (int(status) >> 16) & 0xf
    time = (int(status) >> 20) & 0x1fff
    radar_pos = ((int(status) >> 76) & 0x1fff) - 1000
    all = {"dx": dx,
           "status": sost,
           "position": position,
           "time": time,
           'radar_pos': radar_pos}
    return all


def check_right(rad_cors):
    right_prep = 250
    return rad_cors >= right_prep


def check_left(rad_cors):
    left_prep = -223
    return rad_cors <= left_prep


class tracker:
    def run(tracklog):
        try:
            try:
                tracklog.write(b"[0] Starting...")
                c2s = client2server()
            except:
                tracklog.write(b"Error before loop")
            tracklog.write(b"[+] Starting main loop...\n")

            while True:
                status = c2s.getStatus()
                parced_status = parce_status(status)

                try:
                    dx = parced_status['dx']
                    if dx > 2048:
                        dx -= 4096
                    stat = parced_status['status']
                    pol = parced_status['position']
                    time = parced_status['time']
                    abs_cor = parced_status['radar_pos']
                    log = f"time: {parced_status['time']}, dx: {parced_status['dx']}, radar_pos: {parced_status['radar_pos']}"
                    tracklog.write(log.encode())
                    log = "\n"
                    tracklog.write(log.encode())
                except:
                    tracklog.write(b"parcer_error. Sorry Max daun")
                    tracklog.write(str(int(status)).encode())
                    tracklog.write("\n".encode())
                    continue
                # end of logging part

                # start of moving part
                try:
                    if dx == -1536:
                        if pol == 4:
                            c2s.moveLeft(50)
                        elif pol == 3:
                            c2s.moveRight(50)

                    # Здесь надо подобрать значения
                    value = 30

                    if dx > value:
                        if pol == 2:
                            c2s.Stop()
                            status = c2s.moveLeft(50)
                        else:
                            status = c2s.moveLeft(50)

                        # Пересчет статуса
                            # parced_status = parce_status(status)
                            # dx = parced_status['dx']
                            # if dx > 2048:
                            #     dx -= 4096
                            # stat = parced_status['status']
                            # pol = parced_status['position']
                            # time = parced_status['time']
                            # abs_cor = parced_status['radar_pos']
                            # # Конец пересчета статуса
                            #
                            # if check_left(abs_cor):
                            #     c2s.Stop()

                    if dx < -value:
                        if pol == 1:
                            status = c2s.Stop()
                            status = c2s.moveRight(80)
                        else:
                            status = c2s.moveRight(80)

                        # Пересчет статуса
                            # parced_status = parce_status(status)
                            # dx = parced_status['dx']
                            # if dx > 2048:
                            #     dx -= 4096
                            # stat = parced_status['status']
                            # pol = parced_status['position']
                            # time = parced_status['time']
                            # abs_cor = parced_status['radar_pos']
                        # Конец пересчета статуса

                        # if check_right(abs_cor):
                        #     c2s.Stop()
                except:
                    tracklog.write(b"moving_error")
                    tracklog.write("\n".encode())

        except Exception as e:
            import traceback
            exc = traceback.format_exc().encode()
            tracklog.write(exc)