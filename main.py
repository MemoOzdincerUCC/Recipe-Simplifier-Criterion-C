import tkinter as tk 
from tkinter import ttk
from bs4 import BeautifulSoup # BeautifulSoup is a scraper program, after extensive research and testing, I found it's the one that fit my needs best.
import requests # Requests is a HTTP-based library that can send nearly all request methods. My program uses GET and HEAD (ln. 17,22,38,62,68)

URL = "strValue" # I assigned a random string value to this variable as it will store strings.
SoupResult = 'Your Recipe Will Appear Here:'+'\n'+'_'*42+'\n'+'\n'+'_'*42+'\n'+'\n'+'_'*42+'\n'+'\n'+'_'*42+'\n'+'\n'+'_'*42+'\n'+'\n'+'_'*42+'\n' # Decorative Banner
usrinput = tk.StringVar # I use stringvar as it supports pulling user input from a text field (What this value is for)
TestURL = "https://sites.google.com/ucc.on.ca/recipesimplifier-test/home" # This is my website that is for testing multiple aspects of the program.
FormattingNumbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
def MasterFunction(): # This function is the scraper, it identifies the website the user entered, and scrapes the parsed information respectively.
    global URL # For good practice, and to avoid errors, I set the class of the two primary variables as 'global'.
    global SoupResult
    URL = (EnterURL.get()) # Gets the URL the user entered from text box.
    result = str(EnterURL) 

    if 'damndelicious.net' in URL: # Identifies website to decide which scraper to use.
        source = requests.get(URL).text
        SoupResult = BeautifulSoup(source, 'lxml') # source is the URL, lxml is the parser, it filters through the HTML.
        SoupResult = SoupResult.find('div',class_='left').text # In the websites' HTML, I found the class names they use for their recipes, I use this to identify them.

    elif 'kitchentreaty.com' in URL:
        source = requests.get(URL).text
        SoupResult = BeautifulSoup(source, 'lxml')
        SoupResult = SoupResult.find('div',class_='wprm-recipe-ingredients-container wprm-block-text-normal').text
        for FormattingNumber in FormattingNumbers:
            SoupResult.replace(FormattingNumber,"\n"+FormattingNumber) # The formatting for this website is tricky, they don't use <ul> like the other ones, so I formatted it myself.
        SoupResult = SoupResult.replace("1","\n1") 
        SoupResult = SoupResult.replace("2","\n"+"2")
        SoupResult = SoupResult.replace("3","\n"+"3")
        SoupResult = SoupResult.replace("4","\n"+"4")
        SoupResult = SoupResult.replace("5","\n"+"5")
        SoupResult = SoupResult.replace("6","\n"+"6")
        SoupResult = SoupResult.replace("7","\n"+"7")
        SoupResult = SoupResult.replace("8","\n"+"8")
        SoupResult = SoupResult.replace("9","\n"+"9")
        SoupResult = SoupResult.replace("/\n", "/") # I made it so there's a newline before every quantity (numerals) except the fractions.
        SoupResult = SoupResult.replace("\n/","/")
    elif 'simplyrecipes.com' in URL:
        source = requests.get(URL).text
        SoupResult = BeautifulSoup(source, 'lxml')
        SoupResult = SoupResult.find('div',class_='entry-details recipe-ingredients').text
        SoupResult = SoupResult.replace("\ningredients","ingredients")
        SoupResult = SoupResult.replace("\nIngredients","Ingredients")
        SoupResult = SoupResult.replace("\ningredients:","ingredients:")
        SoupResult = SoupResult.replace("\nIngredients:","Ingredients:")
        SoupResult = SoupResult.replace(" Special", "Special")
    else:
        popupmessage() # This function is activated if the domain isn't found in the entry field, it will give an error.
    OT = tk.Text(root)
    OT.insert(1.0,SoupResult)
    OT.configure(font='Roboto_Slab 23')
    OT.configure(state='disabled')
    OT.place(x=50,y=320, height=300, width=450) # OT is a read only text widget I created as Labels do not support scrolling. Its properties are below (ln. 54-58)

    # Since my GUI is small, sometimes it isn't able to display all of the text. I implemented a scroll bar to fix this.
    scroll_y = tk.Scrollbar(root, orient="vertical", command=OT.yview)
    scroll_y.place(x=500,y=320, height=300)

    OT.configure(yscrollcommand=scroll_y.set)
def ForbiddenFound(): # If the website blacklists the user's IP or the bot's instance, it will give a 403, this function alerts the user if that happens.
    ForbiddenPopup = tk.Tk()
    ForbiddenPopup.wm_title("Website Warning!")
    ForbiddenText = ttk.Label(ForbiddenPopup, text="The website you tried to reach has blocked your network or the program!\nPlease contact the developer, or the website for more info.")
    ExitButton = ttk.Button(ForbiddenPopup, text="Okay", command = ForbiddenPopup.destroy)
    ForbiddenPopup.mainloop()
