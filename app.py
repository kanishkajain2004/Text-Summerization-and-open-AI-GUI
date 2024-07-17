#core packages
import tkinter as tk 
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import *
import tkinter.filedialog
# import os
import openai
import PyPDF2
#other pkgs
import time
timestr=time.strftime("%Y%M%D-%H%M%S")

#NLP pkg
from spacy_summerization import text_summarizer
from nltk_summerization import nltk_summarizer

#web scrapping pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

window=tk.Tk()
window.title("SUMMARIZER GUI")
window.geometry('1000x900')
window.config(background='darkblue')



#style
style=ttk.Style(window)
style.configure('lefttab.TNotebook',tabposition='wn')
#Tabs
tab_control=ttk.Notebook(window,style='centertab.TNotebook')

tab1=ttk.Frame(tab_control)
tab2=ttk.Frame(tab_control)
tab3=ttk.Frame(tab_control)
tab4=ttk.Frame(tab_control)
tab5=ttk.Frame(tab_control)

#add tabs to Notebook
tab_control.add(tab1,text=f'{"Home":^20s}')
tab_control.add(tab2,text=f'{"File":^30s}')
tab_control.add(tab3,text=f'{"URL":^25s}')
tab_control.add(tab4,text=f'{"Chatbot":^20s}')
tab_control.add(tab5,text=f'{"Pdf":^25s}')

#Lables
label1=Label(tab1,text='Summarizer',padx=5,pady=5, background='darkblue', fg='white', font=("arial", 15),borderwidth=2,relief="solid")
label1.grid(column=0,row=0)
label2=Label(tab2,text='File Processing',padx=5,pady=5, background='darkblue', fg='white', font=("arial", 15),borderwidth=2,relief="solid")
label2.grid(column=0,row=0)
label3=Label(tab3,text='URL',padx=5,pady=5, background='darkblue', fg='white', font=("arial", 15),borderwidth=2,relief="solid")
label3.grid(column=0,row=0)
label4=Label(tab4,text='Chatbot',padx=5,pady=5, background='darkblue', fg='white', font=("arial", 15),borderwidth=2,relief="solid")
label4.grid(column=0,row=0)
label5=Label(tab5,text='PDF Summarizer',padx=5,pady=5, background='darkblue', fg='white', font=("arial", 15),borderwidth=2,relief="solid")
label5.grid(column=0,row=0)

tab_control.pack(expand=True,fill='both')

#functions
def get_summary():
    raw_text=entry.get('1.0',tk.END)
    final_text=text_summarizer(raw_text)
    print(final_text)
    result='\nSummary: {}'.format(final_text)
    tab1_display.insert(tk.END,result)

def save_summary():
    raw_text=entry.get('1.0',tk.END)
    final_text=text_summarizer(raw_text)
    #file_name= 'your summary'+ timestr +'.txt'
    
    with open('file_name.txt','w') as f:
        f.write(final_text)
    result='\nName of File: {},\nSummary: {}'.format('file_name.txt',final_text)
    tab1_display.insert(tk.END,result)

#clear function

def clear_text():
    entry.delete('1.0',END)
def clear_display_result():
    tab1_display.delete('1.0',END)

def clear_text_file():
    displayed_file.delete('1.0',END)
def clear_text_result():
    tab2_display_text.delete('1.0',END)

def clear_url_entry():
    url_entry.delete(0,END)
def clear_url_display():
    tab3_display_text.delete('1.0',END)
    
#open file function

def openfiles():
    file1=tkinter.filedialog.askopenfilename(filetype=(('Text Files',".txt"),("All files","*")))
    read_text=open(file1).read()
    displayed_file.insert(tk.END,read_text)
def get_file_summary():
    raw_text=displayed_file.get('1.0',tk.END)
    final_text=text_summarizer(raw_text)
    result='\nSummary: {}'.format(final_text)
    tab2_display_text.insert(tk.END,result)

#open pdf function
def openpdf():
    file_pdf=tkinter.filedialog.askopenfilename(filetype=(('PDF Files',".pdf"),("All files","*")))
    pdf_file = PyPDF2.PdfReader(file_pdf)
    for i in range(len(pdf_file.pages)):
        content = pdf_file.pages[i].extract_text()
        displayed_pdf.insert(tk.END,content)

