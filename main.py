import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pushnator import save_login_data, load_login_data, execute_site_automation
from zapbot import processar_envio


def open_site_window():
    site_window = tk.Toplevel(root)
    site_window.title("PUSHNATOR")
    site_window.geometry("600x300")
    site_window.configure(bg="#F0F0F0")

    username_label = tk.Label(site_window, text="CPF/CNPJ:", bg="#F0F0F0")
    username_label.pack(pady=5)
    username_entry = tk.Entry(site_window, width=50)
    username_entry.pack(pady=5)

    password_label = tk.Label(site_window, text="Senha:", bg="#F0F0F0")
    password_label.pack(pady=5)
    password_entry = tk.Entry(site_window, width=50, show="*")
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
    directory_button = tk.Button(site_window, text="Selecionar Diretório", command=select_directory)
    directory_button.pack(pady=5)

    directory_display = tk.Text(site_window, height=2, width=50, state="disabled", wrap="word")
    directory_display.pack(pady=5)

    save_credentials_var = tk.IntVar()
    save_credentials_check = tk.Checkbutton(site_window, text="Salvar credenciais", variable=save_credentials_var, bg="#F0F0F0")
    save_credentials_check.pack(pady=10)

    def execute_automation():
        username = username_entry.get()
        password = password_entry.get()
        directory = directory_var.get()

        if save_credentials_var.get():
            save_login_data(username, password)

        try:
            execute_site_automation(username, password, directory)
            messagebox.showinfo("Sucesso", "Automação concluída com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    execute_button = tk.Button(site_window, text="LOGIN", command=execute_automation)
    execute_button.pack(pady=10)

def open_whatsapp_window():
    whatsapp_window = tk.Toplevel(root)
    whatsapp_window.title("ZAPBOT")
    whatsapp_window.geometry("600x500")
    whatsapp_window.configure(bg="#E0F7FA")

    phone_label = tk.Label(whatsapp_window, text="Número de Telefone:", bg="#E0F7FA")
    phone_label.pack(pady=5)
    phone_entry = tk.Entry(whatsapp_window, width=30)
    phone_entry.pack(pady=5)

    message_label = tk.Label(whatsapp_window, text="Mensagem:", bg="#E0F7FA")
    message_label.pack(pady=5)
    message_entry = tk.Text(whatsapp_window, width=50, height=5)
    message_entry.pack(pady=5)

    time_label = tk.Label(whatsapp_window, text="Horário de Envio (HH:MM):", bg="#E0F7FA")
    time_label.pack(pady=5)
    time_entry = tk.Entry(whatsapp_window, width=10)
    time_entry.pack(pady=5)

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

    def send_files(file_display):
        files = file_display.get("1.0", tk.END).strip().split('\n')
        if files:
            # Adaptar esta função se necessário
            pass

    def enviar_mensagem():
        phone_number = phone_entry.get()
        message = message_entry.get("1.0", tk.END).strip()
        media_path = file_display.get("1.0", tk.END).strip()
        if not phone_number or not message:
            messagebox.showerror("Erro", "Número de telefone e mensagem são obrigatórios.")
            return
        processar_envio(phone_number, message, media_path)
        messagebox.showinfo("Sucesso", "Mensagem e mídia enviadas com sucesso!")

    schedule_button = tk.Button(whatsapp_window, text="Enviar", command=enviar_mensagem)
    schedule_button.pack(pady=20)

    select_files_button = tk.Button(whatsapp_window, text="Selecionar Arquivos", command=lambda: select_files(file_display))
    select_files_button.pack(pady=5)

    file_display = tk.Text(whatsapp_window, height=8, width=50, state="disabled", wrap="word")
    file_display.pack(pady=5)

    send_files_button = tk.Button(whatsapp_window, text="Enviar Arquivos", command=lambda: send_files(file_display))
    send_files_button.pack(pady=5)

# Cria a janela principal apenas uma vez
root = tk.Tk()
root.title("BITBOOP")
root.geometry("600x500")
root.configure(bg="#191970")

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

site_button = tk.Button(
    root,
    text=button_config["pushnator"]["text"],
    command=open_site_window,
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
pushnator_image = pushnator_image.resize((186, 239), Image.LANCZOS)

zapbot_image_path = "img/ZapBot.png"
zapbot_image = Image.open(zapbot_image_path)
zapbot_image = zapbot_image.resize((218, 269), Image.LANCZOS)

pushnator_image_tk = ImageTk.PhotoImage(pushnator_image)
zapbot_image_tk = ImageTk.PhotoImage(zapbot_image)

pushnator_image_label = tk.Label(root, image=pushnator_image_tk, bg="#191970")
pushnator_image_label.grid(row=1, column=0, padx=10, pady=10)

zapbot_image_label = tk.Label(root, image=zapbot_image_tk, bg="#191970")
zapbot_image_label.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
