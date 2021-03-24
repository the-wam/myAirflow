import glob

from utile import load_json, dump_json, unique_name, load_last_json

envPath = ""


def my_transforme():

    # load path
    # listJson = sorted(glob.glob(f"{envPath}data/json/*.json"), reverse=True)
    list_json = load_last_json(f"{envPath}data/json/*.json", 2)
    data = {}

    # select two most recent files
    # for one_path in listJson[:2]:
    for one_path in list_json:
        data[one_path] = load_json(one_path)

    # transforme data

    # compare the two last Json files
    if data[list_json[0]] == data[list_json[1]]:
        print("nothing new")
        return "stop"
    else:
        new_data = []
        for i, manga in enumerate(data[list_json[0]]):
            if data[list_json[1]][0] == manga:
                new_data = data[list_json[0]][:i]
                break

        if not new_data:
            print("all is new !")
            print("log: search if data is missing")
            dump_json(f"{envPath}data/json/{unique_name('json')}", new_data)
            return "continue"
        else:
            print(f"log : return Newdata {len(new_data)}")
            dump_json(f"{envPath}data/json/{unique_name('json')}", new_data)
            return "continue"


if __name__ == "__main__":
    my_transforme()