def get_pdf_summary():
    raw_text=displayed_pdf.get('1.0',tk.END)
    final_text=text_summarizer(raw_text)
    result='\nSummary: {}'.format(final_text)
    tab5_display_text.insert(tk.END,result)   

#url function
#featch text from url

def get_text():
    raw_text=str(url_entry.get())
    page=urlopen(raw_text)
    soup=BeautifulSoup(page,'html')
    
    fetched_text= ' '.join(map(lambda p:p.text,soup.find_all('p')))
    url_display.insert(tk.END,fetched_text)

def get_url_summary():
    raw_text=url_display.get('1.0',tk.END)
    final_text=text_summarizer(raw_text)
    result='\nSummary: {}'.format(final_text)
    tab3_display_text.insert(tk.END,result)

# Chatbot functions
def generate():
    prompt= ent_qst.get()

    openai.api_key = "sk-proj-MlDxsPDsSuiuHaRbv4abT3BlbkFJWRjB2zWwFzBPukCQQfSW"

    response= openai.chat.completions.create(
        model= "gpt-3.5-turbo",
        messages=[
            {"role":"user", "content": prompt}
        ]
    )

    result = response.choices[0].message['content']
    txt_result.insert(1.0, result)

def clear():
    txt_result.delete(1.0, tk.END)


#main Home tab
l1=Label(tab1,text="Enter Text To Summarize", padx=5,pady=5, bg='white', fg='black')
l2=Label(tab1,text="Summerized Text", padx=5,pady=5, bg='white', fg='black')
l1.grid(column=0,row=1)
l2.grid(column=0,row=7)

entry = ScrolledText(tab1,height=10)
entry.grid(row=2,column=0,columnspan=2,padx=10,pady=10)


#buttons
button1=Button(tab1,text='Reset',command=clear_text,width=12,bg='blue',fg='white', font=("arial", 10))
button1.grid(row=4,column=0,pady=10,padx=10)
button2=Button(tab1,text='Summarizer',command=get_summary,width=12,bg='green',fg='white', font=("arial", 10))
button2.grid(row=4,column=1,pady=10,padx=10)
button3=Button(tab1,text='Clear Result',command=clear_display_result,width=12,bg='red',fg='white', font=("arial", 10))
button3.grid(row=6,column=0,pady=10,padx=10)
button4=Button(tab1,text='Save',command=save_summary,width=12,bg='yellow',fg='white', font=("arial", 10))
button4.grid(row=6,column=1,pady=10,padx=10)

#display screen for result
tab1_display=ScrolledText(tab1,height=10)
tab1_display.grid(row=8,column=0,columnspan=3,padx=5,pady=5)

#file processing tab
l1=Label(tab2,text="Open file to summarize", bg='black', fg='white', padx=5,pady=5)
l1.grid(row=1,column=0)

displayed_file=ScrolledText(tab2,height=10)
displayed_file.grid(row=2,column=0,columnspan=3,padx=5,pady=3)

#button for second tab reading tab

b0=Button(tab2,text="Open File", width=12,command=openfiles,bg="red",fg='white', font=("arial", 10))
b0.grid(row=3,column=0,padx=10,pady=10)
b1=Button(tab2,text="Reset", width=12,command=clear_text_file,bg="green",fg='white', font=("arial", 10))
b1.grid(row=3,column=1,padx=10,pady=10)
b2=Button(tab2,text="Summarize", width=12,command=get_file_summary,bg="pink",fg='white', font=("arial", 10))
b2.grid(row=3,column=2,padx=10,pady=10)
b3=Button(tab2,text="Clear_Result", width=12,command=clear_text_result,bg="blue",fg='white', font=("arial", 10))
b3.grid(row=5,column=1,padx=10,pady=10)
b4=Button(tab2,text="Close", width=12,command=window.destroy,bg='black',fg='white', font=("arial", 10))
b4.grid(row=5,column=2,padx=10,pady=10)

#display screen 
tab2_display_text=ScrolledText(tab2,height=10)
tab2_display_text.grid(row=7,column=0,columnspan=3,padx=5,pady=5)

