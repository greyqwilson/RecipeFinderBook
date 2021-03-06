#Recipe Finder tool with GUI built using tkinter and ttk
#Greyson Wilson
#CS 2520

from functools import partial
from json import *
import json
import random
import string
from textwrap import wrap
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter.scrolledtext import ScrolledText
from tokenize import String
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
        

class RS_ImageBox(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.imgPath = StringVar(value=DEFAULT_IMG_PATH)
        self.defaultImgPath = DEFAULT_IMG_PATH
        self.recipe = recipe
        #Image variables to handle opening, resizing, widget
        try:
            openImgVar = PilImage.open(self.imgPath.get())
        except FileNotFoundError:
            print("Failed to locate default image 'default.png'")
            return
        
        openImgVar.thumbnail((400,400))
        self.imgTkVar = ImageTk.PhotoImage(openImgVar)
        self.img = Label(self, image=self.imgTkVar)
        self.img.grid(column=0, row=0)
        self.grid(column=1, row=1)
    
    def UpdateImage(self):
        self.imgPath.set(self.recipe.img)
        if self.imgPath.get() not in ["", " "]:
            try:
                openImgVar = PilImage.open(self.imgPath.get())
            except FileNotFoundError:
                openImgVar = PilImage.open(DEFAULT_IMG_PATH)
                print("Failed to find recipe image. Using default")
            openImgVar.thumbnail((400,400))
            self.imgTkVar = ImageTk.PhotoImage(openImgVar)
            self.img = Label(self, image=self.imgTkVar, anchor=NW).grid(column=0, row=0)
        else:
            print("No image path entered. Skipping")

class RS_RecipePreview(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master, name="!rs_recipepreview")
        # self.nameLabel = Label(self, text="Name")
        # self.imgLabel = Label(self, text="Image")
        # self.ingredientsLabel = Label(self, text="Ingredients")
        # self.instructionsLabel = Label(self, text="Instructions")
        # self.prepTimeLabel = Label(self, text="Prep time")
        # self.cookTimeLabel = Label(self, text="Cook time")
        # self.tagsLabel = Label(self, text="Tags")
        self.recipe = recipe
        self.name = StringVar(value=" ")
        self.ingredients = StringVar(value=" ")
        self.instructions = StringVar(value=" ")
        self.prepTime = StringVar(value=" ")
        self.cookTime = StringVar(value=" ")
        self.tags = StringVar(value=" ")

        self.imageBox = RS_ImageBox(master=self, recipe=recipe)

        self.infoFrame = Frame(self)
        self.namePreview = Label(self.infoFrame, textvariable=self.name)
        self.ingredientsPreview = Label(self.infoFrame, textvariable=self.ingredients, wraplength=200, justify= CENTER, height=10)
        self.instructionsPreview = Label(self.infoFrame, textvariable=self.instructions, wraplength=200, justify=LEFT, height=10)
        self.prepTimePreview = Label(self.infoFrame, textvariable=self.prepTime)
        self.cookTimePreview = Label(self.infoFrame, textvariable=self.cookTime)
        self.tagsPreview = Label(self.infoFrame, textvariable=self.tags, wraplength=200, justify=CENTER, height=10)

        self.imageBox.grid(column=1, row=1)
        self.infoFrame.grid(column=2, row=1)
        
        self.namePreview.grid(column=0, row=1)
        self.ingredientsPreview.grid(column=0, row=2)
        self.instructionsPreview.grid(column=0, row=3)
        self.prepTimePreview.grid(column=0, row=4)
        self.cookTimePreview.grid(column=0, row=5)
        self.tagsPreview.grid(column=0, row=6)

    def UpdateIngPreview(self):
        ingString = ""
        for ing in self.recipe.ingredients:
            ingString += "> " + ing + "\t"
        self.ingredients.set(ingString)

    def UpdateTagPreview(self):
        tagString = ""
        for tag in self.recipe.tags:
            tagString += tag + "; "
        self.tags.set(tagString)

    def UpdatePreview(self):
        #print("RS_RecipePreview.UpdatePreview sees this recipe name:", self.recipe.name)
        self.name.set(self.recipe.name)
        self.UpdateIngPreview()
        self.instructions.set(self.recipe.instructions)
        self.prepTime.set("Prep time:" + self.recipe.prepTime)
        self.cookTime.set("Cook time:" + self.recipe.cookTime)
        self.UpdateTagPreview()
        self.imageBox.UpdateImage()


class RS_InstructionsEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.recipe = recipe
        self.entryFrame = Frame(self, width=1, height=1)
        self.instructionsBox = ScrolledText(self.entryFrame, width=50, height=20) #maybe just use text
        self.instructionsLabel = Label(self, text="Instructions")
        self.instructionsButton = Button(self, text="Change", command=self.Change)
        #Grids
        self.entryFrame.grid(column=0, row=1)
        self.instructionsLabel.grid(column=0, row=0)
        self.instructionsBox.grid(column=0, row= 0)
        self.instructionsButton.grid(column=1, row=1)
    
    def PreviewChange(self):
        print("blah")

    def Change(self):
        self.recipe.instructions = self.instructionsBox.get(1.0, END)

class RS_ImageEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.recipe = recipe
        self.imgBox = Entry(self)
        self.imgLabel = Label(self, text="Image path")
        self.imgButton = Button(self, text="Change", command=self.Change)
        #Grids
        self.imgLabel.grid(column=0, row=0)
        self.imgBox.grid(column=0, row= 1)
        self.imgButton.grid(column=1, row=1)
    
    def PreviewChange(self):
        print("blah")

    def Change(self):
        self.recipe.img = self.imgBox.get()
        

class RS_NameEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.recipe = recipe
        self.nameBox = Entry(self)
        self.nameLabel = Label(self, text="Name")
        self.nameButton = Button(self, text="Change", command=self.Change)
        #Grids
        self.nameLabel.grid(column=0, row=0)
        self.nameBox.grid(column=0, row= 1)
        self.nameButton.grid(column=1, row=1)
    
    def PreviewChange(self):
        print("blah")

    def Change(self):
        self.recipe.name = self.nameBox.get()


class RS_IngredientEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.recipe = recipe
        self.ingredientsBox = Entry(self)
        self.ingredientsLabel = Label(self, text="Ingredients")
        self.ingredientsButton = Button(self, text="Change", command=self.Change)
        #Grids
        self.ingredientsLabel.grid(column=0, row=0)
        self.ingredientsBox.grid(column=0, row= 1)
        self.ingredientsButton.grid(column=1, row=1)

    #     self.ingredientsBox.bind("<Key>", self.callback)
    
    # def callback(self, event):
    #     if event.char in string.ascii_letters:
    #         event.widget.insert(END, random.randint(2, 4))
    #         return "break"

    def PreviewChange(self):
        print("blah")

    def Change(self):
        entries = self.ingredientsBox.get().split(sep=',')
        for entry in entries:
            if entry not in self.recipe.ingredients and entry != string.whitespace:
                self.recipe.ingredients.append(entry.lower())
                

class RS_PrepTimeEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.recipe = recipe
        self.preptimeBox = Entry(self)
        self.preptimeLabel = Label(self, text="Prep time")
        self.preptimeButton = Button(self, text="Change", command=self.Change)
        #Grids
        self.preptimeLabel.grid(column=0, row=0)
        self.preptimeBox.grid(column=0, row= 1)
        self.preptimeButton.grid(column=1, row=1)
    
    def PreviewChange(self):
        print("blah")

    def Change(self):
        self.recipe.prepTime = self.preptimeBox.get()

class RS_CookTimeEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.recipe = recipe
        self.cooktimeBox = Entry(self)
        self.cooktimeLabel = Label(self, text="Cook time")
        self.cooktimeButton = Button(self, text="Change", command=self.Change)
        #Grids
        self.cooktimeLabel.grid(column=0, row=0)
        self.cooktimeBox.grid(column=0, row= 1)
        self.cooktimeButton.grid(column=1, row=1)
    
    def PreviewChange(self):
        print("blah")

    def Change(self):
        self.recipe.cookTime = self.cooktimeBox.get()

class RS_TagsEntry(ttk.Frame):
    def __init__(self, recipe, master=None):
        super().__init__(master)
        self.recipe = recipe
        self.tagsBox = Entry(self)
        self.tagsLabel = Label(self, text="Tags")
        self.tagsButton = Button(self, text="Change", command=self.Change)
        #Grids
        self.tagsLabel.grid(column=0, row=0)
        self.tagsBox.grid(column=0, row= 1)
        self.tagsButton.grid(column=1, row=1)
    
    def PreviewChange(self):
        print("blah")

    def Change(self):
        entries = self.tagsBox.get().split(sep=',')
        print("Tags:", entries)
        for entry in entries:
            #Check for duplicates
            if entry not in self.recipe.tags:
                entry = entry.rstrip()
                self.recipe.tags.append(entry.lower())

class RS_EditSuite(ttk.Frame):
    def __init__(self, recipeBook, master=None):
        super().__init__(master, name="!rs_editsuite")
        #Recipe book passed on creation
        self.recipeBook = recipeBook
        self.newRecipe = Recipe("New Recipe")

        self.innerFrame = Frame(self)
        self.imgEntry = RS_ImageEntry(master=self.innerFrame, recipe=self.newRecipe)
        self.nameEntry = RS_NameEntry(master=self.innerFrame, recipe=self.newRecipe)
        self.ingredientsEntry = RS_IngredientEntry(master=self.innerFrame, recipe=self.newRecipe)
        self.preptimeEntry = RS_PrepTimeEntry(master=self.innerFrame, recipe=self.newRecipe)
        self.cooktimeEntry = RS_CookTimeEntry(master=self.innerFrame, recipe=self.newRecipe)
        self.tagsEntry = RS_TagsEntry(master=self.innerFrame, recipe=self.newRecipe)
        self.instructionsEntry = RS_InstructionsEntry(master=self, recipe=self.newRecipe)
        self.changeAllButton = Button(master=self, text="Change/update all", command=self.ChangeAll)
        self.saveRecipeButton = Button(master=self, text="Save recipe", command=self.SaveRecipe)

        self.imgEntry.grid(column=0, row=0)
        self.nameEntry.grid(column=0, row=1)
        self.ingredientsEntry.grid(column=0, row=2)
        self.preptimeEntry.grid(column=0, row=3)
        self.cooktimeEntry.grid(column=0, row=4)
        self.tagsEntry.grid(column=0, row=5)
        self.changeAllButton.grid(column=0, row=6)
        self.saveRecipeButton.grid(column=0, row=7)

        self.innerFrame.grid(column=0, row=0)
        self.instructionsEntry.grid(column=1, row=0)

        

    def UpdatePreview(self):
        self.master.children['!rs_recipepreview'].UpdatePreview()
        #print("RS_EditSuite.UpdatePreview sees this recipe name:", self.newRecipe.name)

    def ChangeAll(self):
        self.nameEntry.Change()
        self.ingredientsEntry.Change()
        self.instructionsEntry.Change()
        self.preptimeEntry.Change()
        self.cooktimeEntry.Change()
        self.tagsEntry.Change()
        self.imgEntry.Change()

        self.UpdatePreview()

    def SaveRecipe(self):
        self.recipeBook.recipes.append(self.newRecipe)
        self.recipeBook.SaveRecipeFile()
        self.master.master.children['!mainwindow'].children['!notebook'].children['!frame'].children['!ingredientsearchbox'].UpdateButtons()
        
        
        

class RecipeStationWindow(Toplevel):
    def __init__(self, recipeBook, master=None):
        super().__init__(master, name='!recipestationwindow')
        self.config(border='15', width='800', height='600')
        self.minsize(800,600)
        self.title("Recipe station")
        self.recipeBook = recipeBook
        #self.innerFrame = Frame(self)
        self.editAddSuite = RS_EditSuite(master=self, recipeBook=self.recipeBook)
        self.preview = RS_RecipePreview(master=self, recipe=self.children['!rs_editsuite'].newRecipe)
        self.editAddSuite.grid(column=0, row=0)
        self.preview.grid(column=1, row=0)
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
        self.button = Button(self, text="Recipe Station", command=self.MakeWindow, anchor=E)
        self.button.grid(column=0, row=0)
        self.stationStatus = False
        self.recipeStation = None
        self.grid(column=0, row=1)

    def MakeWindow(self):
        if self.stationStatus == False:
            print("Opening recipe station")
            self.stationStatus = True
            self.recipeStation = RecipeStationWindow(recipeBook=self.master.master.book)
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
        
        self.searchButton = Button(self.searchBarFrame, text="Search/Set", command=self.Search)
        self.searchButton.grid(column=1, row=0)

        self.refreshButton = Button(self.searchBarFrame, text="Refresh", command=self.UpdateRecipeBox)
        self.refreshButton.grid(column=1, row=1)
        
        self.allRecipesBox = ScrolledText(self.master, width=35)
        self.allRecipesBox.grid(column=1, row=0)
        self.UpdateRecipeBox()
    
    def Search(self):
        for recipe in self.master.master.master.book.recipes:
            if recipe.name.lower() == self.stringVar.get().lower():
                print(recipe.name, "found!")
                self.master.master.master.activeRecipe = recipe
                #maybe this can be a toggle \/
                self.allRecipesBox.config(state='normal')
                self.allRecipesBox.delete(1.0, END)
                self.allRecipesBox.insert(INSERT, recipe.name)
                self.allRecipesBox.insert(INSERT, "\n")
                self.allRecipesBox.config(state='disabled')
                ##                          /\
                self.master.master.master.children['!recipeinfobox'].UpdateInfo()
            else:
                self.UpdateRecipeBox()
    
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
        self.recipeBook = self.master.master.book

        self.optionButton = Button(self, text="Option Placeholder", command=self.Options, anchor=E, justify=RIGHT)
        self.optionButton.grid(column=0, row=1)

        # self.openButton = Label(self, text="Open Recipe Book")
        # self.openButton.grid(column=0, row=2)

        self.fileName = StringVar(value=RB_FILE)
        self.fileEntry = Entry(self, textvariable=self.fileName)
        self.fileEntry.grid(column=0, row=3)
        
        self.fileEntryButton = Button(self, text="Open file", command= self.LoadRecipeBook, anchor=E, justify=RIGHT)
        self.fileEntryButton.grid(column=1, row=3)

        self.grid(column=0, row=2)
    
    #Should ideally simply load the recipe book and the first recipe
    def LoadRecipeBook(self):
        self.recipeBook = self.recipeBook.OpenRecipeFile(self.fileName.get())
        #ingBox = self.master.children.get('ingredientbox')
        #print(ingBox)
        # recipeLabel = self.master.children['!recipelabel']
        # recipeImg = self.master.children['!imagebox']
        # ingBoxWidget = self.master.children['!ingredientbox']
        # recipeLabel.UpdateLabel(self.recipeBook.recipes[0].name)
        # recipeImg.UpdateImage(self.recipeBook.recipes[0].img)
        # ingBoxWidget.UpdateIngBox(self.recipeBook.recipes[0].ingredients)

    
    def Options(self):
        print("Unimplemented")

class RecipeInfoBox(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, name='!recipeinfobox')
        
        self.recipeBook = self.master.book
        self.infoFrame = Frame(self, bg="#313740")
        self.recipeName = RecipeLabel(self.infoFrame)
        self.imgBox = ImageBox(self)
        self.ingredientBox = IngredientBox(self.infoFrame)
        self.instructionsBox = InstructionsBox(self.infoFrame)
        self.prepTimeBox = PrepTimeBox(self.infoFrame)
        self.cookTimeBox = CookTimeBox(self.infoFrame)
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
        self.prepTimeBox.grid(column=0, row=4)
        self.cookTimeBox.grid(column=0, row=5)
        self.tagsBox.grid(column=0, row=6)
        #self.activeRecipe = self.master.activeRecipe


        #Default values is 1st recipe in recipes
        self.recipeName.UpdateLabel(self.recipeBook.recipes[0].name)
        self.imgBox.UpdateImage(self.recipeBook.recipes[0].img)
        self.ingredientBox.UpdateIngBox(self.recipeBook.recipes[0].ingredients)
        self.instructionsBox.UpdateInsBox(self.recipeBook.recipes[0].instructions)
        self.prepTimeBox.UpdatePrepBox(self.recipeBook.recipes[0].prepTime)
        self.cookTimeBox.UpdateCookBox(self.recipeBook.recipes[0].cookTime)
        self.tagsBox.UpdateTagsBox(self.recipeBook.recipes[0].tags)

    def UpdateInfo(self):
        #Update name, image, ingredients, instructions, tags
        self.activeRecipe = self.master.activeRecipe
        self.recipeName.UpdateLabel(self.activeRecipe.name)
        self.imgBox.UpdateImage(self.activeRecipe.img)
        self.ingredientBox.UpdateIngBox(self.activeRecipe.ingredients)
        self.instructionsBox.UpdateInsBox(self.activeRecipe.instructions)
        self.prepTimeBox.UpdatePrepBox(self.activeRecipe.prepTime)
        self.cookTimeBox.UpdateCookBox(self.activeRecipe.cookTime)
        self.tagsBox.UpdateTagsBox(self.activeRecipe.tags)

class PrepTimeBox(ttk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.boxText = StringVar()
        self.boxText.set(" ")
        self.prepTimeLabel = Label(self, textvariable=self.boxText, justify=LEFT)
        self.prepTimeLabel.grid(column=0, row=0)
        
    def UpdatePrepBox(self, ptime):
        self.boxText.set("Prep time: " + ptime)

class CookTimeBox(ttk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.boxText = StringVar()
        self.boxText.set(" ")
        self.prepTimeLabel = Label(self, textvariable=self.boxText, justify=LEFT)
        self.prepTimeLabel.grid(column=0, row=0)
        
    def UpdateCookBox(self, ctime):
        self.boxText.set("Cook time: " + ctime)

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

    def UpdateButtons(self):
        self.ingredients =  self.master.master.master.book.GetAllIngredients()
        for ing in self.ingredients:
            if ing not in self.buttonStates:
                self.buttonStates[ing] = False
                cvar = StringVar()#--
                cvar.set("_"+ing)#--
                button = Checkbutton(self.canvas, text=ing, justify=LEFT, bg='#A73337', activebackground='#773337',
                                                        variable=cvar, onvalue=ing, offvalue="_"+ing)
                self.canvas.create_window(4, 25 * self.buttonIndex, window=button, anchor=W, height=20) 
                button.bind("<Configure>", lambda event, canvas = self.canvas : self.event_onFrameConfigure(canvas))

                self.lastSelect.set(cvar.get())
                self.controlVars[ing] = cvar
                #Implementation from https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter Dologan
                partialFunction = partial(self.AddToSearch, cvar.get())
                button.config(command=partialFunction)
                self.buttonArray.append(button)
                self.buttonIndex += 1

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
        self.img = Label(self, image=self.imgTkVar)
        self.img.grid(column=0, row=0)
        self.grid(column=1, row=1)

        #self.resizedImg.load()
        #self.imgVar = PhotoImage(file=self.imgPath.get(), width=400, height=400)

        self.imgState = True
        self.toggleStringVar = StringVar()
        self.toggleStringVar.set("-")
        self.toggleButton = Button(master, textvariable=self.toggleStringVar, command=self.ToggleImage).grid(column=0, row=0)
    
    def UpdateImage(self, imgPath):
        self.imgPath.set(imgPath)
        try:
            openImgVar = PilImage.open(self.imgPath.get())
        except FileNotFoundError:
            print("Recipe image not found. Using default")
            openImgVar = PilImage.open(DEFAULT_IMG_PATH)

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
    def __init__(self, master=None, title = "New Window", *args, **kwargs):
        super().__init__(master)
        self.config(border='15', width='800', height='600')
        self.master.minsize(800,400)
        self.master.title("Recipe Book")
        self.book = RecipeBook()
        self.book = self.book.OpenRecipeFile(RB_FILE)
        #Default recipe is first in list
        self.activeRecipe = self.book.recipes[0]
        #self.book.GetAllIngredients()
        self.grid()

        ##Widget classes below

        #self.imageBox = ImageBox(master=self)
        #self.ingBox = IngredientBox(master=self)
        #self.searchBox = SearchBox(master=self)
        #self.ingSearchBox = IngredientSearchBox(master=self)
        #print("after widget made:", self.ingSearchBox.controlVar.get())
        #self.recipeBox = RecipeLabel(master=self)

        self.sideButtonsFrame = Frame(master=self)
        self.sideButtonsFrame.grid(column=4, row=1)
        self.fileBox = FileOpBox(master=self.sideButtonsFrame)
        self.searchTabs = SearchTabs(master=self)
        self.recipeInfoBox = RecipeInfoBox(master=self)
        self.recipeStation = RecipeStationBox(master = self.sideButtonsFrame)
        
        self.mainloop()
            
def CreateTestRecipe():
    recipe = Recipe("Peanut butter and jelly sandwich")
    recipe.ingredients.append("peanut butter")
    recipe.ingredients.append("fruit jelly")
    recipe.ingredients.append("bread")
    recipe.img = "pbj.png"
    recipe.instructions = "Grab two slices of bread. On one slice, slather peanut butter on a single side. On the other slide, " + \
     "slather jelly onto a single side. Place the sides together so that the peanut butter and jelly touch"
    recipe.cookTime = "0 minutes"
    recipe.prepTime = "2 minutes"
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
    recipe.cookTime = "15 minutes"
    recipe.prepTime = "1 hour"
    recipe.tags += ["starch", "italian", "pasta"]
    return recipe

class Recipe:
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.img = None
        self.tags = []
        self.prepTime = ""
        self.cookTime = ""
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

    def OpenRecipeFile(self, fileName):
        #Change to not return but add all of this to self
        print("Opening recipe file:", fileName)
        try:
            file = open(fileName, mode='r')
            readIn = file.read()
            bookDict = json.loads(readIn)
            decodedBook = RecipeBookDecoder(bookDict)
            #print("interpretted: ", decodedBook)
            #print("type:", type(decodedBook))
            #print("Recipes:", decodedBook.recipes)
            return decodedBook
            
        except FileNotFoundError:
            try:
                print("Failed to open given name. Opening default file: ", RB_FILE)
                file = open(RB_FILE, mode='r')
                readIn = file.read()
                bookDict = json.loads(readIn)
                decodedBook = RecipeBookDecoder(bookDict)
                return decodedBook

            except FileNotFoundError:
                print("Failed to find default file. Please place", RB_FILE, "in root directory")
            finally:
                file.close()
                
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
        #print("All available ingredients:", allAvailableIngredients)
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
        r.prepTime = recipe['prepTime']
        r.cookTime = recipe['cookTime']
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

def CreateWindow():
        root = tkinter.Tk()
        window = MainWindow(master=root, title="Recipe Book")
        root.mainloop()

def GetRecipeBookObj():
    "Gets reference to the book object from the tk widget hierarchy"
    print("unimplemented")

def TkHierarchyFinder(tkinterobj):
    while(tkinterobj != None):
        print(tkinterobj.winfo_name)
        tkinterobj = tkinterobj.master

overlay = None #Overlay for images

def main():
    # book = RecipeBook()
    # book.recipes += [CreateTestRecipe()]
    # book.recipes += [CreateTestRecipe2()]
    # book.SaveRecipeFile()
    #book.CreateWindow()
    CreateWindow()

main()
