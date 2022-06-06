#!/usr/bin/env python

import gVars


class Room:

    def setRoomNum(self, number):
        self.roomNum = number

    def setCapacity(self, capacity):
        self.capacity = capacity

    def __init__(self, number, capacity):
        self.roomNum = number
        self.capacity = capacity
        self.booklist = [False]*365

    def setBooked(self, startDay, endDay):
        if startDay>endDay:
            return
        if startDay == endDay:
            endDay = startDay + 1
        for i in range(startDay, endDay):
            self.booklist[i-1] = True

    def isAvailable(self, startDay, endDay):
        if startDay < 1 or endDay > 365 or startDay > endDay:
            return False

        isRoomAvailable = True
        if endDay == startDay:
            endDay = startDay + 1
        for i in range(startDay, endDay):
            if self.booklist[i-1]:
                isRoomAvailable = False;
                break;

        return isRoomAvailable


class Guest:

    def __init__(self, guestId, name):
        self.gusetId = guestId
        self.name = name


class Booking:

    def __init__(self, guestID, guestName, guestNum, roomNumber, ciDate, coDate, ciMonth, ciDay, coMonth, coDay):
        self.gusetID = guestID
        self.guestName = guestName
        self.guestNum = guestNum
        self.roomNumber = roomNumber
        self.ciDate = ciDate
        self.coDate = coDate
        self.ciMonth = ciMonth
        self.ciDay = ciDay
        self.coMonth = coMonth
        self.coDay = coDay

    def print2Nums(self, num):
        if num<10 and num>0:
            return "0"+str(num)
        return str(num)

    def printBooking(self, isByRoom):
        ret = ""
        if isByRoom==True:
            ret = "Guest " + str(self.gusetID) + " - " + str(self.guestName)
        else:
            ret = "Room " + str(self.roomNumber)
        ret = ret + ", " + str(self.guestNum) + " guest(s) from "
        ret = ret + self.print2Nums(self.ciMonth) + "/"
        ret = ret + self.print2Nums(self.ciDay) + " to "
        ret = ret + self.print2Nums(self.coMonth) + "/"
        ret = ret + self.print2Nums(self.coDay) + "."
        return ret


def printMainMenu() :
    print "Main Menu - please select an option:"
    print "1.) Add guest "
    print "2.) Add room "
    print "3.) Add booking "
    print "4.) View bookings "
    print "5.) Quit"


def handleAddGuest():
    sel = "A"
    while sel == "A":
        name = raw_input("Please enter guest name:")
        gVars.guestIdSeq += 1
        guestid = gVars.guestIdSeq
        guest = Guest(guestid, name);
        gVars.guestMap[guestid] = guest
        print "Guest "+name+" has been created with guest ID: "+str(guestid)
        sel = "";
        while sel != "R" and sel != "A":
            sel = raw_input("Would you like to [A]dd a new guest or [R]eturn to the previous menu?")


def handleAddRoom():
    sel = "A"

    while sel == "A":
        # input roomnum
        while True:
            roomNoStr = raw_input("Please enter room number:")
            roomNum = int(roomNoStr)
            if roomNum in gVars.roomMap:
                print "Room already exists."
            else:
                break

        capacityStr = raw_input("Please enter room capacity:")
        capacity = int(capacityStr)

        room = Room(roomNum, capacity)
        gVars.roomMap[roomNum] = room

        sel = ""
        while sel != "A" and sel != "R":
            sel = raw_input("Would you like to [A]dd a new room or [R]eturn to the previous menu?")


