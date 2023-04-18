from tkinter import *
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
detergentstr=["tide","percil","purex","seventhgeneration","surfexcel","all","gain","xtra","armandhammer"]
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
        self.setup()
        self.resultconfigure(["","","",""])
        self.recents()
        self.populars()
        self.menusetup()
    def setup(self):
        deterentry=Entry(width=30)
        enter=Button(text="Enter",fg="black",bg="white",command=lambda:self.enter(deterentry))
         
        deterentry.place(x=15,y=50)
        enter.place(x=200,y=50)
    
    def sanitize(self,entry):
        entry=entry.replace(" ","")
        
    def enter(self,entry):
        entry=entry.get()
        searches=[]
        for i in range(len(detergents)):
            for search in detergents[i]:
                if entry in detergentstr[i]+search:
                    searches.append(detergentstr[i]+search)
        while len(searches)<4:
            searches.append("")          
        self.resultconfigure(searches)
        print(searches)

    def menusetup(self):
        
        settings=Button(window,text="Settings")
        settings.place(x=650,y=425)
        
    def select(self,text):
        print(text)
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

    def recents(self):
        recents=Frame(width=300,height=200)
        recents.place(x=400,y=70)
        result1=Button(master=recents, text="results",width=30)
        result1.place(y=0)
        result2=Button(master=recents,text="results",width=30)
        result2.place(y=40)
        result3=Button(master=recents, text="results",width=30)
        result3.place(y=80)
        result4=Button(master=recents,text="results",width=30)
        result4.place(y=120)
        result5=Button(master=recents,text="results",width=30)
        result5.place(y=160)


    def populars(self):
        populars=Frame(width=300,height=180,)
        populars.place(x=20,y=230)
        
        
        popular1=Button(master=populars,text=f"tide {tide[0]}",width=18)
        popular1.place(x=0,y=0)
        popular2=Button(master=populars,text=f"tide {tide[1]}",width=18)
        popular2.place(x=150)
        popular3=Button(master=populars,text=f"percil {percil[0]}",width=18)
        popular3.place(y=40)
        popular4=Button(master=populars,text=f"percil {percil[1]}",width=18)
        popular4.place(x=150,y=40)
        popular5=Button(master=populars,text=f"all {all[0]}",width=18)
        popular5.place(y=80)
        popular6=Button(master=populars,text=f"all {all[1]}",width=18)
        popular6.place(x=150,y=80)
        popular7=Button(master=populars,text=f"purex {purex[0]}",width=18)
        popular7.place(y=120)
        popular8=Button(master=populars,text=f"purex {purex[1]}",width=18)
        popular8.place(x=150,y=120)

hardtext=Text(window)
interactables=Interactable(window)
window.mainloop()



