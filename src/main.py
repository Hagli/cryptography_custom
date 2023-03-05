# coding: utf-8
from __future__ import print_function
from S_box import create_s_box

s_box = create_s_box()

p_layer_order = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51, 4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38,
                 54, 7, 23, 39, 55, 8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59, 12, 28, 44, 60, 13,
                 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]

block_size = 64
ROUND_LIMIT = 16

def round_function(state, key):
    # XOR block with key
    new_state = state ^ key

    # S_box
    state_nibs = []
    for x in range(0, block_size, 4):
        nib = (new_state >> x) & 0xF
        sb_nib = s_box[nib]
        state_nibs.append(sb_nib)

    state_bits = []
    for y in state_nibs:
        nib_bits = [1 if t == '1'else 0 for t in format(y, '04b')[::-1]]
        state_bits += nib_bits

    # P_box
    state_p_layer = [0 for _ in range(64)]
    for p_index, std_bits in enumerate(state_bits):
        state_p_layer[p_layer_order[p_index]] = std_bits

    round_output = 0
    for index, ind_bit in enumerate(state_p_layer):
        round_output += (ind_bit << index)
    
    return round_output

def key_function(key, round_count):

    r = [1 if t == '1'else 0 for t in format(key, '0128b')[::-1]]
    # rotate key
    h = r[-61:] + r[:-61]
    round_key_int = 0
    for index, ind_bit in enumerate(h):
        round_key_int += (ind_bit << index)

    # S box 8-bit MSB
    upper_nibble = (round_key_int >> 124) & 0xF
    second_nibble = (round_key_int >> 120) & 0xF
    upper_nibble = s_box[upper_nibble]
    second_nibble = s_box[second_nibble]

    # XOR with round_counter
    xor_portion = ((round_key_int >> 62) & 0x1F) ^ round_count

    # combine
    round_key_int = (round_key_int & 0x00FFFFFFFFFFFFF83FFFFFFFFFFFFFFF) + (upper_nibble << 124) + (second_nibble << 120) + (xor_portion << 62)
    return round_key_int


# 128-bit Encrypt and Decrypt
def encrypt(block, ext_key):

    key_schedule = []
    current_round_key = ext_key
    round_state = block

    # Key schedule
    for rnd_cnt in range(ROUND_LIMIT):
        key_schedule.append(current_round_key >> 64)
        current_round_key = key_function(current_round_key, rnd_cnt + 1)

    # Feistel Network
    for rnd in range(ROUND_LIMIT):
        upper_64 = (round_state >> 64)
        lower_64 = (round_state & 0xFFFFFFFFFFFFFFFF)
        rounded_lower = round_function(lower_64, key_schedule[rnd])
        rounded_upper = upper_64 ^ rounded_lower
        round_state = (rounded_upper + (lower_64 << 64))

    return(hex(round_state))

def decrypt(block, ext_key):

    key_schedule = []
    current_round_key = ext_key
    round_state = block

    # Key schedule
    for rnd_cnt in range(ROUND_LIMIT):
        key_schedule.append(current_round_key >> 64)
        current_round_key = key_function(current_round_key, rnd_cnt + 1)

    # Feistel Network
    for rnd in reversed(range(ROUND_LIMIT)):
        upper_64 = (round_state >> 64)
        lower_64 = (round_state & 0xFFFFFFFFFFFFFFFF)
        rounded_upper = round_function(upper_64, key_schedule[rnd])
        prev_upper = lower_64 ^ rounded_upper
        round_state = (upper_64 + (prev_upper << 64))

    return(hex(round_state))

# String Encrypt and Decrypt
def string_encrypt(string, key):
    arr = bytes(string, 'ascii')

    blocks = []
    for i in range(0, len(arr), 4):
        blocks.append(int.from_bytes(arr[i:i+4], 'big'))

    enc_blocks = []
    for block in blocks:
        res = encrypt(block, key)
        enc_blocks.append(int(res, 0))
    
    enc_stream = b''
    for block in enc_blocks:
        enc_stream += int.to_bytes(block, 16, 'big')

    return enc_stream

def string_decrypt(byte_stream, key):

    blocks = []
    for i in range(0, len(byte_stream), 16):
        blocks.append(int.from_bytes(byte_stream[i:i+16], 'big'))

    dec_blocks = []
    for block in blocks:
        res = decrypt(block, key)
        dec_blocks.append(int(res, 0))

    dec_string = ''
    for block in dec_blocks:
        dec_string += int.to_bytes(block, 16, 'big').decode('ascii')

    return dec_string


### Main
import time
string = open('beemovie double.txt', 'r').read()

start_time = time.time()

test_enc = string_encrypt(string, 0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0)
#print(test_enc)
test_dec = string_decrypt(test_enc, 0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0)

print("--- %s seconds ---" % (time.time() - start_time))