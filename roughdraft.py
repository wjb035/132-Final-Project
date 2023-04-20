from tkinter import *
import re
window=Tk()
window.title("Mann Co. Detergent Thing")
window.geometry('720x470')

global tide
tide=["original scent","ultra oxi","free and gentle","with downy","hygenic clean"]
global percil
percil=["original scent","oxi power", "odor fighter","active scent booster","intense fresh"]
global purex
purex=["mountain breeze","natural elements","baby soft"]
global seventhgeneration
seventhgeneration=["all scents","easy dose"]
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
class Text(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.guisetup()

    def guisetup(self):
        deterlabel=Label(text="Please enter your detergent type",
                        font=("Arial",16))
        recentlabel=Label(text="Recently Searched Detergents:",
                        font=("Arial",14))
        orlabel=Label(text="Or select a popular detergent type:",
                        font=("Arial",14))
        resultlabel=Label(text="Search Results:",
                          font=("Arial",14))
        deterlabel.place(x=15,y=20)
        recentlabel.place(x=400,y=20)
        orlabel.place(x=15,y=200)
        resultlabel.place(x=15,y=70)
class Interactable(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        self.recentlist= []
        self.setup() 
        self.resultconfigure(["","","",""])
        self.recentconfigure(["","","","","",""])
        self.populars()
        self.menusetup()
    @property
    def recentlist(self):
        return self._recentlist
    
    @recentlist.setter
    def recentlist(self,val):
        self._recentlist=val

    def setup(self):
        deterentry=Entry(width=30)
        enter=Button(text="Enter",fg="black",bg="white",command=lambda:self.enter(deterentry))
         
        deterentry.place(x=15,y=50)
        enter.place(x=200,y=50)
    
    def sanitize(self,entry):
        entry=entry.replace(" ","")
        entry=entry.lower()
        remover=re.findall('[a-z]', entry)
        entry="".join(map(str,remover))
        return entry

    def enter(self,entry):
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
        
        settings=Button(window,text="Settings")
        settings.place(x=650,y=425)
    
    def select(self,text):
        if len(text) > 0:
            self.recentadd(text)

        
    def recentadd(self,text):
        self.recentlist.insert(0,text)
        while len(self.recentlist) < 6:
            self.recentlist.append("")
        self.recentconfigure(self.recentlist)

    def resultconfigure(self,searches):
        results=Frame()
        results.place(x=20,y=100,width=400,height=100)
        
        result1=Button(master=results, text=f"{searches[0]}",command=lambda:self.select(searches[0]),width=20)
        result1.place(x=0,y=0)
        result2=Button(master=results, text=f"{searches[1]}",command=lambda:self.select(searches[1]),width=20)
        result2.place(x=160)
        result3=Button(master=results,text=f"{searches[2]}",command=lambda:self.select(searches[2]),width=20)
        result3.place(x=0,y=40)
        result4=Button(master=results,text=f"{searches[3]}",command=lambda:self.select(searches[3]),width=20)
        result4.place(x=160,y=40)

    def recentconfigure(self,recent):
        recents=Frame(width=300,height=250)
        recents.place(x=420,y=70)
        recent1=Button(master=recents, text=f"{recent[0]}",command=lambda:self.select(recent[0]),width=30)
        recent1.place(y=0)
        recent2=Button(master=recents,text=f"{recent[1]}",command=lambda:self.select(recent[1]),width=30)
        recent2.place(y=40)
        recent3=Button(master=recents, text=f"{recent[2]}",command=lambda:self.select(recent[2]),width=30)
        recent3.place(y=80)
        recent4=Button(master=recents,text=f"{recent[3]}",command=lambda:self.select(recent[3]),width=30)
        recent4.place(y=120)
        recent5=Button(master=recents,text=f"{recent[4]}",command=lambda:self.select(recent[4]),width=30)
        recent5.place(y=160)
        recent6=Button(master=recents,text=f"{recent[5]}",command=lambda:self.select(recent[5]),width=30)
        recent6.place(y=200)


    def populars(self):
        populars=Frame(width=300,height=180)
        populars.place(x=20,y=230)
        
        
        popular1=Button(master=populars,text=f"{detergentstr[0]} {tide[0]}",command=lambda:self.select(detergentstr[0]+" "+tide[0]),width=18)
        popular1.place(x=0,y=0)
        popular2=Button(master=populars,text=f"{detergentstr[0]} {tide[1]}",command=lambda:self.select(detergentstr[0]+" "+tide[1]),width=18)
        popular2.place(x=150)
        popular3=Button(master=populars,text=f"{detergentstr[1]} {percil[0]}",command=lambda:self.select(detergentstr[1]+" "+percil[0]),width=18)
        popular3.place(y=40)
        popular4=Button(master=populars,text=f"{detergentstr[1]} {percil[1]}",command=lambda:self.select(detergentstr[1]+" "+percil[1]),width=18)
        popular4.place(x=150,y=40)
        popular5=Button(master=populars,text=f"{detergentstr[5]} {all[0]}",command=lambda:self.select(detergentstr[5]+" "+all[0]),width=18)
        popular5.place(y=80)
        popular6=Button(master=populars,text=f"{detergentstr[5]} {all[1]}",command=lambda:self.select(detergentstr[5]+" "+all[1]),width=18)
        popular6.place(x=150,y=80)
        popular7=Button(master=populars,text=f"{detergentstr[2]} {purex[0]}",command=lambda:self.select(detergentstr[2]+" "+purex[0]),width=18)
        popular7.place(y=120)
        popular8=Button(master=populars,text=f"{detergentstr[2]} {purex[1]}",command=lambda:self.select(detergentstr[2]+" "+purex[1]),width=18)
        popular8.place(x=150,y=120)

hardtext=Text(window)
interactables=Interactable(window)
window.mainloop()



