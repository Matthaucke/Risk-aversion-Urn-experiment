
# 16.01.2017

# Imports
import sys
from random import randint
from clickableLabel import *
from os import listdir
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Ass2V6 import *

# Main Program
app = QApplication(sys.argv)
window = QMainWindow()

ui = Ui_MainWindow()
ui.setupUi(window)


# My own code start here!
#
# Main variables
window.destinationFile              = "SPSSfile.csv"  # Resultfile
window.EmailListFile                = "EmailLottery.csv"
window.page                         = 0
window.experimentCondition          = 0 # 0 = 100, 1= 10, 2 = 2
window.experimentConditionPosition  = 0 # 0 = urn A = 50/50 and urn B is unknown, 1 = urn A is unknown and urn B is 50/50
window.Age                          = 0
window.Gender                       = ""
window.Education                    = ""
window.Nationality                  = ""
window.experimentConditionList      = [100,10,2]
window.experiment5050SplitPoint     = 0
window.experimentUnknownSplitPoint  = 0
window.experimentRandom             = -1
window.positiveExperimentCounter    = 0                         # number of positive results
window.activeExperimentRound        = 0                         # Variable to hold the active experiment round on page 3
window.positiveExperimentExists     = False                     # Shows if a positive result on page 3 exists
window.choosenUrnList               = ["",""]
window.marbleList                   = ["",""]
window.selectedConditionList        = [0,0]                     # random urn = 0, 50/50 urn = 1
window.widthWidget                  = 1261                      # Width of StackedWidget
window.heightWidget                 = 781                       # Height of StackedWidget
window.RandUrnName                  = "Urn B"                   # Urn B is default Random
window.FiftyFiftyUrnName            = "Urn A"                   # Urn A is default 50/50

# Functionlibrary
#
# Open Fullscreen and center widget:
def windowfullscreen():
    window.showFullScreen()
    windowCentreH = window.width()/2
    windowCentreV = window.height()/2
    ui.stackedWidget.setGeometry(windowCentreH - window.widthWidget/2, windowCentreV - window.heightWidget/2,
                         window.widthWidget, window.heightWidget)

# Initialize the SPSS-File and decide in which conditions the participant is going to be
def InitFileAndExperiment():
    if window.destinationFile in listdir():                         # Look for result file and create a new one, if it does not exist
        file = open(window.destinationFile, 'r')
        lines = file.readlines()

        for line in lines:
            dataList = []
            dataList.append(line.split(','))

        try: # try is used In case experiment crashed before files could have been stored
            window.experimentCondition  = int(dataList[-1][4]) + 1  # Get the last condition!
            if window.experimentCondition > 2:                      # set the limit of the conditions to 2
                window.experimentCondition = 0                      # set the condition to the start value when the limit is reached
        except:
            print ("exception found but has not to be handled")

    else:
        file = open(window.destinationFile, 'w')
        header = "Age,Gender,Education,Nationality,ExpCond,CondPositon,ChoosenUrn1,Marble1,ChoosenUrn2,Marble2"
        file.write(header)

    # Save variables for position and splitpoints
    window.experimentConditionPosition  = randint(0, 1)                 # 0 = urn A = 50/50 and urn B is unknown, 1 = urn A is unknown and urn B is 50/50
    window.experiment5050SplitPoint     = int(window.experimentConditionList[window.experimentCondition]/2)     # either 50, 5 or 1
    window.experimentUnknownSplitPoint  = randint(0,window.experimentConditionList[window.experimentCondition]) # Red marbels, ranging from 0 to 2/10/100

    #Save which Urn is random or 50/50. Urn B is default Random and Urn A is default 50/50
    if window.experimentConditionPosition == 1:                         #  1 = urn A is unknown and urn B is 50/50
        window.RandUrnName = "Urn A"
        window.FiftyFiftyUrnName = "Urn B"

