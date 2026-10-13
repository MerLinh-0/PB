import csv

logs = []
with open("/home/merlin/PB/przetwarzanie-wizualizacja/small.log", newline='') as file:
    logreader = csv.reader(file, delimiter='\t')
    for log in logreader:
        logs.append(log)

# ile jest w nim linii
print(f"ile jest w nim linii: {len(logs)}")

# ile jest wpisów dla użytkownika bob i alice
bob = []
alice = []
for log in logs:
    if log[1] == "bob":
        bob.append(log)
    elif log[1] == "alice":
        alice.append(log)

print(f"ile jest wpisów dla użytkownika bob: {len(bob)} i alice: {len(alice)}")

# jaki jest łączny czas operacji dla ''boba'';
operation_time = 0
for b in bob:
    operation_time += int(b[5])

print(f"jaki jest łączny czas operacji dla ''boba'': {operation_time}")

# dla podanego użytkownika policzy łączne czasy jego operacji na każdym unikalnym serwerze (hoście)
user = input("podaj użytkownika: ")
time = {}
for log in logs:
    if log[1] == user:
        if log[0] not in time:
            time[log[0]] = int(log[5])
        else:
            time[log[0]] += int(log[5])

print(f"Dla użytkownika {user}:")
for host, t in time.items():
    print(f"Host: {host}, czas: {t}")
print(f"Łącznie: {sum(time.values())}")






