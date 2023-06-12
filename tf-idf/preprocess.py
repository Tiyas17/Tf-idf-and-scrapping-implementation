# DOUBT: yeh numbers <>= symbols data mein hai abhi. hatana hai kya?
# Preprocessing questions data to add title and remove examples

import os
import sys

folder_path = "../Leetcode-Questions-Scrapper/Qdata/"
index_path = "../Leetcode-Questions-Scrapper/index.txt"
new_folder_path = "Data/QData"
num_ques = 2405

# store contents of index.txt with line numbers as index
title = {}
with open(index_path, 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        title[i+1] = line.strip()

# Iterate over Qdata folder to read files
for index in range(1, num_ques+1):
    subfolder_path = os.path.join(folder_path, str(index))
    file_path = os.path.join(subfolder_path, str(index) + ".txt")
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            remove = "Example"
            removeIndex = None
            for ind, line in enumerate(lines):
                if remove in line:
                    removeIndex = ind
                    break
                    
            newContent = lines[:removeIndex]
            # print(newContent)
            # print(removeIndex)
            # break
        
        # Create a new folder to add preprocessed content
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            
        new_file_path = os.path.join(new_folder_path, f"{index}.txt")
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(title[index] + "\n")
            file.writelines(newContent)
    else:
        print(f"File {index} does not exist")

print("Preprocessing done")