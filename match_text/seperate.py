import re

f = open("results_3.txt", "r")
data = f.readlines()
# print(data)
matched_count = 0
mismatched_count = 0
total_count = 0
for i,n in enumerate (data):
    underscore_removed = n.split('_')[1]
    # print(underscore_removed)
    myString = re.sub(r"[\n\t\s]*", "", underscore_removed)
    # print(ascii(myString))
    splitted = myString.split(":")

    #####################
    # for replacing Q with O
    # O_replaced = splitted[1]
    # print(splitted)
    # O_replaced = O_replaced.replace("Q", "O")

    # if splitted[0] == O_replaced:
    ###################

    try :
        O_replaced = splitted[1].replace("Q", "O")
        if splitted[0] == O_replaced:
            total_count+=1
            matched_count+=1
            # print(f"Matched -- Actual: {[splitted[0]]} Prediction: {splitted[1]}")
        else:
            print(f"Mismatched -- Actual: {[splitted[0]]} Prediction: {splitted[1]}")
            mismatched_count +=1
            total_count+=1
    except:
        print("detection failed")
        mismatched_count +=1
    # break
print(f"Total Count {total_count}")
print(f"matched Count {matched_count}")
print(f"Mismatched Count {mismatched_count}")
print(f"Accuracy: {(int(matched_count)/int(total_count))*100}")