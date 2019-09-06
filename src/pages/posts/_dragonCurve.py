# n is int >= 1
# base is array of angles
# mirrored is a boolean
def getTurn(base, n, mirrored):
    baseSize = len(base) + 1

    while n % baseSize == 0:
        n //= baseSize

    if mirrored:
        if (n // baseSize) % 2 == 0:
            return base[n % baseSize - 1]
        else:
            return -base[len(base) - n % baseSize]
    else:
        return base[n % baseSize - 1]

print([getTurn([90], n, True) for n in range(1, 8)])
# [90, 90, -90, 90, 90, -90, -90]

print([getTurn([90, 60], n, False) for n in range(1, 9)])
# [90, 60, 90, 90, 60, 60, 90, 60]