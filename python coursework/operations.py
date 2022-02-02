import os
import datetime as dt

# Function to display welcome message at the starting of the program
def start():
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Hello and Welcome to library management system")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# Function to read the txt file data and display data on the terminal
def displayData():
    print("\n\n------------------------------------------------------------------------")
    print("{:<10}{:<27}{:<15}{:<10}{:<10}".format("Book ID","Book Name","Author","Quantity","Price"))
    print("------------------------------------------------------------------------")
    
    i = 1
    file_r = open("book details.txt","r")
    for line in file_r:
        data = line.replace("\n","")
        data = data.split(",")
        bookName,author,quantity,price = data
        print("{:<10}{:<27}{:<15}{:<10}{:<7}".format(i,bookName,author,quantity,price))
        i = i + 1
        
    print("------------------------------------------------------------------------")
    file_r.close()

# Function that creates a dictionary and puts book id as keys and book details as values
def dictionary():
    i = 1
    file_r = open("book details.txt","r")
    dict = {}
    for line in file_r:
        data = line.replace("\n","")
        data = data.split(",")
        dict[i] = data
        i = i + 1
    file_r.close()
    return dict

# Function to input operation value which determines the operation to be executed                                
def operationInput():
    displayData()
    print("\n\nEnter '1' to borrow a book")
    print("Enter '2' to return a book")
    print("Enter '3' to exit")

    correct = False
    while correct == False:
        try:
            value = int(input("\n\nPlease enter a value: "))
            if value == 1 or value == 2 or value == 3:
                correct = True
            else:
                print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("Invalid input!!!")
                print("Please provide value as 1, 2 or 3.")
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                operationInput()

        except:
            print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Invalid input!!!")
            print("Please provide value as 1, 2 or 3.")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

            operationInput()
        
    process(value)

# Function that carries out all the process of borrow, return or exit
def process(value):
    dict = dictionary()
    # Passing dictionary value returned from function dictionary()
    valueList = list(dict.values())
       
    if value == 1:
        cost = 0
        bookBorrowed = []
        while(True):
            try:
                id = int(input("\n\nEnter the ID of the book that the customer wants to borrow: "))

                if id <= len(valueList) and id > 0:
                    if int(valueList[id-1][2]) > 0:
                        #Calculating total cost while borrowing book
                        cost += float(valueList[id-1][3].split("$")[1])
                        bookname = valueList[id-1][0]
                        #Updating the quantity of the stock
                        valueList[id-1][2] = str(int(valueList[id-1][2]) - 1)
                        bookBorrowed.append(bookname)

                        #Setting date and time of borrow
                        borrow_date = dt.datetime.now().date()
                        borrow_time = dt.datetime.now().time()
                                        
                        print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print("\t\t\tBook borrowed successfully!!!")
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                        #Displaying updated stock from txt file
                        file_w = open("temp.txt","w")
                        for i in range(len(valueList)):
                            file_w.write(valueList[i][0]+","+valueList[i][1]+","+valueList[i][2]+","+valueList[i][3]+"\n")
                        file_w.close()
                        os.remove("book details.txt")
                        os.rename("temp.txt","book details.txt")

                        condition = input("\n\nDoes the customer want to borrow other books as well? (y/n) : ").lower()
                        if condition == "y" or condition == "yes":
                            displayData()
                        else:
                            #Generating borrow note
                            borrowNote(bookBorrowed,cost,borrow_date,borrow_time)
                            operationInput()
                        
                    else:
                        print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print("\t\t\tBook is not available!!!")
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                            
                        condition = input("\n\nDoes the customer want to borrow other books as well? (y/n) : ").lower()
                        if condition == "y" or condition == "yes":
                            displayData()
                        else:
                            try:
                                borrowNote(bookBorrowed,cost,borrow_date,borrow_time)
                                operationInput()
                            except:
                                operationInput()

                else:
                    print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print("\t\tPlease provide a valid book ID!!!")
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                    displayData()

            except ValueError:
                print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("\t\tPlease provide a valid book ID!!!")
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            
                displayData()

            except OSError:
                print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("\t\tPlease provide a valid customer name!!!")
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                borrowNote(bookBorrowed,cost,borrow_date,borrow_time)
                operationInput()
                              
    elif value == 2:
        bookReturned = []
        fine = 0
        while(True):
            try:
                id = int(input("\n\nEnter the ID of the book that the customer wants to return: "))

                if id <= len(valueList) and id > 0:
                    bookname = valueList[id-1][0]
                    valueList[id-1][2] = str(int(valueList[id-1][2]) + 1)
                    bookReturned.append(bookname)

                    return_date = dt.datetime.now().date()
                    return_time = dt.datetime.now().time()

                    duration = 10
                    lending_duration = int(input("Enter the lending duration (days) of the book: "))
                    #Calculating whether the fine is applicable or not
                    if lending_duration > duration:
                        #Calculating applicable fine days
                        fine_days = lending_duration - duration
                        fine += fine_days * 0.5

                    file_w = open("temp.txt","w")
                    for i in range(len(valueList)):
                        file_w.write(valueList[i][0]+","+valueList[i][1]+","+valueList[i][2]+","+valueList[i][3]+"\n")
                    file_w.close()
                    os.remove("book details.txt")
                    os.rename("temp.txt","book details.txt")

                    condition = input("\n\nDoes the customer want to return other books as well? : ")
                    if condition == "y" or condition == "Y":
                        displayData()
                    else:
                        print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print("\t\t\tBook returned successfully!!!")
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                
                        returnNote(bookReturned,fine,return_date,return_time)
                        operationInput()
                            
                else:
                    print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print("\t\tPlease provide a valid book ID!!!")
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                    displayData()

            except ValueError:
                print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("\t\tPlease provide a valid customer name or book ID!!!")
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                displayData()

            except OSError:
                print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("\t\tPlease provide a valid customer name!!!")
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

                borrowNote(bookBorrowed,cost,borrow_date,borrow_time)
                operationInput()
                    
    elif value == 3:
        end()
        os._exit(0)
        
