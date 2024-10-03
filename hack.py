import re
import subprocess
import time
import numpy as np
import pygame

shell_command = ['./main']
proc = subprocess.Popen(shell_command)
pid = proc.pid

time.sleep(1)

maps_fname = f'/proc/{pid}/maps'
mem_fname = f'/proc/{pid}/mem'

with open(maps_fname, 'r') as f:
    for line in f:
        m = re.match(r'([0-9a-f]+)-([0-9a-f]+) ([-r])', line)
        if 'stack' in line and m.group(3) == 'r':
            start = int(m.group(1), 16)
            end = int(m.group(2), 16)
            break

print(f'stack start: {start:x}, end: {end:x}')
addr = start
mem_file = open(mem_fname, 'rb+')
mem_file.seek(start)
mem = mem_file.read(end - start)
data = np.frombuffer(mem, dtype=np.uint8)
player_offset = (data.reshape(-1, 8) == np.array([0x00, 0x07, 0x00, 0x06] * 2, dtype=np.uint8).reshape(1, 8)).all(1).nonzero()[0][0] * 8 - 6
boss_offset = player_offset + 9 * 2
bomb_offset = boss_offset + 9 * 2
player_hp_offset = player_offset - 0x125b2 + 0x14123

def read_mem(offset, nbytes):
    mem_file.seek(addr + offset)
    return mem_file.read(nbytes)

def write_mem(offset, data):
    mem_file.seek(addr + offset)
    mem_file.write(data)

def print_hex(data):
    print(list(map(hex, data)))

def get_bombs():
    bomb_size = 20
    used_offset = 2
    i = 0
    bombs = []
    while 1:
        boffset = bomb_offset + i * bomb_size
        bomb_used = read_mem(boffset + used_offset, 1)[0]
        if bomb_used: 
            bombs.append(boffset)
        else:
            break
        i += 1
    return bombs

pygame.mixer.init()
pygame.mixer.music.load('res/BGM/bomb.ogg')
pygame.mixer.music.play(-1)

bomb_audio = pygame.mixer.Sound('res/SE/X10_01.wav')

old_bombs = []
while True:
    bombs = get_bombs()
    if False:
        if len(bombs) == 0:
            write_mem(boss_offset + 6, b'\x00\x04\x00\x04')
        else:
            bomb_xy = read_mem(bombs[0] + 8, 4)
            write_mem(boss_offset + 6, bomb_xy)
    if len(set(old_bombs) - set(bombs)) > 0:
        bomb_audio.play()
    old_bombs = bombs
    write_mem(player_hp_offset, b'\x05')
    time.sleep(0.1)
