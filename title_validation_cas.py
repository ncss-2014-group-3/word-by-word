#Checking that a title was actually recieved
if title is None:
    #if a title wasn't recieved, informs the user that the title was not recieved
    print("We didn't recieve a Title for your story.")
else:
    #this checks if the title can be allowed by our system
    title_check = re.match("^[A-Za-z0-9]([A-Za-z0-9!\"\(\)?',\.\:;]+|[A-Za-z0-9])*$", title)
    #checks that there are spaces in the title 
    if " " in title:
        #checks that the title_check is true
        if title_check == True:
            print("The title acceptance was successful.")
        #checks that there are not spaces in the title
        elif " " not in title:
            #checks that the title_check is true
            if check == True:
                print("The title acceptance was successful.")
            #if everything else fails.
            else:
                print("The title you submitted wasn't successful.")
                

    
    
