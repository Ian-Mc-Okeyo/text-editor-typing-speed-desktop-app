from tkinter import*
from tkinter import font
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pyttsx3
import threading
import sqlite3
import math
import string
from  matplotlib import pyplot as plt
from datetime import *
from random import randint

root = Tk()
root.title('N@ikr@m Text Editor')
root.config(bg='#696969')

#root.iconbitmap("/home/naikram/Downloads/icon.ico")

text = Text(root, height=37, width=166, bg='#F5F5F5', undo=True, selectforeground='black', selectbackground='blue', wrap=WORD)
text.grid(column=0, row=0, pady=5, padx=10)

# adding a scrollbar
scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=text.yview)
text.configure(yscroll=scrollbar.set)
scrollbar.grid(column=1, row=0, sticky='ns')

# status bar

status_bar = LabelFrame(root, bg='#A9A9A9', height=10)
status_bar.grid(column=0, row=1, sticky='we', padx=10)

number_of_words_label = Label(status_bar, text=f'Words: 0\t\tLine:1\tColumn:0', bg='#A9A9A9', fg='#FFFFFF')
number_of_words_label.pack(anchor=CENTER)

def count_words(event):
    words = text.get(1.0, END)
    words = words.replace('\n', ' ')
    word_number = 0
    for word in words.split(' '):
        if word !='':
            word_number+=1
    position = text.index(INSERT)
    position=position.split('.')

    number_of_words_label.config(text=f'Words: {word_number}\t\tLine:{position[0]}\tColumn:{position[1]}')

text.bind('<space>', count_words)
text.bind('<Motion>', count_words)
text.bind('<Key>', count_words)

main_menu = Menu(root, bg='#696969', fg='#FFFFFF')
root.config(menu=main_menu)

def open_text():
    global text
    global doc_dir
    doc_dir = filedialog.askopenfilename(initialdir='/home/naikram/Documents')
    text_file = open(doc_dir, 'r')
    doc = text_file.read()
    text.delete(1.0, END)
    text.insert(END, doc)

    text_file.close()
    title=doc_dir.split('/')[len(doc_dir.split('/'))-1]
    root.title(f'Text Editor_{title}')

def save(event):
    text_file = open(doc_dir, 'w')
    doc = text.get(1.0, END)
    text_file.write(doc)

    text_file.close()
    messagebox.showinfo(title='Info', message='Document is successfully Saved')
text.bind('<Control-s>', save)
text.bind('<Control-S>', save)

def save_as():
    global doc_dir
    directory = filedialog.asksaveasfile(initialdir='/home/naikram/Documents')
    doc_dir = directory.name
    title=doc_dir.split('/')[len(doc_dir.split('/'))-1]
    root.title(f'Text Editor_{title}')

file_menu = Menu(main_menu, bg='#696969', fg='#FFFFFF')
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=root.quit)
file_menu.add_command(label='Exit', command=root.quit)
file_menu.add_separator()
file_menu.add_command(label='Open', command=open_text)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Save', command=lambda:save(''))

#function to bolden text
def bold(event):
    bold_font = font.Font(text, text.cget('font'))
    bold_font.configure(weight='bold')
    text.tag_configure('bold', font=bold_font)

    current_tags = text.tag_names('sel.first')
    if 'bold' in current_tags:
        text.tag_remove('bold', 'sel.first', 'sel.last')
    else:
        text.tag_add('bold', 'sel.first', 'sel.last')

# function to italicise
def italics(event):
    italics_font = font.Font(text, text.cget('font'))
    italics_font.configure(slant='italic')
    text.tag_configure('italic', font=italics_font)
    current_tags = text.tag_names('sel.first')

    if 'italic' in current_tags:
        text.tag_remove('italic', 'sel.first', 'sel.last')
    else:
        text.tag_add('italic', 'sel.first', 'sel.last')

# function to underline text
def underline(event):
    underline = font.Font(text, text.cget('font'))
    underline.configure(underline=True)
    text.tag_configure('underline', font=underline)
    current_tags = text.tag_names('sel.first')

    if 'underline' in current_tags:
        text.tag_remove('underline', 'sel.first', 'sel.last')
    else:
        text.tag_add('underline', 'sel.first', 'sel.last')

# function to select all
def select_all(event):
    text.tag_add(SEL, '1.0', END)
    text.mark_set(INSERT, '1.0')
    text.see(INSERT)

edit_menu = Menu(main_menu, bg='#696969', fg='#FFFFFF')
main_menu.add_cascade(label='Edit', menu=edit_menu)

edit_menu.add_command(label='Copy', accelerator='Ctrl+c', command=lambda: root.focus_get().event_generate('<<Copy>>'))
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+x', command=lambda: root.focus_get().event_generate('<<Cut>>'))
edit_menu.add_separator()
edit_menu.add_command(label='Paste', accelerator = 'Ctrl+p', command=lambda: root.focus_get().event_generate('<<Paste>>'))
edit_menu.add_separator()
edit_menu.add_command(label='Undo', accelerator='Ctrl+y', command= text.edit_undo)
edit_menu.add_separator()
edit_menu.add_command(label='Redo', accelerator = 'Ctrl+y', command=text.edit_redo)
edit_menu.add_separator()

# select all
edit_menu.add_command(label='Select All', accelerator = 'Ctrl+a', command=lambda:select_all(''))
text.bind("<<Control-a>>", select_all)

