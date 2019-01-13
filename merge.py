# CSE 160 
# Huanshu Liu and Angel Chen 
# Merging two csv files 
# We need to conduct this merge.py first then run our code in pj.py 
import csv 
# Read in the csv files: user_log_format1.csv (longer list one) and user_info_format1.csv (shorter one)
# rename the csv file names: user_actions.csv & user_demographics.csv 

def read_csv(path):
    """
    Reads the CSV file at path, and returns a list of rows from the file.
    Parameters: path: path to a CSV file. 
    Returns: list of dictionaries: Each dictionary maps the columns of the CSV file
    to the values found in one row of the CSV file. 
    """
    output = []
    csv_file = open(path)
    for row in csv.DictReader(csv_file):
        output.append(row)
    csv_file.close()    
    return output

def merge(reader_1, reader_2):
    """
    To merge two lists into one: reader_1 is the longer list, reader_2 is the smaller list
    Return a result list of dictionaries with combined informations on age and gender for an user 
    """
    nested_dictionary = dict()
    for dictionary in reader_1:
        if nested_dictionary.has_key(dictionary['user_id']):
            nested_dictionary[dictionary['user_id']].append(dictionary)
        else:
            nested_dictionary[dictionary['user_id']] = [dictionary]
  
    nested_dictionary_1 = dict()
    for dictionary in reader_2:
        nested_dictionary_1[dictionary['user_id']] = dictionary
   
    
    for key in nested_dictionary.keys(): 
        if nested_dictionary_1.has_key(key) == False:  
            del nested_dictionary[key] 
            
        else:
            for element in nested_dictionary[key]:
                element['age_range'] = nested_dictionary_1[key]['age_range']
                element['gender'] = nested_dictionary_1[key]['gender']   

    result_list = []
    for sub_list in nested_dictionary.values():
        for i in range(len(sub_list)):
            result_list.append(sub_list[i])   
    return result_list 
 
def write_to_csv(user_lst): 
    """
    To convert a list of dictionaries into a seperate csv file called merged.csv 
    """
    # Find the columns names for each lst 
    keys = user_lst[0].keys() 
    # Store our merged list into a csv file such that we can reduce the runtime 
    with open('merged.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, keys)
        writer.writeheader() 
        writer.writerows(user_lst)
    csv_file.close() 

# Testing 
def test_merge(): 
    list_1 = [{'user_id': 10010, 'age_range': 20, 'gender': 1},
          {'user_id': 10011, 'age_range': 30, 'gender': 0},
          {'user_id': 10012, 'age_range': 40, 'gender': 1},
          {'user_id': 10013, 'age_range': 20, 'gender': 0},
          {'user_id': 10014, 'age_range': 30, 'gender': 1},
          {'user_id': 10015, 'age_range': 40, 'gender': 1},
          {'user_id': 10016, 'age_range': 50, 'gender': 1},
          {'user_id': 10017, 'age_range': 20, 'gender': 0},
          {'user_id': 10018, 'age_range': 20, 'gender': 1},
          {'user_id': 10019, 'age_range': 20, 'gender': 1},]
    list_2 = [{'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 10012, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 10013, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 19, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 10013, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 20, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},
          {'user_id': 11111, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0},]
    
    assert merge(list_2, list_1) == [{'user_id': 10012, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 18, 'time_stamp': 0, 'action_type': 0, 'gender': 1, 'age_range': 40}, 
                 {'user_id': 10013, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 19, 'time_stamp': 0, 'action_type': 0, 'gender': 0, 'age_range': 20}, 
                 {'user_id': 10013, 'item_id': 12, 'cat_id': 16, 'seller_id': 12, 'brand_id': 20, 'time_stamp': 0, 'action_type': 0, 'gender': 0, 'age_range': 20}]

def main():
    test_merge() 
    print "We have passed the assertion test! "

    print "Our project starts!"
    print "Let's read the csv first."
    user_list_2 = read_csv("user_demographics.csv")
    print "We are done with reading the csv with age and gender! "
    user_list_1 = read_csv("user_actions.csv")
    print "We are done with reading the csv with action informations! " 
    print "Now we merge 2 csv files."
    user_lst = merge(user_list_1, user_list_2)
    print "We finished merging the two files, now we will export our list into a merged.csv file." 
    write_to_csv(user_lst)
    print "Writing dict into csv is done; Thanks for merging!" 

if __name__ =="__main__": 
  main () 

    