# Save the data of the experiment
def saveExperiment():
    if window.destinationFile in listdir():
        file = open(window.destinationFile, 'a')

        detail = "\n {0:d},{1:s},{2:s},{3:s},{4:d},{5:d},{6:d},{7:s},{8:d},{9:s}".format(
            window.Age
            , window.Gender
            , window.Education
            , window.Nationality
            , window.experimentCondition
            , window.experimentConditionPosition
            , window.selectedConditionList[0]
            , window.marbleList[0]
            , window.selectedConditionList[1]
            , window.marbleList[1])

        file.write(detail)
        file.close()

# Function to enable the Entry-fields of Page 1 after the defined time ia reached
def handlePage1Timer():
    window.secondPage1 += 1
    if window.secondPage1 == 10:  # 10 seconds, so people read the consent form!
        window.timerPage1.stop()
        ui.Consent.setEnabled(True)
        ui.CheckYes.setEnabled(True)
        ui.CheckNo.setEnabled(True)
        ui.Continue.setEnabled(True)

# General Action handler for available actions of page 1 (Consent form)
def ActionHandlerPage1():
    if ui.CheckYes.isChecked():
        window.page = 1
        ui.stackedWidget.setCurrentIndex(window.page)
    else:
        ui.DontParticipate.show()  # show Widget with error message and leave button

# Function to init and handle the tasks for Page 1 (Consent form)
def InitAndHandlePage1():
    ui.DontParticipate.hide()  # hides Leave message and button

    # Timer after 10 Second you can continue! To make sure people don't skip the consent form!
    window.timerPage1 = QTimer()
    window.secondPage1 = 0
    window.timerPage1.start(1000)
    window.timerPage1.timeout.connect(handlePage1Timer)

    # Connect the Continue-Button with the action handler for page 1
    ui.Continue.clicked.connect(ActionHandlerPage1)
    # Connect the Leave-BUtton with last action hander for page 5
    ui.LeaveExp.clicked.connect(ActionHandlerPage5)  # Allows to terminate the experiment

# General Action handler for available actions of page 2 (Demographics)
def ActionHandlerPage2():
    errorDetected = False

    if ui.Age.value() == 0 or ui.Age.value() < 10:  # Restrict age to a realistic age of a student participant
        ui.ErrorAge.show()
        errorDetected = True
    else:
        window.Age = ui.Age.value()
        ui.ErrorAge.hide()

    if ui.Male.isChecked():
        window.Gender = "male"
        ui.ErrorGender.hide()
    elif ui.Female.isChecked():
        window.Gender = "female"
        ui.ErrorGender.hide()

    if not ui.Male.isChecked() and not ui.Female.isChecked():
        ui.ErrorGender.show()
        errorDetected = True

    if ui.Degree.currentText() == "Please indicate":
        ui.ErrorDegree.show()
        errorDetected = True
    else:
        window.Education = ui.Degree.currentText()
        ui.ErrorDegree.hide()

    if ui.Nationality.currentText()== "Please indicate":
         ui.ErrorNationality.show()
         errorDetected = True
    else:
        window.Nationality = ui.Nationality.currentText()
        ui.ErrorNationality.hide()

    if errorDetected == False:
        window.page = 2
        ui.stackedWidget.setCurrentIndex(window.page)

        # Set timer for third page, so it starts when user switched over to third pages
        TimerPage3()

# Function to init and handle the tasks for Page 2 (Demographics)
def InitAndHandlePage2():
    # hide the error messages
    ui.ErrorAge.hide()
    ui.ErrorDegree.hide()
    ui.ErrorGender.hide()
    ui.ErrorNationality.hide()

    ui.Continue2.clicked.connect(ActionHandlerPage2)