def borrowNote(bookBorrowed,cost,borrow_date,borrow_time):
    customerName = input("\n\nEnter the customer's name: ")
    print("\n")

    #Extracting minute,second and microsecond from datetime module
    minute = dt.datetime.now().time().minute
    second = dt.datetime.now().time().second
    microsec = dt.datetime.now().time().microsecond
    #Generating unique id for note 
    random = minute + second + microsec

    #Seperating borrowed books by comma
    books = ",".join(bookBorrowed)

    #Generating borrow note           
    borrow_w = open("Borrow_"+customerName+"("+str(random)+").txt","w")
    borrow_w.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    borrow_w.write("\t\t\tCustomer Borrow Detail\n")
    borrow_w.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    borrow_w.write("Name of borrower: "+customerName+"\n")
    borrow_w.write("Books borrowed: "+ books +"\n")
    borrow_w.write("Date of issue: "+str(borrow_date)+"\n")
    borrow_w.write("Time of issue: "+str(borrow_time)+"\n\n")
    borrow_w.write("Total price: $"+str(cost))
    borrow_w.close()

    #Reading and printing the generated note on the shell
    borrow_r = open("Borrow_"+customerName+"("+str(random)+").txt","r")
    print(borrow_r.read())

def returnNote(bookReturned,fine,return_date,return_time):          
    customerName = input("\n\nEnter the customer's name: ")
    print("\n")

    minute = dt.datetime.now().time().minute
    second = dt.datetime.now().time().second
    microsec = dt.datetime.now().time().microsecond
    random = minute + second + microsec

    books = ",".join(bookReturned)
                                
    return_w = open("Return_"+customerName+"("+str(random)+").txt","w")
    return_w.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    return_w.write("\t\t\tCustomer Return Detail\n")
    return_w.write("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    return_w.write("Name of returner: "+customerName+"\n")
    return_w.write("Books returned: "+ books +"\n")
    return_w.write("Date of issue: "+str(return_date)+"\n")
    return_w.write("Time of issue: "+str(return_time)+"\n\n")
    return_w.write("Fine: $"+str(fine))
    return_w.close()

    return_r = open("Return_"+customerName+"("+str(random)+").txt","r")
    print(return_r.read())

#Displaying Thank You message at the end of the program
def end():       
    print("\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Thank you for using our library management system")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
