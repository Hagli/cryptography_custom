from S_box import substitute
from P_box import permute
from Key_expansion import expand_key

def feistel_single_round(key, round_state, s_box, p_box, round_counter): # block = key = integer 128 bit
    upper_64 = (round_state >> 64)
    lower_64 = (round_state & 0xFFFFFFFFFFFFFFFF)
    keyround = expand_key(key, round_counter, s_box)
    rounded_lower = lower_64^keyround
    rounded_lower = substitute(rounded_lower, s_box)
    rounded_lower = permute(rounded_lower, p_box)
    rounded_upper = upper_64 ^ rounded_lower
    round_state = (rounded_upper + (lower_64 << 64))
    return round_state