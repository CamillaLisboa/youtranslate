import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox, Label, Entry, Button, Frame, Toplevel, Text, END
from PIL import Image, ImageTk

# Função para conectar ao banco de dados e criar as tabelas de usuários e palavras
def create_database():
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            english_word TEXT NOT NULL,
            portuguese_translation TEXT NOT NULL,
            english_meaning TEXT,
            portuguese_meaning TEXT
        )
    ''')

    if not user_exists('admin@admin'):
        register_user('admin@admin', 'admin123')
    if not user_exists('user@user'):
        register_user('user@user', 'user123')
    
    conn.commit()
    conn.close()

def register_user(email, password):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
    conn.commit()
    conn.close()

def user_exists(email):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def authenticate_user(email, password):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hashed_password))
    user = cursor.fetchone()
    conn.close()
    
    return user is not None

def add_translation(english_word, portuguese_translation, english_meaning, portuguese_meaning):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO translations (english_word, portuguese_translation, english_meaning, portuguese_meaning)
        VALUES (?, ?, ?, ?)
    ''', (english_word, portuguese_translation, english_meaning, portuguese_meaning))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Palavra adicionada com sucesso!")

def view_translations():
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM translations')
    translations = cursor.fetchall()
    conn.close()
    
    result = ""
    for translation in translations:
        result += f"ID: {translation[0]}\n"
        result += f"Inglês: {translation[1]}, Tradução: {translation[2]}\n"
        result += f"Significado em inglês: {translation[3]}, Significado em português: {translation[4]}\n\n"
    return result

def update_translation(id, english_word, portuguese_translation, english_meaning, portuguese_meaning):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE translations
        SET english_word = ?, portuguese_translation = ?, english_meaning = ?, portuguese_meaning = ?
        WHERE id = ?
    ''', (english_word, portuguese_translation, english_meaning, portuguese_meaning, id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Tradução atualizada com sucesso!")

def delete_translation(id):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM translations WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Tradução deletada com sucesso!")

def search_translation(query):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM translations
        WHERE english_word = ? OR portuguese_translation = ?
    ''', (query, query))
    translation = cursor.fetchone()
    conn.close()

    if translation:
        result = f"ID: {translation[0]}\n"
        result += f"Inglês: {translation[1]}, Tradução: {translation[2]}\n"
        result += f"Significado em inglês: {translation[3]}, Significado em português: {translation[4]}\n"
    else:
        result = "Nenhuma tradução encontrada para essa palavra."
    
    return result

# Funções de interface gráfica
def show_admin_interface():
    admin_window = Toplevel(root)
    admin_window.title("Admin - Gerenciamento de Traduções")
    admin_window.geometry("600x400")

    def on_view():
        result_text.delete(1.0, END)
        result_text.insert(END, view_translations())
    
    def on_add():
        add_translation(entry_english.get(), entry_portuguese.get(), entry_english_meaning.get(), entry_portuguese_meaning.get())

    def on_edit():
        try:
            translation_id = int(entry_id.get())
            update_translation(translation_id, entry_english.get(), entry_portuguese.get(), entry_english_meaning.get(), entry_portuguese_meaning.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um ID válido")

    def on_delete():
        try:
            translation_id = int(entry_id.get())
            delete_translation(translation_id)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um ID válido")
    
    # Layout para admin
    Label(admin_window, text="Palavra em Inglês").grid(row=0, column=0)
    entry_english = Entry(admin_window)
    entry_english.grid(row=0, column=1)

    Label(admin_window, text="Tradução em Português").grid(row=1, column=0)
    entry_portuguese = Entry(admin_window)
    entry_portuguese.grid(row=1, column=1)

    Label(admin_window, text="Significado em Inglês").grid(row=2, column=0)
    entry_english_meaning = Entry(admin_window)
    entry_english_meaning.grid(row=2, column=1)

    Label(admin_window, text="Significado em Português").grid(row=3, column=0)
    entry_portuguese_meaning = Entry(admin_window)
    entry_portuguese_meaning.grid(row=3, column=1)

    Label(admin_window, text="ID de Tradução (para editar ou excluir)").grid(row=4, column=0)
    entry_id = Entry(admin_window)
    entry_id.grid(row=4, column=1)

    # Botões para ações
    Button(admin_window, text="Adicionar", command=on_add).grid(row=5, column=1)
    Button(admin_window, text="Visualizar", command=on_view).grid(row=5, column=2)
    Button(admin_window, text="Editar", command=on_edit).grid(row=6, column=1)
    Button(admin_window, text="Excluir", command=on_delete).grid(row=6, column=2)

    result_text = Text(admin_window, width=70, height=15)
    result_text.grid(row=7, column=0, columnspan=3)

def show_user_interface():
    user_window = Toplevel(root)
    user_window.title("User - Consulta de Traduções")
    user_window.geometry("400x300")

    def on_search():
        result_text.delete(1.0, END)
        result_text.insert(END, search_translation(entry_search.get()))
    
    Label(user_window, text="Buscar Palavra").pack()
    entry_search = Entry(user_window)
    entry_search.pack()

    Button(user_window, text="Buscar", command=on_search).pack()

    result_text = Text(user_window, width=50, height=10)
    result_text.pack()

def on_login():
    email = entry_email.get()
    password = entry_password.get()
    
    if authenticate_user(email, password):
        if email == 'admin@admin':
            show_admin_interface()
        elif email == 'user@user':
            show_user_interface()
    else:
        messagebox.showerror("Erro", "Acesso negado")

# Configuração da tela principal
root = tk.Tk()
root.title("You Translate")
root.geometry("400x500")

# Carregar a imagem
image = Image.open("images/You Translate.png")
photo = ImageTk.PhotoImage(image)
Label(root, image=photo).pack()

Label(root, text="E-mail").pack()
entry_email = Entry(root)
entry_email.pack()

Label(root, text="Senha").pack()
entry_password = Entry(root, show="*")
entry_password.pack()

Button(root, text="Login", command=on_login).pack()

# Criar banco de dados e tabelas se não existirem
create_database()

root.mainloop()
