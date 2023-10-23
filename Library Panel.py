import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
from tkinter import CENTER
import datetime
import re

class GirisPaneli(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Library Management System")

        # Kullanıcı adı etiketi ve metin kutusu
        self.id_label = tk.Label(self.master, text="Username:")
        self.id_label.pack()

        self.id_entry = tk.Entry(self.master)
        self.id_entry.pack()

        # Şifre etiketi ve metin kutusu
        self.parola_label = tk.Label(self.master, text="Password:")
        self.parola_label.pack()

        self.parola_entry = tk.Entry(self.master, show="*")
        self.parola_entry.pack()

        # Giriş düğmesi
        self.giris_dugmesi = tk.Button(self.master, text="Log In", command=self.giris_yap)
        self.giris_dugmesi.pack()

        # Üye ol düğmesi
        self.uyeol_dugmesi = tk.Button(self.master, text="Sign Up", command=self.uye_ol)
        self.uyeol_dugmesi.pack(side=tk.BOTTOM, pady=10)

        # MySQL bağlantısı
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )

        self.center_window()

    def center_window(self):
        window_width = 400
        window_height = 300
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def giris_yap(self):
        id = self.id_entry.get()
        parola = self.parola_entry.get()

        # Boş alan kontrolü yap
        if not id or not parola:
            self.show_error_message("Please fill in the blank fields!")
            return

        try:
            # Veritabanında kullanıcıyı kontrol etmek için bir sorgu yapın
            cursor = self.conn.cursor()
            query = "SELECT * FROM kullanici WHERE id = %s AND parola = %s"
            cursor.execute(query, (id, parola))

            # Sorgu sonucunu alın
            result = cursor.fetchone()

            if result:
                kullanici_tipi = result[3]  # Kullanıcı tipi, admin mi yoksa öğrenci/öğretmen mi
                onay_durumu = result[4]  # Öğretmenin onay durumu
                if kullanici_tipi == "admin":
                    self.show_success_message("You are successfully logged in, welcome admin!")
                    self.master.withdraw()  # Giriş panelini gizle
                    admin_pencere = tk.Tk()
                    admin_paneli = AdminPaneli(admin_pencere, self)
                    admin_pencere.geometry("400x400")
                    admin_pencere.mainloop()
                elif kullanici_tipi == "ogrenci":
                    self.show_success_message("You are successfully logged in, welcome student!")
                    self.master.withdraw() # Giriş panelini gizle
                    ogrenci_pencere =tk.Tk()
                    ogrenci_paneli = OgrenciPaneli(ogrenci_pencere, self)
                    ogrenci_pencere.geometry("400x400")
                    ogrenci_pencere.mainloop()
                elif kullanici_tipi == "ogretmen":
                    if onay_durumu == 1:
                        self.show_success_message("You are successfully logged in, welcome teacher!")
                        self.master.withdraw() # Giriş panelini gizle
                        ogretmen_pencere =tk.Tk()
                        ogrenci_paneli = OgretmenPaneli(ogretmen_pencere, self)
                        ogretmen_pencere.geometry("400x400")
                        ogretmen_pencere.mainloop()
                    else:
                        self.show_error_message("After your membership is approved, you can log in.")
            else:
                self.show_error_message("Wrong username or password!")
            
            cursor.close()
        except mysql.connector.Error as err:
            self.show_error_message("Error: A problem occurred while querying the database.\nError message: " + str(err))

    def uye_ol(self):
        self.master.withdraw()  # Giriş panelini gizle
        uyeol_pencere = tk.Tk()
        uyeol_paneli = UyeOlPaneli(uyeol_pencere, self)
        uyeol_pencere.geometry("400x400")
        uyeol_pencere.mainloop()

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def show_success_message(self, message):
        messagebox.showinfo("Successful", message)