# underline command
edit_menu.add_command(label='Underline', accelerator='Ctrl+u',  command=lambda:underline(''))
text.bind('<Control-u>', underline)

main_menu.add_command(label='Bold', command=lambda:bold(''))
main_menu.add_separator()
text.bind('<Control-b>', bold)
main_menu.add_command(label='Italics', command=lambda:italics(''))
# text.bind('<Control-i>', italics)

#function to speak
def speak():
    engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)
    # rate = engine.getProperty('rate')
    # engine.setProperty('rate', 150)
    engine.say(text.get(1.0, END))
    engine.runAndWait()

main_menu.add_command(label='Speak', command=speak)
def right_click(event):
    pop_menu = Menu(root, tearoff=2)
    pop_menu.add_command(label='Copy', accelerator='Ctrl+c', command=lambda: root.focus_get().event_generate('<<Copy>>'))
    pop_menu.add_separator()
    pop_menu.add_command(label='Cut', accelerator='Ctrl+x', command=lambda: root.focus_get().event_generate('<<Cut>>'))
    pop_menu.add_separator()
    pop_menu.add_command(label='Paste', accelerator='Ctrl+p', command=lambda: root.focus_get().event_generate('<<Paste>>'))
    pop_menu.add_separator()
    pop_menu.add_command(label='Redo', accelerator = 'Ctrl+y', command=text.edit_redo)

    try:
        pop_menu.tk_popup(event.x_root, event.y_root)
    finally:
        pop_menu.grab_release()

text.bind('<Button-3>', right_click)

# this section creates the more options menu

options_menu = Menu(main_menu)
main_menu.add_cascade(label='Options', menu=options_menu)

#creating the color menu
color_menu = Menu(options_menu, bg='#696969', fg='#FFFFFF')
options_menu.add_cascade(label='Background', menu=color_menu)

#commands to change the background colors
def background_color(color):
    text.config(background=color)

# adding commands to the color menu
color_menu.add_command(label='Blue', background='Blue', command=lambda:background_color('Blue'))
color_menu.add_command(label='Black', background='Black', foreground='White', command=lambda:background_color('Black'))
color_menu.add_command(label='Green', background='Green', command=lambda:background_color('Green'))
color_menu.add_command(label='Red', background='Red', command=lambda:background_color('Red'))
color_menu.add_command(label='White', background='White', command=lambda:background_color('White'))
color_menu.add_command(label='Yellow', background='Yellow', command=lambda:background_color('Yellow'))
color_menu.add_command(label='Cyan', background='Cyan', command=lambda:background_color('Cyan'))
color_menu.add_command(label='Magenta', background='Magenta', command=lambda:background_color('Magenta'))

font_menu = Menu(options_menu, bg='#696969', fg='#FFFFFF')
options_menu.add_cascade(label='Font', menu=font_menu)
font_menu.add_command(label='Helvetica', font=('Helvetica'))
font_menu.add_command(label='Times', font=('Times'))

#creating the font color menu
font_color_menu = Menu(options_menu)
options_menu.add_cascade(label='Font Color', menu=font_color_menu)

#creating the font color function
def foreground_color(color):
    text.config(foreground=color)

#creating the font color commands
font_color_menu.add_command(label='Blue', foreground='Blue', command=lambda:foreground_color('Blue'))
font_color_menu.add_command(label='Black', foreground='Black', command=lambda:foreground_color('Black'))
font_color_menu.add_command(label='Green', foreground='Green', command=lambda:foreground_color('Green'))
font_color_menu.add_command(label='Red', foreground='Red', command=lambda:foreground_color('Red'))
font_color_menu.add_command(label='Yellow', foreground='Yellow', command=lambda:foreground_color('Yellow'))
font_color_menu.add_command(label='Cyan', foreground='Cyan', command=lambda:foreground_color('Cyan'))
font_color_menu.add_command(label='Magenta', foreground='Magenta', command=lambda:foreground_color('Magenta'))

# creating the themes functions and commands
theme = Menu(options_menu, bg='#696969', fg='#FFFFFF')
options_menu.add_cascade(label='Theme', menu=theme)

def themes(color, fore):
    root.config(background=color)
    text.config(bg=color, fg='Black')
    main_menu.config(background=color, foreground=fore)
    options_menu.config(bg=color)
    edit_menu.config(bg=color)
    file_menu.config(bg=color)
    font_color_menu.config(bg=color)
    font_menu.config(bg=color)
    color_menu.config(bg=color)
    status_bar.config(bg=color, fg='Black')
    number_of_words_label.config(bg=color, fg='Black')


theme.add_command(label='Dark mode', background='Black', foreground='White', command=lambda:themes('#373737', 'White'))
theme.add_command(label='Light mode', background='White', foreground='Black', command=lambda:themes('White', 'Black'))

# This section develops the types test window and all its functionalities
options_menu.add_separator()
type_test = Menu(options_menu)
options_menu.add_cascade(label='Typing test', menu=type_test)

# creating the database for the users
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(First_name TEXT, Last_name TEXT, password TEXT, scores TEXT)')

conn.commit()
conn.close()

