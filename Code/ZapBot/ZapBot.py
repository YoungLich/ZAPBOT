import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from zapbot_code import processar_envio

# ------------Configurações do Botão------------#

button_config = {
    "zapbot": {
        "text": "ZAPBOT",
        "bg_color": "#3CB371",
        "fg_color": "black",
        "font": ("Arial", 15, "bold"),
        "width": 15,
        "height": 2,
        "position": "center"
    }
}

# ------------ZapBot------------#

def format_time(event):
    time_str = time_entry.get()
    if len(time_str) == 4 and time_str.isdigit():
        formatted_time = f"{time_str[:2]}:{time_str[2:]}"
        time_entry.delete(0, tk.END)
        time_entry.insert(0, formatted_time)

def open_whatsapp_window():
    global whatsapp_window  # Declare whatsapp_window as global
    global time_entry  # Declare time_entry como global
    whatsapp_window = tk.Toplevel(root)
    whatsapp_window.title("ZAPBOT")
    whatsapp_window.geometry("600x600")
    whatsapp_window.configure(bg="#5eb294")

    contact_label = tk.Label(whatsapp_window, text="Nome do Contato:", bg="#5eb294")
    contact_label.pack(pady=5)
    contact_entry = tk.Entry(whatsapp_window, width=30)
    contact_entry.pack(pady=5)

    def save_contact():
        contact_name = contact_entry.get()
        if contact_name:
            with open("saved_contacts.txt", "a") as f:
                f.write(contact_name + "\n")
            contact_entry.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")
        else:
            messagebox.showerror("Erro", "O nome do contato não pode estar vazio.")

    save_contact_button = tk.Button(whatsapp_window, text="Salvar Contato", command=save_contact)
    save_contact_button.pack(pady=5)

    def load_contacts():
        try:
            with open("saved_contacts.txt", "r") as f:
                contacts = f.readlines()
            return [contact.strip() for contact in contacts]
        except FileNotFoundError:
            return []

    def delete_contact(selected_contact):
        contacts = load_contacts()
        if selected_contact in contacts:
            contacts.remove(selected_contact)
            with open("saved_contacts.txt", "w") as f:
                for contact in contacts:
                    f.write(contact + "\n")
            messagebox.showinfo("Sucesso", "Contato excluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Contato não encontrado.")
    
    def select_contacts():
        contacts = load_contacts()
        if not contacts:
            messagebox.showinfo("Sem Contatos", "Nenhum contato salvo encontrado.")
            return
        
        select_window = tk.Toplevel(whatsapp_window)
        select_window.title("Selecionar Contatos")
        select_window.geometry("300x400")
        
        contact_listbox = tk.Listbox(select_window, selectmode=tk.MULTIPLE, width=40, height=15)
        for contact in contacts:
            contact_listbox.insert(tk.END, contact)
        contact_listbox.pack(pady=10)

        def confirm_selection():
            selected_indices = contact_listbox.curselection()
            if len(selected_indices) > 10:
                messagebox.showwarning("Limite Excedido", "Você pode selecionar no máximo 10 contatos.")
                return

            selected_contacts = [contacts[i] for i in selected_indices]
            if selected_contacts:
                contacts_var.set(', '.join(selected_contacts))
                select_window.destroy()
            else:
                messagebox.showinfo("Nenhum Contato Selecionado", "Nenhum contato foi selecionado.")
        
        def delete_selected_contact():
            selected_index = contact_listbox.curselection()
            if selected_index:
                selected_contact = contacts[selected_index[0]]
                delete_contact(selected_contact)
                contact_listbox.delete(selected_index)
            else:
                messagebox.showwarning("Nenhum Selecionado", "Selecione um contato para excluir.")

        confirm_button = tk.Button(select_window, text="Confirmar", command=confirm_selection)
        confirm_button.pack(pady=5)

        delete_button = tk.Button(select_window, text="Excluir Contato", command=delete_selected_contact)
        delete_button.pack(pady=5)

    select_contacts_button = tk.Button(whatsapp_window, text="Selecionar Contatos", command=select_contacts)
    select_contacts_button.pack(pady=5)

    contacts_var = tk.StringVar()
    contacts_display = tk.Entry(whatsapp_window, textvariable=contacts_var, width=50, state="readonly")
    contacts_display.pack(pady=5)

    message_label = tk.Label(whatsapp_window, text="Mensagem:", bg="#5eb294")
    message_label.pack(pady=5)
    message_entry = tk.Text(whatsapp_window, width=50, height=5)
    message_entry.pack(pady=5)

    time_label = tk.Label(whatsapp_window, text="Horário de Envio (HH:MM):", bg="#5eb294")
    time_label.pack(pady=5)
    time_entry = tk.Entry(whatsapp_window, width=10)
    time_entry.pack(pady=5)

    time_entry.bind("<KeyRelease>", format_time)  # Vincula a função de formatação

    def select_files(file_display):
        files = filedialog.askopenfilenames(
            title="Selecione os Arquivos",
            filetypes=[("All Files", "*.*"), ("PDF Files", "*.pdf"), ("PNG Files", "*.png"), ("JPG Files", "*.jpg"), ("Word Documents", "*.docx"), ("Excel Files", "*.xlsx")]
        )
        if files:
            file_paths = '\n'.join(files)
            file_display.config(state="normal")
            file_display.delete(1.0, tk.END)
            file_display.insert(tk.END, file_paths)
            file_display.config(state="disabled")

    def enviar_mensagem():
        selected_contacts = contacts_var.get().split(', ')
        message = message_entry.get("1.0", tk.END).strip()
        media_path = file_display.get("1.0", tk.END).strip()
        
        if not selected_contacts or not message:
            messagebox.showerror("Erro", "Por favor, selecione contatos e insira uma mensagem.")
            return

        for contact in selected_contacts:
            processar_envio(contact, message, media_path)
        messagebox.showinfo("Sucesso", "Mensagens enviadas com sucesso!")

    send_button = tk.Button(whatsapp_window, text="Enviar Mensagem", command=enviar_mensagem)
    send_button.pack(pady=10)

    file_display = tk.Text(whatsapp_window, height=5, width=50, state="disabled", wrap="word")
    file_display.pack(pady=5)

    select_files_button = tk.Button(whatsapp_window, text="Selecionar Arquivos", command=lambda: select_files(file_display))
    select_files_button.pack(pady=5)

