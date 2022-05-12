"""
Add all the services like referral and the recommendation algorithms
create a service for getting numbers too.
"""

"""
Sentence will be self.descrition

"""
def stringCleaningService(sentence: str):
    
    if sentence is not None:
        try:
            string = sentence
            length = len(string)
            print("Start cleaning!")
            for i in range(length):
                print("again")
                if (string[i] == "<"):
                    for n in range(i,length):
                        if string[n] == ">":
                            raise ValidationError(_("Remove both '<' and '>'"))
                            
                if (string[i] == "<") and (string[i+1] == "/"):
                    raise ValidationError(_("Remove the '</' from your description"))

                    
                if (string[i] == "(") and (string[i+1] == "s") and (string[i+2] == "u") and (string[i+3] == "b") and (string[i+4] == ")"):
                    print("First Phase!")

                    string2 = str.replace(string, "(sub)", "<sub>")
                    string = string2
                    print("Finished")
                elif (string[i] == "(") and (string[i+1] == "/") and (string[i+2] == "s") and (string[i+3] == "u") and (string[i+4] == "b") and (string[i+5] == ")"):
                    print("Second Phase!")
                    string2 = str.replace(string, "(/sub)", "</sub>")
                    string = string2
                    print("Finished")
                elif (string[i] == "(") and (string[i+1] == "s") and (string[i+2] == "u") and (string[i+3] == "p") and (string[i+4] == ")"):

                    print("Second Phase!")
                    string2 = str.replace(string, "(sup)", "<sup>")
                    string = string2
                    print("Finished")
                elif (string[i] == "(") and (string[i+1] == "/") and (string[i+2] == "s") and (string[i+3] == "u") and (string[i+4] == "p") and (string[i+5] == ")"):
                    print("Second Phase!")
                    string2 = str.replace(string, "(/sup)", "</sup>")
                    string = string2
                    print("Finished")


            sentence = string
            return sentence


        except:
            raise ValidationError(_('An error occurred!'))
    





def reverseStringCleaningService(sentence: str):
    if sentence is not None:
        string = sentence
        length = len(string)
        print("Start cleaning!")
        for i in range(length):
            print("again")
             
            if (string[i] == "<") and (string[i+1] == "s") and (string[i+2] == "u") and (string[i+3] == "b") and (string[i+4] == ">"):
                print("First Phase!")

                string2 = str.replace(string, "<sub>", "(sub)")
                string = string2
                print("Finished")
            elif (string[i] == "<") and (string[i+1] == "/") and (string[i+2] == "s") and (string[i+3] == "u") and (string[i+4] == "b") and (string[i+5] == ">"):
                print("Second Phase!")
                string2 = str.replace(string, "</sub>", "(/sub)")
                string = string2
                print("Finished")
            elif (string[i] == "<") and (string[i+1] == "s") and (string[i+2] == "u") and (string[i+3] == "p") and (string[i+4] == ">"):

                print("Second Phase!")
                string2 = str.replace(string, "<sup>", "(sup)")
                string = string2
                print("Finished")
            elif (string[i] == "<") and (string[i+1] == "/") and (string[i+2] == "s") and (string[i+3] == "u") and (string[i+4] == "p") and (string[i+5] == ">"):
                print("Second Phase!")
                string2 = str.replace(string, "</sup>", "(/sup)")
                string = string2
                print("Finished")


        sentence = string
        return sentence






def ScoreRange(value: int):
    if value == 0:
        return 50
    else:
        return 100 - value

