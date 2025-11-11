from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
 
 

window = Tk()
 

window.title("Kullanıcı Giriş Ekranı")
 

 
window.geometry("390x220")
 

window.resizable(width=False, height=False)
 
 

 
# Hata mesajımızı bu Label'e yazdıracaz
L3 = Label(window)
L3.place(x=148,y=200)
 
def giris():
    # E1 ve E2 adlı Entry'e girilen değeri, get() fonksiyonuyla çekip sorguluyoruz. 
    if (E1.get() == str("mami")) and (E2.get() == str("1234")):
        L3['text'] = ("Giriş Başarılı...") 
        messagebox.showinfo("Başlık", "Giriş Başarılı")
        print("başarılı")
    else:
        L3['text'] = ("Hatalı Giriş !")
        messagebox.showerror("Hata Başlık", "Hatalı Giriş")
 
L1 = Label(window, text="Kullanıcı Adı")
L1.place(x=75, y=15)
 
E1 = Entry(window, width=25)
E1.place(x=77,y=45)
 
L2 = Label(window, text="Şifre")
L2.place(x=75, y=80)
 
E2 = Entry(window, textvariable=StringVar(),show='*', width=25)
E2.place(x=77, y=110)
 
bt = Button(window, text="Giriş Yap", padx="20",pady="5", command=giris)
bt.place(x=75,y=150)
 
window.mainloop()