def expand_key(key, round_counter, s_box):
    key_bit = format(key, 'b')
    key_bit = (128-len(key_bit))*'0'+key_bit
    half = len(key_bit)//2
    key_a = key_bit[:half]
    key_b = key_bit[half:]
    new_key = key_b+key_a
    sub_0 = format(s_box[int(new_key[:4],2)],'b')
    sub_0 = (4-len(sub_0))*'0'+sub_0
    sub_1 = format(s_box[int(new_key[4:8],2)], 'b')
    sub_1 = (4-len(sub_1))*'0'+sub_1
    sub_3 = format(int(new_key[62:66],2)^round_counter, 'b')
    sub_3 = (4-len(sub_3))*'0'+sub_3
    new_key = sub_0+sub_1+new_key[8:62]+sub_3+new_key[66:]
    return (int(new_key,2))