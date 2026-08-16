#!/usr/bin/env python3
"""TCP bridge for Lara gripper servo (Dynamixel-style protocol on /dev/ttyACM0).

Deploy on hrg-desktop (replaces /home/hrg/Robotum/robot_gripper.py):
  scp src/xyz_motion/robot_gripper_server.py hrg@192.168.2.13:/home/hrg/Robotum/robot_gripper.py

Commands (one per TCP message, lowercase unless numeric):
  open              - fully open (goal POS_OPEN)
  close             - fully close (goal POS_CLOSE)
  close_until_stall - step closed until load/position stall (unknown object size)
  <integer>         - move to that Dynamixel goal position (e.g. 600..1500)
"""
import socket
import serial
import time

PORT = "/dev/ttyACM0"
BAUD = 1_000_000
SERVO_ID = 6
POS_OPEN = 1500
POS_CLOSE = 600
MOVE_TIME_MS = 800

ADDR_GOAL_POS = 0x2A
ADDR_PRESENT_POSITION = 0x24
ADDR_PRESENT_LOAD = 0x28
INST_WRITE = 0x03
INST_READ = 0x02

# Adaptive close tuning
CLOSE_STEP = 35
CLOSE_STEP_TIME_MS = 250
LOAD_STALL_THRESHOLD = 70
POSITION_EPS = 8


def checksum_sum(s):
    return (~(s & 0xFF)) & 0xFF


def packet(sid, inst, params):
    length = len(params) + 2
    body = [sid, length, inst] + params
    return bytes([0xFF, 0xFF] + body + [checksum_sum(sum(body))])


def write_regs(ser, sid, start_addr, data_bytes):
    ser.write(packet(sid, INST_WRITE, [start_addr] + data_bytes))
    ser.flush()


def read_register(ser, sid, addr, nbytes=2):
    ser.reset_input_buffer()
    ser.write(packet(sid, INST_READ, [addr, nbytes]))
    time.sleep(0.01)
    buf = ser.read(32)
    if len(buf) < 7 or buf[0] != 0xFF or buf[1] != 0xFF:
        return None
    if buf[2] != sid or buf[4] != 0:
        return None
    return buf[5] | (buf[6] << 8)


def move_to(ser, sid, pos, time_ms, speed=0):
    pos = max(0, min(4095, int(pos)))
    time_ms = max(0, min(0xFFFF, int(time_ms)))
    data = [
        pos & 0xFF,
        (pos >> 8) & 0xFF,
        time_ms & 0xFF,
        (time_ms >> 8) & 0xFF,
        speed & 0xFF,
        (speed >> 8) & 0xFF,
    ]
    write_regs(ser, sid, ADDR_GOAL_POS, data)


def close_until_stall(ser, sid):
    """Close in small steps until load rises or position stops changing."""
    pos = read_register(ser, sid, ADDR_PRESENT_POSITION)
    if pos is None:
        pos = POS_OPEN
        move_to(ser, sid, pos, MOVE_TIME_MS)
        time.sleep(MOVE_TIME_MS / 1000.0 + 0.05)

    print(f"[INFO] close_until_stall start pos={pos}")
    while pos > POS_CLOSE:
        target = max(POS_CLOSE, pos - CLOSE_STEP)
        move_to(ser, sid, target, CLOSE_STEP_TIME_MS, speed=150)
        time.sleep(CLOSE_STEP_TIME_MS / 1000.0 + 0.08)

        load = read_register(ser, sid, ADDR_PRESENT_LOAD)
        new_pos = read_register(ser, sid, ADDR_PRESENT_POSITION)
        if load is not None and load >= LOAD_STALL_THRESHOLD:
            print(f"[INFO] stall by load={load} at pos~{new_pos}")
            break
        if new_pos is not None:
            if target < pos and abs(new_pos - pos) <= POSITION_EPS:
                print(f"[INFO] stall by position pos={new_pos} (cmd {target})")
                break
            pos = new_pos
        else:
            pos = target

    print(f"[INFO] close_until_stall done pos~{pos}")


def handle_command(ser, cmd):
    if cmd == "open":
        print("-> OPEN gripper")
        move_to(ser, SERVO_ID, POS_OPEN, MOVE_TIME_MS)
    elif cmd == "close":
        print("-> CLOSE gripper")
        move_to(ser, SERVO_ID, POS_CLOSE, MOVE_TIME_MS)
    elif cmd == "close_until_stall":
        print("-> CLOSE_UNTIL_STALL")
        close_until_stall(ser, SERVO_ID)
    else:
        try:
            pos = int(cmd)
            print(f"-> MOVE gripper to {pos}")
            move_to(ser, SERVO_ID, pos, MOVE_TIME_MS)
        except ValueError:
            print(f"[WARN] unknown command: {cmd}")


def main():
    ser = serial.Serial(PORT, BAUD, timeout=0.05)
    print(f"[INFO] Serial {PORT} @ {BAUD}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 5000))
    sock.listen(5)
    print("[INFO] Listening on port 5000")

    while True:
        conn, addr = sock.accept()
        print(f"[INFO] Client {addr}")
        with conn:
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                cmd = chunk.decode(errors="replace").strip().lower()
                if cmd:
                    handle_command(ser, cmd)


if __name__ == "__main__":
    main()