class UyeOlPaneli(tk.Frame):
    def __init__(self, master=None, previous_frame=None):
        super().__init__(master)
        self.master = master
        self.master.title("Sign Up")
        self.previous_frame = previous_frame

        # Kullanıcı adı etiketi ve metin kutusu
        self.id_label = tk.Label(self.master, text="Username:")
        self.id_label.pack()

        self.id_entry = tk.Entry(self.master)
        self.id_entry.pack()

        # E-posta etiketi ve metin kutusu
        self.eposta_label = tk.Label(self.master, text="E-mail:")
        self.eposta_label.pack()

        self.eposta_entry = tk.Entry(self.master)
        self.eposta_entry.pack()

        # Şifre etiketi ve metin kutusu
        self.parola_label = tk.Label(self.master, text="Password:")
        self.parola_label.pack()

        self.parola_entry = tk.Entry(self.master, show="*")
        self.parola_entry.pack()

        # Şifre tekrar etiketi ve metin kutusu
        self.parola_tekrar_label = tk.Label(self.master, text="Repeat Password:")
        self.parola_tekrar_label.pack()

        self.parola_tekrar_entry = tk.Entry(self.master, show="*")
        self.parola_tekrar_entry.pack()

        # Durum etiketi ve combobox
        self.durum_label = tk.Label(self.master, text="Status:")
        self.durum_label.pack()

        self.durum_var = tk.StringVar()
        self.durum_var.set("Student")

        self.durum_combobox = ttk.Combobox(self.master, textvariable=self.durum_var, state="readonly")
        self.durum_combobox['values'] = ("Student", "Teacher")
        self.durum_combobox.pack()

        self.durum_combobox.bind("<<ComboboxSelected>>", self.update_durum)  # Durum değiştiğinde update_durum metodu çağrılacak

        # Üye ol düğmesi
        self.uyeol_dugmesi = tk.Button(self.master, text="Sign Up", command=self.uye_ol)
        self.uyeol_dugmesi.pack()

        # Girişe Dön düğmesi
        self.girise_don_dugmesi = tk.Button(self.master, text="Log In", command=self.girise_don)
        self.girise_don_dugmesi.pack(side=tk.BOTTOM, pady=10)

        self.center_window()

    def update_durum(self, event):
        self.durum_var.set(self.durum_combobox.get())  # durum_var'ı güncelle


    def center_window(self):
        window_width = 400
        window_height = 400
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def uye_ol(self):
        id = self.id_entry.get()
        eposta = self.eposta_entry.get()
        parola = self.parola_entry.get()
        parola_tekrar = self.parola_tekrar_entry.get()
        durum = self.durum_var.get()

        # Boş alan kontrolü yap
        if not id or not eposta or not parola or not parola_tekrar:
            self.show_error_message("Please fill in the blank fields!")
            return

        # E-posta kontrolü yap
        if "@" not in eposta or "." not in eposta:
            self.show_error_message("Please enter a valid e-mail address!")
            return
        
        # Şifre kontrolü yap
        if parola != parola_tekrar:
            self.show_error_message("Passwords not match! Please check your password.")
            return


        if durum == "Student":
            durum = "ogrenci"
            onay_durumu = True
            
            try:
                # Veritabanına yeni bir kullanıcı ekleme sorgusu yapın
                cursor = self.previous_frame.conn.cursor()
                query = "INSERT INTO kullanici (id, eposta, parola, durum) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id, eposta, parola, durum))
                self.previous_frame.conn.commit()

                self.show_success_message("You have successfully registered! You will be redirected to the login page.")
                cursor.close()

                # Üye ol panelini kapatıp giriş panelini yeniden aç
                self.master.destroy()
                self.previous_frame.master.deiconify()
            
            except mysql.connector.Error as err:
                self.show_error_message("Error: A problem occurred while querying the database.\nError message: " + str(err))

        elif durum == "Teacher":
            durum = "ogretmen"
            onay_durumu = False  # Yeni eklenen satırın onay_durumu sütunu varsayılan olarak 0 (False) olacak

            try:
                # Veritabanına yeni bir kullanıcı ekleme sorgusu yapın
                cursor = self.previous_frame.conn.cursor()
                query = "INSERT INTO kullanici (id, eposta, parola, durum, onay_durumu) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (id, eposta, parola, durum, onay_durumu))
                self.previous_frame.conn.commit()

                self.show_success_message("You have successfully registered! After your membership is approved, you can log in.")
                cursor.close()

                # Üye ol panelini kapatıp giriş panelini yeniden aç
                self.master.destroy()
                self.previous_frame.master.deiconify()

            except mysql.connector.Error as err:
                self.show_error_message("Hata: Veritabanı sorgusu sırasında bir sorun oluştu.\nHata mesajı: " + str(err))

    def girise_don(self):
        self.master.destroy()  # Üye ol panelini kapat
        self.previous_frame.master.deiconify()  # Giriş panelini göster

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    def show_success_message(self, message):
        messagebox.showinfo("Successful", message)

