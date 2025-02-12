import random
number=random.randint(1,100)
print("Welcome to NumGuess!!")
name=input("Enter Username: ")

i=1
while True:    
    for i in range(10):
        guess=int(input(print("Please enter your guess between 1 and 100: ")))
        if guess>number:
            print("Your guess is a tad bit higher than what I had in mind")
        elif guess<number:
            print("You'll have to go a little higher if you want to win!")
        elif guess==number:
            print("There you are...see I sensed there was something special about you!")
            print("You managed to guess it in ",i, " attempts")
            break
 
        else:
            print("Please enter a valid input")
        i+=1
    retry=input("Do you want to retry[Yes/No]: ").lower()
    if retry!="Yes":
         break

    

    
