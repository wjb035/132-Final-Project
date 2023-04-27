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
xtra=["mountaian rain"]
global armandhammer
armandhammer=["sensitive skin","plus oxiclean","clean burst"]

global detergents
detergents=[tide,percil,purex,seventhgeneration,surfexcel,all,gain,xtra,armandhammer]
global detergentstr
detergentstr=["tide","percil","purex","seventhgeneration","surfexcel","all","gain","xtra","a&h"]
global weightdetected
weightdetected=True
class Text(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.guisetup()

    def guisetup(self):
        deterlabel=Label(text="Please enter your detergent type:",
                        font=("times new roman",20))
        recentlabel=Label(text="Recently Searched Detergents:",
                        font=("times new roman",20))
        orlabel=Label(text="Or select a popular detergent type:",
                        font=("times new roman",20))
        resultlabel=Label(text="Search Results:",
                          font=("times new roman",18))
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
        deterentry=Entry(width=30,font=("times new roman",16),)
        enter=Button(text="Enter",font=("times new roman",14),fg="black",bg="white",command=lambda:self.enter(deterentry))
         
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
        settings=Button(window,text="Settings",font=("times new roman",16))
        settings.place(x=1100,y=600)
        
    def clearsetup(self):
        clear=Button(window,text="Clear",font=("times new roman",16),command=lambda:self.clear())
        clear.place(x=1010,y=600)

    def clear(self):
        try:
            self.header.destroy()
            self.detergenthelp.destroy() 
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
            if weight < 6:
                amount=(weight / 6) * 45
            elif weight < 11:
                amount=(weight / 11) * 65
            elif weight < 16:
                amount=(weight / 16) * 90
            elif weight < 21:
                amount=(weight/21) * 120
            else: 
                amount=120
        
        amount=round(amount,0)
        if amount%5!=0:
            amount+= 5-amount%5
        return amount
    def select(self,text):
        self.clear()
        if weightdetected==True:
            datastat=f"Weight ({self.weightget()} pounds)\n is detected on the weight sensor\nDetergent used: {text}"
        else:
            datastat=f"Weight is not detected on the weight sensor\nDetergent used: {text}"
        if len(text) > 0:
            self.recentadd(text)
        #add clear button next to settings
            self.detergenthelp=Frame(width=600,height=400,bg="gray")
            self.detergenthelp.place(x=350,y=150)
            self.header=Label(master=self.detergenthelp,text=datastat,font=("Times New Roman",20))
            self.header.place(x=90,y=0)
            self.popup=Label(master=self.detergenthelp,text=f"Fill up the detergent cup to {self.amountcalc(text)} mL")
            self.popup.place(x=90,y=100)
    
    @property
    def detergenthelp(self):
        return self._detergenthelp
    
    @detergenthelp.setter
    def detergenthelp(self,value):
        self._detergenthelp=value

    @property
    def popup(self):
        return self._popup
    
    @popup.setter
    def popup(self,value):
        self._popup=value

    @property
    def header(self):
        return self._header
    @header.setter
    def header(self,value):
        self._header=value

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
        
        result1=Button(master=results, text=f"{searches[0]}",font=("times new roman",16),command=lambda:self.select(searches[0]),width=20)
        result1.place(x=0,y=0)
        result2=Button(master=results, text=f"{searches[1]}",font=("times new roman",16),command=lambda:self.select(searches[1]),width=20)
        result2.place(x=280)
        result3=Button(master=results,text=f"{searches[2]}",font=("times new roman",16),command=lambda:self.select(searches[2]),width=20)
        result3.place(x=0,y=50)
        result4=Button(master=results,text=f"{searches[3]}",font=("times new roman",16),command=lambda:self.select(searches[3]),width=20)
        result4.place(x=280,y=50)

    def recentconfigure(self,recent):
        recents=Frame(width=500,height=300)
        recents.place(x=700,y=70)
        recent1=Button(master=recents, text=f"{recent[0]}",font=("times new roman",16),command=lambda:self.select(recent[0]),width=35)
        recent1.place(y=0)
        recent2=Button(master=recents,text=f"{recent[1]}",font=("times new roman",16),command=lambda:self.select(recent[1]),width=35)
        recent2.place(y=50)
        recent3=Button(master=recents, text=f"{recent[2]}",font=("times new roman",16),command=lambda:self.select(recent[2]),width=35)
        recent3.place(y=100)
        recent4=Button(master=recents,text=f"{recent[3]}",font=("times new roman",16),command=lambda:self.select(recent[3]),width=35)
        recent4.place(y=150)
        recent5=Button(master=recents,text=f"{recent[4]}",font=("times new roman",16),command=lambda:self.select(recent[4]),width=35)
        recent5.place(y=200)
        recent6=Button(master=recents,text=f"{recent[5]}",font=("times new roman",16),command=lambda:self.select(recent[5]),width=35)
        recent6.place(y=250)

    def populars(self):
        populars=Frame(width=600,height=200)
        populars.place(x=20,y=300)
        
        
        popular1=Button(master=populars,text=f"{detergentstr[0]} {tide[0]}",font=("times new roman",16),command=lambda:self.select(detergentstr[0]+" "+tide[0]),width=20)
        popular1.place(x=0,y=0)
        popular2=Button(master=populars,text=f"{detergentstr[0]} {tide[1]}",font=("times new roman",16),command=lambda:self.select(detergentstr[0]+" "+tide[1]),width=20)
        popular2.place(x=280)
        popular3=Button(master=populars,text=f"{detergentstr[1]} {percil[0]}",font=("times new roman",16),command=lambda:self.select(detergentstr[1]+" "+percil[0]),width=20)
        popular3.place(y=50)
        popular4=Button(master=populars,text=f"{detergentstr[1]} {percil[1]}",font=("times new roman",16),command=lambda:self.select(detergentstr[1]+" "+percil[1]),width=20)
        popular4.place(x=280,y=50)
        popular5=Button(master=populars,text=f"{detergentstr[5]} {all[0]}",font=("times new roman",16),command=lambda:self.select(detergentstr[5]+" "+all[0]),width=20)
        popular5.place(y=100)
        popular6=Button(master=populars,text=f"{detergentstr[5]} {all[1]}",font=("times new roman",16),command=lambda:self.select(detergentstr[5]+" "+all[1]),width=20)
        popular6.place(x=280,y=100)
        popular7=Button(master=populars,text=f"{detergentstr[2]} {purex[0]}",font=("times new roman",16),command=lambda:self.select(detergentstr[2]+" "+purex[0]),width=20)
        popular7.place(y=150)
        popular8=Button(master=populars,text=f"{detergentstr[2]} {purex[1]}",font=("times new roman",16),command=lambda:self.select(detergentstr[2]+" "+purex[1]),width=20)
        popular8.place(x=280,y=150)

hardtext=Text(window)
interactables=Interactable(window)
window.mainloop()