# This is the animation of the marble going up on page 3
def animatePage3():

    if window.choosenUrnList[window.activeExperimentRound] == "B":
        if window.marbleList[window.activeExperimentRound] == "blue":
            currentY = ui.UrnBBlue.y()
            if ui.UrnBBlue.y() > 390:
                ui.UrnBBlue.setGeometry(809, currentY - 10,40,40)
            else:
                window.timerAnimationPage3.stop()
                ui.MessageMarble.show()

        else:
            currentY = ui.UrnBRed.y()
            if ui.UrnBRed.y() > 390:
                ui.UrnBRed.setGeometry(809, currentY - 10, 40, 40)
            else:
                window.timerAnimationPage3.stop()
                ui.MessageMarble.show()
    else:
        if window.marbleList[window.activeExperimentRound] == "blue":
            currentY = ui.UrnABlue.y()
            if ui.UrnABlue.y() > 390:
                ui.UrnABlue.setGeometry(353, currentY - 10,40,40)
            else:
                window.timerAnimationPage3.stop()
                ui.MessageMarble.show()
        else:
            currentY = ui.UrnARed.y()
            if ui.UrnARed.y() > 390:
                ui.UrnARed.setGeometry(353, currentY - 10, 40, 40)
            else:
                window.timerAnimationPage3.stop()
                ui.MessageMarble.show()

# Function to start the Timer for the animation
def startAnimationPage3():
    window.timerAnimationPage3 = QTimer()
    window.timerAnimationPage3.timeout.connect(animatePage3)
    window.timerAnimationPage3.start(50)

# General Action handler for available actions of page 3 (Experiment-page)
# I set the following as defaults so that I only need one "if condition"
def ActionHandlerPage3():

    splitPoint                                                  = window.experimentUnknownSplitPoint # default splitpoint
    window.choosenUrnList[window.activeExperimentRound]         = "A"                                # default selected urn
    window.selectedConditionList[window.activeExperimentRound]  =  0                                 # 0 = Random urn choosen!
    window.marbleList[window.activeExperimentRound]             = "red"                              # default marble
    window.messageNextRound = "Now you have a second chance to enter the £30 lottery!"               # default loosing message!

    # get the clicked Urn by checking its position in the StackedWidget
    btnClicked = window.sender()
    if (btnClicked.x() == 740):
        window.choosenUrnList[window.activeExperimentRound] = "B"
    # So participants only can click once
    window.urnA.setEnabled(False)
    window.urnB.setEnabled(False)

    # Calculate the min value of the randomization of the experiment.
    if (window.choosenUrnList[window.activeExperimentRound] == "A"):
        if (window.experimentConditionPosition == 0): # 0 = Urn A is 50/50!
            window.selectedConditionList[window.activeExperimentRound]  = 1 # 1 = 50/50 Condition is selected
            splitPoint                                                  = window.experiment5050SplitPoint
    else:
        if (window.experimentConditionPosition == 1): # 1 = Urn B is 50/50!
            window.selectedConditionList[window.activeExperimentRound]  = 1 # 1 = 50/50 Condition is selected
            splitPoint                                                  = window.experiment5050SplitPoint

    # This calculates the random number to decide whether participant has drawn a blue or red marble!
    # If we are in the 50/50 condition we need a 50% probability to either draw red or blue
    # the split point of the 50/50 urn is always half of the max numbers of marbles, so 1, 5 o 50.
    # The splitPoint of the unknown ratio urn can be thought of as the number of red marbles in the condition: It can range from 0 to 2/10/100
    # In case of the random urn, if the splitPoint = 0 then it's ALWAYS a blue marble (As if 0 red marbles are in the urn)
    # If splitpoint is the maximum of marbles of the condition, so either 2/10/00 then marble will ALWAYS be red
    # (As if only 2/10/100 red marbles are in the urn).
    window.experimentRandom = randint(1, window.experimentConditionList[window.experimentCondition])

    # Only if the window.experimentRandom is bigger (NOT EQUAL!) than the splitpoint, then we have drawn a blue marble, otherwise it is a red marble!
    if (window.experimentRandom > splitPoint):
        window.marbleList[window.activeExperimentRound] = "blue"
        window.messageNextRound = "You will enter the £30 lottery, now you can even double your chance to win!" # this saves the winning message

    # Calculate the experiment result
    if ((window.activeExperimentRound == 0 and window.marbleList[window.activeExperimentRound]    == "blue")  or
        (window.activeExperimentRound == 1 and window.marbleList[window.activeExperimentRound]    == "red" )       ):
        window.positiveExperimentCounter    += 1
        window.positiveExperimentExists     = True
        buttonMessage   = "Congratulation"
    else:
        buttonMessage   = "Bad luck"

    # Finalize the message and print it out
    buttonMessage = buttonMessage + ", you have picked a " + window.marbleList[window.activeExperimentRound] + " marble. Please press continue"

    # This shows "start the next round" if we are in the first round!!
    if (window.activeExperimentRound == 0 ):
        buttonMessage = buttonMessage + " to start the next round"

    ui.Outcome.setText(buttonMessage)

    # Now all decisions have been done, and we can save the result
    if (window.activeExperimentRound == 1 ):
        saveExperiment()

    # Start the animation:
    startAnimationPage3()

