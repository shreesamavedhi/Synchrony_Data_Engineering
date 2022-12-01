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

        if "id" not in split_line[0] or "name" not in split_line[1] or "city" not in split_line[2]:
            print("Key cannot be zero")
            return -1

        cur_id = split_line[0].replace("id", "").replace("=", "").replace("^", "")
        cur_name = split_line[1].replace("name", "").replace("=", "").replace("^", "")
        cur_city = split_line[2].replace("city", "").replace("=", "").replace("^", "")
    
        if len(cur_id) == 0:
            cur_id = "NULL"
        if len(cur_name) == 0:
            cur_name = "NULL"
        if len(cur_city) == 0:
            cur_city = "NULL"

        dict_.create(cur_id, cur_name, cur_city)
    
    return dict_.file_list

def test():
    
    tests_path = 'testing_files/file_tests/'
    results_path = 'testing_files/file_test_results/'
    expected_path = 'testing_files/file_test_expected/'
    test_flag = True

    for p in Path(tests_path).iterdir():
        file_name = f"{p.name}"
        file_list = parse_data(tests_path + file_name)
        if file_list == -1:
            text_file = open(results_path + file_name, 'w')
            text_file.write("-1")
            text_file.close()

            try:
                # Assertions for each file tested
                assert filecmp.cmp(expected_path + file_name, results_path + file_name)
            except:
                print(f"test for " + file_name + " has unexpected result")
                test_flag = False
                continue
            
        else:   
            final_df = pd.DataFrame(file_list, columns=["id", "name", "city"])
            final_df.to_csv(results_path + file_name.replace(".txt", ".csv"), sep="|", index=False)

            try:
                # Assertions for each file tested
                assert filecmp.cmp(expected_path + file_name.replace(".txt", ".csv"), results_path + file_name.replace(".txt", ".csv"))
            except:
                print(f"test for " + file_name + " has unexpected result")
                test_flag = False
                continue
        
    
    if(test_flag):
        print("\n $$$ All tests passed!! $$$ \n")
    else:
        print("\n ### Some tests failed ### \n")

    return

if __name__ == "__main__":

    print("\n*** Welcome to Input File Processor! ***\n \n\
Please enter the input data in the following format into a text file: \n\
id=_^^name=_^^city=_ \n\
Then, select 'user' mode, and enter the name of the file. \n\
If you would like to test the program, select 'test' mode. \n\
If you would like to exit, select 'done' mode. \n\
")
    while(1):
        mode = input("Type 'test', 'user', or 'done': ")

        if (mode == "test"):
            print("\n ***test mode begin*** \n")
            test()
            print("***exiting test mode*** \n \n")

        elif (mode == "user"):

            print("\n ***user mode begin*** \n")
            file_name_usr = input("type file name: ")

            if (exists(file_name_usr)):
                file_list = parse_data(file_name_usr)
                final_df = pd.DataFrame(file_list, columns=["id", "name", "city"])
                final_df.to_csv("file_usr_results/" + file_name_usr.replace(".txt", ".csv"), sep="|", index=False)
                print("\n file saved! \n")
            else:
                print("\n file does not exist! \n")
            
            print("***exiting user mode*** \n")

        elif (mode == "done"):
            print("\n ***exiting program*** \n")
            break

        else:
            print("\ninvalid mode!\n")