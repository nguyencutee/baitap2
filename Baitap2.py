import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
from unidecode import unidecode

class DatabaseApp:
    def __init__(self, root):   
        self.root = root
        self.root.title("Quản lý sinh viên")
        self.root.geometry("900x600")

        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='5432')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='danhsach')

        # Create the GUI elements
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Connection section
        connection_frame = tk.LabelFrame(self.root, text="Kết nối Database", padx=10, pady=10)
        connection_frame.pack(pady=10, fill="x")

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(connection_frame, textvariable=self.db_name, width=15).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(connection_frame, textvariable=self.user, width=15).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        tk.Entry(connection_frame, textvariable=self.password, show="*", width=15).grid(row=0, column=5, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(connection_frame, textvariable=self.host, width=15).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(connection_frame, textvariable=self.port, width=10).grid(row=1, column=3, padx=5, pady=5)

        tk.Button(connection_frame, text="Kết nối", command=self.connect_db).grid(row=1, column=4, padx=10, pady=5)

        # Query section
        query_frame = tk.LabelFrame(self.root, text="Truy vấn dữ liệu", padx=10, pady=10)
        query_frame.pack(pady=10, fill="x")

        tk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name, width=15).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Tải dữ liệu", command=self.load_data).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(query_frame, text="Xoá", command=self.clear_data).grid(row=0, column=3, padx=10, pady=5)
        tk.Button(query_frame, text="Sửa", command=self.update_data).grid(row=0, column=4, padx=10, pady=5)

        # Data display
        self.data_display = tk.Text(self.root, height=10, width=90)
        self.data_display.pack(pady=10)

        # Insert section
        insert_frame = tk.LabelFrame(self.root, text="Thêm sinh viên", padx=10, pady=10)
        insert_frame.pack(pady=10, fill="x")

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()
        self.column3 = tk.StringVar()

        tk.Label(insert_frame, text="Họ và tên:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1, width=20).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="MSSV:").grid(row=0, column=2, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2, width=15).grid(row=0, column=3, padx=5, pady=5)

        tk.Label(insert_frame, text="Tình trạng:").grid(row=0, column=4, padx=5, pady=5)
        choice_tt = ttk.Combobox(insert_frame, width=15, textvariable=self.column3, state="readonly")
        choice_tt['values'] = ("Còn học", "Nghỉ học", "Bảo lưu")
        choice_tt.grid(row=0, column=5, padx=5, pady=5)
        choice_tt.current(0)

        tk.Button(insert_frame, text="Thêm", command=self.insert_data).grid(row=0, column=6, padx=10, pady=5)

    def create_menu(self):
        # Tạo thanh menu
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Tạo menu Hướng dẫn
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Hướng dẫn sử dụng", command=self.show_readme)
        help_menu.add_command(label="Hướng dẫn Sửa", command=self.show_change)
        help_menu.add_command(label="Hướng dẫn Tải dữ liệu", command=self.show_loaddata)
        help_menu.add_command(label="Hướng dẫn Xoá", command=self.show_clear)
        menu_bar.add_cascade(label="Hướng dẫn", menu=help_menu)

        # Tạo menu thoát
        exit_menu = tk.Menu(menu_bar, tearoff=0)
        exit_menu.add_command(label="Thoát", command=self.quit)
        menu_bar.add_cascade(label="Thoát", menu=exit_menu)

    def quit(self):
        self.root.quit()

    def show_readme(self):
        readme_text = (
            "1. Kết nối đến cơ sở dữ liệu PostgreSQL bằng cách nhấn 'Kết nối'.\n"
            "2. Nhập tên bảng dữ liệu và chọn các chức năng: Tải dữ liệu, Xóa, Sửa.\n"
            "3. Để thêm sinh viên mới, điền thông tin và nhấn 'Thêm'.\n"
        )
        messagebox.showinfo("Hướng dẫn sử dụng", readme_text)

    def show_change(self):
        readme_text = (
           "1. Nhập MSSV bạn muốn sửa, sau đó nhập họ và tên hoặc tình trạng.\n"
           "2. Nhấn 'Sửa', hệ thống sẽ cập nhật thông tin sinh viên.\n"
        )
        messagebox.showinfo("Hướng dẫn Sửa", readme_text)

    def show_loaddata(self):
        readme_text = (
           "1. Nhập MSSV muốn xem, nhấn 'Tải dữ liệu' để tải dữ liệu sinh viên.\n"
           "2. Không nhập MSSV, nhấn 'Tải dữ liệu' để tải tất cả dữ liệu sinh viên.\n"
        )
        messagebox.showinfo("Hướng dẫn Tải dữ liệu", readme_text)

    def show_clear(self):
        readme_text = (
           "1. Nhập MSSV muốn xóa, nhấn 'Xóa' dữ liệu sinh viên.\n"
           "2. Không nhập MSSV, nhấn 'Xoá' để xóa tất cả dữ liệu sinh viên.\n"
        )
        messagebox.showinfo("Hướng dẫn Xoá", readme_text)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Thành công", "Đã kết nối tới Database")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        if not hasattr(self, 'cur'):
            messagebox.showerror("Error", "Database chưa kết nối!")
            return
        try:
            mssv = self.column2.get()
            if not mssv:
                query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
                self.cur.execute(query)
                rows = self.cur.fetchall()
                self.data_display.delete(1.0, tk.END)
                if rows:
                    for row in rows:
                        self.data_display.insert(tk.END, f'Họ và tên: "{row[0]}", MSSV: "{row[1]}", Tình trạng: "{row[2]}", Email: "{row[3]}"\n')
            else:
                query = sql.SQL("SELECT * FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
                self.cur.execute(query, [mssv])
                row = self.cur.fetchone()
                self.data_display.delete(1.0, tk.END)
                if row:
                    self.data_display.insert(tk.END, f'Họ và tên: "{row[0]}", MSSV: "{row[1]}", Tình trạng: "{row[2]}", Email: "{row[3]}"\n')
                else:
                    self.data_display.insert(tk.END, "Không tìm thấy sinh viên\n")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi tải dữ liệu: {e}")

    def insert_data(self):
        if not hasattr(self, 'cur'):
            messagebox.showerror("Error", "Database chưa kết nối!")
            return
        try:
            hoten = self.column1.get()
            mssv = self.column2.get()
            tinhtrang = self.column3.get()
            if not hoten or not mssv or not tinhtrang:
                messagebox.showinfo("Error", "Không được bỏ trống ô")
                return
            else:
                last_name = unidecode(hoten.split()[-1].lower())
                email = f"{last_name}.{mssv}@vanlanguni.vn"
                query = sql.SQL("INSERT INTO {} (hoten, mssv, tinhtrang, email) VALUES (%s, %s, %s, %s)").format(sql.Identifier(self.table_name.get()))
                self.cur.execute(query, (hoten, mssv, tinhtrang, email))
                self.conn.commit()

            messagebox.showinfo("Thành công", "Thêm sinh viên thành công")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi thêm dữ liệu: {e}")

    def clear_data(self):
        if not hasattr(self, 'cur'):
            messagebox.showerror("Error", "Database đang không được kết nối. Làm ơn kết nối trước!")
            return
        try:
            mssv = self.column2.get()
            if not mssv:
                truncate_query = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY").format(sql.Identifier(self.table_name.get()))
                self.cur.execute(truncate_query)
                self.conn.commit()
                self.data_display.delete(1.0, tk.END)
                messagebox.showinfo("Success", "Mọi dữ liệu đều đã được xoá")
            else:
                delete_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
                self.cur.execute(delete_query, (mssv,))
                self.conn.commit()
                self.data_display.delete(1.0, tk.END)
                if self.cur.rowcount > 0:
                    messagebox.showinfo("Success", f"Dữ liệu của MSSV {mssv} đã được xoá")
                else:
                    messagebox.showinfo("Info", f"Không tìm thấy dữ liệu cho MSSV {mssv}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error clearing data: {e}")
            
    def update_data(self):
        if not hasattr(self, 'cur'):
            messagebox.showerror("Error", "Database đang không được kết nối. Làm ơn kết nối trước!")
            return
        try:
            mssv = self.column2.get()
            hoten = self.column1.get()
            if not mssv:
                messagebox.showerror("Error", "MSSV không thể trống để sửa!")
                return
            
            last_name = unidecode(hoten.split()[-1].lower())
            email = f"{last_name}.{mssv}@vanlanguni.vn"
            update_query = sql.SQL("UPDATE {} SET hoten = %s, tinhtrang = %s, email = %s WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(update_query, (hoten, self.column3.get(), email, mssv))
            self.conn.commit()
        
            if self.cur.rowcount > 0:
                messagebox.showinfo("Success", "Cập nhật dữ liệu thành công!")
            else:
                messagebox.showinfo("Info", f"Không tìm thấy dữ liệu cho MSSV {mssv}.")
        except Exception as e:
                messagebox.showerror("Error", f"Lỗi khi cập nhật dữ liệu: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