#creating the window for typing test
def type_test_window(f_name, l_name, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    top = Tk()
    top.config(bg ='#ADD8E6')
    top.title('Typing Speed')
    c.execute(f'SELECT * FROM users WHERE First_name="{f_name}" AND Last_name="{l_name}"')
    data = c.fetchall()

    global sp_values
    sp_values = data[0][3]
    # extracting the speed and accuracy data from the database
    global speedList
    speedList = []
    accList = []
    spAccData = sp_values.split('.')
    for data in spAccData:
        if data == '0' or data == '':
            continue
        d = data.split('/')
        speedList.append(int(d[0]))
        accList.append(int(d[1]))

    #calculating the average speed
    global average_sp
    total = 0
    for sp in speedList:
        total += sp
    if len(speedList)==0:
        average_sp = 0
    else:
        average_sp = round(total/len(speedList), 1)

    # calculating the average accuracy
    global aver_acc
    total = 0
    for acc in accList:
        total += acc
    if len(accList)==0:
        aver_acc = 0
    else:
        aver_acc = round(total/len(accList), 1)

    # typing test strings

    a = '''Most of the cat species have stripes on their fur as well as on their skin. It is actually true that similar to human fingerprints, the unique pattern of stripes on Tigers acts like their identity. Even if you shave off the fur of Tigers or house cats, you would still see the stripes. One of the most common knowledge to any wildlife lovers, wild animals enjoy a surprise kill but not as much as Tigers. Due to their stripe camouflage, they hide behind thick bushes and attack their victim from behind. It is also said that Tigers are less likely to attack when we see them, in fact, most of the villages in India wear a face mask on the back of their head just to trick the Tigers.'''
    b = '''A day is longer than a year on Venus. This one might sound completely out there. A day is how long it takes a planet to rotate fully, and a year is how long it takes a planet to orbit the Sun. Venus is one of only two planets that rotates clockwise, and it spins much slower than others in the solar system. Some think this is due to it being knocked into a different direction by another planet, or it just gradually slowed to a halt then started turning the other way. It takes 243 Earth days for Venus to do one complete rotation, and 225 Earth days to orbit the Sun. Therefore, a day is longer than a year on Venus.'''
    c = '''So far, scientists have found no evidence that life exists elsewhere in the solar system. But as we learn more about how "extreme" microbes live in underwater volcanic vents or in frozen environments, more possibilities open up for where they could live on other planets. These aren't the aliens people once feared lived on Mars, but microbial life in the solar system is a possibility. Microbial life is now considered so likely on Mars that scientists take special precautions to sterilize spacecraft before sending them over there. That's not the only place, though. With several icy moons scattered around the solar system, it's possible there are microbes somewhere in the oceans of Jupiter's Europa, or perhaps underneath the ice at Saturn's Enceladus, among other locations.'''
    d = '''An average Boeing 747 aircraft has over 150 miles (240 kilometers) of wires inside its body, or roughly the distance between Amsterdam and the south of Belgium. The longest wiring, however, that can be found in an airplane is in the double-decker plane Airbus A380 — its 320 miles of cables would stretch as far as Leicester to Glasgow. The windows on an airplane are round for a reason. After a series of accidents in the early days of commercial flying, the engineers uncovered that having square windows with sharp corners compromised the safety of the aircraft. On the other hand, round windows used since then can take the repeated pressure during a flight. Did you know that 80 percent of crashes occur in the first three minutes of a flight and the last eight minutes.'''
    e = '''The black box, also known as the Flight Data Recorder, is actually painted bright orange. The heat-resistant paint used to coat the boxes' exteriors comes in a highlighter-orange hue, which also happens to make them easier to find in case of an accident. The Boeing 747 burns about 1 gallon of fuel every second, or 5 gallons per mile. Reversing this gives us the figure of 0.2 miles per gallon of fuel. This is much lower than the average car's fuel efficiency at about 25 miles per gallon. But, considering the number of passengers the 747 carries, it is far more efficient. This breakdown explains that, because the plane can carry about 500 people, it's actually getting 100 miles per gallon per person.'''
    f = '''It’s important to remember that although the ocean produces at least 50 per cent of the oxygen on Earth, roughly the same amount is consumed by marine life. Like animals on land, marine animals use oxygen to breathe, and both plants and animals use oxygen for cellular respiration. Oxygen is also consumed when dead plants and animals decay in the ocean. This is particularly problematic when algal blooms die and the decomposition process uses oxygen faster than it can be replenished. This can create areas of extremely low oxygen concentrations, or hypoxia. These areas are often called dead zones, because the oxygen levels are too low to support most marine life. National Centers for Coastal Ocean Science conducts extensive research and forecasting on algal blooms and hypoxia to lessen the harm done to the ocean ecosystem and human environment.'''
    g = '''Scientists estimate that 50-80 per cent of the oxygen production on Earth comes from the ocean. The majority of this production is from oceanic plankton — drifting plants, algae, and some bacteria that can photosynthesize. One particular species, Prochlorococcus, is the smallest photosynthetic organism on Earth. But this little bacteria produces up to 20 per cent of the oxygen in our entire biosphere. That’s a higher percentage than all of the tropical rain forests on land combined. Calculating the exact percentage of oxygen produced in the ocean is difficult because the amounts are constantly changing. Scientists can use satellite imagery to track photosynthesizing plankton and estimate the amount of photosynthesis occurring in the ocean, but satellite imagery cannot tell the whole story. The amount of plankton changes seasonally and in response to changes in the water’s nutrient load, temperature, and other factors. Studies have shown that the amount of oxygen in specific locations varies with time of day and with the tides'''
    h = '''Researchers have suggested that Hitler suffered from a number of diseases including- Parkinson’s disease. Some described him as a neurotic psychopath. Parkinson’s disease is a degenerative disorder of the central nervous system that affects the movement, memory pattern, thinking and behavior of the patient. It is reported that for the last 11 years of his life, Hitler suffered from mental and physical symptoms of the Parkinson’s disease. Some historians argued that his decision making was affected during WWII due to his possible dementia or memory loss as a result of the disease.'''
    j = '''As a result of the Holocaust engineered by Hitler and his Nazi regime, 6 million Jews or around 78 per cent of the total Jewish population (around 7.3 million) in Nazi occupied Europe at that time and an additional 5 million non-Jewish people were killed. From 1941 to 1945, Jews and other racial, political and ethnic minorities in Europe were targeted and systematically murdered by the Nazi forces.'''
    k = '''Adolf Hitler, one of the worst dictators ever if not the worst in recorded human history, was responsible for 60 to 85 million deaths during the WWII as he had triggered the conflict. His name brings connotations of murder, misery, warfare, holocaust and the attempted extermination of the Jews and other minorities. Hitler openly expressed his hatred of Jews in his book ‘Mein Kampf’. He warned everyone about his intention to drive the Jews and minorities from Germany’s cultural, intellectual and cultural life. Before invading Poland and triggering the WWII, Hitler gave example of Genghis Khan to his generals. He said that though Genghis Khan happily led millions of women and children to slaughter with predetermination, history still considered him solely the founder of the Mongol state; not as a murderer.'''
    l = '''In 323 B.C. Alexander the Great fell ill after downing a bowl of wine at a party. Two weeks later, the 32-year-old ruler was dead. Given that Alexander’s father had been murdered by his own bodyguard, suspicion fell on those surrounding Alexander, most notably his general Antipater and Antipater’s son Cassander (who would eventually order the murders of Alexander’s widow and son). Some ancient biographers even speculated that Aristotle, who had connections with Antipater’s family, may have been involved. In modern times, medical experts have speculated that malaria, lung infection, liver failure or typhoid fever may have done Alexander in.'''
    m = '''Plutarch’s “Lives of the Noble Greeks and Romans,” written 400 years after Alexander’s death, reports that “a most agreeable odor” exuded from Alexander’s skin, and that “his breath and body all over was so fragrant as to perfume the clothes which he wore.” The olfactory detail was part of a tradition, begun during Alexander’s lifetime, of ascribing godlike attributes to the conquering king. Alexander himself openly called himself Son of Zeus during a visit to Siwah in 331 B.C. '''
    n = '''Alexander the Great’s military tactics and strategies are still studied in military academies today. From his first victory at age 18, Alexander gained a reputation of leading his men to battle with impressive speed, allowing smaller forces to reach and break the enemy lines before his foes were ready. After securing his kingdom in Greece, in 334 B.C. Alexander crossed into Asia (present-day Turkey) where he won a series of battles with the Persians under Darius III. The centerpiece of Alexander’s fighting force was the 15,000-strong Macedonian phalanx, whose units held off the sword-wielding Persians with 20-foot-long pikes called sarissa.'''
    p = '''Alexander’s father, Philip II of Macedon, hired Aristotle, one of history’s greatest philosophers, to educate the 13-year-old prince. Little is known about Alexander’s three-year tutelage but presumably by the end of it Aristotle’s wise but worldly approach had sunk in. According to legend, while still a prince in Greece, Alexander sought out the famed ascetic Diogenes the Cynic, who rejected social niceties and slept in a large clay jar. Alexander approached the thinker in a public plaza, asking Diogenes if there was anything he in his great riches could do for him. “Yes,” Diogenes replied, “stand aside; you’re blocking my sun.” Alexander was charmed by Diogenes’ refusal to be impressed, stating, “If I were not Alexander, I would be Diogenes.” Years later, in India, Alexander paused his military conquests to have lengthy discussions with the gymnosophists, “naked philosophers” from the Hindu or Jain religions who eschewed human vanity and clothing.'''


    # appending the string items into the list
    words_list = []
    words_list.extend((a,b,c,d,e,f,g,h,j,k,l,m,n,p))

    #creating the window's design interface
    name_label = Label(top, text='Name: ', font=('Helvetica', 15), bg='#ADD8E6')
    name_label.grid(column=0, row=0)
    name_label1 = Label(top, text=f'{f_name} {l_name}', font=('Helvetica', 15), bg='#ADD8E6')
    name_label1.grid(column=1, row=0)

    av_sp = Label(top, text='Avrg Speed: ', font=('Helvetica', 15), bg='#ADD8E6')
    av_sp.grid(column=0, row=1)
    av_sp1 = Label(top, text=f'{average_sp} W/min', font=('Helvetica', 15), bg='#ADD8E6')
    av_sp1.grid(column=1, row=1)

    av_ac = Label(top, text='Avrg Accuracy: ', font=('Helvetica', 15),bg='#ADD8E6')
    av_ac.grid(column=0, row=2)
    av_ac1 = Label(top, text=f'{aver_acc}%', font=('Helvetica', 15), bg='#ADD8E6')
    av_ac1.grid(column=1, row=2)

    texbox1 = Text(top, height=15, width=160, wrap=WORD, background='#E6E6FA')
    texbox1.grid(column=0, row=3, padx=10, pady=5, columnspan=3)

    texbox2 = Text(top, height=15, width=160, wrap=WORD, background='#E6E6FA')
    texbox2.grid(column=0, row=4, padx=10, pady=5, columnspan=3)

    def graph():
        x = []
        for n in range(len(speedList)):
            x.append(n+1)
        plt.grid(True)
        plt.plot(x,speedList)
        plt.title('Typing Progress')
        plt.xlabel('Number of Trials')
        plt.ylabel('Scores')
        plt.show()

    progress_btn = Button(top, text = 'Show Progress', command=graph, bg='#87CEEB', fg='#0000CD')
    progress_btn.grid(column=0, row=5)

    speed_label = Label(top, text='', font=('Helvetica', 15), bg='#ADD8E6')
    speed_label.grid(column=2, row=0)

    acc_label = Label(top, text='', font=('Helvetica', 15), bg='#ADD8E6')
    acc_label.grid(column=2, row=1)

    time_label = Label(top, text='', fg='#8B0000', font=('Helvetica', 15), bg='#ADD8E6')
    time_label.grid(column=2, row=2)
    global time_count
    global finish
    time_count = 0
    finish = True

    def update_time():
        global time_count
        global finish
        global sp_values
        global aver_acc
        global average_sp
        global speedList
        time_count+=1
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        if finish:
            time_label.config(text=f'Time: {str(time_count)}')
            time_label.after(1000, update_time)
        else:
            str_text1 = texbox1.get(1.0, END)
            str_text2 = texbox2.get(1.0, END)
            len_text1 = len(str_text1.translate(str.maketrans('', '', string.whitespace)))
            len_text2 = len(str_text2.translate(str.maketrans('', '', string.whitespace)))
            len_dffrnce = len_text1-len_text2
            if len_dffrnce >60:
                messagebox.showerror(title = 'Cheating Detected!', message='A large number of words you have typed do not match with the given test!')
            else:
                # calculating the average speed and accuracy
                acc = 0
                split_text1 = str_text1.split(' ')
                split_text2 = str_text2.split(' ')
                for x in range (min(len(split_text1), len(split_text2))):
                    if split_text1[x] == split_text2[x]:
                        acc+=1
                accuracy = round(acc/len(split_text1)*100, 0) # calculating the accuracy
                # updating the average accuracy labeling to reflect the current results
                if aver_acc == 0: # if the original average accuracy is 0(a new user), then the average accuracy becomes the dubut results
                    aver_acc = accuracy
                else: # if this is not a new user, we compute the new average accuracy
                    aver_acc = (aver_acc+accuracy)/2
                av_ac1.config(text=f'{aver_acc}%')
                acc_label.config(text=f'Acc: {accuracy}%')

                speed = math.trunc(round(len(split_text2)/(time_count/60), 0)) # calculating the speed
                # updating the average speed labeling to reflect the current results
                if average_sp == 0: # if the original average speed is 0(a new user), then the average speed becomes the dubut results
                    average_sp = speed
                else: # if this is not a new user, we compute the new average speed
                    average_sp = (average_sp+speed)/2
                av_sp1.config(text=f'{average_sp} W/min')
                speed_label.config(text=f'Speed: {speed} w/min')
                speedList.append(average_sp)
                
                sp_values += str(speed) + '/'+ str(accuracy)+'.'
                c.execute(f'UPDATE users SET scores="{sp_values}" WHERE First_name="{f_name}" AND Last_name="{l_name}"')
            time_count = 0
            conn.commit()
            conn.close()


    def take_test():
        global time_label
        global finish
        finish = True
        y = randint(0, 13)
        texbox1.config(state='normal')
        texbox1.delete(1.0, END)
        texbox2.delete(1.0, END)
        texbox1.insert(END, words_list[y])
        texbox1.config(state='disabled')
        test_btn.config(state='disabled')
        speed_label.config(text='')
        acc_label.config(text='')
        finish_btn.config(state='normal')
        update_time()
        
    test_btn = Button(top, text='Start Typing Test', command=take_test, anchor='w', bg='#87CEEB', fg='#0000CD')
    test_btn.grid(column=1, row=5)

    def finished():
        global finish
        test_btn.config(state='normal')
        finish_btn.config(state='disabled')
        finish = False

    finish_btn = Button(top, text='Submit when finished', command=finished, anchor='e', state='disabled', bg='#87CEEB', fg='#0000CD')
    finish_btn.grid(column=2, row=5)

    top_menu = Menu(top, bg='#87CEEB')
    top.config(menu=top_menu)

    menu1 = Menu(top_menu, background='#E6E6FA', fg='black')
    top_menu.add_cascade(label='Main', menu=menu1)


    def change_details():
        window = Tk()
        window.resizable(False, False)
        window.config(background='#E6E6FA')
        window.title('Enter Your Password to continue')
        window.geometry('400x150')
        window.resizable(False, False)
        pass_label = Label(window, text='Enter Password: ', background='#E6E6FA')
        pass_label.grid(column=0, row=0, pady=10)
        pass_entry = Entry(window, font=('Helvetica', 15), show='*')
        pass_entry.grid(column=1, row=0, pady=10)

        def ok():
            if pass_entry.get() == password:
                window.destroy()
                change_window=Tk()
                change_window.resizable(False, False)
                change_window.config(background='#E6E6FA')
                change_window.title('Change details')
                change_window.geometry('500x250')

                first_name_label = Label(change_window, text='First Name: ', background='#E6E6FA')
                first_name_label.grid(column=0, row=0, pady=5)
                last_name_label = Label(change_window, text='Last Name: ', background='#E6E6FA')
                last_name_label.grid(column=0, row=1)
                password_label = Label(change_window, text='Password:', background='#E6E6FA')
                password_label.grid(column=0, row=2, pady=5)
                confirm_pass = Label(change_window, text='Confirm Password: ', background='#E6E6FA')
                confirm_pass.grid(column=0, row=3)

                first_name_entry = Entry(change_window, width=30, font=('Helvetica', 15))
                first_name_entry.grid(column=1, row=0, pady=5, columnspan=2)
                last_name_entry = Entry(change_window, width=30, font=('Helvetica', 15))
                last_name_entry.grid(column=1, row=1, columnspan=2)
                password_entry = Entry(change_window, width=30, font=('Helvetica', 15), show='*')
                password_entry.grid(column=1, row=2, pady=5, columnspan=2)
                confirm_pass_entry = Entry(change_window, width=30, font=('Helvetica', 15), show='*')
                confirm_pass_entry.grid(column=1, row=3, columnspan=2)

                first_name_entry.insert(0, f_name)
                last_name_entry.insert(0, l_name)
                password_entry.insert(0, password)

                cancel_button = Button(change_window, text='Cancel', fg='#FF0000', bg='#FA8072', anchor='e', command=change_window.destroy)
                cancel_button.grid(column=1, row=4, pady=10)

                def change():
                    conn = sqlite3.connect("users.db")
                    c = conn.cursor()
                    c.execute("""UPDATE users SET 
                            First_name = :first,
                            Last_name = :last,
                            password = :pass
                            WHERE First_name = :f AND Last_name=:l""",
                            {
                                'first': first_name_entry.get(),
                                'last': last_name_entry.get(),
                                'pass': password_entry.get(),
                                'f': f_name,
                                'l': l_name
                            }
                            )
                    conn.commit()
                    conn.close()
                    name_label1.config(text=f'{first_name_entry.get()} {last_name_entry.get()}')
                    change_window.destroy()

                change_button = Button(change_window, text='Confirm', fg='#00008B', bg='#6495ED', anchor='e', command=change)
                change_button.grid(column=2, row=4, pady=10,)

                change_window.mainloop()
            else:
                messagebox.showerror(title='ERROR!', message='Wrong Password. Try Again')
                window.destroy()

        confirm_btn = Button(window, text='OK', fg='#00008B', bg='#6495ED', anchor='e', command=ok)
        confirm_btn.grid(column=1, row=1)

        cancel_btn = Button(window, text='Cancel',fg='#FF0000', bg='#FA8072', anchor='e', command=window.destroy)
        cancel_btn.grid(column=0, row=1)

        window.mainloop()

    menu1.add_command(label='Change details', command=change_details)
    menu1.add_command(label = 'Log Out', command=top.destroy)
    menu1.add_command(label='Exit', command=top.destroy)

    def delete_acc():
        window = Tk()
        window.resizable(False, False)
        window.config(background='#E6E6FA')
        window.title('Delete Account')
        window.geometry('400x150')
        window.resizable(False, False)
        pass_label = Label(window, text='Enter Password: ', background='#E6E6FA')
        pass_label.grid(column=0, row=0, pady=10)
        pass_entry = Entry(window, font=('Helvetica', 15), show='*')
        pass_entry.grid(column=1, row=0, pady=10)

        def confirm_pass():
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            if pass_entry.get()==password:
                c.execute(f'DELETE FROM users WHERE First_name="{f_name}" AND Last_name="{l_name}"')
                top.destroy()
                messagebox.showinfo(title='', message='Account deleted')
            else:
                messagebox.showerror(title='ERROR!', message='Wrong Password. Try Again')
                window.destroy
            conn.commit()
            conn.close()
            window.destroy()
        
        confirm_btn = Button(window, text='Confirm', fg='#00008B', bg='#6495ED', anchor='e', command=confirm_pass)
        confirm_btn.grid(column=1, row=1)

        cancel_btn = Button(window, text='Cancel',fg='#FF0000', bg='#FA8072', anchor='e', command=window.destroy)
        cancel_btn.grid(column=0, row=1)

        window.mainloop()
    menu1.add_command(label='Delete Account', command=delete_acc)

    options = Menu(top_menu, bg='#E6E6FA', fg='black')
    top_menu.add_cascade(label='Options', menu=options)

    font_size = Menu(options)
    options.add_cascade(label='Font size', menu=font_size)

    fore_ground = Menu(options)
    options.add_cascade(label='Font Color', menu=fore_ground)

    def fore_g(color):
        texbox1.config(foreground=color)
        texbox2.config(foreground=color)

    fore_ground.add_command(label='Black', foreground='Black', command=lambda:fore_g('Black'))
    fore_ground.add_command(label='Blue', foreground='Blue', command=lambda:fore_g('Blue'))
    fore_ground.add_command(label='Red', foreground='Red', command=lambda:fore_g('Red'))
    fore_ground.add_command(label='Green', foreground='Green', command=lambda:fore_g('Green'))
    fore_ground.add_command(label='Yellow', foreground='Yellow', command=lambda:fore_g('Yellow'))
    fore_ground.add_command(label='Cyan', foreground='Cyan', command=lambda:fore_g('Cyan'))
    fore_ground.add_command(label='Magenta', foreground='Magenta', command=lambda:fore_g('Magenta'))

    back_ground = Menu(options)
    options.add_cascade(label='Background', menu=back_ground)

    def back_g(color):
        texbox1.config(background=color)
        texbox2.config(background=color)

    back_ground.add_command(label='Black', foreground='White', background='Black', command=lambda:back_g('Black'))
    back_ground.add_command(label='Blue', foreground='Black', background='Blue', command=lambda:back_g('Blue'))
    back_ground.add_command(label='Red', foreground='Black', background='Red', command=lambda:back_g('Red'))
    back_ground.add_command(label='Green', foreground='Black', background='Green', command=lambda:back_g('Green'))
    back_ground.add_command(label='Yellow', foreground='Black', background='Yellow', command=lambda:back_g('Yellow'))
    back_ground.add_command(label='Cyan', foreground='Black', background='Cyan', command=lambda:back_g('Cyan'))
    back_ground.add_command(label='Magenta', foreground='Black', background='Magenta', command=lambda:back_g('Magenta'))

    options.add_separator()
    theme1 = Menu(options)
    options.add_cascade(label='Themes', menu=theme1)

    def theme_1(color, fore):
        top.config(background=color)
        texbox1.config(background=color, fg='Black')
        texbox2.config(background=color, fg='Black')
        menu1.config(background=color, fg=fore)
        options.config(background=color, fg=fore)
        top_menu.config(background=color, fg=fore)
        fore_ground.config(background=color, fg=fore)
        back_ground.config(background=color, fg=fore)
        name_label.config(background=color)
        name_label1.config(background=color)
        av_ac.config(background=color)
        av_ac1.config(background=color)
        av_sp.config(background=color)
        av_sp1.config(background=color)
        progress_btn.config(background=color, fg=fore)
        test_btn.config(background=color, fg=fore)
        finish_btn.config(background=color, fg=fore)
        speed_label.config(background=color)
        acc_label.config(background=color)
        time_label.config(background=color)
        if color=='#373737':
            plt.style.use('dark_background')
            plt.grid(True)
        else:
            plt.style.use('fivethirtyeight')
            plt.grid(True)
    
    def default_theme():
        top.config(background='#ADD8E6')
        texbox1.config(background='#E6E6FA')
        texbox2.config(background='#E6E6FA')
        top_menu.config(background='#87CEEB', fg='black')
        menu1.config(background='#E6E6FA', fg='black')
        options.config(bg='#E6E6FA', fg='black')
        finish_btn.config(bg='#87CEEB', fg='#0000CD')
        progress_btn.config(bg='#87CEEB', fg='#0000CD')
        test_btn.config(bg='#87CEEB', fg='#0000CD')
        name_label.config(background='#ADD8E6')
        name_label1.config(background='#ADD8E6')
        av_ac.config(background='#ADD8E6')
        av_ac1.config(background='#ADD8E6')
        av_sp.config(background='#ADD8E6')
        av_sp1.config(background='#ADD8E6')
        speed_label.config(background='#ADD8E6')
        acc_label.config(background='#ADD8E6')
        time_label.config(background='#ADD8E6')
        plt.style.use('fivethirtyeight')

    theme1.add_command(label='Dark', foreground='White', background='Black', command=lambda:theme_1('#373737', 'White'))
    theme1.add_command(label='Light', foreground='Black', background='White', command=lambda:theme_1('White', 'Black'))
    theme1.add_command(label='Default', foreground='Black', background='White', command=default_theme)
    conn.commit()
    conn.close()

    #rankinig the user
    rank = 'BEGINNER *'
    rank_color = '#A0522D'
    if average_sp <=25 :
        rank='BEGINNER *'
        rank_color = '#A0522D'
    elif average_sp >25 and average_sp <=40:
        rank='ARMATURE **'
        rank_color = '#FF00FF'
    elif average_sp > 40 and average_sp <=70:
        rank = 'SEMI-PRO ***'
        rank_color = '#0000CD'
    elif average_sp > 70 and average_sp <= 100:
        rank = 'PRO ****'
        rank_color = '#00FF00'
    elif average_sp > 100:
        rank = 'WORLD CLASS *****'
        rank_color = '#FFFF00'

    top_menu.add_cascade(label=f'                                                                           {rank} LEVEL', font=('Helvetica', 15), foreground=rank_color)

    top.rowconfigure(0, weight=1)
    top.rowconfigure(1, weight=1)
    top.rowconfigure(2, weight=1)
    top.rowconfigure(3, weight=1)
    top.rowconfigure(4, weight=1)
    top.rowconfigure(5, weight=1)

    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)
    top.columnconfigure(2, weight=1)
    top.columnconfigure(3, weight=1)

    top.mainloop()