# ------------Janela Principal------------#

root = tk.Tk()
root.title("ZAPBOT")
root.geometry("580x380")
root.configure(bg="#202a50")

# Impede que a janela seja redimensionada
root.resizable(False, False)

button_config = {
    "zapbot": {
        "text": "ZAPBOT",
        "bg_color": "#3CB371",
        "fg_color": "black",
        "font": ("Arial", 15, "bold"),
        "width": 15,
        "height": 2,
        "position": "center"
    }
}

def open_zapbot_window():
    open_whatsapp_window()

# Centralizar o botão na grid
zapbot_button = tk.Button(
    root,
    text=button_config["zapbot"]["text"],
    command=open_zapbot_window,
    bg=button_config["zapbot"]["bg_color"],
    fg=button_config["zapbot"]["fg_color"],
    font=button_config["zapbot"]["font"],
    width=button_config["zapbot"]["width"],
    height=button_config["zapbot"]["height"]
)

# Corrigido: Centralizando o botão e a imagem na grid
zapbot_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Redimensiona a imagem antes de convertê-la para ImageTk.PhotoImage
zapbot_image_path = "img/ZapBot.png"
zapbot_image = Image.open(zapbot_image_path)
zapbot_image = zapbot_image.resize((186, 239), Image.LANCZOS)
zapbot_image_tk = ImageTk.PhotoImage(zapbot_image)

zapbot_image_label = tk.Label(root, image=zapbot_image_tk, bg="#202a50")

zapbot_image_label.grid(row=1, column=1, padx=10, pady=10)

# Configura a grid para expandir e encher o espaço
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
