import csv
import re
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

contacts_dict = {}

for row in contacts_list[1:]:
    fio_parts = " ".join (row [:3]).split()

    if len(fio_parts) >= 3:
        key = (fio_parts[0], fio_parts[1], fio_parts[2])
    elif len(fio_parts) >= 2:
        key = (fio_parts[0], fio_parts[1])
    else:
        print (f' Отсутствует ФАМИЛИЯ или ИМЯ сотрудника {fio_parts} , запись не обработана')
        continue

    if not any(all(item in exist_key for item in key[:len(exist_key)]) for exist_key in contacts_dict):
        for i in range(3):
            row[i] = fio_parts[i] if i < len(fio_parts) else ""
        contacts_dict[key] = row

    else:
        for exist_key in contacts_dict:
            if len(exist_key) >= 3 :
                if exist_key[0:3] == key or exist_key[0:2] == key :
                    for i in range(3, len(row)):
                        if not contacts_dict[exist_key][i]:
                            contacts_dict[exist_key][i] = row[i]

            elif len(exist_key) == 2:
                if exist_key == key or exist_key == key[0:2]:
                    for i in range(3, len(row)):
                        if not contacts_dict[exist_key][i]:
                            contacts_dict[exist_key][i] = row[i]
            else:
                print(f' Отсутствует ФАМИЛИЯ или ИМЯ сотрудника {key} , запись не обработана')

updated_contacts_list = [contacts_list[0]] + list(contacts_dict.values())
phone_pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
ext_pattern = r"\s*?\(?доб\.?\s*?(\d{4})\)?"
repl_phone_pattern = r"+7(\2)\3-\4-\5"
repl_ext_pattern = r" доб.\1"
for row in updated_contacts_list[1:]:
    row[5] = re.sub(phone_pattern,repl_phone_pattern,row[5])
    row[5] = re.sub(ext_pattern, repl_ext_pattern, row[5])

with open("phonebook.csv", "w", encoding="utf-8", newline = "") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(updated_contacts_list)