def login():
    log_in_window=Tk()
    log_in_window.resizable(False, False)
    log_in_window.config(background='#E6E6FA')
    log_in_window.title('Log In')
    log_in_window.geometry('500x240')

    first_name_label = Label(log_in_window, text='First Name: ', background='#E6E6FA')
    first_name_label.grid(column=0, row=0, pady=5)
    last_name_label = Label(log_in_window, text='Last Name: ', background='#E6E6FA')
    last_name_label.grid(column=0, row=1)
    password_label = Label(log_in_window, text='Password:', background='#E6E6FA')
    password_label.grid(column=0, row=2, pady=5)

    first_name_entry = Entry(log_in_window, width=30, font=('Helvetica', 15))
    first_name_entry.grid(column=1, row=0, pady=5, columnspan=2)
    last_name_entry = Entry(log_in_window, width=30, font=('Helvetica', 15))
    last_name_entry.grid(column=1, row=1, columnspan=2)
    password_entry = Entry(log_in_window, width=30, font=('Helvetica', 15), show='*')
    password_entry.grid(column=1, row=2, pady=5, columnspan=2)

    cancel_button = Button(log_in_window, text='Cancel', fg='#FF0000', bg='#FA8072', anchor='e', command=log_in_window.destroy)
    cancel_button.grid(column=1, row=3, pady=10)

    def log_in(e):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute('SELECT * FROM users')
        data = c.fetchall()
        print(data)

        info = (str(first_name_entry.get()), str(last_name_entry.get()), password_entry.get())
        new_data = []
        for user in data:
            new_user = list(user)
            new_user.pop()
            new_data.insert(0, tuple(new_user))
        if info in new_data:
            a,b,d = first_name_entry.get(), last_name_entry.get(), password_entry.get()
            log_in_window.destroy()
            type_test_window(a, b, d)
        else:
            log_in_window.destroy()
            messagebox.showerror(title='', message='Wrong user name or password')

        conn.commit()
        conn.close()

    log_in_button = Button(log_in_window, text='Login In', fg='#00008B', bg='#6495ED', anchor='e', command=lambda:log_in(''))
    log_in_button.grid(column=2, row=3, pady=10,)
    log_in_window.bind('<Return>', log_in)

    log_in_window.mainloop()