def handleAddBooking():
    #select guest
    while True:
        inputGuestID = raw_input("Please enter guest ID:")
        bookingGuestID = int(inputGuestID)
        if bookingGuestID > gVars.guestIdSeq or bookingGuestID not in gVars.guestMap:
            print "Guest does not exist."
        else:
            selGuest = gVars.guestMap[bookingGuestID]
            break

    #select room
    roomSelected = False
    while not roomSelected:
        inputRoom = raw_input("Please enter room number:")
        bookingRoomNo = int(inputRoom)
        if bookingRoomNo not in gVars.roomMap:
            print "Room does not exist."
            continue

        selectedRoom = gVars.roomMap[bookingRoomNo]
        inputGuestsNum = raw_input("Please enter number of guests:")
        guestsNum = int(inputGuestsNum)
        if selectedRoom.capacity < guestsNum:
            print "Guest count exceeds room capacity of: " + str(selectedRoom.capacity)
            selectedRoom = None
        else:
            roomSelected = True

    # input checkin month
    while True:
        inputCiMonth = raw_input("Please enter check-in month:")
        ciMonth = int(inputCiMonth)
        if ciMonth > 12 or ciMonth < 1:
            print "Invalid month."
        else:
            break
    #input checkin day
    while True:
        inputCiDay = raw_input("Please enter check-in day:")
        ciDay = int(inputCiDay)
        if isDayValidForMonth(ciDay, ciMonth):
            break
        else:
            print "Invalid day."

    startDay = dateToDayNumber(ciMonth, ciDay)

    # input checkout month
    while True:
        inputCoMonth = raw_input("Please enter check-out month:")
        coMonth = int(inputCoMonth)
        if coMonth > 12 or coMonth < 1 or coMonth<ciMonth:
            print "Invalid month."
        else:
            break
    # input checkout day
    while True:
        inputCoDay = raw_input("Please enter check-out day:")
        coDay = int(inputCoDay)
        tempEndDay = dateToDayNumber(coMonth, coDay);
        if isDayValidForMonth(coDay, coMonth) and startDay <= tempEndDay:
            break
        else:
            print "Invalid day."

    endDay = dateToDayNumber(coMonth, coDay)

    isRoomAvailable = selectedRoom.isAvailable(startDay, endDay)

    if not isRoomAvailable:
        print "Room is not available during that period. "
        roomSelected = False
        selectedRoom = None
        loopTimes = 0
        while not roomSelected:
            inputNewRoomNum = raw_input("Please enter new room number:")
            newRoomNum = int(inputNewRoomNum)
            if newRoomNum not in gVars.roomMap:
                print "Room does not exist."
                continue

            selectedRoom = gVars.roomMap[newRoomNum]
            if selectedRoom.capacity < guestsNum:
                print "Guest count exceeds room capacity of: " + str(selectedRoom.capacity)
                selectedRoom = None
            elif not selectedRoom.isAvailable(startDay, endDay):
                print "Room is not available during that period. "
                selectedRoom = None
            else:
                roomSelected = True

            loopTimes += 1
            if loopTimes > 3 and not roomSelected:
                print "*** maybe no suitable room for booking, will return to main menu ***"
                return

    booking = Booking(bookingGuestID, selGuest.name, guestsNum, selectedRoom.roomNum, startDay, endDay, ciMonth, ciDay, coMonth, coDay);
    gVars.bookingList.append(booking);
    selectedRoom.setBooked(startDay, endDay);
    print "*** Booking successful! ***"


def dateToDayNumber(month, day):
    if day < 1 or day > 31 or month < 1 or month >12:
        return 0
    if month == 1:
        return day
    if month == 2:
        return 31 + day
    if month == 3:
        return 59 + day
    if month == 4:
        return 90 + day
    if month == 5:
        return 120 + day
    if month == 6:
        return 151 + day
    if month == 7:
        return 181 + day
    if month == 8:
        return 212 + day
    if month == 9:
        return 243 + day
    if month == 10:
        return 273 + day
    if month == 11:
        return 304 + day
    return 334 + day


def isDayValidForMonth(day, month):
    if day < 1:
        return False
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        maxDay = 31
    elif month == 2:
        maxDay = 28
    else:
        maxDay = 30

    if day > maxDay:
        return False
    return True


def viewRoomBookings():
    while True:
        roomNumStr = raw_input("Please enter room number:")
        roomNum = int(roomNumStr)
        if roomNum in gVars.roomMap:
            print "Room " + str(roomNum) + " bookings:"
            for booking in gVars.bookingList:
                if booking.roomNumber == roomNum:
                    print booking.printBooking(True)
            break
        else:
            print "Room does not exist."


def viewGuestBookings():
    while True:
        inputStr = raw_input("Please enter guest ID:")
        inputGuestId = int(inputStr)
        if inputGuestId in gVars.guestMap:
            print "Guest " + str(inputGuestId) + ":" + str(gVars.guestMap[inputGuestId].name)
            for booking in gVars.bookingList:
                if booking.gusetID == inputGuestId:
                    print booking.printBooking(False)
            break
        else:
            print "Guest does not exist."


def handleViewBookings():
    sel = ""
    while True:
        sel = raw_input("Would you like to view [G]uest bookings, [R]oom booking, or e[X]it?")
        if sel == "G":
            viewGuestBookings()
        elif sel == "R":
            viewRoomBookings()
        elif sel == "X":
            break


def handleExitSystem():
    print "Thanks for using FedUni Hotel Bookings!"


def handleMainMenu():
    sel=1
    while sel!=5:
        printMainMenu()
        selstr = raw_input()
        sel = int(selstr)
        if sel==1:
            handleAddGuest()
        elif sel==2:
            handleAddRoom()
        elif sel==3:
            handleAddBooking()
        elif sel==4:
            handleViewBookings()
        elif sel==5:
            handleExitSystem()
        else:
            print "Value must be between 1 and 5. Please try again:"

def preCreateTestData():
    gVars.guestIdSeq += 1
    guestid = gVars.guestIdSeq
    guest1 = Guest(guestid, "eee")
    gVars.guestMap[guestid] = guest1

    gVars.guestIdSeq += 1
    guestid = gVars.guestIdSeq
    guest2 = Guest(guestid, "isa")
    gVars.guestMap[guestid] = guest2

    room1 = Room(101, 3)
    room2 = Room(102, 4)
    gVars.roomMap[101] = room1
    gVars.roomMap[102] = room2


print "-----------------------------------------------"
print "------ Welcome to FedUni Hotel Bookings ------- "
print "-----------------------------------------------"

preCreateTestData()
handleMainMenu()




