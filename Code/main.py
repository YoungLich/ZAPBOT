import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pushnator_incluir import save_login_data, load_login_data, execute_site_automation
from pushnator_excluir import excluir_processos, execute_site_automation  # Ajustado para importar apenas funções existentes
from zapbot import processar_envio

#------------Pushnator------------#

def show_login_window(action):
    login_window = tk.Toplevel(root)
    login_window.title("PUSHNATOR")
    login_window.geometry("600x300")
    login_window.configure(bg="#F0F0F0")

    username_label = tk.Label(login_window, text="CPF/CNPJ:", bg="#F0F0F0")
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window, width=50)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Senha:", bg="#F0F0F0")
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, width=50, show="*")
    password_entry.pack(pady=5)

    saved_username, saved_password = load_login_data()
    if saved_username and saved_password:
        username_entry.insert(0, saved_username)
        password_entry.insert(0, saved_password)

    def select_directory():
        directory = filedialog.askdirectory(title="Selecione o Diretório para Salvar a Planilha")
        if directory:
            directory_var.set(directory)
            directory_display.config(state="normal")
            directory_display.delete(1.0, tk.END)
            directory_display.insert(tk.END, directory)
            directory_display.config(state="disabled")

    directory_var = tk.StringVar()
    directory_button = tk.Button(login_window, text="Selecionar Diretório", command=select_directory)
    directory_button.pack(pady=5)

    directory_display = tk.Text(login_window, height=2, width=50, state="disabled", wrap="word")
    directory_display.pack(pady=5)

    save_credentials_var = tk.IntVar()
    save_credentials_check = tk.Checkbutton(login_window, text="Salvar credenciais", variable=save_credentials_var, bg="#F0F0F0")
    save_credentials_check.pack(pady=10)

    def execute_automation():
        username = username_entry.get()
        password = password_entry.get()
        directory = directory_var.get()

        if save_credentials_var.get():
            save_login_data(username, password)

        try:
            if action == "incluir":
                execute_site_automation(username, password, directory)
            elif action == "excluir":
                excluir_processos(username, password, directory)  # Chamada correta da função
            messagebox.showinfo("Sucesso", "Automação concluída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    execute_button = tk.Button(login_window, text="Executar", command=execute_automation)
    execute_button.pack(pady=10)

def open_inclusion_exclusion_window():
    inclusion_exclusion_window = tk.Toplevel(root)
    inclusion_exclusion_window.title("Incluir/Excluir Processos")
    inclusion_exclusion_window.geometry("400x200")
    inclusion_exclusion_window.configure(bg="#F0F0F0")

    def include_processes():
        show_login_window("incluir")

    def exclude_processes():
        show_login_window("excluir")

    include_button = tk.Button(inclusion_exclusion_window, text="Incluir Processos", command=include_processes)
    include_button.pack(pady=20)

    exclude_button = tk.Button(inclusion_exclusion_window, text="Excluir Processos", command=exclude_processes)
    exclude_button.pack(pady=20)

#------------ZapBot------------#

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

#------------Main Window------------#

root = tk.Tk()
root.title("BITBOOP")
root.geometry("580x380")
root.configure(bg="#202a50")

# Impede que a janela seja redimensionada
root.resizable(False, False)

button_config = {
    "pushnator": {
        "text": "PUSHNATOR",
        "bg_color": "black",
        "fg_color": "white",
        "font": ("Arial", 15, "bold"),
        "width": 15,
        "height": 2,
        "position": "left"
    },
    "zapbot": {
        "text": "ZAPBOT",
        "bg_color": "#3CB371",
        "fg_color": "black",
        "font": ("Arial", 15, "bold"),
        "width": 15,
        "height": 2,
        "position": "right"
    }
}

def open_pushnator_window():
    open_inclusion_exclusion_window()

site_button = tk.Button(
    root,
    text=button_config["pushnator"]["text"],
    command=open_pushnator_window,
    bg=button_config["pushnator"]["bg_color"],
    fg=button_config["pushnator"]["fg_color"],
    font=button_config["pushnator"]["font"],
    width=button_config["pushnator"]["width"],
    height=button_config["pushnator"]["height"]
)
site_button.grid(row=0, column=0, padx=50, pady=10, sticky="w")

whatsapp_button = tk.Button(
    root,
    text=button_config["zapbot"]["text"],
    command=open_whatsapp_window,
    bg=button_config["zapbot"]["bg_color"],
    fg=button_config["zapbot"]["fg_color"],
    font=button_config["zapbot"]["font"],
    width=button_config["zapbot"]["width"],
    height=button_config["zapbot"]["height"]
)
whatsapp_button.grid(row=0, column=1, padx=50, pady=10, sticky="e")

pushnator_image_path = "img/Pushnator.png"
pushnator_image = Image.open(pushnator_image_path)
pushnator_image_tk = ImageTk.PhotoImage(pushnator_image)
pushnator_image = pushnator_image.resize((186, 239), Image.LANCZOS)

zapbot_image_path = "img/ZapBot.png"
zapbot_image = Image.open(zapbot_image_path)
zapbot_image_tk = ImageTk.PhotoImage(zapbot_image)
zapbot_image = zapbot_image.resize((218, 269), Image.LANCZOS)

pushnator_image_tk = ImageTk.PhotoImage(pushnator_image)
zapbot_image_tk = ImageTk.PhotoImage(zapbot_image)

pushnator_image_label = tk.Label(root, image=pushnator_image_tk, bg="#202a50")
pushnator_image_label.grid(row=1, column=0, padx=10, pady=10)

zapbot_image_label = tk.Label(root, image=zapbot_image_tk, bg="#202a50")
zapbot_image_label.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