def sign_in():
    sign_in_window=Tk()
    sign_in_window.resizable(False, False)
    sign_in_window.config(background='#E6E6FA')
    sign_in_window.title('Sign In')
    sign_in_window.geometry('500x250')

    first_name_label = Label(sign_in_window, text='First Name: ', background='#E6E6FA')
    first_name_label.grid(column=0, row=0, pady=5)
    last_name_label = Label(sign_in_window, text='Last Name: ', background='#E6E6FA')
    last_name_label.grid(column=0, row=1)
    password_label = Label(sign_in_window, text='Password:', background='#E6E6FA')
    password_label.grid(column=0, row=2, pady=5)
    confirm_pass = Label(sign_in_window, text='Confirm Password: ', background='#E6E6FA')
    confirm_pass.grid(column=0, row=3)

    first_name_entry = Entry(sign_in_window, width=30, font=('Helvetica', 15))
    first_name_entry.grid(column=1, row=0, pady=5, columnspan=2)
    last_name_entry = Entry(sign_in_window, width=30, font=('Helvetica', 15))
    last_name_entry.grid(column=1, row=1, columnspan=2)
    password_entry = Entry(sign_in_window, width=30, font=('Helvetica', 15), show='*')
    password_entry.grid(column=1, row=2, pady=5, columnspan=2)
    confirm_pass_entry = Entry(sign_in_window, width=30, font=('Helvetica', 15), show='*')
    confirm_pass_entry.grid(column=1, row=3, columnspan=2)

    cancel_button = Button(sign_in_window, text='Cancel', fg='#FF0000', bg='#FA8072', anchor='e', command=sign_in_window.destroy)
    cancel_button.grid(column=1, row=4, pady=10)

    def sign_in_btn():
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        #restricting the program not to allow null values
        if password_entry.get=='' or first_name_entry.get()=='' or last_name_entry.get()=='':
            messagebox.showerror(title='Credentials Error', message='Null values cannot be used as user data')
        #checking if password matches the confirmation password
        elif password_entry.get()==confirm_pass_entry.get():
            #checking if the user names already exist in the database to avoid duplicates
            c.execute('SELECT * FROM users')
            data = c.fetchall()
            info  = (str(first_name_entry.get()), str(last_name_entry.get()))
            new_data = []
            for user in data:
                new_user = list(user)
                new_user.pop()
                new_user.pop()
                new_data.insert(0, tuple(new_user))
            if info in new_data:
                messagebox.showerror(title='', message='Sorry the a user already exists with similar first and last name')
            else:
                c.execute("INSERT INTO users VALUES(:f_name, :l_name, :pass, :score)",
                    {
                        'f_name': str(first_name_entry.get()),
                        'l_name': str(last_name_entry.get()),
                        'pass': str(password_entry.get()),
                        'score': '0.'
                    })
                conn.commit()
                a,b,d = first_name_entry.get(), last_name_entry.get(), password_entry.get()
                sign_in_window.destroy()
                type_test_window(a, b, d)
        else:
            messagebox.showerror(title='Error!', message='The password does not match the confirmation password you have entered')
        conn.commit()
        conn.close()

    sign_in_button = Button(sign_in_window, text='Sign In', fg='#00008B', bg='#6495ED', anchor='e', command=sign_in_btn)
    sign_in_button.grid(column=2, row=4, pady=10,)

    sign_in_window.mainloop()

type_test.add_command(label='Log in', command=login)
type_test.add_command(label='Sign in', command=sign_in)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

root.mainloop()