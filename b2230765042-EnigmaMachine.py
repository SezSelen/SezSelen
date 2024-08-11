#Selen N. SEZGİN
#Student ID: 2230765042

import sys
import os

def error_checking_mechanism():
    path_key = sys.argv[2]
    path_input = sys.argv[3]

    try:
        if len(sys.argv) < 6:  # Remember, sys.argv[0] is the script name itself
            pass
        else:
            raise IndexError
    except IndexError:
        print("Parameter Number Error!")
    try:
        if sys.argv[1] == "enc":
            pass
        elif sys.argv[1] == "dec":
            pass
        else:
            raise TypeError
    except TypeError:
        print("Undefined Parameter Error!")

    # KEY FILE CHECKS
    try:

        key_exist = os.path.exists(path_key)
        if key_exist:
            pass#key_path exists
            key_file = open(path_key, "r")
            try:
                if key_file.readable():
                    pass#file readable continue
                    # Read the content of the file
                    content = key_file.read()
                    if len(content.strip()) != 0:
                        pass#file not empty-continue
                        list_number = ["\n", "[", "]", '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                                       '13', '14', '15', '16', ","]
                        # Check each character in the content
                        for char in content:
                            # Check if the character is a letter or whitespace
                            if char not in list_number:
                                print(f"Error: '{char}' is not a number or bracket or comma.")
                                break
                        else:
                            pass#characters are all OK
                    else:
                        print("Key File Is Empty")
                else:
                    raise IOError
            except IOError:
                print("Key File not readable")
        else:
            raise OSError
    except IndexError:
        print("Key Path not provided in the command line arguments.")

    # INPUT FILE CHECKS

    try:

        # Check whether the specified path exists or not
        isExist = os.path.exists(path_input)
        if isExist:
            pass#path exists
            input_file = open(path_input, "r")
            try:
                if input_file.readable():
                    pass#File is readable
                    # Read the content of the file
                    content = input_file.read()
                    if len(content.strip()) != 0:
                        pass #file not empty continue
                    else:
                        print("File Is Empty")
                else:
                    raise IOError
            except IOError:
                print("Input File not readable")
        else:
            raise OSError  # filenotfound Error
    except IndexError:
        print("Path not provided in the command line arguments.")

#ENCRYPTION
def letter_to_number():
    path_key = sys.argv[2]
    path_input = sys.argv[3]
    alphabet_list = [(chr(65 + i), i + 1) for i in range(26)]  # list of tuples like (A,1),...
    alphabet_list.append((" ", 27))
    inputfile = open(path_input, "r")
    text = inputfile.readline()
    text = text.upper()  # Convert text to uppercase for consistency
    result = []
    for char in text:
        if char.isalpha():
            # Convert the letter to its corresponding position in the alphabet
            position = ord(char) - ord('A') + 1
        elif char == ' ':
            position = 27  # Replace white space with 27
        else:
            continue  # Skip non-alphabetic characters
        result.append(position)  # Add the position to the result list
    return result

def matrix_preparation():
    # Replace letters with their corresponding positions in "ATTACK NOW"
    result = letter_to_number()
    # ['AT', 'TA', 'CK', ' N', 'OW']
    # [1, 20, 20, 1, 3, 11, 27, 14, 15, 23]

    my_list = result
    result_other = []
    # Iterate over the list two by two and create sublist
    for i in range(0, len(my_list), 2):
        sublist = my_list[i:i + 2]
        result_other.append(sublist)
    return result_other

    # [[1, 20], [20, 1], [3, 11], [27, 14], [15, 23]]
def make_matrix_for_words():

    result_other_other = []

    # Iterate over the list and convert each element to a sublist with single-element lists
    for sublist in matrix_preparation():
        new_sublist = [[x] for x in sublist]
        result_other_other.append(new_sublist)
    return  result_other_other

def key_file_prep():
    path_key = sys.argv[2]
    # [[[1], [20]], [[20], [1]], [[3], [11]], [[27], [14]], [[15], [23]]]
    # key file data
    with open(path_key, 'r') as file:
        # Read the lines from the file
        lines = file.readlines()
    # Initialize an empty matrix
    key_matrix = []

    # Iterate over the lines and split them by comma to create lists
    for line in lines:
        # Split the line by comma and convert the elements to integers
        row = [int(x) for x in line.strip().split(',')]
        # Add the row to the matrix
        key_matrix.append(row)
    return key_matrix
    # Print the matrix
    # [[1, 2], [1, 3]]

def multiplication():
    matrix1 = key_file_prep()
    matrix2 = make_matrix_for_words()
    result = []
    for sublist in matrix2:
        result_multiplication = [[0 for _ in range(len(sublist[0]))] for _ in range(len(matrix1))]
        for i in range(len(matrix1)):
            for j in range(len(sublist[0])):
                for k in range(len(sublist)):
                    result_multiplication[i][j] += matrix1[i][k] * sublist[k][j]
        result.append(result_multiplication)
    return result


def write_enc_output():
    result = multiplication()
    print(result)
    flattened_result = [item for sublist in result for item in sublist]
    # Write each item as integers to a file
    with open('output_enc.txt', 'w') as file:
        for i, sublist in enumerate(flattened_result):
            for j, item in enumerate(sublist):
                file.write(str(item))
                if i != len(flattened_result) - 1 or j != len(sublist) - 1:
                    file.write(',')



#####DECODING WITH INVERSE

def read_cipher_text():
    file_path=sys.argv[4]
    cipher_text=[]
    with open(file_path, 'r') as file:
        line = file.readline().strip()  # Read the line and remove leading/trailing whitespaces
        numbers = [int(num) for num in line.split(',') if num.strip()]  # Split the line into numbers and skip empty strings
        sublists = [numbers[i:i+2] for i in range(0, len(numbers), 2)]  # Create sublists of two numbers each
        cipher_text.extend(sublists)  # Add sublists to the cipher_text list
    return cipher_text


def get_inverse(matrix): #calculates the inverse of the desired matrix(in our case it is key matrix)
    n = len(matrix)
    identity = [[0] * n for _ in range(n)]
    for i in range(n):
        identity[i][i] = 1

    # Concatenate the matrix with the identity matrix
    augmented_matrix = [row + identity_row for row, identity_row in zip(matrix, identity)]

    # Perform Gauss-Jordan elimination
    for fd in range(n):
        fdScaler = 1.0 / augmented_matrix[fd][fd]
        for j in range(n*2):
            augmented_matrix[fd][j] *= fdScaler
        for i in range(n):
            if i != fd:
                crScaler = augmented_matrix[i][fd]
                for j in range(n*2):
                    augmented_matrix[i][j] = augmented_matrix[i][j] - crScaler * augmented_matrix[fd][j]

    # Extract the inverse matrix from the augmented matrix
    inverse = [row[n:] for row in augmented_matrix]

    return inverse

def decrypt_matrix( encrypted_matrix, key_matrix_inverse): #where key and encrypted matrix is multiplied for decryption
    encrypted_matrix = read_cipher_text()
    n = len(encrypted_matrix)
    decrypted_matrix = [[0] for _ in range(n)]  # Initialize the decrypted matrix

    for i in range(n):
        for j in range(1):  # Adjust the range for the column
            decrypted_matrix[i][j] = int(key_matrix_inverse[i][0] * encrypted_matrix[0][j] + key_matrix_inverse[i][1] * encrypted_matrix[1][j])

    return decrypted_matrix

# Example usage
key_matrix_inverse = get_inverse(key_file_prep())  # Example inverse key matrix  # gives the encrypted list of [[41,61],...]
encrypted_matrix=read_cipher_text()

def write_dec_output(encrypted_matrix_list):
    with open('output_dec.txt', 'w') as file:
        for i, decrypted_matrix in enumerate(encrypted_matrix_list):
            for j, item in enumerate(decrypted_matrix):
                file.write(str(item))
                if j != len(decrypted_matrix) - 1:
                    file.write(',')
            if i != len(encrypted_matrix_list) - 1:
                file.write('\n')

def main():
    error_checking_mechanism() #all error checks are here.

    if sys.argv[1] == "enc":
        write_enc_output()

    if sys.argv[1] == "dec":
        key_matrix_inverse = get_inverse(key_file_prep())
        encrypted_matrix_list = read_cipher_text()  # Get encrypted matrices
        decrypted_matrix_list = []

        for encrypted_matrix in encrypted_matrix_list:
            decrypted_matrix = decrypt_matrix(encrypted_matrix, key_matrix_inverse)
            decrypted_matrix_list.append(decrypted_matrix)

        write_dec_output(decrypted_matrix_list)

if __name__ == "__main__":
    main()