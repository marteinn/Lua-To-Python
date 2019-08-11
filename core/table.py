import re
from collections import OrderedDict


def is_castable_int(val):
    return re.search(r'^([0-9]*)$', val)


class Table(object):
    def __init__(self, *args, **kwargs):
        self.val_list = [None, *args]
        self.val_dict = OrderedDict()

        for key, val in kwargs.items():
            if key[:2] == "__":
                if is_castable_int(key):
                    key = int(key)

                if isinstance(key, int):
                    # Numbers passed in constructor cannot override existing values
                    if key >= len(self.val_list):
                        self.val_dict[key] = val
                    continue

            self.val_dict[key] = val

    def __len__(self):
        return len(self.val_list) - 1

    def __getitem__(self, key):
        if is_castable_int(key):
            key = int(key)

        if isinstance(key, int) and key < len(self.val_list):
            return self.val_list[key]

        return self.val_dict[key]

    def __setitem__(self, key, value):
        if is_castable_int(key):
            key = int(key)

        if isinstance(key, int) and key < len(self.val_list):
            self.val_list[key] = value
            return

        self.val_dict[key] = value
        return None

    def __getattr__(self, key):
        return self.val_dict[key]

    def __str__(self):
        list_rep = str(self.val_list[1:])
        list_rep = list_rep[1:-1]

        dict_rep = str(self.val_dict)
        dict_rep = dict_rep[12:-2]
        return "[{0}, {1}]".format(list_rep, dict_rep)

"""
t = Table(1, 2, 3, 4, __1=5, __99="99 val", __word="word val")
print(len(t))  # 4

tt = Table(1)
print(len(tt))  # 1

print(t["1"])  # 1
print(t["99"])  # 99 val
print(t["martin"])  # word val
print(t.martin)  # word val

t["test"] = "ing"
t["2"] = "ing"
print(t["test"])
print(t["2"])

print(t)
"""
