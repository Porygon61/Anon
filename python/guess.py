import os 
import random
import math
import time

cwd = os.path.abspath(__file__)

print('Hello to my little Game:\nThis is a Number Guessing Game!')


Your_Name = str(input("First of All, What's your Name ?\n"))
while Your_Name == '':
    Your_Name = str(input("First of All, What's your Name ?\n"))

print(' ')

Difficulty = input("Well " + Your_Name + ", Choose your difficulty:\nType a number between 1 and 5.\n\n1 being 'easy' and 5 being 'hard' \n")
while Difficulty != '1' and Difficulty != '2' and Difficulty != '3' and Difficulty != '4' and Difficulty != '5':
    Difficulty = input("Well " + Your_Name + ", Choose your difficulty:\nType a number between 1 and 5.\n\n1 being 'easy' and 5 being 'hard' \n")

if Difficulty == '1':
    y = 10
    number = random.randint(1,y)
elif Difficulty == '2':
    y = 20
    number = random.randint(1,y)
elif Difficulty == '3':
    y = 50
    number = random.randint(1,y)
elif Difficulty == '4':
    y = 100
    number = random.randint(1,y)
elif Difficulty == '5':
    y = 1000
    number = random.randint(1,y)
else:
    print("Please enter a number between 1 and 5.")
    exit()

print(' ')

print("Well, " + Your_Name + f" I'm thinking of a number between 1 and {y}")

User_Number = int(input("Take a guess: \n"))

time.sleep(0.5)

if User_Number == number:
    print("\nYou guessed right!")
else:
    print("\nNope. The number I was thinking of was " + str(number) + "\n")
    
time.sleep(0.5)

Again = input("Do you want to play again?\n\nType 'y or 'n': \n\n")

if Again == 'y':
    for i in range(random.randint(1, 15)):
        time.sleep(random.random())
        print('.', end='')
    print('\n')
    os.system(cwd)
elif Again == 'n':
    print("Bye!")
    exit()
else:
    print("Please type 'y' or 'n'.")