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


# Main
test_vectors_128 = {1: (0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0, 0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0)} # key, block

def cipher(block, ext_key):

    key_schedule = []
    current_round_key = ext_key
    round_state = block

    # Key schedule
    for rnd_cnt in range(ROUND_LIMIT):
        key_schedule.append(current_round_key >> 64)
        current_round_key = key_function(current_round_key, rnd_cnt + 1)

    # Feistel Network
    for rnd in range(ROUND_LIMIT - 1):
        upper_64 = (round_state >> 64)
        lower_64 = (round_state & 0xFFFFFFFFFFFFFFFF)
        rounded_lower = round_function(lower_64, key_schedule[rnd])
        rounded_upper = upper_64 ^ rounded_lower
        round_state = (rounded_upper + (lower_64 << 64))

    return(hex(round_state))

output = cipher(0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0, 0xF0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F0)
print(output)