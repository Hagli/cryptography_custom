def create_p_box():
    #kek = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15]
    a = []
    for i in range(64):
        a.append(i)
    random.seed(1)
    random.shuffle(a)
    return(a)

def permutate(plainbit, p_box):
    plainbit = format(plainbit, 'b')
    shadowbit = plainbit
    for i in range(64):
        plainbit[i] = shadowbit[s_box[i]]
    return plainbit