class AdminPaneli(tk.Frame):
    def __init__(self, master=None, previous_frame=None, connection=None):
        super().__init__(master)
        self.master = master
        self.master.title("Admin Panel")
        self.previous_frame = previous_frame
        self.master = master
        self.master.title("Admin Panel")
        self.conn = connection

        # Kullanıcı Silme Butonu
        self.kullanici_silme_dugmesi = tk.Button(self.master, text="Delete User", command=self.kullanici_sil)
        self.kullanici_silme_dugmesi.pack()

        # Kitap Listeleme Butonu
        self.kitap_listeleme_dugmesi = tk.Button(self.master, text="List Books", command=self.kitaplari_listele)
        self.kitap_listeleme_dugmesi.pack()

        # Kitap Ekleme Butonu
        self.kitap_ekleme_dugmesi = tk.Button(self.master, text="Add Book", command=self.kitap_ekle)
        self.kitap_ekleme_dugmesi.pack()

        # Kullanımdaki Kitapları Görüntüleme Butonu
        self.kullanımdaki_kitaplar_dugmesi = tk.Button(self.master, text="View Books in Use", command=self.kullanımdaki_kitaplar)
        self.kullanımdaki_kitaplar_dugmesi.pack()

        # Öğretmen Onayı Butonu
        self.ogretmen_onayi_dugmesi = tk.Button(self.master, text="Teacher Approval / Approvals", command=self.ogretmen_onayi)
        self.ogretmen_onayi_dugmesi.pack()

        # Çıkış Yap Butonu
        self.girise_don_dugmesi = tk.Button(self.master, text="Log Out", command=self.girise_don)
        self.girise_don_dugmesi.pack(side=tk.BOTTOM, pady=10)

        self.center_window()

    def center_window(self):
        window_width = 400
        window_height = 400
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def open_new_window(self, title):
        new_window = tk.Toplevel(self.master)
        new_window.title(title)
        self.master.withdraw()
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(new_window))

        frame = tk.Frame(new_window)
        frame.pack(side=tk.BOTTOM, pady=10)

        back_button = tk.Button(frame, text="Return to Admin Panel", command=lambda: self.back_to_admin_panel(new_window))
        back_button.pack(side="bottom")

        return new_window

    def close_window(self, window):
        window.destroy()
        self.master.deiconify()

    def back_to_admin_panel(self, window):
        window.destroy()
        self.master.deiconify()

    def girise_don(self):
        tk.messagebox.showinfo("Logged Out", "Successfully logged out.")  # Çıkış yapıldığında mesaj ver
        self.master.destroy()  # Üye ol panelini kapat        
        self.previous_frame.master.deiconify()  # Giriş panelini göster

    def kullanici_sil(self):
        silme_penceresi = self.open_new_window("User Deletion")
        silme_penceresi.geometry("400x400")

        # Pencereyi merkeze yerleştirmek için
        screen_width = silme_penceresi.winfo_screenwidth()
        screen_height = silme_penceresi.winfo_screenheight()
        x = int(screen_width/2 - 410/2)  # Pencerenin yatayda merkezde olmasını sağlar
        y = int(screen_height/2 - 400/2)  # Pencerenin dikeyde merkezde olmasını sağlar
        silme_penceresi.geometry(f"410x400+{x}+{y}")

        def execute_delete_query(selected_user):
            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )

            cursor = connection.cursor()

            # Kullanıcıyı veritabanından silme
            delete_query = "DELETE FROM kullanici WHERE id = %s"
            cursor.execute(delete_query, (selected_user,))
            connection.commit()
            messagebox.showinfo("User has been deleted", f"{selected_user} has been successfully deleted.")

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()

        def sil():
            selected_item = treeview.focus()
            if selected_item:
                selected_user = treeview.item(selected_item)["values"][0]
                user_info = selected_user.split(" - ")[0]
                execute_delete_query(user_info)
                treeview.delete(selected_item)

        def yenile():
            treeview.delete(*treeview.get_children())

            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )
            cursor = connection.cursor()
            
            cursor.execute(query)
            kullanici_listesi = cursor.fetchall()
            for kullanici in kullanici_listesi:
                user_id = kullanici[0]
                user_role = kullanici[1]
                if user_role == "ogrenci":
                    user_role = "Student"
                elif user_role == "ogretmen":
                    user_role = "Teacher"
                treeview.insert("", tk.END, values=(user_id, user_role))

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()

        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )

        # Kullanıcıları almak için sorgu
        query = "SELECT id, durum, onay_durumu FROM kullanici WHERE durum <> 'admin' AND (durum = 'ogrenci' OR onay_durumu = 1)"

        cursor = connection.cursor()
        cursor.execute(query)

        kullanici_listesi = cursor.fetchall()

        # Scrollbar oluştur
        scrollbar = ttk.Scrollbar(silme_penceresi)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tablo oluştur
        treeview = ttk.Treeview(silme_penceresi, columns=("Kullanıcı", "Durum"))
        treeview.heading("Kullanıcı", text="User")
        treeview.heading("Durum", text="Status")
        treeview.pack(fill=tk.BOTH, expand=True)

        # Tablonun sol tarafındaki boş kısmı gizle
        treeview["show"] = "headings"

        for kullanici in kullanici_listesi:
            user_id = kullanici[0]
            user_role = kullanici[1]
            onay_durumu = kullanici[2]

            if user_role == "ogrenci":
                user_role = "Student"
            elif user_role == "ogretmen":
                user_role = "Teacher"
            treeview.insert("", tk.END, values=(user_id, user_role))

        # Sil butonu
        sil_button = tk.Button(silme_penceresi, text="Sil", command=sil)
        sil_button.pack()

        # Yenile butonu
        yenile_button = tk.Button(silme_penceresi, text="Yenile", command=yenile)
        yenile_button.pack()

        # Veritabanı bağlantısını kapat
        cursor.close()
        connection.close()

    def kitaplari_listele(self):
        # Pencere oluşturma
        listeleme_penceresi = self.open_new_window("Books")
        listeleme_penceresi.geometry("400x400")

        # Pencereyi merkeze yerleştirmek için
        screen_width = listeleme_penceresi.winfo_screenwidth()
        screen_height = listeleme_penceresi.winfo_screenheight()
        window_width = 800
        window_height = 400
        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)
        listeleme_penceresi.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )
        cursor = connection.cursor()

        # Kitap listesini sorgula ve al
        def get_book_list():
            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM kitaplar"
            cursor.execute(query)
            book_list = cursor.fetchall()
            return book_list

        # Kitap listesini göster
        def show_book_list():
            book_list = get_book_list()
            treeview.delete(*treeview.get_children())  # Mevcut verileri temizle
            for book in book_list:
                treeview.insert("", "end", values=book)

        def sil():
            selected_item = treeview.selection()
            if selected_item:
                kitap_adi = treeview.item(selected_item, "values")[0]
                query = "DELETE FROM kitaplar WHERE kitap_adi = %s"
                cursor.execute(query, (kitap_adi,))
                connection.commit()
                show_book_list()
                messagebox.showinfo("Success", "Book has been deleted.")
            else:
                messagebox.showerror("Error", "Please select a book.")
        
        def yenile():
            treeview.delete(*treeview.get_children())

            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )
            cursor = connection.cursor()
            
            # Kitap listesini sorgula ve al
            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM kitaplar"
            cursor.execute(query)
            book_list = cursor.fetchall()
            
            # Kitap listesini göster
            treeview.delete(*treeview.get_children())  # Mevcut verileri temizle
            for book in book_list:
                treeview.insert("", "end", values=book)

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()

        def ara():
            search_keyword = arama_kutusu.get().lower()
            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM kitaplar WHERE LOWER(kitap_adi) LIKE %s"
            cursor.execute(query, (f"%{search_keyword}%",))
            search_results = cursor.fetchall()
            treeview.delete(*treeview.get_children())  # Mevcut verileri temizle
            for result in search_results:
                treeview.insert("", "end", values=result)

        # Arama kutusu
        arama_kutusu = tk.Entry(listeleme_penceresi, width=60)
        arama_kutusu.pack(side=tk.TOP, padx=10, pady=10)

        # Ara butonu
        ara_button = tk.Button(listeleme_penceresi, text="Search", command=ara)
        ara_button.pack(side=tk.TOP, padx=10, pady=5)

        # Kitap listesi tablosu
        treeview = ttk.Treeview(listeleme_penceresi, columns=("Kitap Adı", "Yazar", "Yayın Yılı", "Kategori"))
        treeview.heading("Kitap Adı", text="Book Name")
        treeview.heading("Yazar", text="Writer")
        treeview.heading("Yayın Yılı", text="Release Year")
        treeview.heading("Kategori", text="Category")
        treeview.pack()

        # Tablonun sol tarafındaki boş kısmı gizle
        treeview["show"] = "headings"

        # Sil butonu
        sil_button = tk.Button(listeleme_penceresi, text="Delete", command=sil)
        sil_button.pack()
        
        # Yenile butonu
        yenile_button = tk.Button(listeleme_penceresi, text="Refresh", command=yenile)
        yenile_button.pack()

        # Kitap listesini göster
        show_book_list()

    def kitap_ekle(self):
        ekleme_penceresi = self.open_new_window("Add Book")
        # Pencereyi merkeze yerleştirmek için
        screen_width = ekleme_penceresi.winfo_screenwidth()
        screen_height = ekleme_penceresi.winfo_screenheight()
        x = int(screen_width/2 - 400/2)  # Pencerenin yatayda merkezde olmasını sağlar
        y = int(screen_height/2 - 400/2)  # Pencerenin dikeyde merkezde olmasını sağlar
        ekleme_penceresi.geometry(f"400x400+{x}+{y}")
        
        kitap_adi_label = tk.Label(ekleme_penceresi, text="Book Name:")
        kitap_adi_label.pack()
        kitap_adi_entry = tk.Entry(ekleme_penceresi)
        kitap_adi_entry.pack()

        yazar_label = tk.Label(ekleme_penceresi, text="Writer:")
        yazar_label.pack()
        yazar_entry = tk.Entry(ekleme_penceresi)
        yazar_entry.pack()

        yayin_yili_label = tk.Label(ekleme_penceresi, text="Release Year:")
        yayin_yili_label.pack()
        yayin_yili_entry = tk.Entry(ekleme_penceresi)
        yayin_yili_entry.pack()

        kategori_label = tk.Label(ekleme_penceresi, text="Category:")
        kategori_label.pack()
        kategori_entry = tk.Entry(ekleme_penceresi)
        kategori_entry.pack()

        def execute_insert_query():
            kitap_adi = kitap_adi_entry.get()
            yazar = yazar_entry.get()
            yayin_yili = yayin_yili_entry.get()
            kategori = kategori_entry.get()

            if kitap_adi == "" or yazar == "":
                messagebox.showerror("Error", "Book name and Writer cannot be blank.")
                return

            if yayin_yili == "":
                result = messagebox.askquestion("Information", "Release year left blank. If you don't know the year of release, you can continue. If you continue, the release year will be assigned as the current year.\nDo you want to continue?")
                if result == "no":
                    return
                else:
                    # Varsayılan bir tarih atanıyor
                    yayin_yili = datetime.date.today().year
            else:
            # Yayın tarihine sadece rakam ve belirli noktalama işaretlerinin girilmesi kontrolü
                if not re.match(r'^[\d\-\/\.]+$', yayin_yili):
                    messagebox.showerror("Error", "Invalid release year. Release year should contain numbers only.\nLeave blank if you don't know the publication year.")
                    return
                
            # Kategori kontrolü
            kategori = kategori_entry.get()
            if kategori == "":
                result = messagebox.askquestion("Information", "Category left blank. If you don't know the category of the book, you can continue. If the category is left blank, the name of the book will be assigned to the category by default.\nDo you want to continue?")
                if result == "no":
                    return
                else:
                    # Varsayılan bir tarih atanıyor
                    kategori = kitap_adi_entry.get()

            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )

            cursor = connection.cursor()

            # Kitap ekleme sorgusu
            insert_query = "INSERT INTO kitaplar (kitap_adi, yazar, yayin_yili, kategori) VALUES (%s, %s, %s, %s)"
            kitap_bilgileri = (kitap_adi, yazar, yayin_yili, kategori)
            cursor.execute(insert_query, kitap_bilgileri)
            connection.commit()

            messagebox.showinfo("Book Added", "The book has been successfully added.")

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()

            # Entry alanlarını temizle
            kitap_adi_entry.delete(0, tk.END)
            yazar_entry.delete(0, tk.END)
            yayin_yili_entry.delete(0, tk.END)
            kategori_entry.delete(0, tk.END)

        # Ekle butonu
        ekle_button = tk.Button(ekleme_penceresi, text="Add", command=execute_insert_query)
        ekle_button.pack()
    
    def kullanımdaki_kitaplar(self):
        listeleme_penceresi = self.open_new_window("Books in Use")
        listeleme_penceresi.geometry("400x400")

        # Pencereyi merkeze yerleştirmek için
        screen_width = listeleme_penceresi.winfo_screenwidth()
        screen_height = listeleme_penceresi.winfo_screenheight()
        x = int(screen_width/2 - 1000/2)  # Pencerenin yatayda merkezde olmasını sağlar
        y = int(screen_height/2 - 400/2)  # Pencerenin dikeyde merkezde olmasını sağlar
        listeleme_penceresi.geometry(f"1000x400+{x}+{y}")

        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )
        cursor = connection.cursor()
        
        def yenile():
            kitap_listesi.delete(*kitap_listesi.get_children())

            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )
            cursor = connection.cursor()

            # Kullanıcıların üzerindeki kitap listesini sorgula ve al
            query = "SELECT kullanici_id, kitap_adi, yazar, yayin_yili, kategori FROM uzerimdeki_kitaplar"
            cursor.execute(query)
            book_list = cursor.fetchall()

            # Kitap listesini göster
            for book in book_list:
                kitap_listesi.insert("", "end", values=book)

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()

        # Kitap listesi tablosu
        kitap_listesi = ttk.Treeview(listeleme_penceresi, columns=("Kullanıcı ID", "Kitap Adı", "Yazar", "Yayın Yılı", "Kategori"))
        kitap_listesi.heading("Kullanıcı ID", text="User ID")
        kitap_listesi.heading("Kitap Adı", text="Book Name")
        kitap_listesi.heading("Yazar", text="Writer")
        kitap_listesi.heading("Yayın Yılı", text="Release Year")
        kitap_listesi.heading("Kategori", text="Category")
        kitap_listesi.pack()

        # Tablonun sol tarafındaki boş kısmı gizle
        kitap_listesi["show"] = "headings"

        # Yenile butonu
        yenile_button = tk.Button(listeleme_penceresi, text="Refresh", command=yenile)
        yenile_button.pack()

        # Veritabanından kitapları çekme ve gösterme
        yenile()

        # Önceki pencereyi gizle
        self.master.withdraw()

    def ogretmen_onayi(self):
        listeleme_penceresi = self.open_new_window("Teacher Approval / Approvals")
        listeleme_penceresi.geometry("400x400")

        # Pencereyi merkeze yerleştirmek için
        screen_width = listeleme_penceresi.winfo_screenwidth()
        screen_height = listeleme_penceresi.winfo_screenheight()
        x = int(screen_width/2 - 400/2)  # Pencerenin yatayda merkezde olmasını sağlar
        y = int(screen_height/2 - 400/2)  # Pencerenin dikeyde merkezde olmasını sağlar
        listeleme_penceresi.geometry(f"400x400+{x}+{y}")
        
         # MySQL bağlantısı
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )
        
        # Öğretmen kayıtlarını veritabanından alın
        cursor = self.conn.cursor()
        query = "SELECT * FROM kullanici WHERE durum = 'ogretmen' AND onay_durumu = 0"
        cursor.execute(query)
        ogretmenler = cursor.fetchall()
        cursor.close()

        # Öğretmen kayıtlarını listeleyen bir tablo ekleyin
        table = ttk.Treeview(listeleme_penceresi, columns=("id", "eposta"))
        table.heading("id", text="Username")
        table.heading("eposta", text="E-mail")
        table.pack()

        # Tablonun sol tarafındaki boş kısmı gizle
        table["show"] = "headings"

        # Öğretmen kayıtlarını tabloya ekle
        for ogretmen in ogretmenler:
            table.insert("", "end", values=(ogretmen[0], ogretmen[1], ogretmen[3]))

        # Onay düğmesi
        def onayla():
            # Seçilen öğretmen kayıtlarını onayla
            selected_items = table.selection()

            if len(selected_items) == 0:
                messagebox.showwarning("Error", "Please select a user.")
                return
            
            for item in selected_items:
                ogretmen_id = table.item(item)["values"][0]

                try:
                    cursor = self.conn.cursor()
                    query = "UPDATE kullanici SET onay_durumu = 1 WHERE id = %s"
                    cursor.execute(query, (ogretmen_id,))
                    self.conn.commit()
                    cursor.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", "An error occurred while granting consent.\nError message: " + str(err))

            messagebox.showinfo("Successful", "Selected teacher registrations approved!")

            # Tabloyu güncelle
            table.delete(*table.get_children())
            cursor = self.conn.cursor()
            query = "SELECT * FROM kullanici WHERE durum = 'ogretmen' AND onay_durumu = 0"
            cursor.execute(query)
            ogretmenler = cursor.fetchall()
            cursor.close()

            for ogretmen in ogretmenler:
                table.insert("", "end", values=(ogretmen[0], ogretmen[1], ogretmen[3]))

        # Onay düğmesini ekleyin
        onay_dugmesi = tk.Button(listeleme_penceresi, text="Approve Selected", command=onayla)
        onay_dugmesi.pack()

        # Onaylamama düğmesi
        def onaylamama():
            # Seçilen öğretmen kayıtlarını sil
            selected_items = table.selection()

            if len(selected_items) == 0:
                messagebox.showwarning("Error", "Please select a user.")
                return
            
            for item in selected_items:
                ogretmen_id = table.item(item)["values"][0]

                try:
                    cursor = self.conn.cursor()
                    query = "DELETE FROM kullanici WHERE id = %s"
                    cursor.execute(query, (ogretmen_id,))
                    self.conn.commit()
                    cursor.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", "An error occurred while deleting the teacher registration.\nError message: " + str(err))

            messagebox.showinfo("Successful", "Selected teacher registrations deleted!")

            # Tabloyu güncelle
            table.delete(*table.get_children())
            cursor = self.conn.cursor()
            query = "SELECT * FROM kullanici WHERE durum = 'ogretmen' AND onay_durumu = 0"
            cursor.execute(query)
            ogretmenler = cursor.fetchall()
            cursor.close()

            for ogretmen in ogretmenler:
                table.insert("", "end", values=(ogretmen[0], ogretmen[1], ogretmen[3]))

        # Onaylamama düğmesini ekleyin
        onaylamama_dugmesi = tk.Button(listeleme_penceresi, text="Reject Selected (Delete User)", command=onaylamama)
        onaylamama_dugmesi.pack()

