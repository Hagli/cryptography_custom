def create_s_box() :
    # transform integer to its multiplicative inverse in the field
    transform_map = [0, # 0 is mapped to itself, it should not have any multiplicative inverse
                     1, 9, 14, 13, 11, 7, 6, 15, 4, 12, 5, 10, 4, 3, 8]
    for i in range(len(transform_map)):
        x = transform_map[i]
        x = x^(x << 1)^(x << 2)^(x << 3)^(x << 4)^3
        x = x & 15
        transform_map[i] = x
    return(transform_map)

def substitute(plainbit, s_box): #plainbit in 64 bit
    a = 0
    for i in range(16):
        l = s_box[(plainbit >> i*4) & 15]
        a = a^(l << i*4)
    return (a)