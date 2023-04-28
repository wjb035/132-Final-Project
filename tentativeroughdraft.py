from tkinter import *
import re
window=Tk()
window.title("Mann Co. Detergent Thing")
window.geometry('1300x660')

global tide
tide=["original scent","ultra oxi","free and gentle","with downy","hygenic clean"]
global percil
percil=["original scent","oxi power", "odor fighter","stain fighter","intense fresh"]
global purex
purex=["mountain breeze","natural elements","baby soft"]
global seventhgeneration
seventhgeneration=["all scents"]
global surfexcel
surfexcel=["easy wash","front load"]
global all
all=["free clear","free clear eco", "free clear oxi", "odor relief"]
global gain
gain=["original + aroma boost"]
global xtra
xtra=["mountain rain"]
global armandhammer
armandhammer=["sensitive skin","plus oxiclean","clean burst"]

global detergents
detergents=[tide,percil,purex,seventhgeneration,surfexcel,all,gain,xtra,armandhammer]
global detergentstr
detergentstr=["tide","percil","purex","seventhgeneration","surfexcel","all","gain","xtra","a&h"]
global weightdetected
weightdetected=False
global yesstat
yesstat=False
import serial
#ser = serial.Serial(port='COM3', baudrate=9600, timeout=1)

tnr="times new roman"
class Text(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.guisetup()

    def guisetup(self):
        deterlabel=Label(text="Please enter your detergent type:",
                        font=(tnr,20))
        recentlabel=Label(text="Recently Searched Detergents:",
                        font=(tnr,20))
        orlabel=Label(text="Or select a popular detergent type:",
                        font=(tnr,20))
        resultlabel=Label(text="Search Results:",
                          font=(tnr,18))
        deterlabel.place(x=15,y=20)
        recentlabel.place(x=700,y=20)
        orlabel.place(x=15,y=250)
        resultlabel.place(x=15,y=85)
class Interactable(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.recentlist= []
        self.setup() 
        self.resultconfigure(["","","",""])
        self.recentconfigure(["","","","","",""])
        self.populars()
        self.menusetup()
        self.clearsetup()
    @property
    def recentlist(self):
        return self._recentlist
    
    @recentlist.setter
    def recentlist(self,val):
        self._recentlist=val

    def setup(self):
        deterentry=Entry(width=30,font=(tnr,16),)
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


    def menusetup(self):
        #when making settings make sure to self.clear()
        settings=Button(window,text="Settings",font=(tnr,16),command=lambda:self.weightsetup())
        settings.place(x=1100,y=600)
    """ def yesstat(self):
        global yesstat
        yesstat=True
        self.weightsetup() """
    def weightsetup(self):
        self.clear()
        """if weightdetected==True:
            pass
        global detergenthelp
        detergenthelp=Frame(width=600,height=400,bg="gray")
        detergenthelp.place(x=350,y=150)
        checklabel=Label(master=detergenthelp,text=f"Ready to calibrate the sensor?\nIf not, press the clear button!\nIf so, press the yes button!\nIt will take 15-20s, that is normal.",font=(tnr,20))
        checklabel.place(x=120)
        checkbutton=Button(master=detergenthelp,text="Yes",font=(tnr,18),command=lambda: self.yesstat())
        checkbutton.place(x=250,y=150)
        if yesstat==True:
            ser = serial.Serial(port='COM3', baudrate=9600, timeout=1)
            counter=0
            while counter<15:
                status=ser.readline().decode("ascii")
                if len(status) > 4:
                    print(status)
                    counter+=1"""
                #global yesstat
                #yesstat=False
            #yesstat=False


    def clearsetup(self):
        clear=Button(window,text="Clear",font=(tnr,16),command=lambda:self.clear())
        clear.place(x=1010,y=600)
    def clear(self):
        try:
            detergenthelp.destroy() 
        except:
            pass
    def weightget(self):
        weightgrams=2438
        weightpoundsraw=weightgrams/453.6
        weightpounds=round(weightpoundsraw,2)
        return 13#weightpounds
    
    def amountcalc(self,text):
        weight = self.weightget()
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
                    amount=(weight/21)


        amount=round(amount,0)
        if amount%5!=0:
            amount+= 5-amount%5
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
            detergenthelp=Frame(width=600,height=400,bg="gray")
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
        results=Frame()
        results.place(x=20,y=120,width=600,height=130)
        
        result1=Button(master=results, text=f"{searches[0]}",font=(tnr,16),command=lambda:self.select(searches[0]),width=20)
        result1.place(x=0,y=0)
        result2=Button(master=results, text=f"{searches[1]}",font=(tnr,16),command=lambda:self.select(searches[1]),width=20)
        result2.place(x=280)
        result3=Button(master=results,text=f"{searches[2]}",font=(tnr,16),command=lambda:self.select(searches[2]),width=20)
        result3.place(x=0,y=50)
        result4=Button(master=results,text=f"{searches[3]}",font=(tnr,16),command=lambda:self.select(searches[3]),width=20)
        result4.place(x=280,y=50)

    def recentconfigure(self,recent):
        recents=Frame(width=500,height=300)
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
        populars=Frame(width=600,height=200)
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



