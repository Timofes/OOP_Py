import tkinter as tk
from tkinter import ttk, messagebox
from Menu import Menu

class MusicStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Музыкальные инструменты")
        self.root.geometry("1200x700")
        
        self.store = Menu({
            'dbname': 'JavaOOP',
            'user': 'postgres',
            'password': '1234',
            'host': 'localhost'
        })
        
        self.create_widgets()
        self.create_tabs()
        self.refresh_all_tables()
    
    def create_widgets(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
    
    def create_tabs(self):
        self.tab_mi = ttk.Frame(self.notebook)
        self.tab_drums = ttk.Frame(self.notebook)
        self.tab_flutes = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_mi, text="Инструменты")
        self.notebook.add(self.tab_drums, text="Барабаны")
        self.notebook.add(self.tab_flutes, text="Флейты")
        
        self.create_instruments_tab()
        self.create_drums_tab()
        self.create_flutes_tab()
    
    def create_instruments_tab(self):
        columns = ("id", "color", "material")
        self.mi_tree = ttk.Treeview(self.tab_mi, columns=columns, show="headings")
        self.mi_tree.heading("id", text="ID")
        self.mi_tree.heading("color", text="Цвет")
        self.mi_tree.heading("material", text="Материал")
        
        for col in columns:
            self.mi_tree.column(col, width=100, anchor=tk.CENTER if col == "id" else tk.W)
        
        btn_frame = tk.Frame(self.tab_mi)
        tk.Button(btn_frame, text="Добавить", command=self.add_instrument).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_instrument).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_instrument).pack(side=tk.LEFT, padx=5)
        
        scrollbar = ttk.Scrollbar(self.tab_mi, orient=tk.VERTICAL, command=self.mi_tree.yview)
        self.mi_tree.configure(yscrollcommand=scrollbar.set)
        
        self.mi_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.mi_tree.bind("<Double-1>", lambda e: self.edit_instrument())
    
    def create_drums_tab(self):
        columns = ("id", "form", "diameter", "instrument_id", "color", "material")
        self.drums_tree = ttk.Treeview(self.tab_drums, columns=columns, show="headings")
        self.drums_tree.heading("id", text="ID барабана")
        self.drums_tree.heading("form", text="Форма")
        self.drums_tree.heading("diameter", text="Диаметр")
        self.drums_tree.heading("instrument_id", text="ID инструмента")
        self.drums_tree.heading("color", text="Цвет")
        self.drums_tree.heading("material", text="Материал")
        
        for col in columns:
            self.drums_tree.column(col, width=100, anchor=tk.CENTER if col in ("id", "instrument_id") else tk.W)
        
        btn_frame = tk.Frame(self.tab_drums)
        tk.Button(btn_frame, text="Добавить", command=self.add_drum).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_drum).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_drum).pack(side=tk.LEFT, padx=5)
        
        scrollbar = ttk.Scrollbar(self.tab_drums, orient=tk.VERTICAL, command=self.drums_tree.yview)
        self.drums_tree.configure(yscrollcommand=scrollbar.set)
        
        self.drums_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.drums_tree.bind("<Double-1>", lambda e: self.edit_drum())
    
    def create_flutes_tab(self):

        columns = ("id", "holes", "holder", "instrument_id", "color", "material")
        self.flutes_tree = ttk.Treeview(self.tab_flutes, columns=columns, show="headings")
        self.flutes_tree.heading("id", text="ID флейты")
        self.flutes_tree.heading("holes", text="Отверстия")
        self.flutes_tree.heading("holder", text="Держание")
        self.flutes_tree.heading("instrument_id", text="ID инструмента")
        self.flutes_tree.heading("color", text="Цвет")
        self.flutes_tree.heading("material", text="Материал")
        
        for col in columns:
            self.flutes_tree.column(col, width=100, anchor=tk.CENTER if col in ("id", "instrument_id", "holes") else tk.W)
        
        btn_frame = tk.Frame(self.tab_flutes)
        tk.Button(btn_frame, text="Добавить", command=self.add_flute).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Редактировать", command=self.edit_flute).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_flute).pack(side=tk.LEFT, padx=5)
        
        scrollbar = ttk.Scrollbar(self.tab_flutes, orient=tk.VERTICAL, command=self.flutes_tree.yview)
        self.flutes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.flutes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        btn_frame.pack(fill=tk.X, pady=5)
        
        self.flutes_tree.bind("<Double-1>", lambda e: self.edit_flute())
    
    def refresh_all_tables(self):
        self.refresh_instruments()
        self.refresh_drums()
        self.refresh_flutes()
    
    def refresh_instruments(self):
        for item in self.mi_tree.get_children():
            self.mi_tree.delete(item)
        
        for instrument in self.store.get_all_instruments():
            self.mi_tree.insert("", tk.END, values=(
                instrument.id, 
                instrument.body_color, 
                instrument.body_material
            ))
    
    def refresh_drums(self):
        for item in self.drums_tree.get_children():
            self.drums_tree.delete(item)
        
        for drum in self.store.get_all_drums():
            self.drums_tree.insert("", tk.END, values=(
                drum.id_drum,
                drum.form,
                drum.diameter,
                drum.musical_instrument.id,
                drum.musical_instrument.body_color,
                drum.musical_instrument.body_material
            ))
    
    def refresh_flutes(self):
        for item in self.flutes_tree.get_children():
            self.flutes_tree.delete(item)
        
        for flute in self.store.get_all_flutes():
            self.flutes_tree.insert("", tk.END, values=(
                flute.id_flute,
                flute.count_hole,
                flute.holder_method,
                flute.musical_instrument.id,
                flute.musical_instrument.body_color,
                flute.musical_instrument.body_material
            ))
    
    def add_instrument(self):
        self.instrument_form("Добавить инструмент")
    
    def edit_instrument(self):
        selected = self.mi_tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите инструмент для редактирования")
            return
        
        instrument_id = self.mi_tree.item(selected[0])['values'][0]
        instrument = self.store.get_instrument(instrument_id)
        if instrument:
            self.instrument_form("Редактировать инструмент", instrument)
    
    def instrument_form(self, title, instrument=None):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.grab_set()
        
        tk.Label(form, text="Цвет:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        color_entry = tk.Entry(form, width=30)
        color_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Материал:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        material_entry = tk.Entry(form, width=30)
        material_entry.grid(row=1, column=1, padx=5, pady=5)
        
        if instrument:
            color_entry.insert(0, instrument.body_color)
            material_entry.insert(0, instrument.body_material)
        
        def save():
            color = color_entry.get()
            material = material_entry.get()
            
            if not color or not material:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            try:
                if instrument:
                    instrument.body_color = color
                    instrument.body_material = material
                    instrument.save()
                    messagebox.showinfo("Успех", "Инструмент обновлен")
                else:
                    self.store.create_instrument(color, material)
                    messagebox.showinfo("Успех", "Инструмент добавлен")
                
                self.refresh_instruments()
                form.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка базы данных: {str(e)}")
        
        tk.Button(form, text="Сохранить", command=save).grid(row=2, columnspan=2, pady=10)
    
    def delete_instrument(self):
        selected = self.mi_tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите инструмент для удаления")
            return
        
        instrument_id = self.mi_tree.item(selected[0])['values'][0]
        try:
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот инструмент?"):
                self.store.delete_instrument(instrument_id)
                self.refresh_instruments()
                messagebox.showinfo("Успех", "Инструмент удален")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def add_drum(self):
        self.drum_form("Добавить барабан")
    
    def edit_drum(self):
        selected = self.drums_tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите барабан для редактирования")
            return
        
        drum_id = self.drums_tree.item(selected[0])['values'][0]
        drum = self.store.get_drum(drum_id)
        if drum:
            self.drum_form("Редактировать барабан", drum)
    
    def drum_form(self, title, drum=None):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.grab_set()
        
        instruments = self.store.get_all_instruments()
        instrument_options = {f"{i.id} - {i.body_color} {i.body_material}": i.id for i in instruments}
        
        tk.Label(form, text="Форма:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        form_entry = tk.Entry(form, width=30)
        form_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Диаметр:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        diameter_entry = tk.Entry(form, width=30)
        diameter_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Инструмент:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        instrument_var = tk.StringVar(form)
        instrument_combobox = ttk.Combobox(form, textvariable=instrument_var, values=list(instrument_options.keys()))
        instrument_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        if drum:
            form_entry.insert(0, drum.form)
            diameter_entry.insert(0, drum.diameter)
            for text, id in instrument_options.items():
                if id == drum.musical_instrument.id:
                    instrument_var.set(text)
                    break
        
        def save():
            form_val = form_entry.get()
            diameter_val = diameter_entry.get()
            instrument_text = instrument_var.get()
            
            if not form_val or not diameter_val or not instrument_text:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            try:
                diameter = int(diameter_val)
                instrument_id = instrument_options[instrument_text]
                
                if drum:
                    drum.form = form_val
                    drum.diameter = diameter
                    drum.musical_instrument = self.store.get_instrument(instrument_id)
                    drum.save()
                    messagebox.showinfo("Успех", "Барабан обновлен")
                else:
                    self.store.create_drum(form_val, diameter, instrument_id)
                    messagebox.showinfo("Успех", "Барабан добавлен")
                
                self.refresh_drums()
                form.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Диаметр должен быть числом")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка базы данных: {str(e)}")
        
        tk.Button(form, text="Сохранить", command=save).grid(row=3, columnspan=2, pady=10)
    
    def delete_drum(self):
        selected = self.drums_tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите барабан для удаления")
            return
        
        drum_id = self.drums_tree.item(selected[0])['values'][0]
        try:
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот барабан?"):
                self.store.delete_drum(drum_id)
                self.refresh_drums()
                messagebox.showinfo("Успех", "Барабан удален")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def add_flute(self):
        self.flute_form("Добавить флейту")
    
    def edit_flute(self):
        selected = self.flutes_tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите флейту для редактирования")
            return
        
        flute_id = self.flutes_tree.item(selected[0])['values'][0]
        flute = self.store.get_flute(flute_id)
        if flute:
            self.flute_form("Редактировать флейту", flute)
    
    def flute_form(self, title, flute=None):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.grab_set()
        
        instruments = self.store.get_all_instruments()
        instrument_options = {f"{i.id} - {i.body_color} {i.body_material}": i.id for i in instruments}
        
        tk.Label(form, text="Количество отверстий:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        holes_entry = tk.Entry(form, width=30)
        holes_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Способ держания:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        holder_entry = tk.Entry(form, width=30)
        holder_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form, text="Инструмент:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        instrument_var = tk.StringVar(form)
        instrument_combobox = ttk.Combobox(form, textvariable=instrument_var, values=list(instrument_options.keys()))
        instrument_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        if flute:
            holes_entry.insert(0, flute.count_hole)
            holder_entry.insert(0, flute.holder_method)
            for text, id in instrument_options.items():
                if id == flute.musical_instrument.id:
                    instrument_var.set(text)
                    break
        
        def save():
            holes_val = holes_entry.get()
            holder_val = holder_entry.get()
            instrument_text = instrument_var.get()
            
            if not holes_val or not holder_val or not instrument_text:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return
            
            try:
                holes = int(holes_val)
                instrument_id = instrument_options[instrument_text]
                
                if flute:
                    flute.count_hole = holes
                    flute.holder_method = holder_val
                    flute.musical_instrument = self.store.get_instrument(instrument_id)
                    flute.save()
                    messagebox.showinfo("Успех", "Флейта обновлена")
                else:
                    self.store.create_flute(holes, holder_val, instrument_id)
                    messagebox.showinfo("Успех", "Флейта добавлена")
                
                self.refresh_flutes()
                form.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Количество отверстий должно быть числом")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка базы данных: {str(e)}")
        
        tk.Button(form, text="Сохранить", command=save).grid(row=3, columnspan=2, pady=10)
    
    def delete_flute(self):
        selected = self.flutes_tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите флейту для удаления")
            return
        
        flute_id = self.flutes_tree.item(selected[0])['values'][0]
        try:
            if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту флейту?"):
                self.store.delete_flute(flute_id)
                self.refresh_flutes()
                messagebox.showinfo("Успех", "Флейта удалена")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    
    def on_exit(self):
        self.store.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicStoreApp(root)
    root.mainloop()