# Function to init and handle the tasks for Page 3 (Experiment-page)
def InitAndHandlePage3():

    # Condition text, depending on the active experiment round, 0 = 1st round, 1= 2nd round
    # Urn A is always left, Urn B is always right!
    if ( window.activeExperimentRound == 0):

        window.HundredMarbles = "Consider the following problem carefully, then click on one of the urns. On the table are two urns, labelled A and B, " \
                            "containing red and blue marbles, and you have to draw a marble from one of the urns. If you get a blue marble, you will be entered " \
                            "into a £30 lottery draw.\n"+window.FiftyFiftyUrnName+" contains 50 red marbles and 50 blue marbles. "+window.RandUrnName+ \
                            " contains 100 marbles in an unknown color ratio, from 100 red marbles and 0 blue marbles to 0 red marbles and 100 blue marbles. " \
                            "The mixture of red and blue marbles in "+window.RandUrnName+" has been decided by writing the numbers 0, 1, 2, . . ., 100 " \
                            "on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. " \
                            "The number chosen was used to determine the number of blue marbles to be put into "+window.RandUrnName+", but you " \
                            "do not know the number. Every possible mixture of red and blue marbles in "+window.RandUrnName+" is equally likely.\nYou have " \
                            "to decide whether you prefer to draw a marble at random from Urn A or Urn B. " \
                            "What you hope is to draw a blue marble and be entered for the £30 lottery draw. Consider very carefully from which urn you" \
                            " prefer to draw the marble, then click on one of the urns below."

        window.TenMarbles = "Consider the following problem carefully, then click on one of the urns. On the table are two urns, labelled A and B, " \
                            "containing red and blue marbles, and you have to draw a marble from one of the urns. If you get a blue marble, you will be entered " \
                            "into a £30 lottery draw.\n"+window.FiftyFiftyUrnName+" contains 5 red marbles and 5 blue marbles. "+window.RandUrnName+ \
                            " contains 10 marbles in an unknown color ratio, from 10 red marbles and 0 blue marbles to 0 red marbles and 10 blue marbles. " \
                            "The mixture of red and blue marbles in "+window.RandUrnName+" has been decided by writing the numbers 0, 1, 2, . . ., 10 " \
                            "on separate slips of paper, shuffling the slips thoroughly, and then drawing one of them at random. " \
                            "The number chosen was used to determine the number of blue marbles to be put into "+window.RandUrnName+", but you " \
                            "do not know the number. Every possible mixture of red and blue marbles in "+window.RandUrnName+" is equally likely.\nYou have " \
                            "to decide whether you prefer to draw a marble at random from Urn A or Urn B. " \
                            "What you hope is to draw a blue marble and be entered for the £30 lottery draw. Consider very carefully from which urn you" \
                            " prefer to draw the marble, then click on one of the urns below."

        window.TwoMarbles = "Consider the following problem carefully, then click on one of the urns. On the table are two urns, labelled A and B, " \
                            "containing red and blue marbles, and you have to draw a marble from one of the urns. If you get a blue marble, you will be entered " \
                            "into a £30 lottery draw.\n"+window.FiftyFiftyUrnName+" contains 1 red marble and 1 blue marble. "+window.RandUrnName+ \
                            " contains 2 marbles in an unknown color ratio, from 2 red marbles and 0 blue marbles to 0 red marbles and 2 blue marbles. " \
                            "The mixture of red and blue marbles in "+window.RandUrnName+" has been decided by writing the numbers 0, 1, 2 on separate slips" \
                            " of paper, shuffling the slips thoroughly, and then drawing one of them at random. The number " \
                            "chosen was used to determine the number of blue marbles to be put into "+window.RandUrnName+", but you do not know " \
                            "the number. Every possible mixture of red and blue marbles in "+window.RandUrnName+" is equally likely." \
                            "\nYou have to decide whether you prefer to draw a marble at random from Urn A or Urn B. " \
                            "What you hope is to draw a blue marble and be entered for the £30 lottery draw. Consider very carefully from which urn you" \
                            " prefer to draw the marble, then click on one of the urns below."

        # Creates clickable label
        # The following setting are only once necessary, so we do them in Round 0
        window.urnA = ClickableLabel(ui.page3)
        window.urnA.setPixmap(QtGui.QPixmap(("urn.jpg")))
        window.urnA.setScaledContents(True)
        window.urnA.setGeometry(280, 450, 185, 255)
        window.urnA.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))# Changing cursor hints the participants where to click
        window.urnA.setEnabled(False)

        window.urnB = ClickableLabel(ui.page3)
        window.urnB.setPixmap(QtGui.QPixmap(("urn.jpg")))
        window.urnB.setScaledContents(True)
        window.urnB.setGeometry(740, 450, 185, 255)
        window.urnB.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        window.urnB.setEnabled(False)

        window.urnA.clicked.connect(ActionHandlerPage3)
        window.urnB.clicked.connect(ActionHandlerPage3)

    else:

        # Change the text for the next round!
        window.HundredMarbles = window.messageNextRound + " In the first draw the winning marble was blue, however in this second " \
                            "draw the winning marble is red!\nMoreover, the marble you have chosen was re-entered into the urn and" \
                            " the ratios of marbles in both urns are the same as in the first round.\nAgain, "+window.FiftyFiftyUrnName+" contains 50 red marbles and 50 blue marbles. " \
                            +window.RandUrnName+" contains 100 marbles in the exact same unknown color ratio as in the first round, from 100 red marbles and 0 blue marbles to 0 red marbles and 100 blue " \
                            "marbles.\nYou have to decide whether you prefer to draw a marble at random from Urn A or Urn B. This time you " \
                            "hope to draw a red marble and be entered for the £30 lottery draw."

        window.TenMarbles = window.messageNextRound + " In the first draw the winning marble was blue, however in this second " \
                            "draw the winning marble is red!\nMoreover, the marble you have chosen was re-entered into the urn and" \
                            " the ratios of marbles in both urns are the same as in the first round.\nAgain, " +window.FiftyFiftyUrnName + " contains 5 red marbles and 5 blue marbles. " \
                            + window.RandUrnName + " contains 10 marbles in the exact same unknown color ratio as in the first round, from 10 red marbles and 0 blue marbles to 0 red marbles and 10 blue " \
                            "marbles.\nYou have to decide whether you prefer to draw a marble at random from Urn A or Urn B. This time you " \
                            "hope to draw a red marble and be entered for the £30 lottery draw."

        window.TwoMarbles = window.messageNextRound + " In the first draw the winning marble was blue, however in this second " \
                            "draw the winning marble is red!\nMoreover, the marble you have chosen was re-entered into the urn and" \
                            " the ratios of marbles in both urns are the same as in the first round.\nAgain, " + window.FiftyFiftyUrnName + " contains 1 red marble and 1 blue marble. " \
                            + window.RandUrnName + " contains 2 marbles in the exact same unknown color ratio as in the first round, from 2 red marbles and 0 blue marbles to 0 red marbles and 2 blue " \
                            "marbles.\nYou have to decide whether you prefer to draw a marble at random from Urn A or Urn B. This time you " \
                            "hope to draw a red marble and be entered for the £30 lottery draw."


        # Put marbles back:
        ui.UrnABlue.setGeometry(353, 520, 40, 40)
        ui.UrnARed.setGeometry(353, 520, 40, 40)
        ui.UrnBBlue.setGeometry(809, 520, 40, 40)
        ui.UrnBRed.setGeometry(809, 520, 40, 40)
        TimerPage3()

    # hide message for marble draw
    ui.MessageMarble.hide()

    # set text
    if window.experimentCondition == 0: # window.experimentCondition 0 = 100 marbles
        ui.ChangeInstr.setText(window.HundredMarbles)
    elif window.experimentCondition == 1: # window.experimentCondition 1 = 10 marbles
        ui.ChangeInstr.setText(window.TenMarbles)
    elif window.experimentCondition == 2: # window.experimentCondition 2 = 2 marbles
        ui.ChangeInstr.setText(window.TwoMarbles)


