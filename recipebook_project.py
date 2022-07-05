#Recipe Finder tool with GUI built using tkinter and ttk
#Greyson Wilson
#CS 2520

from functools import partial
from json import *
import json
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter.scrolledtext import ScrolledText
from PIL import Image as PilImage
from PIL import ImageTk

RB_FILE = "recipebook.txt"
ING_FILE = "ingredients.txt"
DEFAULT_IMG_PATH = "default.png"


class SearchTabs(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.notebook = ttk.Notebook(self.master, width=500, height=400)
        self.notebook.grid(column=2, row=1)#, sticky=NSEW)

        self.ingSearchFrame = Frame(self.notebook, bg="#573337")
        self.ingSearchFrame.grid(column=0, row=0)
        self.ingSearch = IngredientSearchBox(self.ingSearchFrame)
        self.ingSearch.grid(column=0, row=0)

        self.recSearchFrame = Frame(self.notebook, bg="#523123")
        self.recSearchFrame.grid(column=0, row=0)
        self.recSearch = SearchBox(self.recSearchFrame)
        self.recSearch.grid(column=0, row=0)
        
        # self.ingSearchLabel = Label(self.ingSearchFrame, text="Ing search label")
        # self.ingSearchLabel.grid(column=0, row=0)
    
        
        self.notebook.add(self.ingSearchFrame, text="Search Ingredient")
        self.notebook.add(self.recSearchFrame, text="Search Recipe")
        

class RS_ImageEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.imgBox = Label(self)
        self.imgLabel = Label(self, text="Image path")
        self.imgButton = Button(self, text="Change")
        #Grids
        self.imgLabel.grid(column=0, row=0)
        self.imgBox.grid(column=0, row= 1)
        self.imgButton.grid(column=1, row=1)
        

class RS_NameEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.nameBox = Entry(self)
        self.nameLabel = Label(self, text="Name")
        self.nameButton = Button(self, text="Change")
        #Grids
        self.nameLabel.grid(column=0, row=0)
        self.nameBox.grid(column=0, row= 1)
        self.nameButton.grid(column=1, row=1)


class RS_IngredientEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.ingredientsBox = Entry(self)
        self.ingredientsLabel = Label(self, text="Ingredients")
        self.ingredientsButton = Button(self, text="Change")
        #Grids
        self.ingredientsLabel.grid(column=0, row=0)
        self.ingredientsBox.grid(column=0, row= 1)
        self.ingredientsButton.grid(column=1, row=1)

class RS_PrepTimeEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.preptimeBox = Entry(self)
        self.preptimeLabel = Label(self, text="Prep time")
        self.preptimeButton = Button(self, text="Change")
        #Grids
        self.preptimeLabel.grid(column=0, row=0)
        self.preptimeBox.grid(column=0, row= 1)
        self.preptimeButton.grid(column=1, row=1)

class RS_CookTimeEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.cooktimeBox = Entry(self)
        self.cooktimeLabel = Label(self, text="Cook time")
        self.cooktimeButton = Button(self, text="Change")
        #Grids
        self.cooktimeLabel.grid(column=0, row=0)
        self.cooktimeBox.grid(column=0, row= 1)
        self.cooktimeButton.grid(column=1, row=1)

class RS_TagsEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.tagsBox = Entry(self)
        self.tagsLabel = Label(self, text="Tags")
        self.tagsButton = Button(self, text="Change")
        #Grids
        self.tagsLabel.grid(column=0, row=0)
        self.tagsBox.grid(column=0, row= 1)
        self.tagsButton.grid(column=1, row=1)

class RS_EditSuite(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #Recipe book passed on creation
        self.recipeBook = self.master.recipeBook
        self.newRecipe = Recipe("New Recipe")
        self.imgEntry = RS_ImageEntry(master=self, recipe=self.newRecipe)
        self.nameEntry = RS_NameEntry(master=self, recipe=self.newRecipe)
        self.ingredientsEntry = RS_IngredientEntry(master=self, recipe=self.newRecipe)
        self.preptimeEntry = RS_PrepTimeEntry(master=self, recipe=self.newRecipe)
        self.cooktimeEntry = RS_CookTimeEntry(master=self, recipe=self.newRecipe)
        self.tagsEntry = RS_TagsEntry(master=self, recipe=self.newRecipe)

        self.imgEntry.grid(column=0, row=0)
        self.nameEntry.grid(column=0, row=1)
        self.ingredientsEntry.grid(column=0, row=2)
        self.preptimeEntry.grid(column=0, row=3)
        self.cooktimeEntry.grid(column=0, row=4)
        self.tagsEntry.grid(column=0, row=5)
        

class RecipeStationWindow(Toplevel):
    def __init__(self, recipeBook, master=None):
        super().__init__(master, name='!recipestationwindow')
        self.config(border='15', width='800', height='600')
        self.minsize(800,600)
        self.title("Recipe station")
        self.recipeBook = recipeBook
        self.editAddSuite = RS_EditSuite(self)
        self.editAddSuite.grid(column=0, row=0)
        self.newButton = Button(self, text="New Recipe")
        self.editButton = Button(self, text="Edit Recipe", command=self.EditMenu)

        self.mainloop()
    
    def Close(self):
        self.destroy()

    def EditMenu(self):
        print("Unimplemented")
        #Open a list of recipes to edit or enter in search box

#Rename to recipe station
class RecipeStationBox(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.button = Button(text="Recipe Station", command=self.MakeWindow)
        self.button.grid(column=4, row=0, rowspan=2)
        self.stationStatus = False
        self.recipeStation = None

    def MakeWindow(self):
        if self.stationStatus == False:
            print("Opening recipe station")
            self.stationStatus = True
            self.recipeStation = RecipeStationWindow(recipeBook=self.master.book)
            #self.recipeStation.focus
        else:
            print("Closing recipe station")
            self.stationStatus = False
            try:
                self.master.children['!recipestationwindow'].destroy()
            except KeyError:
                print("Recipe station window was already destroyed.")
class SearchBox(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.activeRecipe = self.master.master.master.activeRecipe
        self.stringVar = StringVar()
        self.stringVar.set("Search for recipe")
        
        self.searchBarFrame = Frame(self.master)
        self.searchBarFrame.grid(column=2, row=0)
        
        self.searchEntryBox = ttk.Entry(self.searchBarFrame, textvariable=self.stringVar)
        self.searchEntryBox.grid(column=0, row = 0)
        
        self.searchButton = Button(self.searchBarFrame, text="Search", command=self.Search)
        self.searchButton.grid(column=1, row=0)
        
        self.allRecipesBox = ScrolledText(self.master, width=35)
        self.allRecipesBox.grid(column=1, row=0)
        self.UpdateRecipeBox()
    
    def Search(self):
        for recipe in self.master.master.master.book.recipes:
            if recipe.name == self.stringVar.get():
                print(recipe.name)
                self.master.master.master.activeRecipe = recipe
                self.master.master.master.children['!recipeinfobox'].UpdateInfo()
                
    
    def UpdateRecipeBox(self):
        self.allRecipesBox.config(state='normal')
        self.allRecipesBox.delete(1.0, END)
        for recipe in self.master.master.master.book.recipes:
            self.allRecipesBox.insert(INSERT, recipe.name)
            self.allRecipesBox.insert(INSERT, "\n")
        self.allRecipesBox.config(state='disabled')


class FileOpBox(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #self.recipeBook = RecipeBook()
        self.recipeBook = self.master.book
        self.openButtonT = Button(text="Open Recipe Book T", command=self.TestOpen)
        self.openButtonT.grid(column=4, row=2)
        self.openButton = Button(text="Open Recipe Book(Option placeholder)", command=self.LoadRecipeBook)
        self.openButton.grid(column=4, row=3)

    #Should ideally simply load the recipe book and the first recipe
    def LoadRecipeBook(self):
        self.recipeBook = self.recipeBook.OpenRecipeFile()
        #ingBox = self.master.children.get('ingredientbox')
        #print(ingBox)
        recipeLabel = self.master.children['!recipelabel']
        recipeImg = self.master.children['!imagebox']
        ingBoxWidget = self.master.children['!ingredientbox']
        recipeLabel.UpdateLabel(self.recipeBook.recipes[0].name)
        recipeImg.UpdateImage(self.recipeBook.recipes[0].img)
        ingBoxWidget.UpdateIngBox(self.recipeBook.recipes[0].ingredients)
    
    def TestOpen(self):
        self.recipeBook = self.recipeBook.OpenRecipeFile()
        #ingBox = self.master.children.get('ingredientbox')
        #print(ingBox)
        recipeLabel = self.master.children['!recipelabel']
        recipeImg = self.master.children['!imagebox']
        ingBoxWidget = self.master.children['!ingredientbox']
        recipeLabel.UpdateLabel(self.recipeBook.recipes[0].name)
        recipeImg.UpdateImage(self.recipeBook.recipes[0].img)
        ingBoxWidget.UpdateIngBox(self.recipeBook.recipes[0].ingredients)

class RecipeInfoBox(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, name='!recipeinfobox')
        
        self.recipeBook = self.master.book
        self.infoFrame = Frame(self, bg="#313740")
        self.recipeName = RecipeLabel(self.infoFrame)
        self.imgBox = ImageBox(self)
        self.ingredientBox = IngredientBox(self.infoFrame)
        self.instructionsBox = InstructionsBox(self.infoFrame)
        self.tagsBox = TagsBox(self.infoFrame)

        self.recipeName.recipeLabel.config(bg="#929fb0")
        self.ingredientBox.ingredientsLabel.config(bg="#929fb0")
        #self.instructionsBox.config(bg="#929fb0")
        #self.tagsBox.config(bg="#929fb0")

        self.grid(column=1, row=1)
        self.imgBox.grid(column=0, row=0)
        self.infoFrame.grid(column=1, row=0)

        self.recipeName.grid(column=0, row=1)
        self.ingredientBox.grid(column=0, row=2)
        self.instructionsBox.grid(column=0, row=3)
        self.tagsBox.grid(column=0, row=4)
        #self.activeRecipe = self.master.activeRecipe


        #Default values is 1st recipe in recipes
        self.recipeName.UpdateLabel(self.recipeBook.recipes[0].name)
        self.imgBox.UpdateImage(self.recipeBook.recipes[0].img)
        self.ingredientBox.UpdateIngBox(self.recipeBook.recipes[0].ingredients)
        self.instructionsBox.UpdateInsBox(self.recipeBook.recipes[0].instructions)
        self.tagsBox.UpdateTagsBox(self.recipeBook.recipes[0].tags)

    def UpdateInfo(self):
        #Update name, image, ingredients, instructions, tags
        self.activeRecipe = self.master.activeRecipe
        self.recipeName.UpdateLabel(self.activeRecipe.name)
        self.imgBox.UpdateImage(self.activeRecipe.img)
        self.ingredientBox.UpdateIngBox(self.activeRecipe.ingredients)
        self.instructionsBox.UpdateInsBox(self.activeRecipe.instructions)
        self.tagsBox.UpdateTagsBox(self.activeRecipe.tags)

class InstructionsBox(ttk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.boxText = StringVar()
        self.boxText.set("")
        self.instructionsBox = Label(self, textvariable=self.boxText, anchor=W, wraplength=250, justify=LEFT)
        self.instructionsBox.grid(column=0, row=0)

    def UpdateInsBox(self, ins):
        self.boxText.set(ins)

class TagsBox(ttk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.boxText = StringVar()
        self.boxText.set("")
        self.tagsBox = Label(self, textvariable=self.boxText, anchor=W, wraplength=250, justify=CENTER)
        self.tagsBox.grid(column=0, row=0)

    def UpdateTagsBox(self, tags):
        prtStr = ""
        for ingredient in tags:
            prtStr += ingredient + "; "
        self.boxText.set(prtStr)

class IngredientBox(ttk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.buttonText = tkinter.StringVar()
        self.boxText = tkinter.StringVar()
        self.boxText.set("")
        self.ingredientsLabel = Label(self, textvariable=self.boxText, anchor=W, wraplength=250, justify=CENTER)
        self.ingredientsLabel.grid(column=0, row=0)
        self._ingredients = []
    
    def UpdateIngBox(self, ingList):
        prtStr = ""
        for ingredient in ingList:
            prtStr += "> " + ingredient + "\t"
        self.boxText.set(prtStr)

class IngredientSearchBox(ttk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.searchIngredients = []
        self.ingredients =  self.master.master.master.book.GetAllIngredients()
        # self.ingredients = ["apples", "banana", "carrots", "d-fruit", "flour", "water", "garlic", "crushed tomatoes", 
        #                     "peanut butter", "fruit jelly", "bread", "eggs", "oil", "sugar", "chocolate", "lemons", "cinnamon",
        #                     "curry powder", "ground beef", "bagel", "butter", "navy beans", "barley", "oats",
        #                     "curry powder", "ground beef", "bagel", "butter", "navy beans", "barley", "oats",
        #                     "curry powder", "ground beef", "bagel", "butter", "navy beans", "barley", "LAST"]
        self.searchButton = Button(master, text="Search", command=self.Search)
        self.searchButton.grid(column=2, row=0)
        self.canvas = Canvas(self.master, bg="#573337", width=150, confine=True)
        self.canvas.grid(column=2, row=1, sticky=NS, rowspan=3)
        self.innerFrame = Frame(self.master)#.grid(column=3, row= 0)

        #Make into separate class
        self.canMakeBoxLabel = Label(self.master, text="Can make")
        self.canMakeBoxLabel.grid(column=1, row=0)
        self.canMakeBox = ScrolledText(self.master, width=35, height=10)
        self.canMakeBox.grid(column=1, row=1)
        self.canMakeBox.insert(tkinter.INSERT, " ")
        self.canMakeBox.config(state='disabled')

        self.canNearlyMakeBoxLabel = Label(self.master, text="Can nearly make")
        self.canNearlyMakeBoxLabel.grid(column=1, row=2)
        self.canNearlyMakeBox = ScrolledText(self.master, width=35, height=10)
        self.canNearlyMakeBox.grid(column=1, row=3)
        self.canNearlyMakeBox.insert(tkinter.INSERT, " ")
        self.canNearlyMakeBox.config(state='disabled')

        self.MakeScrollBar()
        self.buttonIndex = 0
        self.buttonArray = [] #Stores all checkbox buttons in an array so all can be accessed 
        self.controlVars = {} #This is a very bad way to implement this
        self.buttonStates = {}
        self.controlVar = StringVar()
        self.controlVar.set(None)
        self.lastSelect = StringVar()
        self.lastSelect.set(None)
        self.CreateButtons()
        

    def CreateButtons(self):
        for ing in self.ingredients:
            #Keep track of button states via dictionary
            self.buttonStates[ing] = False
            cvar = StringVar()#--
            cvar.set("_"+ing)#--
            button = Checkbutton(self.canvas, text=ing, justify=LEFT, bg='#A73337', activebackground='#773337',
                                                    variable=cvar, onvalue=ing, offvalue="_"+ing)#--
            self.canvas.create_window(4, 25 * self.buttonIndex, window=button, anchor=W, height=20) #<--- comment out
            button.bind("<Configure>", lambda event, canvas = self.canvas : self.event_onFrameConfigure(canvas)) #<---comment out
            #button.grid(column=0, row=self.buttonIndex+1) <--uncomment this to return to previous good implementation
            #print(button.setvar())
            #button.variable = self.controlVar
            self.lastSelect.set(cvar.get()) ######How do i get the most recently selected value or button?
            self.controlVars[ing] = cvar #--
            #Implementation from https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter Dologan
            partialFunction = partial(self.AddToSearch, cvar.get())
            button.config(command=partialFunction)
            self.buttonArray.append(button)
            self.buttonIndex += 1
        #print("controlvar after all ingredient buttons made:", self.controlVar.get())


    def MakeScrollBar(self):
        
        #self.canvas.create_window((0,0), window=self.innerFrame, anchor=CENTER)
        self.scrollbar = Scrollbar(master=self.master, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(column=3, row=1, sticky=NS, rowspan=3)
        self.canvas['yscrollcommand'] = self.scrollbar.set
        #self.innerFrame.config(bg="#000000")
        #self.innerFrame.bind("<Configure>", lambda event, canvas = self.canvas : self.event_onFrameConfigure(canvas))
    
    #Implemented from https://stackoverflow.com/questions/60696180/tkinter-embedded-plot-in-canvas-widget-scrollbar-is-not-working DYD 
    def event_onFrameConfigure(self, canvas):
        canvas.config(scrollregion=self.canvas.bbox(ALL))
    
    def Search(self):
        print(self.searchIngredients)
        # rb = RecipeBook()
        # rb.recipes.append(CreateTestRecipe())
        # testR = Recipe("Spaghetti")
        # testR.ingredients = ["eggs", "flour", "water", "oil", "crushed tomatoes", "garlic"]
        # testR.img = "spaghetti.png"
        # rb.recipes.append(testR)
        # rb.SaveRecipeFile()
        # rb.OpenRecipeFile()
        rb = self.master.master.master.book
        canMake, canNearlyMake = rb.MatchRecipe(self.searchIngredients)
        print("canMake var is:", canMake)
        print("canNearlyMake var is:", canNearlyMake)

        self.canMakeBox.config(state='normal')
        #Clear old entries in box
        self.canMakeBox.delete(1.0, END)
        for cm in canMake:
            self.canMakeBox.insert(tkinter.INSERT, cm)
            self.canMakeBox.insert(tkinter.INSERT, "\n")
        self.canMakeBox.insert(tkinter.INSERT, " ")
        self.canMakeBox.config(state='disabled')
        
        self.canNearlyMakeBox.config(state='normal')
        self.canNearlyMakeBox.delete(1.0, END)
        for cnm in canNearlyMake:
            self.canNearlyMakeBox.insert(tkinter.INSERT, cnm)
            self.canNearlyMakeBox.insert(tkinter.INSERT, "\n")
        self.canNearlyMakeBox.insert(tkinter.INSERT, " ")
        self.canNearlyMakeBox.config(state='disabled')
        
        # r = RecipeBook()
        # r.MatchRecipe(list)

    def AddToSearch(self, ingredient):
        # for btn in self.buttonArray:
        #     value = btn.cget('variable')
        #     #value = [btn['variable']]
        #     print("value: {}".format(value))
        #print(dict(self.buttonArray[0]))
        #print(self.buttonArray[0].keys())
        # print("self.buttonArray[0] is of type", type(self.buttonArray[0]))
        # print("variable:", self.buttonArray[0]['variable'])
        # print("onvalue:", self.buttonArray[0]['onvalue'])
        # print("offvalue:", self.buttonArray[0]['offvalue'])
        

        #I understand this is a very messy way to handle this, but I was unsuccessful with the ttk implementation given my constraints
        #var = self.controlVar.get()
        var = ingredient #--
        #print("(Ingredient Chosen) controlVar after button pressed:", var)

        #Snip _ offvalue tag
        if var[0] == "_":
            var = var[1:]
        if self.buttonStates[var] == False:
            self.searchIngredients.append(var)
            self.buttonStates[var] = True
            print(var, "added to search list.")
        elif self.buttonStates[var] == True:
            self.searchIngredients.remove(var)
            self.buttonStates[var] = False
            print(var, "removed search list.")
        #print("Button states now:", self.buttonStates)
        print("Current list:", self.searchIngredients)

        #self.searchIngredients += [ing]
        
class TestBox(ttk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.testString = StringVar()
        self.testString.set("Test string")
        self.navBox = ttk.Combobox(text="menu button", name="combo").grid(column=1, row=3)
        self.w1 = ttk.Entry(textvariable=self.testString).grid(column=1, row=2)
        self.testVar = 1
        self.w2 = ttk.LabeledScale().grid(column=1, row=1)
        self.w3 = ttk.Notebook(name="notebook", height='50', width='100').grid(column=1, row=5)
        self.w4 = ttk.Treeview(master=self.w3, name="tree", columns='2').grid(column=1, row=6)
        self.w5 = ttk.Scrollbar(orient='vertical').grid(column=3, row=0)

class ImageBox(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        #Path setting
        self.imgPath = StringVar()
        self.defaultImgPath = DEFAULT_IMG_PATH
        #self.defaultImgPath.set(DEFAULT_IMG_PATH)
        self.imgPath.set(self.defaultImgPath)
        
        #Image variables to handle opening, resizing, widget
        try:
            openImgVar = PilImage.open(self.imgPath.get())
        except FileNotFoundError:
            print("Failed to locate default image 'default.png'")
            return
        
        #self.resizedImg = openImgVar.resize((400, 400))
        #self.imgTkVar = ImageTk.PhotoImage(self.resizedImg)
        openImgVar.thumbnail((400,400))
        self.imgTkVar = ImageTk.PhotoImage(openImgVar)
        self.img = Label(master, image=self.imgTkVar)
        self.img.grid(column=0, row=0)

        #self.resizedImg.load()
        #self.imgVar = PhotoImage(file=self.imgPath.get(), width=400, height=400)

        self.imgState = True
        self.toggleStringVar = StringVar()
        self.toggleStringVar.set("-")
        self.toggleButton = Button(master, textvariable=self.toggleStringVar, command=self.ToggleImage).grid(column=0, row=0)
    
    def UpdateImage(self, imgPath):
        self.imgPath.set(imgPath)

        openImgVar = PilImage.open(self.imgPath.get())
        #self.resizedImg = openImgVar.resize((400,400))
        #self.imgTkVar = ImageTk.PhotoImage(self.resizedImg)
        openImgVar.thumbnail((400,400))
        self.imgTkVar = ImageTk.PhotoImage(openImgVar)
        #self.imgVar = PhotoImage(file=self.imgPath.get(), width=400, height=400)
        self.img = Label(self.master, image=self.imgTkVar, anchor=NW).grid(column=0, row=0)
    
    def ToggleImage(self):
        if self.imgState == True:
            self.img = Label(self, image=self.imgTkVar).grid(column=0, row=0)
            self.toggleStringVar.set("+")
            self.imgState = False
        else:
            self.img = Label(self, image=self.imgTkVar).grid(column=0, row=0)
            self.toggleStringVar.set("-")
            self.imgState = True

class RecipeLabel(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.recipeName = StringVar()
        self.recipeName.set("Recipe")
        self.recipeLabel = Label(master, textvariable=self.recipeName, font='Arial')
        self.recipeLabel.grid(column=0, row=0)
    
    def UpdateLabel(self, name):
        self.recipeName.set(name)

class MainWindow(ttk.Frame):
    '''
    def __init__(self, title):
        self.root = Tk()
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.master.title(title)
        self.frame.grid()
        #self.root.mainloop()
    '''
    #class AppWindow(ttk.Frame)
    
    def __init__(self, master=None, title = "New Window", *args, **kwargs):
        #self, parent, *args, **kwargs
        #
        super().__init__(master)

        self.config(border='15', width='800', height='600')
        self.master.minsize(800,600)
        self.master.title("Recipe Book")
        self.book = RecipeBook()
        self.book = self.book.OpenRecipeFile()
        #Default recipe is first in list
        self.activeRecipe = self.book.recipes[0]
        self.book.GetAllIngredients()
        #ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.grid()

        ##Widget classes below

        #self.imageBox = ImageBox(master=self)
        #self.ingBox = IngredientBox(master=self)
        #self.searchBox = SearchBox(master=self)
        #self.ingSearchBox = IngredientSearchBox(master=self)
        self.fileBox = FileOpBox(master=self)
        #print("after widget made:", self.ingSearchBox.controlVar.get())
        #self.recipeBox = RecipeLabel(master=self)
        self.searchTabs = SearchTabs(master=self)
        self.recipeInfoBox = RecipeInfoBox(master=self)  # <----WIP
        self.recipeStation = RecipeStationBox(master=self)                     

        #self.testBox = TestBox(master=self)

        #Scrollbar implementation
        #self.scrollbar = Scrollbar(self, orient=VERTICAL).grid(column=5, row=0, sticky=NS)
        
        
        self.mainloop()
    
    def ChangeSlide(self):
        print("Ba")
            
def CreateTestRecipe():
    recipe = Recipe("Peanut butter and jelly sandwich")
    recipe.ingredients.append("peanut butter")
    recipe.ingredients.append("fruit jelly")
    recipe.ingredients.append("bread")
    recipe.img = "pbj.png"
    recipe.instructions = "Grab two slices of bread. On one slice, slather peanut butter on a single side. On the other slide, " + \
     "slather jelly onto a single side. Place the sides together so that the peanut butter and jelly touch"
    recipe.cookTime = 0
    recipe.prepTime = 1.0
    recipe.tags += ["sandwich", "simple"]
    return recipe

def CreateTestRecipe2():
    recipe = Recipe("Spaghetti")
    recipe.ingredients.append("pasta")
    recipe.ingredients.append("tomato sauce")
    recipe.ingredients.append("garlic")
    recipe.ingredients.append("olive oil")
    recipe.ingredients.append("salt")
    recipe.ingredients.append("basil")
    recipe.img = "spaghetti.png"
    recipe.instructions = "Do this and that"
    recipe.cookTime = 15
    recipe.prepTime = 60.0
    recipe.tags += ["starch", "italian", "pasta"]
    return recipe

class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.img = None
        self.tags = []
        self.prepTime = 0.0
        self.cookTime = 0.0
        self.instructions = ""

class RecipeBook(object):
    def __init__(self, *args, **kwargs):
        self.recipes = []
        #self.__type__ = "RecipeBook"

    def __str__(self):
        retStr = ""
        for recipe in self.recipes:
            retStr += recipe.name + "\n\t"
            for ingredient in recipe.ingredients:
                retStr += "- " + ingredient + "\n\t"
            retStr += "Prep time: " + str(recipe.prepTime) + "\n\t"
            retStr += "Cook time: " + str(recipe.cookTime) + "\n\t"
            retStr += "Instructions: " + recipe.instructions + "\n\t"
            for tag in recipe.tags:
                retStr += tag + ";"
            retStr += "\n"
        return retStr

    def CreateWindow(self):
        root = tkinter.Tk()
        window = MainWindow(master=root, title="Recipe Book")
        root.mainloop()
        
        #ttk.Label(window.frame, text="Test Label").grid(column=0, row=0)
        #ttk.Button(window.frame, text = "Quit", command=window.root.destroy).grid(column=1, row=0)
        #image
        #img = PhotoImage(file="salad.png")
        #ttk.Label(window.frame, image=img)
        #ttk.Button(window.frame, text="image here").grid(column=0, row=1)
        #title of recipe
        #Ingredients
        #
        
        #window = AppWindow(title="Recipe Book")
        #window.
        #window.Label(text="test").grid(column=0, row=0)

    def AddRecipe(recipe):
        print("Unimplemented")

    def RemoveRecipe(recipe):
        print("Unimplemented")
    
    def ReviseRecipe(recipe):
        print("Unimplemented")

    def MatchRecipe(self, ingList): #Given ingredients
        #To begin algorithm development, try with lowest problem first
        canMake = []
        canNearlyMake = []
        ingMatches = 0
        
        #Recipe list
        for recipe in self.recipes:

            # Ingredient List
            for i in ingList:
                if i in recipe.ingredients:
                    #print("Found", i, "for", recipe.name)
                    ingMatches += 1
                    continue 
                #else:
                    #print("Not found", i, "for", recipe.name)
                    #print("")
            if ingMatches == len(recipe.ingredients): #testR.ingredients should be a list brought in
                #print("ingMatches:", ingMatches, "\ningList:", len(testR.ingredients))
                ingMatches = 0
                canMake += [recipe.name]
            elif ingMatches/len(recipe.ingredients) > 0.7:
                canNearlyMake += [recipe.name]
                ingMatches = 0
        print("Can make:", str(canMake), "\nCan nearly make:", str(canNearlyMake))
        return canMake, canNearlyMake

    def SearchRecipe(target):
        print("Unimplemented")

    def OpenRecipeFile(self):
        #Change to not return but add all of this to self
        print("OpenRecipeFile called")
        try:
            file = open(RB_FILE, mode='r')
            readIn = file.read()
            bookDict = json.loads(readIn)
            decodedBook = RecipeBookDecoder(bookDict)
            #print("interpretted: ", decodedBook)
            #print("type:", type(decodedBook))
            #print("Recipes:", decodedBook.recipes)
            return decodedBook
            
        except FileNotFoundError:
            print("Something went wrong attempting to read RecipeBook file.")
        #except:
        #    print("Something went wrong decoding file")
        finally:
            file.close()

    def SaveRecipeFile(self):
        try:
            file = open(RB_FILE, mode='+w')
            #Convert the recipe book to a json format
            jsonRecipeBook = json.dumps(self, indent=2, cls=RecipeBookEncoder)
            file.write(jsonRecipeBook)
        except FileNotFoundError:
            print("Something went wrong trying to write to Recipe Book file")
        finally:
            file.close()

    def GetAllIngredients(self):
        allAvailableIngredients = []
        for recipe in self.recipes:
            allAvailableIngredients += recipe.ingredients
        print("All available ingredients:", allAvailableIngredients)
        return allAvailableIngredients
        # try:
        #     file = open(ING_FILE, mode='+w')
        # except FileNotFoundError:
        #     print("Something went wrong making ingredient file")
        # finally:
        #     file.close()

#Made referencing https://pynative.com/make-python-class-json-serializable/
#Makes class a JSONEncoder and simply returns the object itself as a dictionary that is serializable
class RecipeBookEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__

def RecipeBookDecoder(obj):
    book = RecipeBook()
    #We expect a dictionary, so store the value associated with recipes
    recipes = obj['recipes']
    #print("obj['recipes'] is type", type(recipes))
    #print("recipe in recipes are of type", type(recipes[0]))
    for recipe in recipes:
        r = Recipe("test")
        r.name = recipe['name']
        r.img = recipe['img']
        r.prepTime = float(recipe['prepTime'])
        r.cookTime = float(recipe['cookTime'])
        r.instructions = recipe['instructions']

        r.ingredients = []
        for ingredient in recipe['ingredients']:
            r.ingredients += [ingredient]

        r.tags = []
        for tag in recipe['tags']:
            r.tags += [tag]
        book.recipes.append(r)
    #print(book)
    return book

def GetRecipeBookObj():
    "Gets reference to the book object from the tk widget hierarchy"
    print("unimplemented")

overlay = None #Overlay for images

def main():
    book = RecipeBook()
    book.recipes += [CreateTestRecipe()]
    book.recipes += [CreateTestRecipe2()]
    #print(book)
    book.SaveRecipeFile()
    #book.MatchRecipe(ingList=["flour", "eggs", "water", "oil", "garlic", "bread", "peanut butter", "fruit jelly", "crushed tomatoes"])
    book.CreateWindow()
    
    #book.OpenRecipeFile()
    

main()
