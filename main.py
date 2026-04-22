from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
#pprint(contacts_list)
contacts_dict = {}
# TODO 1: выполните пункты 1-3 ДЗ
for row in contacts_list[1:]:
    fio_parts = " ".join (row [:3]).split()
    if len(fio_parts) >= 3:
        key = (fio_parts[0], fio_parts[1], fio_parts[2])
    else:
        key = (fio_parts[0], fio_parts[1])

    if not any(all(item in exist_key for item in key) for exist_key in contacts_dict):
        for i in range(3):
            row[i] = fio_parts[i] if i < len(fio_parts) else ""
        contacts_dict[key] = row
    else:
        for exist_key in contacts_dict:
            for i in range(len(exist_key) - len(key) + 1):
                if  exist_key[i:i + len(key)] == key:
                    for i in range(3, len(row)):
                        if not contacts_dict[exist_key][i]:
                            contacts_dict[exist_key][i] = row[i]
#pprint(contacts_dict.values())
updated_contacts_list = [contacts_list[0]] + list(contacts_dict.values())
phone_pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
ext_pattern = r"\s*?\(?доб\.?\s*?(\d{4})\)?"
repl_phone_pattern = r"+7(\2)\3-\4-\5"
repl_ext_pattern = r" доб.\1"
for row in updated_contacts_list[1:]:
    row[5] = re.sub(phone_pattern,repl_phone_pattern,row[5])
    row[5] = re.sub(ext_pattern, repl_ext_pattern, row[5])
# pprint(updated_contacts_list)
# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline = "") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(updated_contacts_list)