"""
HWID Manager - Interface Graphique Moderne
Interface utilisateur pour gérer et modifier le Hardware ID
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from hwid_manager import HWIDManager
import uuid

class HWIDManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HWID Manager - Hardware ID Tool")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e2e')
        
        self.manager = HWIDManager()
        self.setup_styles()
        self.create_widgets()
        
        # Charge les informations au démarrage
        self.refresh_info()
    
    def setup_styles(self):
        """Configure les styles de l'interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Couleurs modernes
        bg_dark = '#1e1e2e'
        bg_medium = '#2a2a3e'
        bg_light = '#3a3a4e'
        accent = '#89b4fa'
        text_color = '#cdd6f4'
        
        # Style pour les frames
        style.configure('Dark.TFrame', background=bg_dark)
        style.configure('Medium.TFrame', background=bg_medium)
        
        # Style pour les labels
        style.configure('Title.TLabel', 
                       background=bg_dark, 
                       foreground=accent,
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Info.TLabel',
                       background=bg_medium,
                       foreground=text_color,
                       font=('Consolas', 10))
        
        # Style pour les boutons
        style.configure('Action.TButton',
                       background=accent,
                       foreground='#1e1e2e',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Action.TButton',
                 background=[('active', '#b4befe')])
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # En-tête
        header_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame,
                               text="🔐 HWID MANAGER",
                               style='Title.TLabel')
        title_label.pack()
        
        warning_label = tk.Label(header_frame,
                                text="⚠️ Utilisation à des fins éducatives uniquement",
                                bg='#1e1e2e',
                                fg='#f38ba8',
                                font=('Segoe UI', 9, 'italic'))
        warning_label.pack()
        
        # Vérification admin
        admin_status = "✅ Mode Administrateur" if self.manager.is_admin() else "❌ Mode Normal (certaines fonctions désactivées)"
        admin_label = tk.Label(header_frame,
                              text=admin_status,
                              bg='#1e1e2e',
                              fg='#a6e3a1' if self.manager.is_admin() else '#fab387',
                              font=('Segoe UI', 9))
        admin_label.pack()
        
        # Frame pour les informations HWID
        info_frame = ttk.LabelFrame(main_frame,
                                   text=" 📋 Informations HWID Actuelles ",
                                   style='Medium.TFrame')
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Zone de texte pour afficher les informations
        self.info_text = scrolledtext.ScrolledText(info_frame,
                                                   height=15,
                                                   bg='#2a2a3e',
                                                   fg='#cdd6f4',
                                                   font=('Consolas', 10),
                                                   insertbackground='#89b4fa',
                                                   relief=tk.FLAT,
                                                   padx=10,
                                                   pady=10)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame pour les boutons d'action
        action_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Première ligne de boutons
        btn_row1 = ttk.Frame(action_frame, style='Dark.TFrame')
        btn_row1.pack(fill=tk.X, pady=5)
        
        self.create_button(btn_row1, "🔄 Actualiser", self.refresh_info).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.create_button(btn_row1, "🔧 Modifier GUID", self.modify_guid).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.create_button(btn_row1, "🔧 Modifier Product ID", self.modify_product_id).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Deuxième ligne de boutons
        btn_row2 = ttk.Frame(action_frame, style='Dark.TFrame')
        btn_row2.pack(fill=tk.X, pady=5)
        
        self.create_button(btn_row2, "💾 Sauvegarder Registre", self.backup_registry).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.create_button(btn_row2, "🔑 Générer HWID", self.generate_hwid).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.create_button(btn_row2, "🌐 Changer MAC", self.change_mac_address).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Troisième ligne de boutons
        btn_row3 = ttk.Frame(action_frame, style='Dark.TFrame')
        btn_row3.pack(fill=tk.X, pady=5)
        
        self.create_button(btn_row3, "🔐 Relancer en Admin", self.run_as_admin).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Frame pour les logs
        log_frame = ttk.LabelFrame(main_frame,
                                  text=" 📝 Journal d'activité ",
                                  style='Medium.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame,
                                                 height=8,
                                                 bg='#2a2a3e',
                                                 fg='#cdd6f4',
                                                 font=('Consolas', 9),
                                                 insertbackground='#89b4fa',
                                                 relief=tk.FLAT,
                                                 padx=10,
                                                 pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log("✅ HWID Manager démarré")
        if not self.manager.is_admin():
            self.log("⚠️ Certaines fonctions nécessitent des privilèges administrateur")
    
    def create_button(self, parent, text, command):
        """Crée un bouton stylisé"""
        btn = tk.Button(parent,
                       text=text,
                       command=command,
                       bg='#89b4fa',
                       fg='#1e1e2e',
                       font=('Segoe UI', 10, 'bold'),
                       relief=tk.FLAT,
                       cursor='hand2',
                       activebackground='#b4befe',
                       activeforeground='#1e1e2e',
                       padx=15,
                       pady=8)
        
        # Effets de survol
        btn.bind('<Enter>', lambda e: btn.config(bg='#b4befe'))
        btn.bind('<Leave>', lambda e: btn.config(bg='#89b4fa'))
        
        return btn
    
    def log(self, message):
        """Ajoute un message au journal"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def refresh_info(self):
        """Actualise les informations HWID"""
        self.log("🔄 Actualisation des informations...")
        
        def fetch_info():
            info = self.manager.get_all_hwid_info()
            
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, "╔" + "═" * 78 + "╗\n")
            self.info_text.insert(tk.END, "║" + " " * 25 + "INFORMATIONS HWID" + " " * 36 + "║\n")
            self.info_text.insert(tk.END, "╚" + "═" * 78 + "╝\n\n")
            
            for key, value in info.items():
                self.info_text.insert(tk.END, f"  {key:.<35} {value}\n")
            
            self.log("✅ Informations actualisées")
        
        threading.Thread(target=fetch_info, daemon=True).start()
    
    def modify_guid(self):
        """Modifie le Machine GUID"""
        if not self.manager.is_admin():
            messagebox.showerror("Erreur", "Privilèges administrateur requis!")
            self.log("❌ Modification GUID échouée: privilèges insuffisants")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Modifier Machine GUID")
        dialog.geometry("500x200")
        dialog.configure(bg='#1e1e2e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog,
                text="Nouveau Machine GUID:",
                bg='#1e1e2e',
                fg='#cdd6f4',
                font=('Segoe UI', 10)).pack(pady=20)
        
        entry = tk.Entry(dialog,
                        width=40,
                        bg='#2a2a3e',
                        fg='#cdd6f4',
                        font=('Consolas', 10),
                        insertbackground='#89b4fa')
        entry.pack(pady=10)
        entry.insert(0, str(uuid.uuid4()))
        
        def apply():
            new_guid = entry.get().strip()
            if new_guid:
                if self.manager.modify_machine_guid(new_guid):
                    self.log(f"✅ Machine GUID modifié: {new_guid}")
                    messagebox.showinfo("Succès", "Machine GUID modifié avec succès!")
                    self.refresh_info()
                else:
                    self.log("❌ Échec de la modification du GUID")
                    messagebox.showerror("Erreur", "Échec de la modification")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg='#1e1e2e')
        btn_frame.pack(pady=20)
        
        self.create_button(btn_frame, "✅ Appliquer", apply).pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame, "❌ Annuler", dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def modify_product_id(self):
        """Modifie le Product ID"""
        if not self.manager.is_admin():
            messagebox.showerror("Erreur", "Privilèges administrateur requis!")
            self.log("❌ Modification Product ID échouée: privilèges insuffisants")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Modifier Product ID")
        dialog.geometry("500x200")
        dialog.configure(bg='#1e1e2e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog,
                text="Nouveau Product ID:",
                bg='#1e1e2e',
                fg='#cdd6f4',
                font=('Segoe UI', 10)).pack(pady=20)
        
        entry = tk.Entry(dialog,
                        width=40,
                        bg='#2a2a3e',
                        fg='#cdd6f4',
                        font=('Consolas', 10),
                        insertbackground='#89b4fa')
        entry.pack(pady=10)
        
        # Génère un Product ID au format Windows
        sample_id = f"{uuid.uuid4().hex[:5]}-{uuid.uuid4().hex[:5]}-{uuid.uuid4().hex[:5]}-{uuid.uuid4().hex[:5]}"
        entry.insert(0, sample_id)
        
        def apply():
            new_id = entry.get().strip()
            if new_id:
                if self.manager.modify_product_id(new_id):
                    self.log(f"✅ Product ID modifié: {new_id}")
                    messagebox.showinfo("Succès", "Product ID modifié avec succès!")
                    self.refresh_info()
                else:
                    self.log("❌ Échec de la modification du Product ID")
                    messagebox.showerror("Erreur", "Échec de la modification")
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg='#1e1e2e')
        btn_frame.pack(pady=20)
        
        self.create_button(btn_frame, "✅ Appliquer", apply).pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame, "❌ Annuler", dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def backup_registry(self):
        """Sauvegarde les clés de registre"""
        if not self.manager.is_admin():
            messagebox.showerror("Erreur", "Privilèges administrateur requis!")
            self.log("❌ Sauvegarde échouée: privilèges insuffisants")
            return
        
        self.log("💾 Sauvegarde du registre en cours...")
        
        def backup():
            if self.manager.backup_registry_keys():
                self.log("✅ Sauvegarde créée: hwid_backup.reg")
                messagebox.showinfo("Succès", "Sauvegarde créée avec succès!")
            else:
                self.log("❌ Échec de la sauvegarde")
                messagebox.showerror("Erreur", "Échec de la sauvegarde")
        
        threading.Thread(target=backup, daemon=True).start()
    
    def generate_hwid(self):
        """Génère un nouveau HWID composite"""
        self.log("🔑 Génération d'un nouveau HWID...")
        hwid = self.manager.generate_composite_hwid()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("HWID Composite Généré")
        dialog.geometry("600x200")
        dialog.configure(bg='#1e1e2e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog,
                text="HWID Composite:",
                bg='#1e1e2e',
                fg='#cdd6f4',
                font=('Segoe UI', 10, 'bold')).pack(pady=20)
        
        hwid_text = tk.Text(dialog,
                           height=3,
                           width=70,
                           bg='#2a2a3e',
                           fg='#a6e3a1',
                           font=('Consolas', 10),
                           wrap=tk.WORD)
        hwid_text.pack(pady=10, padx=20)
        hwid_text.insert(1.0, hwid)
        hwid_text.config(state=tk.DISABLED)
        
        def copy_hwid():
            self.root.clipboard_clear()
            self.root.clipboard_append(hwid)
            self.log(f"✅ HWID copié: {hwid[:32]}...")
            messagebox.showinfo("Copié", "HWID copié dans le presse-papiers!")
        
        self.create_button(dialog, "📋 Copier", copy_hwid).pack(pady=10)
    
    def change_mac_address(self):
        """Modifie l'adresse MAC d'une interface réseau"""
        if not self.manager.is_admin():
            messagebox.showerror("Erreur", "Privilèges administrateur requis!")
            self.log("❌ Modification MAC échouée: privilèges insuffisants")
            return
        
        self.log("🌐 Récupération des adaptateurs réseau...")
        
        # Récupérer les adaptateurs réseau
        adapters = self.manager.get_network_adapters()
        
        if not adapters:
            messagebox.showerror("Erreur", "Aucun adaptateur réseau actif trouvé")
            self.log("❌ Aucun adaptateur réseau actif")
            return
        
        # Créer une fenêtre de dialogue
        dialog = tk.Toplevel(self.root)
        dialog.title("Modifier l'adresse MAC")
        dialog.geometry("700x500")
        dialog.configure(bg='#1e1e2e')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog,
                text="Sélectionner un adaptateur réseau:",
                bg='#1e1e2e',
                fg='#cdd6f4',
                font=('Segoe UI', 12, 'bold')).pack(pady=20)
        
        # Frame pour la liste des adaptateurs
        adapter_frame = tk.Frame(dialog, bg='#2a2a3e')
        adapter_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Variable pour stocker l'adaptateur sélectionné
        selected_adapter = tk.StringVar()
        
        # Afficher les adaptateurs avec des radio buttons
        for i, adapter in enumerate(adapters):
            name = adapter.get('Name', 'N/A')
            mac = adapter.get('MacAddress', 'N/A')
            desc = adapter.get('InterfaceDescription', 'N/A')
            
            radio_text = f"{name}\nMAC: {mac}\n{desc}"
            
            radio = tk.Radiobutton(adapter_frame,
                                  text=radio_text,
                                  variable=selected_adapter,
                                  value=name,
                                  bg='#2a2a3e',
                                  fg='#cdd6f4',
                                  selectcolor='#1e1e2e',
                                  activebackground='#3a3a4e',
                                  activeforeground='#89b4fa',
                                  font=('Consolas', 9),
                                  justify=tk.LEFT,
                                  anchor='w')
            radio.pack(pady=5, padx=10, fill=tk.X)
            
            if i == 0:
                selected_adapter.set(name)
        
        # Frame pour l'adresse MAC
        mac_frame = tk.Frame(dialog, bg='#1e1e2e')
        mac_frame.pack(pady=10)
        
        tk.Label(mac_frame,
                text="Nouvelle adresse MAC:",
                bg='#1e1e2e',
                fg='#cdd6f4',
                font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        
        mac_entry = tk.Entry(mac_frame,
                            width=25,
                            bg='#2a2a3e',
                            fg='#cdd6f4',
                            font=('Consolas', 10),
                            insertbackground='#89b4fa')
        mac_entry.pack(side=tk.LEFT, padx=5)
        
        # Générer une MAC aléatoire par défaut
        import random
        random_mac = "02:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        mac_entry.insert(0, random_mac)
        
        def generate_new_mac():
            mac_entry.delete(0, tk.END)
            new_mac = "02:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            mac_entry.insert(0, new_mac)
        
        self.create_button(mac_frame, "🎲 Générer", generate_new_mac).pack(side=tk.LEFT, padx=5)
        
        # Avertissement
        warning_label = tk.Label(dialog,
                                text="⚠️ L'adaptateur réseau sera redémarré après la modification",
                                bg='#1e1e2e',
                                fg='#f38ba8',
                                font=('Segoe UI', 9, 'italic'))
        warning_label.pack(pady=10)
        
        def apply_mac_change():
            adapter_name = selected_adapter.get()
            new_mac = mac_entry.get().strip()
            
            if not adapter_name:
                messagebox.showerror("Erreur", "Veuillez sélectionner un adaptateur")
                return
            
            if not new_mac:
                messagebox.showerror("Erreur", "Veuillez entrer une adresse MAC")
                return
            
            # Confirmation
            confirm = messagebox.askyesno(
                "Confirmation",
                f"Modifier l'adresse MAC de '{adapter_name}' en '{new_mac}'?\n\n"
                "L'adaptateur réseau sera temporairement déconnecté."
            )
            
            if not confirm:
                return
            
            self.log(f"🌐 Modification de l'adresse MAC de '{adapter_name}'...")
            dialog.destroy()
            
            def change_mac():
                if self.manager.spoof_mac_address(adapter_name=adapter_name, new_mac=new_mac):
                    self.log(f"✅ Adresse MAC modifiée avec succès: {new_mac}")
                    messagebox.showinfo("Succès", f"Adresse MAC modifiée avec succès!\n\nNouvelle MAC: {new_mac}")
                    self.refresh_info()
                else:
                    self.log("❌ Échec de la modification de l'adresse MAC")
                    messagebox.showerror("Erreur", "Échec de la modification de l'adresse MAC")
            
            threading.Thread(target=change_mac, daemon=True).start()
        
        # Boutons
        btn_frame = tk.Frame(dialog, bg='#1e1e2e')
        btn_frame.pack(pady=20)
        
        self.create_button(btn_frame, "✅ Appliquer", apply_mac_change).pack(side=tk.LEFT, padx=5)
        self.create_button(btn_frame, "❌ Annuler", dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def run_as_admin(self):
        """Relance le programme en mode administrateur"""
        self.log("🔐 Tentative de relancement en mode administrateur...")
        self.manager.run_as_admin()


def main():
    """Lance l'interface graphique"""
    root = tk.Tk()
    app = HWIDManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
