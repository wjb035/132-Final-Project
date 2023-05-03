from serial.tools.list_ports import comports
from tkinter import *
import re
window=Tk()
window.title("Laundro Buddy")
window.geometry('1300x660')
window.configure(bg="white")
global tide
tide=["original scent","ultra oxi","free and gentle","with downy","hygenic clean"]
global percil
percil=["original scent","oxi power", "odor fighter","stain fighter","intense fresh"]
global purex
purex=["mountain breeze","natural elements","baby soft"]
global seventhgeneration
seventhgeneration=["all scents"]
global all
all=["free clear","free clear eco", "free clear oxi", "odor relief"]
global gain
gain=["original scent"]

#global armandhammer
#armandhammer=["sensitive skin","plus oxiclean","clean burst"]

global detergents
detergents=[tide,percil,purex,seventhgeneration,all,gain]
global detergentstr
detergentstr=["tide","percil","purex","seventhgeneration","all","gain"]
global weightdetected
weightdetected=False
global weight
weight=0
import serial
global calibrated
calibrated=False
tnr="times new roman"
class Text(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.guisetup()

    def guisetup(self):
        deterlabel=Label(text="Please enter your detergent type:",
                        font=(tnr,20),bg="white")
        recentlabel=Label(text="Recently used detergents:",
                        font=(tnr,20),bg="white")
        orlabel=Label(text="Or select a popular detergent type:",
                        font=(tnr,20),bg="white")
        resultlabel=Label(text="Search Results:",
                          font=(tnr,18),bg="white")
        deterlabel.place(x=15,y=20)
        recentlabel.place(x=700,y=20)
        orlabel.place(x=15,y=250)
        resultlabel.place(x=15,y=85)
class Interactable(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.yesstat=False
        self.ser=False
        self.recentlist= []
        self.setup() 
        self.resultconfigure(["","","",""])
        self.recentconfigure(["","","","","",""])
        self.populars()
        self.menusetup()
        self.clearsetup()
        self.colorbutton()
    @property
    def recentlist(self):
        return self._recentlist
    
    @recentlist.setter
    def recentlist(self,val):
        self._recentlist=val

    @property
    def yesstat(self):
        return self._yesstat
    
    @yesstat.setter
    def yesstat(self,val):
        self._yesstat=val
    @property
    def weightlab(self):
        return self._weightlab
    
    @weightlab.setter
    def weightlab(self,val):
        self._weightlab=val
    
    @property
    def ser(self):
        return self._ser
    
    @ser.setter
    def ser(self,val):
        self._ser=val

    def setup(self):
        deterentry=Entry(width=30,font=(tnr,16))
        enter=Button(text="Enter",font=(tnr,14),fg="black",bg="white",command=lambda:self.enter(deterentry))
         
        deterentry.place(x=15,y=55)
        enter.place(x=385,y=55)
    
    def sanitize(self,entry):
        entry=entry.replace(" ","")
        entry=entry.lower()
        remover=re.findall('[a-z]', entry) 
        entry="".join(map(str,remover))
        return entry

    def enter(self,entry):
        self.clear()
        entry=entry.get()
        searches=[]
        for i in range(len(detergents)):
            for search in detergents[i]:
                if self.sanitize(entry) in detergentstr[i]+self.sanitize(search):
                    searches.append(detergentstr[i]+" "+search)
                
        while len(searches)<4:
            searches.append("")
        self.resultconfigure(searches)

    def weightreset(self):
        try:
            self.weightlab.destroy()
        except:
            pass
    def getweight(self):
        self.clear()
        weightheader=Label(window,text="Weight:",font=(tnr,20))
        weightheader.place(x=700,y=450)
        status=""
        self.weightreset()
        if calibrated==True:
            try:
                while len(status)<1:
                    self.ser.reset_input_buffer()
                    status=self.ser.readline().decode()
                    print(status)
                status= re.findall(r"[-+]?(?:\d*\.*\d+)",status)
                if len(status) >1:
                    status=status[1]
                else: 
                    status=status[0]
                global weight
                weight=status
                global weightdetected
                weightdetected=True
                self.weightlab=Label(window,text=f"{status} grams",font=(tnr,16))
                self.weightlab.place(x=700,y=500)
            except:
                self.weightlab=Label(window,text=f"There was an issue with the weight sensor.\nPlease try again, or try calibrating/recalibrating.")
                self.weightlab.place(x=700,y=500)
        else:
            self.weightlab=Label(window,text=f"You haven't calibrated the weight sensor yet,\ntry doing that in settings first!",font=(tnr,16))
            self.weightlab.place(x=700,y=500)

    def menusetup(self):
        settings=Button(window,text="Calibrate Sensors",font=(tnr,16),command=lambda:self.weightsetup())
        settings.place(x=1000,y=600)
        getweight=Button(window,text="Get Weight",font=(tnr,16),command=lambda:self.getweight())
        getweight.place(x=790,y=600)

    def yesstatfunc(self):
        self.yesstat=True
        self.weightsetup()

    
    def weightsetup(self):
        self.clear()
        if weightdetected==True:
            pass
        global detergenthelp
        detergenthelp=Frame(width=600,height=400,bg="white")
        detergenthelp.place(x=350,y=150)
        checklabel=Label(master=detergenthelp,text=f"Ready to calibrate the sensor?\nIf not, press the clear button!\nIf so, press the yes button!\nIt will take 15-20s, that is normal.\nPlace the calibration tool on the scale\n 2 seconds after pressing yes.",font=(tnr,20))
        checklabel.place(x=100)
        checkbutton=Button(master=detergenthelp,text="Yes",font=(tnr,18),command=lambda: self.yesstatfunc())
        checkbutton.place(x=250,y=200)
        
        if self.yesstat==True:
            try:
                if "ttyACM1" in port:
                    self.ser = serial.Serial('/dev/ttyACM1', baudrate=9600, timeout=1)
                elif "ttyACM0" in port:
                    self.ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)

                counter=0
                while counter<15:
                    status=self.ser.readline().decode("ascii")
                    if len(status) > 4:
                        print(status)
                        counter+=1
                status= re.findall(r"[-+]?(?:\d*\.*\d+)",status)
                status=status[1]
                print(status)
                checkbutton.destroy()
                checklabel.destroy()
                checklabel=Label(master=detergenthelp,text=f"Sensor has been calibrated!\n You can now check the weight of your object.",font=(tnr,20))
                checklabel.place(x=80)
                self.yesstat=False
                global calibrated
                calibrated=True
            except:
                checklabel.destroy()
                checklabel=Label(master=detergenthelp,text=f"There was an issue calibrating the sensor.\nIf you would like to recalibrate,\n unplug the blue cable for about 20 seconds and\nplug it back in.",font=(tnr,20))
                checklabel.place(x=70)
                self.yesstat=False

    def colorbutton(self):
        color=Button(window,text="Colors",font=(tnr,16),command=lambda:self.colorchangeformat())
        color.place(x=1180,y=600)
    def colorchangeformat(self):
        self.clear()
        global detergenthelp
        detergenthelp=Frame(width=600,height=200,bg="white")
        detergenthelp.place(x=350,y=150)
        white="#FFFFFF"
        blue="#60e6ff"
        purple="#9c60ff"
        pink="#ff60a7"
        red="#ff142f"
        green="#1aff14"
        colorlabel=Label(detergenthelp,text="Select the color you'd like to use:",font=(tnr,24),bg="white")
        colorlabel.place(x=70)
        bluebutton=Button(master=detergenthelp,text="Blue",bg=blue,font=(tnr,18),command=lambda:self.colorchanger(blue))
        bluebutton.place(x=140,y=100)
        whitebutton=Button(master=detergenthelp,text="White",bg=white,font=(tnr,18),command=lambda:self.colorchanger(white))
        whitebutton.place(x=50,y=100)
        purplebutton=Button(master=detergenthelp,text="Purple",bg=purple,font=(tnr,18),command=lambda:self.colorchanger(purple))
        purplebutton.place(x=215,y=100)
        pinkbutton=Button(master=detergenthelp,text="Pink",bg=pink,font=(tnr,18),command=lambda:self.colorchanger(pink))
        pinkbutton.place(x=310,y=100)
        redbutton=Button(master=detergenthelp,text="Red",bg=red,font=(tnr,18),command=lambda:self.colorchanger(red))
        redbutton.place(x=385,y=100)
        greenbutton=Button(master=detergenthelp,text="Green",bg=green,font=(tnr,18),command=lambda:self.colorchanger(green))
        greenbutton.place(x=455,y=100)

    def colorchanger(self,color):
        window.configure(bg=color)

    def clearsetup(self):
        clear=Button(window,text="Clear",font=(tnr,16),command=lambda:self.clear())
        clear.place(x=920,y=600)
    def clear(self):
        try:
            detergenthelp.destroy() 
        except:
            pass
    def weightget(self):
        weightgrams=float(weight)
        weightpoundsraw=weightgrams/453.6
        weightpounds=round(weightpoundsraw,2)
        return weightpounds
    
    def amountcalc(self,text):
        weight = self.weightget()
        amount=0
        if "tide" in text:
            if weight <= 6:
                amount=(weight / 6) * 45
            elif weight <= 11:
                amount=(weight / 11) * 65
            elif weight <= 16:
                amount=(weight / 16) * 90
            elif weight <= 21:
                amount=(weight/21) * 120
            else: 
                amount=120
        elif "percil" in text:
            if "original scent" in text or "intense fresh" in text:
                if weight <=11:
                    amount=(weight/11) * 45
                elif weight<=16:
                    amount=(weight/16)*75
                elif weight<=21:
                    amount=(weight/21)*105
                else: 
                    amount=105
            elif "oxi power" in text or "odor fighter" in text or "stain fighter" in text:
                if weight <=11:
                    amount=(weight/11)*59
                elif weight<=16:
                    amount=(weight/16)*75
                elif weight<=21:
                    amount=(weight/21)*90
            else:
                amount=95
        elif "purex" in text:
            if "mountain breeze" in text or "natural elements" in text:
                if weight<=11:
                    amount=(weight/11)*42
                elif weight<=16:
                    amount=(weight/11)*63
                elif weight<=21:
                    amount=(weight/21)*85
                else:
                    amount=90
            elif "baby soft" in text:
                if weight<=11:
                    amount=(weight/11)*35
                elif weight<=16:
                    amount=(weight/16)*52
                elif weight<=21:
                    amount=(weight/21)*70
                else:
                    amount=75
        elif "seventhgeneration" in text:
            if weight<=11:
                amount=(weight/11)*22
            elif weight<=16:
                amount=(weight/11)*30
            else:
                amount=35
        elif "all" in text:
            if "free clear" in text or "free clear oxi" in text or "odor relief" in text:
                if weight<=11:
                    amount=(weight/11)*35
                elif weight<=16:
                    amount=(weight/16)*52
                elif weight<=21:
                    amount=(weight/21)*70
                else:
                    amount=75
        elif "gain" in text:
            if weight <= 6:
                amount=(weight / 6) * 45
            elif weight <= 11:
                amount=(weight / 11) * 65
            elif weight <= 16:
                amount=(weight / 16) * 90
            elif weight <= 21:
                amount=(weight/21) * 120
            else: 
                amount=120
        #elif "armhammer" in text:


        amount=5*round(amount/5)
        return amount
    def select(self,text):
        self.clear()
        if weightdetected==True:
            datastat=f"Weight ({self.weightget()} pounds) is\n detected on the weight sensor\nDetergent used: {text}"
        else:
            datastat=f"Weight is not detected on the weight sensor\nDetergent used: {text}"
        if len(text) > 0:
            self.recentadd(text)
        #add clear button next to settings
            global detergenthelp
            detergenthelp=Frame(width=600,height=400,bg="white")
            detergenthelp.place(x=350,y=150)
            header=Label(master=detergenthelp,text=datastat,font=(tnr,20))
            header.place(x=90,y=0)
            popup=Label(master=detergenthelp,text=f"Fill up the detergent cup to {self.amountcalc(text)}\n mL",font=(tnr,20))
            popup.place(x=90,y=100)
   
    def recentadd(self,text):
        if text in self.recentlist:
            self.recentlist.remove(text)
        self.recentlist.insert(0,text)
        while len(self.recentlist) < 6:
            self.recentlist.append("")
        self.recentconfigure(self.recentlist)

    def resultconfigure(self,searches):
        results=Frame(bg="white")
        results.place(x=20,y=120,width=530,height=100)
        
        result1=Button(master=results, text=f"{searches[0]}",font=(tnr,16),command=lambda:self.select(searches[0]),width=20)
        result1.place(x=0,y=0)
        result2=Button(master=results, text=f"{searches[1]}",font=(tnr,16),command=lambda:self.select(searches[1]),width=20)
        result2.place(x=280)
        result3=Button(master=results,text=f"{searches[2]}",font=(tnr,16),command=lambda:self.select(searches[2]),width=20)
        result3.place(x=0,y=50)
        result4=Button(master=results,text=f"{searches[3]}",font=(tnr,16),command=lambda:self.select(searches[3]),width=20)
        result4.place(x=280,y=50)

    def recentconfigure(self,recent):
        recents=Frame(width=430,height=300,bg="white")
        recents.place(x=700,y=70)
        recent1=Button(master=recents, text=f"{recent[0]}",font=(tnr,16),command=lambda:self.select(recent[0]),width=35)
        recent1.place(y=0)
        recent2=Button(master=recents,text=f"{recent[1]}",font=(tnr,16),command=lambda:self.select(recent[1]),width=35)
        recent2.place(y=50)
        recent3=Button(master=recents, text=f"{recent[2]}",font=(tnr,16),command=lambda:self.select(recent[2]),width=35)
        recent3.place(y=100)
        recent4=Button(master=recents,text=f"{recent[3]}",font=(tnr,16),command=lambda:self.select(recent[3]),width=35)
        recent4.place(y=150)
        recent5=Button(master=recents,text=f"{recent[4]}",font=(tnr,16),command=lambda:self.select(recent[4]),width=35)
        recent5.place(y=200)
        recent6=Button(master=recents,text=f"{recent[5]}",font=(tnr,16),command=lambda:self.select(recent[5]),width=35)
        recent6.place(y=250)

    def populars(self):
        populars=Frame(width=530,height=200,bg="white")
        populars.place(x=20,y=300)
    
        popular1=Button(master=populars,text=f"{detergentstr[0]} {tide[0]}",font=(tnr,16),command=lambda:self.select(detergentstr[0]+" "+tide[0]),width=20)
        popular1.place(x=0,y=0)
        popular2=Button(master=populars,text=f"{detergentstr[0]} {tide[1]}",font=(tnr,16),command=lambda:self.select(detergentstr[0]+" "+tide[1]),width=20)
        popular2.place(x=280)
        popular3=Button(master=populars,text=f"{detergentstr[1]} {percil[0]}",font=(tnr,16),command=lambda:self.select(detergentstr[1]+" "+percil[0]),width=20)
        popular3.place(y=50)
        popular4=Button(master=populars,text=f"{detergentstr[1]} {percil[1]}",font=(tnr,16),command=lambda:self.select(detergentstr[1]+" "+percil[1]),width=20)
        popular4.place(x=280,y=50)
        popular5=Button(master=populars,text=f"{detergentstr[5]} {all[0]}",font=(tnr,16),command=lambda:self.select(detergentstr[5]+" "+all[0]),width=20)
        popular5.place(y=100)
        popular6=Button(master=populars,text=f"{detergentstr[5]} {all[1]}",font=(tnr,16),command=lambda:self.select(detergentstr[5]+" "+all[1]),width=20)
        popular6.place(x=280,y=100)
        popular7=Button(master=populars,text=f"{detergentstr[2]} {purex[0]}",font=(tnr,16),command=lambda:self.select(detergentstr[2]+" "+purex[0]),width=20)
        popular7.place(y=150)
        popular8=Button(master=populars,text=f"{detergentstr[2]} {purex[1]}",font=(tnr,16),command=lambda:self.select(detergentstr[2]+" "+purex[1]),width=20)
        popular8.place(x=280,y=150)

hardtext=Text(window)
interactables=Interactable(window)
window.mainloop()



