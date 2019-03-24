led_mask = '(+32)077000505'

vko = open(r'/Volumes/data/PycharmProjects/ICC_connections/fv_vko_numbers.csv', 'r')
vko_nums = ['(+32)0' + line.split(',')[0][2:] for line in vko.readlines()]
vko.close()

full = open(r'/Volumes/data/PycharmProjects/ICC_connections/Traffic_Jan_2019/User Connections(1).csv', 'r')
table = [line.replace('"','').split(',') for line in full.readlines()]
head = table[0]
table = table[1:]

vko_table = open(r'connections_vko.csv', 'w')
led_table = open(r'connections_led.csv', 'w')
svo_table = open(r'connections_svo.csv', 'w')

def list_to_str(li):
    return ','.join(li)

vko_table.write(list_to_str(head))
led_table.write(list_to_str(head))
svo_table.write(list_to_str(head))

users_svo = []
users_led = []
users_vko = []
tx_svo, rx_svo = 0,0
tx_led, rx_led = 0,0
tx_vko, rx_vko = 0,0
svo, led, vko = 0,0,0

for line in table:
    if led_mask in line[1]:
        led_table.write(list_to_str(line))
        users_led.append(line[1])
        tx_led += int(line[4]) if line[4].isdigit() else 0
        rx_led += int(line[5]) if line[5].isdigit() else 0
        led += 1
    elif line[1] in vko_nums:
        vko_table.write(list_to_str(line))
        users_vko.append(line[1])
        tx_vko += int(line[4]) if line[4].isdigit() else 0
        rx_vko += int(line[5]) if line[5].isdigit() else 0
        vko += 1
    else:
        svo_table.write(list_to_str(line))
        users_svo.append(line[1])
        tx_svo += int(line[4]) if line[4].isdigit() else 0
        rx_svo += int(line[5]) if line[5].isdigit() else 0
        svo += 1

vko_table.close()
led_table.close()
svo_table.close()
print(len(table), ' = ', vko + svo + led)
ans = 'tx GB: {tx}\nrx GB: {rx}\nactive users: {users}'
print('\nLED\n' + ans.format(tx=tx_led/(10**9), rx=rx_led/(10**9), users=len(set(users_led))))
print('\nVKO\n' + ans.format(tx=tx_vko/(10**9), rx=rx_vko/(10**9), users=len(set(users_vko))))
print('\nSVO\n' + ans.format(tx=tx_svo/(10**9), rx=rx_svo/(10**9), users=len(set(users_svo))))