def TestButton(): # This function tests all of the modules and errors. If there's a 403, it errors saying it's forbidden. It also tests the scraper and the parser.
    Test = tk.Tk()
    Test.wm_title("Testing All Modules...")
    sourceoftest = requests.get(TestURL).text
    TestResult = BeautifulSoup(sourceoftest,'lxml')
    TestResult = TestResult.find().text
    if '403 Forbidden' in TestResult:
        ForbiddenFound() # See line 59 (Testing for 403)
    else: # Testing scraper and parser, I made two classes on the same level and div, if the parser can differentiate, and show the correct text, it works)
        sourceofmaintest = requests.get(TestURL).text
        TestResult = BeautifulSoup(sourceofmaintest, 'lxml')
        TestResult = TestResult.find('p', class_='CDt4Ke zfr3Q').text
        TestLabel = ttk.Label(Test, text=TestResult)
        TestLabel.pack(side='top', pady='10')
        Test.wm_title("Testing Finished!")
        Test.mainloop()
def popupmessage():  # This error is for when the user enters a wrong, or unsupported website domain.
    popup = tk.Tk()
    popup.wm_title("Error! More info below.")
    label = ttk.Label(popup, text="That is not a valid URL!\nPlease refer to the 'Supported Websites' Button", font='Roboto_Slab 23', justify='center')
    label.pack(side='top', pady='10')
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
def supportedwebsites(): # This button tells the user what the available webstites are.
    AvailableWebsites = tk.Tk()
    AvailableWebsites.wm_title("Supported Websites")
    listofsuppwebsites = ttk.Label(AvailableWebsites, font="Roboto_Mono 23 bold", text='simplyrecipes.com\nkitchentreaty.com\ndamndelicious.net')
    listofsuppwebsites.pack(side='top',pady='10')
    ExitButton = ttk.Button(AvailableWebsites, text="Okay", command = AvailableWebsites.destroy)
    ExitButton.pack()
    AvailableWebsites.mainloop()

####################################################---- MAIN GUI ----###########################################################

# root properties: In these four lines, I set up the orientation, and the window title
root = tk.Tk()
root.title("Recipe Simplifier")
root.geometry('563x683')
root.resizable(height=0, width=0)
# The dimensions 563x683 come from my prototype as that's what worked best while testing.
# I made it non-resizable because the picture can't be resized without compromising ratio or quality.

# In line 14, 15 and 16, I'm defining and placing an image. GIFs have better compatibility than JPEG/PNGs.
img = tk.PhotoImage(file="Cooking background image.gif")
thebackground = tk.Label(master=root,image=img)
thebackground.place(x=0,y=0)
# I first defined the image file as a variable (ln. 14), then I placed it as the background for 'root' (ln. 15-16)

# Line 20,21,22 I made the Title Text
titletext = tk.Label(root, justify="center", bg="white", fg="black",font="Roboto_Slab 50",text="Recipe\n Simplifier", height=2,width=9,padx=0,pady=0)
titletext.place(x=217, y=40)
# I first set up its properties (ln. 20), then I placed it in the correct coordinates (ln. 21)

# I resized this image to 120x120 and converted to a GIF in Photoshop as having PIL do it slowed down the program.
ChefVector = tk.PhotoImage(file='CookingImage.gif')
ChefImage = tk.Label(master=root,image=ChefVector)
ChefImage.place(x=50, y=40)

# This is a label telling the user to enter their URL below.
FullURL = tk.Label(master=root,
                    font="Roboto_Slab 23", text = "Enter The URL Here:")
FullURL.place(x=50,y=190)

# Entry box, this allows the user to type in their desired website
EnterURL = tk.Entry(master=root, font="Roboto_Slab 10 underline", width=57, fg="Blue", textvariable=usrinput)
EnterURL.place(x=50,y=255)

# Stores in a variable 'GoButton', the text that was pulled from the Entry Field.
GoButton = tk.Button(master=root, font="Roboto_Slab 15", text='Go', command=MasterFunction)
GoButton.place(x=470,y=255)

# The button for the Test function, upon pressing, it goes through the entire testing process, and validates all modules.
TestButtonWidget = tk.Button(master=root, font="Roboto_Slab 15", text='Test All Modules', command=TestButton)
TestButtonWidget.place(x=393,y=625)

# I made a button so the user knows which websites are supported (function explained above, ln. 89)
WebsiteSelection = tk.Button(master=root,font="Roboto_Slab 23", text="Supported Websites", command=supportedwebsites, padx=0,pady=1)
WebsiteSelection.place(x=285,y=190)

OutputText = tk.Text(root)
OutputText.insert(1.0,SoupResult)
OutputText.configure(font='Roboto_Slab 23')
OutputText.configure(state='disabled')
OutputText.place(x=50,y=320, height=300, width=450)

# Since my GUI is small, sometimes it isn't able to display all of the text. I implemented a scroll bar to fix this.
scroll_y = tk.Scrollbar(root, orient="vertical", command=OutputText.yview)
scroll_y.place(x=500,y=320, height=300)

# changes the properties of OutputText for it to have a scrollbar.
OutputText.configure(yscrollcommand=scroll_y.set)

root.mainloop()