# Timer for Page 3 ! Starts at InitandHandlePage2
def handlePage3Timer():
    window.secondPage3 += 1
    if window.secondPage3 == 10:  # 10 seconds so participants read the instructions
        window.timerPage3.stop()
        window.urnA.setEnabled(True)
        window.urnB.setEnabled(True)

def TimerPage3():
    window.timerPage3 = QTimer()
    window.secondPage3 = 0
    window.timerPage3.start(1000)
    window.timerPage3.timeout.connect(handlePage3Timer)

# Method to handle the Continue-Event of page 3
def HandlePage3Continue():
    if (window.activeExperimentRound == 0 ):

        # Increase the actual experiment round
        window.activeExperimentRound += 1
        InitAndHandlePage3()
    else:
        if (window.positiveExperimentExists == True ):
            window.page = 3
        else:
            window.page = 4

        ui.stackedWidget.setCurrentIndex(window.page)

# I write this in a separate file, because in a real experiment we should not be able to trace back the contact details
# to the experiment data!
def EmailList():

    if window.EmailListFile in listdir():
        file = open(window.EmailListFile, 'a')
    else:
        file = open(window.EmailListFile, 'w')

    for i in range(0,window.positiveExperimentCounter):
        file.write(window.EmailAddress + "\n")
    file.close()

