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

    # Open file
    file = open(filename, 'r')
    lines = file.readlines()

    # Iterate through every line in file
    for line in lines:

        # split based on ^^ delimeter
        split_line = line.replace("\n", "").split("^^", 2)

        # Check if key is NULL
        if "id" not in split_line[0] or "name" not in split_line[1] or "city" not in split_line[2]:
            print("Key cannot be zero")
            return -1

        # Remove irrelevent "=" abd "^" delimeters, keep only value
        cur_id = split_line[0].replace("id", "").replace("=", "").replace("^", "")
        cur_name = split_line[1].replace("name", "").replace("=", "").replace("^", "")
        cur_city = split_line[2].replace("city", "").replace("=", "").replace("^", "")
    
        # If value is empty string, set to NULL
        if len(cur_id) == 0:
            cur_id = "NULL"
        if len(cur_name) == 0:
            cur_name = "NULL"
        if len(cur_city) == 0:
            cur_city = "NULL"

        # Add to dictionary file_list
        dict_.create(cur_id, cur_name, cur_city)
    
    return dict_.file_list

# Function to test all cases
def test():
    
    tests_path = 'testing_files/file_tests/'
    results_path = 'testing_files/file_test_results/'
    expected_path = 'testing_files/file_test_expected/'
    test_flag = True

    # Iterate through every file in testing_files/file_tests
    for p in Path(tests_path).iterdir():

        # Get file name, send to parse_data function
        file_name = f"{p.name}"
        file_list = parse_data(tests_path + file_name)

        # If file_list is -1, then error occured in parse_data
        if file_list == -1:
            text_file = open(results_path + file_name, 'w')
            text_file.write("-1")
            text_file.close()

            try:
                # Assertions for each file tested compared to expected results
                assert filecmp.cmp(expected_path + file_name, results_path + file_name)
            except:
                # If assertion fails, set test_flag to false
                print(f"test for " + file_name + " has unexpected result")
                test_flag = False
                continue
        
        else:
            # Create dataframe from file_list, save to csv
            final_df = pd.DataFrame(file_list, columns=["id", "name", "city"])
            final_df.to_csv(results_path + file_name.replace(".txt", ".csv"), sep="|", index=False)

            try:
                # Assertions for each file tested compared to expected results
                assert filecmp.cmp(expected_path + file_name.replace(".txt", ".csv"), results_path + file_name.replace(".txt", ".csv"))
            except:
                # If assertion fails, set test_flag to false
                print(f"test for " + file_name + " has unexpected result")
                test_flag = False
                continue
        
    # If test_flag is true, all tests passed
    if(test_flag):
        print("\n $$$ All tests passed!! $$$ \n")
    else:
        print("\n ### Some tests failed ### \n")

    return

if __name__ == "__main__":

# Welcome message
    print("\n*** Welcome to Input File Processor! ***\n \n\
Please enter the input data in the following format into a text file: \n\
id=_^^name=_^^city=_ \n\
Then, select 'user' mode, and enter the name of the file. \n\
If you would like to test the program, select 'test' mode. \n\
If you would like to exit, select 'done' mode. \n\
")
    while(1):
        # Get user input for mode
        mode = input("Type 'test', 'user', or 'done': ")

        if (mode == "test"):
            print("\n ***test mode begin*** \n")
            test()
            print("***exiting test mode*** \n \n")

        elif (mode == "user"):

            print("\n ***user mode begin*** \n")
            file_name_usr = input("type file name: ")

            if (exists(file_name_usr)):
                # Send file to parse_data function
                file_list = parse_data(file_name_usr)
                if (file_list == -1):
                    text_file = open('file_usr_results/' + file_name_usr, 'w')
                    text_file.write("-1")
                    text_file.close()
                    print("\n Error occured in parse_data function, File saved as '-1' \n")
                else:
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