class OgrenciPaneli(tk.Frame):
    def __init__(self, master=None, previous_frame=None):
        super().__init__(master)
        self.master = master
        self.master.title("Student Panel")
        self.previous_frame = previous_frame
        self.user_id = None
        self.master = master
        self.user_id = 1  # Örnek kullanıcı kimliği
        self.added_books = []  # Eklenen kitapların listesi

        # Kitap Listeleme Butonu
        self.kitap_listeleme_dugmesi = tk.Button(self.master, text="List Books", command=self.kitaplari_listele)
        self.kitap_listeleme_dugmesi.pack()

        # Üzerimdeki kitaplar düğmesi
        self.uzerimdeki_kitaplar_dugmesi = tk.Button(self.master, text="Books on Me", command=self.uzerimdeki_kitaplar)
        self.uzerimdeki_kitaplar_dugmesi.pack()

        # Çıkış Yap Butonu
        self.girise_don_dugmesi = tk.Button(self.master, text="Log Out", command=self.girise_don)
        self.girise_don_dugmesi.pack(side=tk.BOTTOM, pady=10)

        self.center_window()

    def center_window(self):
        window_width = 400
        window_height = 300
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def kitaplari_listele(self):
        # Pencere oluşturma
        listeleme_penceresi = tk.Toplevel(self.master)
        listeleme_penceresi.title("Books")
        listeleme_penceresi.geometry("400x400")
        
        # Pencereyi merkeze yerleştirmek için
        screen_width = listeleme_penceresi.winfo_screenwidth()
        screen_height = listeleme_penceresi.winfo_screenheight()
        window_width = 800
        window_height = 480
        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)
        listeleme_penceresi.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )
        cursor = connection.cursor()

        def yenile():
            kitap_listesi.delete(*kitap_listesi.get_children())

            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )
            cursor = connection.cursor()
            
            # Kitap listesini sorgula ve al
            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM kitaplar"
            cursor.execute(query)
            book_list = cursor.fetchall()
            
            # Kitap listesini göster
            kitap_listesi.delete(*kitap_listesi.get_children())  # Mevcut verileri temizle
            for book in book_list:
                kitap_listesi.insert("", "end", values=book)

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()
                

        def ara():
            search_keyword = arama_kutusu.get().lower()
            
            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )
            cursor = connection.cursor()

            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM kitaplar WHERE LOWER(kitap_adi) LIKE %s"
            cursor.execute(query, (f"%{search_keyword}%",))
            search_results = cursor.fetchall()
            
            kitap_listesi.delete(*kitap_listesi.get_children())  # Mevcut verileri temizle
            for result in search_results:
                kitap_listesi.insert("", "end", values=result)

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()
        
        def add_to_account():
            selected_item = kitap_listesi.item(kitap_listesi.focus())['values']
            if selected_item:
                kitap_adi = selected_item[0]
                yazar = selected_item[1]
                yayin_yili = selected_item[2]
                kategori = selected_item[3]

                # Kitabın zaten eklenip eklenmediğini kontrol et
                query = "SELECT COUNT(*) FROM uzerimdeki_kitaplar WHERE kullanici_id = %s AND kitap_adi = %s"
                values = (self.user_id, kitap_adi)
                cursor.execute(query, values)
                result = cursor.fetchone()
                book_count = result[0]

                if book_count > 0:
                    tk.messagebox.showwarning("Error", f"{kitap_adi} is already in your account.")
                else:
                    # Kitabı veritabanına ekle
                    query = "INSERT INTO uzerimdeki_kitaplar (kullanici_id, kitap_adi, yazar, yayin_yili, kategori) VALUES (%s, %s, %s, %s, %s)"
                    values = (self.user_id, kitap_adi, yazar, yayin_yili, kategori)
                    cursor.execute(query, values)
                    connection.commit()
                    tk.messagebox.showinfo("Book Added", f"{kitap_adi} has been added to your account.")
            else:
                tk.messagebox.showwarning("Error", "Please select a book.")

        # Arama kutusu
        arama_kutusu = tk.Entry(listeleme_penceresi, width=60)
        arama_kutusu.pack(side=tk.TOP, padx=10, pady=10)

        # Ara butonu
        ara_button = tk.Button(listeleme_penceresi, text="Search", command=ara)
        ara_button.pack(side=tk.TOP, padx=10, pady=5)

        # Kitap listesi tablosu
        kitap_listesi = ttk.Treeview(listeleme_penceresi, columns=("Kitap Adı", "Yazar", "Yayın Yılı", "Kategori"))
        kitap_listesi.heading("Kitap Adı", text="Book Name")
        kitap_listesi.heading("Yazar", text="Writer")
        kitap_listesi.heading("Yayın Yılı", text="Release Year")
        kitap_listesi.heading("Kategori", text="Category")
        kitap_listesi.pack()

        # Kitapları al ve listeye ekle
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kitaplar")
        kitaplar = cursor.fetchall()
        for kitap in kitaplar:
            kitap_listesi.insert("", tk.END, values=kitap)

        # Veritabanından kitapları çekme
        cursor.execute("SELECT * FROM kitaplar")
        kitaplar = cursor.fetchall()
        
        # Ağaç görünümünü ekrana yerleştirme
        kitap_listesi.pack(pady=20)
        
        # Hesaba Ekle düğmesi
        add_to_account_button = tk.Button(listeleme_penceresi, text="Add to Account", command=add_to_account)
        add_to_account_button.pack()

        # Tablonun sol tarafındaki boş kısmı gizle
        kitap_listesi["show"] = "headings"

        # Yenile butonu
        yenile_button = tk.Button(listeleme_penceresi, text="Refresh", command=yenile)
        yenile_button.pack()

        # Geri Dön Butonu
        geri_don_dugmesi = tk.Button(listeleme_penceresi, text="Back to Student Panel", command=lambda: self.geri_don(listeleme_penceresi))
        geri_don_dugmesi.pack(side=tk.BOTTOM, pady=10)

        # Önceki pencereyi gizle
        self.master.withdraw()

    def uzerimdeki_kitaplar(self):
        # Pencere oluşturma
        kitaplar_penceresi = tk.Toplevel(self.master)
        kitaplar_penceresi.title("Books on Me")
        kitaplar_penceresi.geometry("400x400")

        # Pencereyi merkeze yerleştirmek için
        screen_width = kitaplar_penceresi.winfo_screenwidth()
        screen_height = kitaplar_penceresi.winfo_screenheight()
        window_width = 800
        window_height = 400
        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)
        kitaplar_penceresi.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )
        cursor = connection.cursor()

        def get_my_books():
            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM uzerimdeki_kitaplar WHERE kullanici_id = %s"
            cursor.execute(query, (str(self.user_id),))
            my_books = cursor.fetchall()
            return my_books

        # Üzerimdeki kitapları göster
        def show_my_books():
            my_books = get_my_books()
            added_book_list.delete(*added_book_list.get_children())  # Mevcut verileri temizle
            for book in my_books:
                added_book_list.insert("", "end", values=book)

        def remove_from_account():
            selected_item = added_book_list.selection()
            if selected_item:
                book = added_book_list.item(selected_item)["values"]
                kitap_adi = book[0]
                query = "DELETE FROM uzerimdeki_kitaplar WHERE kullanici_id = %s AND kitap_adi = %s"
                values = (self.user_id, kitap_adi)
                cursor.execute(query, values)
                connection.commit()
                tk.messagebox.showinfo("Book Removed", f"{kitap_adi} has been removed from your account.")
                show_my_books()
            else:
                tk.messagebox.showwarning("Error", "Please select a book.")
        
        added_book_frame = ttk.LabelFrame(kitaplar_penceresi)
        added_book_frame.pack(pady=10)
        
        # Kitap listesi tablosu
        added_book_list = ttk.Treeview(added_book_frame, columns=("Kitap Adı", "Yazar", "Yayın Yılı", "Kategori"))
        added_book_list.heading("Kitap Adı", text="Book Name")
        added_book_list.heading("Yazar", text="Writer")
        added_book_list.heading("Yayın Yılı", text="Release Year")
        added_book_list.heading("Kategori", text="Category")
        added_book_list.pack()

        # Tablonun sol tarafındaki boş kısmı gizle
        added_book_list["show"] = "headings"

        # Kitap listesini göster
        show_my_books()

        # Kitabı kaldırmak için düğmeyi ekle
        remove_button = tk.Button(kitaplar_penceresi, text="Remove", command=remove_from_account)
        remove_button.pack()

        # Geri Dön Butonu
        geri_don_dugmesi = tk.Button(kitaplar_penceresi, text="Back to Student Panel", command=lambda: self.geri_don(kitaplar_penceresi))
        geri_don_dugmesi.pack(side=tk.BOTTOM, pady=10)

        # Önceki pencereyi gizle
        self.master.withdraw()

    def geri_don(self, pencere):
        pencere.destroy()  # Mevcut pencereyi kapat
        self.master.deiconify()  # Öğretmen panelini göster

    def girise_don(self):
        tk.messagebox.showinfo("Logged Out", "Successfully logged out.")  # Çıkış yapıldığında mesaj ver
        self.master.destroy()  # Üye ol panelini kapat        
        self.previous_frame.master.deiconify()  # Giriş panelini göster