#allows you to edit
tab2_display_text.config(state=NORMAL)


# PDF file processing tab
l1=Label(tab5,text="Open pdf to summarize", bg='black', fg='white', padx=5,pady=5)
l1.grid(row=1,column=0)

displayed_pdf=ScrolledText(tab5,height=10)
displayed_pdf.grid(row=2,column=0,columnspan=3,padx=5,pady=3)

#button for second tab reading tab

b0=Button(tab5,text="Open pdf File", width=12,command=openpdf,bg="red",fg='white', font=("arial", 10))
b0.grid(row=3,column=0,padx=10,pady=10)
# b1=Button(tab2,text="Reset", width=12,command=clear_text_file,bg="green")
# b1.grid(row=3,column=1,padx=10,pady=10)
b2=Button(tab5,text="Summarize", width=12,command=get_pdf_summary,bg="pink",fg='white', font=("arial", 10))
b2.grid(row=3,column=1,padx=10,pady=10)
b3=Button(tab5,text="Clear_Result", width=12,command=clear_text_result,bg="blue",fg='white', font=("arial", 10))
b3.grid(row=3,column=2,padx=10,pady=10)
b4=Button(tab5,text="Close", width=12,command=window.destroy,bg='black',fg='white', font=("arial", 10))
b4.grid(row=5,column=1,padx=10,pady=10)

#display screen 
tab5_display_text=ScrolledText(tab5,height=10)
tab5_display_text.grid(row=7,column=0,columnspan=3,padx=5,pady=5)

#allows you to edit
tab5_display_text.config(state=NORMAL)

#url tab
l1=Label(tab3,text="Enter URL To Summarize", bg='black', fg='white', padx=5,pady=5)
l1.grid(row=1,column=0)

raw_entry=StringVar()
url_entry=Entry(tab3,textvariable=raw_entry,width=50)
url_entry.grid(row=1,column=1)

#button
button1=Button(tab3,text="Reset",command=clear_url_entry,width=12,bg="green",fg="white", font=("arial", 10))
button1.grid(row=4,column=0,pady=10,padx=10)
button2=Button(tab3,text='Get Text',command=get_text,width=12,bg='purple',fg='white', font=("arial", 10))
button2.grid(row=4,column=1,pady=10,padx=10)
button3=Button(tab3,text='Clear Result',command=clear_url_display,width=12,bg='red',fg='white', font=("arial", 10))
button3.grid(row=5,column=0,pady=10,padx=10)
button4=Button(tab3,text='Summarize',command=get_url_summary,width=12,bg='pink',fg='white', font=("arial", 10))
button4.grid(row=5,column=1,pady=10,padx=10)


#chatbot tab
# lbl_head = tk.Label(tab4, text= "ChatGPT", font=("arial", 27))#, bg="black", fg="white"
# lbl_head.grid(row=1, column=0)

frm_result=tk.Frame(tab4)
scroll_bar= tk.Scrollbar(frm_result)
# scroll_bar.grid()

txt_result = ScrolledText(tab4,height=10)
txt_result.grid(row=2,column=0,columnspan=2,padx=10,pady=10)

frm_result.grid(padx=10, pady=5)

l1=Label(tab4,text="Enter Query")
l1.grid(row=3,column=0)

ent_qst=Entry(tab4,textvariable=raw_entry,width=50)
ent_qst.grid(row=3,column=1)

btn_gen = tk.Button(tab4, text="Generate", command=generate, width=12,bg='pink',fg='white') # font=("geogio", 15),
btn_gen.grid(row=4, column=0)

btn_clear = tk.Button(tab4, text="Clear", command=clear, width=12,bg='red',fg='white') #font=("geogio", 15), 
btn_clear.grid(row=4, column=1)

scroll_bar.config(command=txt_result.yview)

#display screen for result
url_display=ScrolledText(tab3,height=10)
url_display.grid(row=7,column=0,columnspan=3,padx=5,pady=5)

tab3_display_text=ScrolledText(tab3,height=10)
tab3_display_text.grid(row=10,column=0,columnspan=3,padx=5,pady=5)
window.mainloop()
