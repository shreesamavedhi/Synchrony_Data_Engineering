from pathlib import Path
import pandas as pd
import filecmp
from os.path import exists

def parse_data(filename):

    # Creating dictionary class 
    class CreateDictionary(dict): 
        def __init__(self): 
            self.file_list = []
        # Function to add key:value 
        def create(self, id_, name_, city_): 
            dict = {"id": id_, "name": name_, "city": city_}
            self.file_list.append(dict) 

    # Creating dictionary object 
    dict_ = CreateDictionary()

    file = open(filename, 'r')
    lines = file.readlines()

    for line in lines:
        split_line = line.replace("\n", "").split("^^", 2)
        cur_id = int(split_line[0].replace("id", "").replace("=", "").replace("^", ""))
        cur_name = split_line[1].replace("name", "").replace("=", "").replace("^", "")
        cur_city = split_line[2].replace("city", "").replace("=", "").replace("^", "")
        dict_.create(cur_id, cur_name, cur_city)
    
    return dict_.file_list

def test():
    
    tests_path = 'testing_files/file_tests/'
    results_path = 'testing_files/file_results/'
    expected_path = 'testing_files/file_expected/'

    for p in Path(results_path).glob('**/*.txt'):
        file_name = f"{p.name}"
        file_list = parse_data(tests_path + file_name)
        final_df = pd.DataFrame(file_list, columns=["id", "name", "city"])
        final_df.to_csv(results_path + file_name.replace(".txt", ".csv"), sep="|", index=False)
        try:
            # Assertions for each file tested
            assert filecmp.cmp(expected_path + file_name.replace(".txt", ".csv"), results_path + file_name.replace(".txt", ".csv"))
        except:
            print(f"test for " + file_name + " has unexpected result")
            continue
    return

if __name__ == "__main__":

    while(1):
        mode = input("type 'test', 'user', or 'done': ")

        if (mode == "test"):
            print("test mode begin")
            test()
            print("exiting test mode")

        elif (mode == "user"):

            print("user mode begin")
            file_name_usr = input("type file name: ")

            if (exists(file_name_usr)):
                file_list = parse_data(file_name_usr)
                final_df = pd.DataFrame(file_list, columns=["id", "name", "city"])
                final_df.to_csv( + file_name_usr.replace(".txt", ".csv"), sep="|", index=False)
                print("user mode finished")
            else:
                print("file does not exist")
            
            print("exiting user mode")

        elif (mode == "done"):
            print("exiting program")
            break

        else:
            print("invalid mode")