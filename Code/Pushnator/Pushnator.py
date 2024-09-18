import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pushnator_incluir import save_login_data, load_login_data, automatizar_pje
from pushnator_excluir import excluir_processos

def show_login_window(action):
    login_window = tk.Toplevel(root)
    login_window.title("PUSHNATOR")
    login_window.geometry("500x350")  # Ajustado para acomodar o novo layout
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

    result_path = 'C:/Users/52312819805/Desktop/BITBOOP/output/Incluidos/resultado_inclusao_processos'  # Caminho padrão de resultados
    planilha_path = 'C:/Users/52312819805/Desktop/BITBOOP/Code/Pushnator/Inserir_Push.xlsx'  # Caminho padrão da planilha

    result_path_var = tk.StringVar(value=result_path)
    planilha_path_var = tk.StringVar(value=planilha_path)

    result_label = tk.Label(login_window, text="Caminho para salvar o resultado:", bg="#F0F0F0")
    result_label.pack(pady=5)
    result_entry = tk.Entry(login_window, textvariable=result_path_var, width=50, state='readonly')
    result_entry.pack(pady=5)

    planilha_label = tk.Label(login_window, text="Caminho do arquivo de planilha:", bg="#F0F0F0")
    planilha_label.pack(pady=5)
    planilha_entry = tk.Entry(login_window, textvariable=planilha_path_var, width=50, state='readonly')
    planilha_entry.pack(pady=5)

    save_credentials_var = tk.IntVar()
    save_credentials_check = tk.Checkbutton(login_window, text="Salvar credenciais", variable=save_credentials_var, bg="#F0F0F0")
    save_credentials_check.pack(pady=10)

    def execute_automation():
        username = username_entry.get()
        password = password_entry.get()

        if save_credentials_var.get():
            save_login_data(username, password)

        try:
            if action == "incluir":
                automatizar_pje(username, password, planilha_path, result_path + 'resultado_inclusao_processos.xlsx')
            elif action == "excluir":
                excluir_processos(username, password, planilha_path, result_path + 'resultado_exclusao_processos.xlsx')
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

root = tk.Tk()
root.title("PUSHNATOR")
root.geometry("580x380")
root.configure(bg="#202a50")

root.resizable(False, False)

button_config = {
    "pushnator": {
        "text": "PUSHNATOR",
        "bg_color": "black",
        "fg_color": "white",
        "font": ("Arial", 15, "bold"),
        "width": 15,
        "height": 2,
        "position": "center"
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

site_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

pushnator_image_path = "img/Pushnator.png"
pushnator_image = Image.open(pushnator_image_path)
pushnator_image = pushnator_image.resize((186, 239), Image.LANCZOS)
pushnator_image_tk = ImageTk.PhotoImage(pushnator_image)

pushnator_image_label = tk.Label(root, image=pushnator_image_tk, bg="#202a50")

pushnator_image_label.grid(row=1, column=1, padx=10, pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()
