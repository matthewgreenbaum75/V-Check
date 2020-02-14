
def getData(file):
    """
    Takes a text file as a parameter. Returns a list containing lists of data for each day. Each list has the data at index one, the opening price at index 2, 
    and the clsoing price at index 3.
    """

    dataList  = []
    dayInfo = []
    f = open(file,"r")
    line = f.readline()
    dayInfo = line.split("\t")
    dayInfo[2] = dayInfo[2].rstrip()
    dataList += [dayInfo]
    for line in f:
        dayInfo = line.split("\t")
        dayInfo[2] = dayInfo[2].rstrip()
        dataList += [dayInfo]
    f.close()
    return dataList

def track_V(data, percent_V, day_High):
    """
    Takes a list containing lists of data for each day. 
    Each list has the data at index one, the opening price at index 2, and the clsoing price at index 3. Additionally, takes a percentage as a parameter. This integer is
    the smallest percentage decrease and increase that we consider a V.Returns a list of data containing all of the start and end dates of V's in the list of data passed.
    """
    v_List = []
    day = day_High
    while (day < len(data) - 42):
        if (high_Day(day, data, day_High) == True):
            add_V = check_V(data, day, percent_V, day_High)
            if (add_V[0] == True):
                # start and end of v added to list
                v_List += [[data[day][0], data[add_V[1]][0], data[add_V[1] + add_V[2]][0]]]


                day = add_V[1] + add_V[2]
            else:
                day += add_V[1]
        else:
            day += 1
    return v_List


def high_Day(day, data, day_High):
    for spotDay in data[day - day_High: day]:
        if (spotDay[2] > data[day][2]):
            return False
    return True
    

def check_V(data, day, percent_V, day_High):
    """
    Accepts the same paramters 
    
    """
    #print(data[day][0] + "this is from check_V function")
    
    is_V = False
    # check to see if the next day increases
    # if so restart with the next day
    if (data[day + 1][2] > data[day][2]):
        return [is_V, 1] 
    else:
        # checking to see if anywhere in the next three months the price drops a given percentage
        start_V = True
        bottom_V = False
        end_V = False

        left_V = 1
        
        while ((float(data[day][2]) > float(data[day + left_V][2])) and left_V + day < len(data) and left_V < 21 and
               ((float(data[day][2]) - float(data[day + left_V][2])) / float(data[day][2]) < percent_V)):
            left_V += 1 

        # condition 1 or 2: 21 days go by or day reached was greater than original price and the percentage dropped was never reached 
        if ((left_V == 21) or (float(data[day][2]) <= float(data[day + left_V][2]))):
            return [is_V, left_V]

        # condition 3: reached the end of the data
        if (left_V + day == len(data)):
            return [is_V, left_V - 1]
        
        # condition 4: the percentage drop was reached
        elif ((float(data[day][2]) - float(data[day + left_V][2])) / float(data[day][2]) >= percent_V):

            # finding the bottom of the V
            bottom = find_Bottom_V(data, left_V, day)
            #print(data[day][0], data[bottom][0])

        
            right_V = 0
            peek_right = 0
            for right_V in range(42):
                if (float(data[bottom + right_V][2]) > float(data[bottom + peek_right][2])):
                    peek_right = right_V
                    if (high_Day(peek_right, data, day_High) == True):
                        break
            is_V = True
            return [is_V, bottom, peek_right]
        return [is_v, left_V]
                    
            
            # must make sure if the last day check was the lowest that it doesn't continue to decrease (wouldn't be considered a v)
            #if (bottom - day == 21):
                #****
                #if (data[bottom + 5][2] < data[bottom]):
                    #return [is_V, left_V]
            
##            # loop through the right side of the v to see if it reaches the original price within 42 days
##            right_V = 1
##            up = 10
##            number = 10
##            # condition 1: recovery within 42 days
##            # condition 2: no day decreases more than 1 percent
##            # condition 3: original day is greater than the day checked 
##            while (bottom + right_V < len(data) and right_V < 42 and
##                (float(data[bottom + right_V - 1][2]) - float(data[bottom + right_V][2])) / float(data[bottom + right_V - 1][2]) < .01 and up / number >= 0.7):
##                
##                if (data[bottom + right_V][2] > data[bottom + right_V - 1][2]):
##                    up += 1
##                number += 1
##                print(data[bottom + right_V][0], up / number)
##                right_V += 1
##                
##
##            if ((float(data[bottom + right_V - 1][2]) - float(data[bottom + right_V][2])) / float(data[bottom + right_V - 1][2]) >= .01 or up / number < 0.7):
##                print("yes" + data[bottom + right_V][0])
##                if (float(data[bottom + right_V][2]) >= float(data[day][2])):
##                    is_V = True
##                    return [is_V, bottom, right_V]
##            return [is_V, bottom + right_V - day]
##        else:
##            return [is_V, left_V]

    

def find_Bottom_V(data, left_V, day):
    bottom = day + left_V
    days_remaining = len(data) - (day + left_V)
    if (days_remaining > 20):
        for i in range(21 - left_V):
            if (data[day + left_V + i][2] < data[bottom][2]):
                bottom = day + left_V + i
    else:
        for i in range(days_remaining):
            if (data[day + left_V + i][2] < data[bottom][2]):
                bottom = day + left_V + i
                print(bottom)
    return bottom


def main():
    """
    Main function to test if the functions work.
    """
    file = "AnchorPathSPX2013-2019.txt"
    data = getData(file)
    percent_drop = .02
    day_High = 252
    v_List = track_V(data, percent_drop, day_High)

    
    print("Number of V's found:", len(v_List))
    print(v_List)
    
    
main() 
    
   
