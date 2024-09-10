import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from sheet import entrada, saida, plotar_entrada_saida

def select_file(label):
    caminho_arquivo = filedialog.askopenfilename()
    label.config(text=caminho_arquivo)
    return caminho_arquivo

def execute_functions():
    nfe_entrada_path = label_nfe_entrada.cget("text")
    nfse_tomado_path = label_nfse_tomado.cget("text")
    nfe_saida_path = label_nfe_saida.cget("text")
    nfse_prestado_path = label_nfse_prestado.cget("text")
    sat_path = label_sat.cget("text")

    if not all([nfe_entrada_path, nfse_tomado_path, nfe_saida_path, nfse_prestado_path, sat_path]):
        messagebox.showerror("Erro", "Por favor, selecione todos os arquivos.")
        return

    nfe_entrada = entrada(nfe_entrada_path, nfse_tomado_path)
    nfe_saida = saida(nfe_saida_path, nfse_prestado_path, sat_path)
    plotar_entrada_saida(nfe_entrada, nfe_saida)
    messagebox.showinfo("Sucesso", "Funções executadas com sucesso!")

# Configuração da janela principal
root = tk.Tk()
root.title("Seleção de Arquivos")

# Centralizar a janela na tela
window_width = 600
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Estilo dos widgets
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 10, "bold")
padding = {'padx': 10, 'pady': 5}

# Botões e labels para seleção de arquivos
tk.Label(root, text="NFE Entrada:", font=label_font).grid(row=0, column=0, **padding)
label_nfe_entrada = tk.Label(root, text="", width=50, relief="sunken", anchor="w")
label_nfe_entrada.grid(row=0, column=1, **padding)
tk.Button(root, text="Selecionar", font=button_font, command=lambda: select_file(label_nfe_entrada)).grid(row=0, column=2, **padding)

tk.Label(root, text="NFSE Tomado:", font=label_font).grid(row=1, column=0, **padding)
label_nfse_tomado = tk.Label(root, text="", width=50, relief="sunken", anchor="w")
label_nfse_tomado.grid(row=1, column=1, **padding)
tk.Button(root, text="Selecionar", font=button_font, command=lambda: select_file(label_nfse_tomado)).grid(row=1, column=2, **padding)

tk.Label(root, text="NFE Saída:", font=label_font).grid(row=2, column=0, **padding)
label_nfe_saida = tk.Label(root, text="", width=50, relief="sunken", anchor="w")
label_nfe_saida.grid(row=2, column=1, **padding)
tk.Button(root, text="Selecionar", font=button_font, command=lambda: select_file(label_nfe_saida)).grid(row=2, column=2, **padding)

tk.Label(root, text="NFSE Prestado:", font=label_font).grid(row=3, column=0, **padding)
label_nfse_prestado = tk.Label(root, text="", width=50, relief="sunken", anchor="w")
label_nfse_prestado.grid(row=3, column=1, **padding)
tk.Button(root, text="Selecionar", font=button_font, command=lambda: select_file(label_nfse_prestado)).grid(row=3, column=2, **padding)

tk.Label(root, text="SAT:", font=label_font).grid(row=4, column=0, **padding)
label_sat = tk.Label(root, text="", width=50, relief="sunken", anchor="w")
label_sat.grid(row=4, column=1, **padding)
tk.Button(root, text="Selecionar", font=button_font, command=lambda: select_file(label_sat)).grid(row=4, column=2, **padding)

# Botão para executar as funções
tk.Button(root, text="Executar", font=button_font, command=execute_functions).grid(row=5, column=0, columnspan=3, pady=20)

# Iniciar a interface
root.mainloop()