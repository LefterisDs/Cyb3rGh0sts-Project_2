cnt = 0
i = 0
while True:
    if '7' in list(str(i*7)):
        cnt = cnt + 1

    if cnt == 48:
        print(i*7)
        break

    i = i + 1