def ActionHandlerPage4():
    errorDetected   = False

    ui.ErrorClick.hide()
    ui.ErrorEmail.hide()

    if not ui.YesParticipate.isChecked() and not ui.NoParticipate.isChecked():
        ui.ErrorClick.show()
        errorDetected = True
    elif ui.YesParticipate.isChecked():
        if ui.Email.text().find("@") == -1 or ui.Email.text().find(".") == -1: # Check whether people typed in a valid e-mail!
            ui.ErrorEmail.show()
            errorDetected = True
        else:
            window.EmailAddress = ui.Email.text()
            EmailList()

    # everything ist ok, so let us leave the Page
    if ( errorDetected == False):
        window.page = 4
        ui.stackedWidget.setCurrentIndex(window.page)

# Initialize Page 4 (E-mail Page)
def InitAndHandlePage4():

    ui.ErrorClick.hide()
    ui.ErrorEmail.hide()

    ui.Continue4.clicked.connect(ActionHandlerPage4)

# Exit the experiment!
def ActionHandlerPage5():
    QApplication.quit()

# Initialize Page 5 (Debrief):
def InitAndHandlePage5():
    ui.terminateExp.clicked.connect(ActionHandlerPage5)

# Initiliazation of the experiment
#
# Open Fullscreen:
windowfullscreen()

# Initialization of all the experiment pages
InitFileAndExperiment()

# Init and handle page 1 (Consent form)
ui.stackedWidget.setCurrentIndex(window.page)
InitAndHandlePage1()

# Init and handle page 2 (Demographics)
InitAndHandlePage2()

# Init and handle page 3 (Experiment page)
ui.Continue3.clicked.connect(HandlePage3Continue)
InitAndHandlePage3()

# Init and handle page 4 (Email page)
InitAndHandlePage4()

# Init and handle page 5 (Debrief)
InitAndHandlePage5()
#
# My own code ends here!
#
window.show()
sys.exit(app.exec_())