class OgretmenPaneli(tk.Frame):
    def __init__(self, master=None, previous_frame=None):
        super().__init__(master)
        self.master = master
        self.master.title("Teacher Panel")
        self.previous_frame = previous_frame
        self.user_id = None
        self.master = master
        self.user_id = 1  # Örnek kullanıcı kimliği
        self.added_books = []  # Eklenen kitapların listesi

        # Kitap Listeleme Butonu
        self.kitap_listeleme_dugmesi = tk.Button(self.master, text="List Books", command=self.kitaplari_listele)
        self.kitap_listeleme_dugmesi.pack()

        # Üzerimdeki kitaplar düğmesi
        self.uzerimdeki_kitaplar_dugmesi = tk.Button(self.master, text="Books on Me", command=self.uzerimdeki_kitaplar)
        self.uzerimdeki_kitaplar_dugmesi.pack()

        # Çıkış Yap Butonu
        self.girise_don_dugmesi = tk.Button(self.master, text="Log Out", command=self.girise_don)
        self.girise_don_dugmesi.pack(side=tk.BOTTOM, pady=10)

        self.center_window()

    def center_window(self):
        window_width = 400
        window_height = 300
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def kitaplari_listele(self):
        # Pencere oluşturma
        listeleme_penceresi = tk.Toplevel(self.master)
        listeleme_penceresi.title("Books")
        listeleme_penceresi.geometry("400x400")
        
        # Pencereyi merkeze yerleştirmek için
        screen_width = listeleme_penceresi.winfo_screenwidth()
        screen_height = listeleme_penceresi.winfo_screenheight()
        window_width = 800
        window_height = 480
        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)
        listeleme_penceresi.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )
        cursor = connection.cursor()

        def yenile():
            kitap_listesi.delete(*kitap_listesi.get_children())

            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )
            cursor = connection.cursor()
            
            # Kitap listesini sorgula ve al
            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM kitaplar"
            cursor.execute(query)
            book_list = cursor.fetchall()
            
            # Kitap listesini göster
            kitap_listesi.delete(*kitap_listesi.get_children())  # Mevcut verileri temizle
            for book in book_list:
                kitap_listesi.insert("", "end", values=book)

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()
                

        def ara():
            search_keyword = arama_kutusu.get().lower()
            
            # MySQL bağlantısı
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="201079",
                database="librarysystem"
            )
            cursor = connection.cursor()

            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM kitaplar WHERE LOWER(kitap_adi) LIKE %s"
            cursor.execute(query, (f"%{search_keyword}%",))
            search_results = cursor.fetchall()
            
            kitap_listesi.delete(*kitap_listesi.get_children())  # Mevcut verileri temizle
            for result in search_results:
                kitap_listesi.insert("", "end", values=result)

            # Veritabanı bağlantısını kapat
            cursor.close()
            connection.close()

        def add_to_account():
            selected_item = kitap_listesi.item(kitap_listesi.focus())['values']
            if selected_item:
                kitap_adi = selected_item[0]
                yazar = selected_item[1]
                yayin_yili = selected_item[2]
                kategori = selected_item[3]

                # Kitabın zaten eklenip eklenmediğini kontrol et
                query = "SELECT COUNT(*) FROM uzerimdeki_kitaplar WHERE kullanici_id = %s AND kitap_adi = %s"
                values = (self.user_id, kitap_adi)
                cursor.execute(query, values)
                result = cursor.fetchone()
                book_count = result[0]

                if book_count > 0:
                    tk.messagebox.showwarning("Error", f"{kitap_adi} already exists in your account.")
                else:
                    # Kitabı veritabanına ekle
                    query = "INSERT INTO uzerimdeki_kitaplar (kullanici_id, kitap_adi, yazar, yayin_yili, kategori) VALUES (%s, %s, %s, %s, %s)"
                    values = (self.user_id, kitap_adi, yazar, yayin_yili, kategori)
                    cursor.execute(query, values)
                    connection.commit()
                    tk.messagebox.showinfo("Book Added", f"{kitap_adi} has been added to your account.")
            else:
                tk.messagebox.showwarning("Error", "Please select a book.")


        # Arama kutusu
        arama_kutusu = tk.Entry(listeleme_penceresi, width=60)
        arama_kutusu.pack(side=tk.TOP, padx=10, pady=10)

        # Ara butonu
        ara_button = tk.Button(listeleme_penceresi, text="Search", command=ara)
        ara_button.pack(side=tk.TOP, padx=10, pady=5)

        # Kitap listesi tablosu
        kitap_listesi = ttk.Treeview(listeleme_penceresi, columns=("Kitap Adı", "Yazar", "Yayın Yılı", "Kategori"))
        kitap_listesi.heading("Kitap Adı", text="Book Name")
        kitap_listesi.heading("Yazar", text="Writer")
        kitap_listesi.heading("Yayın Yılı", text="Release Year")
        kitap_listesi.heading("Kategori", text="Category")
        kitap_listesi.pack()

        # Kitapları al ve listeye ekle
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM kitaplar")
        kitaplar = cursor.fetchall()
        for kitap in kitaplar:
            kitap_listesi.insert("", tk.END, values=kitap)

        # Veritabanından kitapları çekme
        cursor.execute("SELECT * FROM kitaplar")
        kitaplar = cursor.fetchall()
        
        # Ağaç görünümünü ekrana yerleştirme
        kitap_listesi.pack(pady=20)
        
        # Hesaba Ekle düğmesi
        add_to_account_button = tk.Button(listeleme_penceresi, text="Add to Account", command=add_to_account)
        add_to_account_button.pack()

        # Tablonun sol tarafındaki boş kısmı gizle
        kitap_listesi["show"] = "headings"

        # Yenile butonu
        yenile_button = tk.Button(listeleme_penceresi, text="Refresh", command=yenile)
        yenile_button.pack()

        # Geri Dön Butonu
        geri_don_dugmesi = tk.Button(listeleme_penceresi, text="Back to Teacher Panel", command=lambda: self.geri_don(listeleme_penceresi))
        geri_don_dugmesi.pack(side=tk.BOTTOM, pady=10)

        # Önceki pencereyi gizle
        self.master.withdraw()

    def uzerimdeki_kitaplar(self):
        # Pencere oluşturma
        kitaplar_penceresi = tk.Toplevel(self.master)
        kitaplar_penceresi.title("Books on Me")
        kitaplar_penceresi.geometry("400x400")

        # Pencereyi merkeze yerleştirmek için
        screen_width = kitaplar_penceresi.winfo_screenwidth()
        screen_height = kitaplar_penceresi.winfo_screenheight()
        window_width = 800
        window_height = 400
        x = int(screen_width/2 - window_width/2)
        y = int(screen_height/2 - window_height/2)
        kitaplar_penceresi.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # MySQL bağlantısı
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="201079",
            database="librarysystem"
        )
        cursor = connection.cursor()

        def get_my_books():
            query = "SELECT kitap_adi, yazar, yayin_yili, kategori FROM uzerimdeki_kitaplar WHERE kullanici_id = %s"
            cursor.execute(query, (str(self.user_id),))
            my_books = cursor.fetchall()
            return my_books

        # Üzerimdeki kitapları göster
        def show_my_books():
            my_books = get_my_books()
            added_book_list.delete(*added_book_list.get_children())  # Mevcut verileri temizle
            for book in my_books:
                added_book_list.insert("", "end", values=book)

        def remove_from_account():
            selected_item = added_book_list.selection()
            if selected_item:
                book = added_book_list.item(selected_item)["values"]
                kitap_adi = book[0]
                query = "DELETE FROM uzerimdeki_kitaplar WHERE kullanici_id = %s AND kitap_adi = %s"
                values = (self.user_id, kitap_adi)
                cursor.execute(query, values)
                connection.commit()
                tk.messagebox.showinfo("Book Removed", f"{kitap_adi} has been removed from your account.")
                show_my_books()
            else:
                tk.messagebox.showwarning("Error", "Please select a book.")
        
        added_book_frame = ttk.LabelFrame(kitaplar_penceresi)
        added_book_frame.pack(pady=10)
        
        # Kitap listesi tablosu
        added_book_list = ttk.Treeview(added_book_frame, columns=("Kitap Adı", "Yazar", "Yayın Yılı", "Kategori"))
        added_book_list.heading("Kitap Adı", text="Book Name")
        added_book_list.heading("Yazar", text="Writer")
        added_book_list.heading("Yayın Yılı", text="Release Year")
        added_book_list.heading("Kategori", text="Category")
        added_book_list.pack()

        # Tablonun sol tarafındaki boş kısmı gizle
        added_book_list["show"] = "headings"

        # Kitap listesini göster
        show_my_books()

        # Kitabı kaldırmak için düğmeyi ekle
        remove_button = tk.Button(kitaplar_penceresi, text="Remove", command=remove_from_account)
        remove_button.pack()

        # Geri Dön Butonu
        geri_don_dugmesi = tk.Button(kitaplar_penceresi, text="Return to Teacher Panel", command=lambda: self.geri_don(kitaplar_penceresi))
        geri_don_dugmesi.pack(side=tk.BOTTOM, pady=10)

        # Önceki pencereyi gizle
        self.master.withdraw()

    def geri_don(self, pencere):
        pencere.destroy()  # Mevcut pencereyi kapat
        self.master.deiconify()  # Öğretmen panelini göster

    def girise_don(self):
        tk.messagebox.showinfo("Logged Out", "Successfully logged out.")  # Çıkış yapıldığında mesaj ver
        self.master.destroy()  # Üye ol panelini kapat        
        self.previous_frame.master.deiconify()  # Giriş panelini göster


root = tk.Tk()
giris_paneli = GirisPaneli(root)
root.geometry("400x300")
root.mainloop()