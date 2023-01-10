import glob
import os

os.path.isfile('./final_data.csv')
os.chdir("account")

total = []
if os.path.isfile('total.txt'):
    with open(f"total.txt") as f:
        lines = f.read().splitlines()
        total.extend(lines)

for file in glob.glob("account*.txt"):
    with open(f"{file}") as f:
        lines = f.read().splitlines()
        total.extend(lines)
unique_list = list(set(total))
print("total:", len(unique_list))
save_file = open("total.txt", "w")
for item in unique_list:
    save_file.write("%s\n" % item)
