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
        "width": 2,
        "height": 2,
        "position": "center"
    }
}

# ------------Funções do ZapBot------------#

def format_time(event):
    time_str = time_entry.get()
    if len(time_str) == 4 and time_str.isdigit():
        formatted_time = f"{time_str[:2]}:{time_str[2:]}"
        time_entry.delete(0, tk.END)
        time_entry.insert(0, formatted_time)

def load_contacts():
    try:
        with open("saved_contacts.txt", "r") as f:
            contacts = f.readlines()
        return [contact.strip() for contact in contacts]
    except FileNotFoundError:
        return []

def save_contact():
    contact_name = contact_entry.get()
    if contact_name and contact_name != "Digite o nome do contato..":
        with open("saved_contacts.txt", "a") as f:
            f.write(contact_name + "\n")
        contact_entry.delete(0, tk.END)
        contact_entry.insert(0, "Digite o nome do contato..")  # Reset placeholder
        messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")
    else:
        messagebox.showerror("Erro", "O nome do contato não pode estar vazio.")

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
        if len(selected_indices) > 50:
            messagebox.showwarning("Limite Excedido", "Você pode selecionar no máximo 50 contatos.")
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
    
    if not selected_contacts or not message or message == "Mensagem..":
        messagebox.showerror("Erro", "Por favor, selecione contatos e insira uma mensagem.")
        return

    for contact in selected_contacts:
        processar_envio(contact, message, media_path)
    messagebox.showinfo("Sucesso", "Mensagens enviadas com sucesso!")

def open_whatsapp_window():
    global whatsapp_window  # Declare whatsapp_window as global
    global time_entry  # Declare time_entry como global
    global contact_entry  # Declare contact_entry como global
    global message_entry  # Declare message_entry como global
    global contacts_var  # Declare contacts_var como global
    global file_display  # Declare file_display como global

    whatsapp_window = tk.Toplevel(root)
    whatsapp_window.title("ZAPBOT")
    whatsapp_window.geometry("550x450")
    whatsapp_window.configure(bg="#5eb294")

    # Frame para contatos
    contact_frame = tk.Frame(whatsapp_window, bg="#5eb294")
    contact_frame.pack(pady=5)

    # Botão "Salvar Contato"
    save_contact_button = tk.Button(contact_frame, text="Salvar Contato", command=save_contact)
    save_contact_button.pack(side=tk.LEFT)

    # Espaçamento entre o botão e o input
    tk.Label(contact_frame, bg="#5eb294").pack(side=tk.LEFT, padx=(5, 5))  # Espaço vazio

    # Input para o nome do contato
    contact_entry = tk.Entry(contact_frame, width=30)
    contact_entry.insert(0, "Digite o nome do contato..")  # Placeholder
    contact_entry.bind("<FocusIn>", lambda e: contact_entry.delete(0, tk.END) if contact_entry.get() == "Digite o nome do contato.." else None)
    contact_entry.bind("<FocusOut>", lambda e: contact_entry.insert(0, "Digite o nome do contato.." ) if contact_entry.get() == "" else None)
    contact_entry.pack(side=tk.LEFT, padx=(0, 5))

    # Frame para seleção de contatos
    select_contacts_frame = tk.Frame(whatsapp_window, bg="#5eb294")
    select_contacts_frame.pack(pady=5)

    # Botão "Selecionar Contatos"
    contacts_var = tk.StringVar()
    select_contacts_button = tk.Button(select_contacts_frame, text="Selecionar Contatos", command=select_contacts)
    select_contacts_button.pack(side=tk.LEFT, padx=(0, 5))

    # Input para exibir contatos selecionados
    contacts_display = tk.Entry(select_contacts_frame, textvariable=contacts_var, width=40, state="readonly")
    contacts_display.pack(side=tk.LEFT)

    # Frame para exibir caminho dos arquivos selecionados
    file_frame = tk.Frame(whatsapp_window, bg="#5eb294")
    file_frame.pack(pady=5)

    file_display = tk.Text(file_frame, height=5, width=50, state="disabled", wrap="word")
    file_display.pack(side=tk.LEFT)

    # Botão para selecionar arquivos
    select_files_button = tk.Button(file_frame, text="Selecionar Arquivos", command=lambda: select_files(file_display))
    select_files_button.pack(side=tk.LEFT, padx=(5, 0))

    # Frame para a mensagem e horário
    message_frame = tk.Frame(whatsapp_window, bg="#5eb294")
    message_frame.pack(pady=5)

    # Input de mensagem
    message_entry = tk.Text(message_frame, width=40, height=15)  # Aumentando a altura
    message_entry.insert(tk.END, "Mensagem..")  # Placeholder
    message_entry.bind("<FocusIn>", lambda e: message_entry.delete("1.0", tk.END) if message_entry.get("1.0", "end-1c") == "Mensagem.." else None)
    message_entry.bind("<FocusOut>", lambda e: message_entry.insert(tk.END, "Mensagem..") if message_entry.get("1.0", "end-1c") == "" else None)
    message_entry.pack(side=tk.LEFT, padx=(0, 5))

    # Input para informar o horário
    time_entry_frame = tk.Frame(message_frame, bg="#5eb294")
    time_entry_frame.pack(side=tk.LEFT)

    time_entry = tk.Entry(time_entry_frame, width=10)
    time_entry.insert(0, "00:00")  # Placeholder
    time_entry.bind("<FocusIn>", lambda e: time_entry.delete(0, tk.END) if time_entry.get() == "00:00" else None)
    time_entry.bind("<FocusOut>", lambda e: time_entry.insert(0, "00:00") if time_entry.get() == "" else None)
    time_entry.pack(side=tk.LEFT)

    time_entry.bind("<KeyRelease>", format_time)  # Vincula a função de formatação

    # Botão "Enviar Mensagem"
    send_button = tk.Button(time_entry_frame, text="Enviar Mensagem", command=enviar_mensagem)
    send_button.pack(side=tk.LEFT, padx=(5, 0))

# ------------Janela Principal------------#

root = tk.Tk()
root.title("ZAPBOT")
root.geometry("580x380")
root.configure(bg="#202a50")

# Impede que a janela seja redimensionada
root.resizable(False, False)

# Centralizar o botão na grid
zapbot_button = tk.Button(
    root,
    text=button_config["zapbot"]["text"],
    command=open_whatsapp_window,
    bg=button_config["zapbot"]["bg_color"],
    fg=button_config["zapbot"]["fg_color"],
    font=button_config["zapbot"]["font"],
    width=button_config["zapbot"]["width"],
    height=button_config["zapbot"]["height"]
)

zapbot_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Redimensiona a imagem antes de convertê-la para ImageTk.PhotoImage
zapbot_image_path = "img/Zapbot.png"
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
