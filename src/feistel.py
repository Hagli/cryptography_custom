import substitue
import permutate
import expand_key

def feistel_single_round(key, block, s_box, p_box, round_counter): # block = key = integer 128 bit
    upper_64 = (round_state >> 64)
    lower_64 = (round_state & 0xFFFFFFFFFFFFFFFF)
    keyround = expand_key(key, round_counter, s_box)
    lower_64 = lower_64^keyround
    lower_64 = substitue(lower_64, s_box)
    lower_64 = permutate(lower_64, p_box)
    rounded_upper = upper_64 ^ rounded_lower
    round_state = (rounded_upper + (lower_64 << 64))
    return round_state