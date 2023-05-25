import numpy as np

table = np.array([['apple', 'green', 'bees'],
                  ['apple', 'apple', 'apple'],
                  ['apple', 'orange', 'grapes']])

# for i in range(len(table)):
#     print(i)


def check_and_remove_same_content(table):
    # Convert the table elements to strings (if not already)
    str_table = np.char.asarray(table)

    # Check if all elements are equal to the first element
    same_content = np.all(np.char.equal(str_table, str_table[0]))

    # Remove duplicates
    unique_table = np.unique(str_table)

    return same_content, unique_table

# Usage example
table = np.array([['apple', 'green', 'bees'],
                  ['apple', 'apple', 'apple'],
                  ['apple', 'orange', 'grapes']])

same_content, unique_table = check_and_remove_same_content(table)
print("Same content:", same_content)  # Output: True
print("Unique table:")
print(unique_table)