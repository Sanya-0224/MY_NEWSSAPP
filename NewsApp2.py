import requests
import webbrowser
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image
import io

class NewsApp:

    def __init__(self):
        # Fetch data
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=8f8a17c749914206ac1a7aa1b26ec115').json()
        # Install GUI load
        self.load_gui()
        # load Welcome page
        self.welcome_page()

    def load_gui(self):
        self.root = Tk()
        self.root.geometry('350x600')
        self.root.resizable(0, 0)
        self.root.title('My Shorts')  # Set window title
        self.root.configure(background='black')

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()
            
    def welcome_page(self):
        self.clear()
        welcome_label = Label(self.root, text="Welcome to My Shorts", bg='black', fg='white', font=('Nunito Sans', 20))
        welcome_label.pack(pady=150)
        start_button = Button(self.root, text="Start Reading", command=self.load_news_item)
        start_button.pack()

    def load_news_item(self, index=0):
        # Clear screen
        self.clear()
        #IMAGE URL
        img_url = self.data['articles'][index]['urlToImage']
        print("Image URL:", img_url)
        try:
            raw_data = urlopen(img_url).read()
            print("Image data retrieved successfully.")
        except Exception as e:
            print("Error retrieving image data:", e)
            return

        try:
            im = Image.open(io.BytesIO(raw_data)).resize((350,250))
            print("Image opened and resized successfully.")
        except Exception as e:
            print("Error opening or resizing image:", e)
            return

        photo = ImageTk.PhotoImage(im)

        label = Label(self.root, image=photo)
        label.image = photo  # Keep reference to the image object to prevent garbage collection
        label.pack()
        
        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='black', fg='white', wraplength=350, justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('Nunito Sans', 15))
         
        details = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white', wraplength=350, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('poppins', 12))
        
        frame = Frame(self.root, bg='black')
        frame.pack(expand=True, fill=BOTH)
        
        prev = Button(frame, text='BACK', width=16, height=3,command=lambda :self.load_news_item(index-1))
        prev.pack(side=LEFT)
        
        next = Button(frame, text='NEXT', width=16, height=3,command=lambda :self.load_news_item(index+1))
        next.pack(side=LEFT)
        
        read = Button(frame, text='Read in depth', width=16, height=3,command=lambda url=self.data['articles'][index]['url']: self.open_link(url))
        read.pack(side=LEFT)
        
        rate = Button(self.root, text='Rate this app', width=50, height=3, command=self.show_rating_page)
        rate.pack(pady=(20, 10))
        
    def open_link(self, url):
        webbrowser.open(url)
        
    def show_rating_page(self):
        rating_window = Toplevel(self.root)
        rating_window.geometry('300x200')
        rating_window.title('Rate this app')

        label = Label(rating_window, text="How would you rate this app?")
        label.pack(pady=10)

        rating_scale = Scale(rating_window, from_=1, to=5, orient=HORIZONTAL)
        rating_scale.pack(pady=10)

        submit_button = Button(rating_window, text="Submit", command=lambda: print("User Rating:", rating_scale.get()))
        submit_button.pack(pady=10)

if __name__ == "__main__":
    obj = NewsApp()
    obj.root.mainloop()
