# -*- coding: utf-8 -*-
"""
HWID Manager - Programme pour afficher et modifier le Hardware ID
ATTENTION: Utiliser uniquement à des fins éducatives et légales
"""

import subprocess
import winreg
import uuid
import hashlib
import platform
import os
import sys
from typing import Dict, List, Optional

class HWIDManager:
    """Gestionnaire pour obtenir et modifier les identifiants matériels"""
    
    def __init__(self):
        self.hwid_info = {}
        
    def get_machine_guid(self) -> str:
        """Récupère le MachineGuid depuis le registre Windows"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY
            )
            value, _ = winreg.QueryValueEx(key, "MachineGuid")
            winreg.CloseKey(key)
            return value
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def get_cpu_id(self) -> str:
        """Récupère l'ID du processeur"""
        try:
            # Essayer avec PowerShell (Windows 11)
            ps_command = "Get-CimInstance -ClassName Win32_Processor | Select-Object -ExpandProperty ProcessorId"
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            
            # Fallback: WMIC (Windows 10 et antérieur)
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'ProcessorId'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                return lines[1].strip()
            return "Non disponible"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def get_disk_serial(self) -> str:
        """Récupère le numéro de série du disque dur"""
        try:
            # Essayer avec PowerShell (Windows 11)
            ps_command = "Get-CimInstance -ClassName Win32_DiskDrive | Select-Object -First 1 -ExpandProperty SerialNumber"
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            
            # Fallback: WMIC (Windows 10 et antérieur)
            result = subprocess.run(
                ['wmic', 'diskdrive', 'get', 'SerialNumber'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            lines = result.stdout.strip().split('\n')
            serials = [line.strip() for line in lines[1:] if line.strip()]
            return serials[0] if serials else "Non disponible"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def get_motherboard_serial(self) -> str:
        """Récupère le numéro de série de la carte mère"""
        try:
            # Essayer avec PowerShell (Windows 11)
            ps_command = "Get-CimInstance -ClassName Win32_BaseBoard | Select-Object -ExpandProperty SerialNumber"
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            
            # Fallback: WMIC (Windows 10 et antérieur)
            result = subprocess.run(
                ['wmic', 'baseboard', 'get', 'SerialNumber'],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                return lines[1].strip()
            return "Non disponible"
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def get_mac_address(self) -> str:
        """Récupère l'adresse MAC"""
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff)
                           for elements in range(0, 2*6, 2)][::-1])
            return mac
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def get_windows_product_id(self) -> str:
        """Récupère le Product ID de Windows"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY
            )
            value, _ = winreg.QueryValueEx(key, "ProductId")
            winreg.CloseKey(key)
            return value
        except Exception as e:
            return f"Erreur: {str(e)}"
    
    def generate_composite_hwid(self) -> str:
        """Génère un HWID composite basé sur plusieurs composants"""
        components = [
            self.get_machine_guid(),
            self.get_cpu_id(),
            self.get_disk_serial(),
            self.get_motherboard_serial(),
            self.get_mac_address()
        ]
        
        # Combine tous les composants et crée un hash
        combined = ''.join(str(c) for c in components)
        hwid_hash = hashlib.sha256(combined.encode()).hexdigest()
        return hwid_hash
    
    def get_all_hwid_info(self) -> Dict[str, str]:
        """Récupère toutes les informations HWID"""
        return {
            "Machine GUID": self.get_machine_guid(),
            "CPU ID": self.get_cpu_id(),
            "Disk Serial": self.get_disk_serial(),
            "Motherboard Serial": self.get_motherboard_serial(),
            "MAC Address": self.get_mac_address(),
            "Windows Product ID": self.get_windows_product_id(),
            "Composite HWID": self.generate_composite_hwid(),
            "Platform": platform.platform(),
            "Computer Name": platform.node()
        }
    
    def modify_machine_guid(self, new_guid: Optional[str] = None) -> bool:
        """
        Modifie le MachineGuid dans le registre
        ATTENTION: Nécessite des privilèges administrateur
        """
        if not self.is_admin():
            print("❌ Privilèges administrateur requis!")
            return False
        
        try:
            if new_guid is None:
                new_guid = str(uuid.uuid4())
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
            )
            winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_guid)
            winreg.CloseKey(key)
            
            print(f"✅ MachineGuid modifié: {new_guid}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la modification: {str(e)}")
            return False
    
    def modify_product_id(self, new_product_id: Optional[str] = None) -> bool:
        """
        Modifie le ProductId de Windows
        ATTENTION: Nécessite des privilèges administrateur
        """
        if not self.is_admin():
            print("❌ Privilèges administrateur requis!")
            return False
        
        try:
            if new_product_id is None:
                # Génère un ProductId aléatoire au format Windows
                new_product_id = f"{uuid.uuid4().hex[:5]}-{uuid.uuid4().hex[:5]}-{uuid.uuid4().hex[:5]}-{uuid.uuid4().hex[:5]}"
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
                0,
                winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
            )
            winreg.SetValueEx(key, "ProductId", 0, winreg.REG_SZ, new_product_id)
            winreg.CloseKey(key)
            
            print(f"✅ ProductId modifié: {new_product_id}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la modification: {str(e)}")
            return False
    
    def get_network_adapters(self) -> List[Dict[str, str]]:
        """Récupère la liste des adaptateurs réseau"""
        try:
            ps_command = """
            Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object Name, InterfaceDescription, MacAddress | ConvertTo-Json
            """
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0 and result.stdout.strip():
                import json
                adapters = json.loads(result.stdout)
                if isinstance(adapters, dict):
                    adapters = [adapters]
                return adapters
            return []
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des adaptateurs: {str(e)}")
            return []
    
    def spoof_mac_address(self, adapter_name: str = None, new_mac: Optional[str] = None) -> bool:
        """
        Modifie l'adresse MAC d'une interface réseau via le registre
        ATTENTION: Nécessite des privilèges administrateur
        """
        if not self.is_admin():
            print("❌ Privilèges administrateur requis!")
            return False
        
        try:
            # Si aucun adaptateur spécifié, lister les adaptateurs disponibles
            if adapter_name is None:
                adapters = self.get_network_adapters()
                if not adapters:
                    print("❌ Aucun adaptateur réseau actif trouvé")
                    return False
                
                print("\n📡 Adaptateurs réseau disponibles:")
                for i, adapter in enumerate(adapters, 1):
                    print(f"{i}. {adapter.get('Name', 'N/A')} - MAC: {adapter.get('MacAddress', 'N/A')}")
                
                choice = input("\nChoisir un adaptateur (numéro): ").strip()
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(adapters):
                        adapter_name = adapters[idx]['Name']
                    else:
                        print("❌ Choix invalide")
                        return False
                except ValueError:
                    print("❌ Entrée invalide")
                    return False
            
            # Générer une nouvelle MAC si non fournie
            if new_mac is None:
                # Générer une MAC aléatoire (en gardant le bit local pour éviter les conflits)
                import random
                new_mac = "02:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
            
            # Nettoyer le format MAC (enlever : et -)
            mac_clean = new_mac.replace(':', '').replace('-', '').upper()
            
            if len(mac_clean) != 12:
                print(f"❌ Format MAC invalide: {new_mac}")
                return False
            
            # Trouver la clé de registre de l'adaptateur
            ps_find_adapter = f"""
            $adapter = Get-NetAdapter | Where-Object {{$_.Name -eq '{adapter_name}'}}
            if ($adapter) {{
                $guid = $adapter.InterfaceGuid
                Write-Output $guid
            }}
            """
            
            result = subprocess.run(
                ['powershell', '-Command', ps_find_adapter],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                print(f"❌ Impossible de trouver l'adaptateur: {adapter_name}")
                return False
            
            adapter_guid = result.stdout.strip()
            
            # Modifier le registre
            reg_path = f"SYSTEM\\CurrentControlSet\\Control\\Class\\{{4D36E972-E325-11CE-BFC1-08002BE10318}}"
            
            # Chercher la sous-clé correspondant à l'adaptateur
            ps_modify = f"""
            $regPath = "HKLM:\\{reg_path}"
            $found = $false
            
            Get-ChildItem $regPath | ForEach-Object {{
                $key = $_
                $netCfgInstanceId = (Get-ItemProperty -Path $key.PSPath -Name "NetCfgInstanceId" -ErrorAction SilentlyContinue).NetCfgInstanceId
                
                if ($netCfgInstanceId -eq "{adapter_guid}") {{
                    Set-ItemProperty -Path $key.PSPath -Name "NetworkAddress" -Value "{mac_clean}"
                    $found = $true
                    Write-Output "SUCCESS"
                }}
            }}
            
            if (-not $found) {{
                Write-Output "NOT_FOUND"
            }}
            """
            
            result = subprocess.run(
                ['powershell', '-Command', ps_modify],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if "SUCCESS" in result.stdout:
                # Redémarrer l'adaptateur réseau
                print(f"✅ Adresse MAC modifiée: {new_mac}")
                print("🔄 Redémarrage de l'adaptateur réseau...")
                
                restart_cmd = f"""
                Disable-NetAdapter -Name '{adapter_name}' -Confirm:$false
                Start-Sleep -Seconds 2
                Enable-NetAdapter -Name '{adapter_name}' -Confirm:$false
                """
                
                subprocess.run(
                    ['powershell', '-Command', restart_cmd],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                
                print("✅ Adaptateur redémarré avec succès!")
                print("ℹ️  Vérifiez la nouvelle adresse MAC avec l'option 1 du menu")
                return True
            else:
                print(f"❌ Impossible de modifier l'adresse MAC")
                return False
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            return False
    
    @staticmethod
    def is_admin() -> bool:
        """Vérifie si le programme est exécuté avec des privilèges administrateur"""
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
    
    @staticmethod
    def run_as_admin():
        """Relance le programme avec des privilèges administrateur"""
        if sys.platform == 'win32':
            import ctypes
            try:
                if not HWIDManager.is_admin():
                    ctypes.windll.shell32.ShellExecuteW(
                        None, "runas", sys.executable, " ".join(sys.argv), None, 1
                    )
                    sys.exit(0)
            except Exception as e:
                print(f"Impossible d'obtenir les privilèges admin: {e}")
    
    def backup_registry_keys(self, backup_file: str = "hwid_backup.reg"):
        """Sauvegarde les clés de registre importantes"""
        if not self.is_admin():
            print("❌ Privilèges administrateur requis!")
            return False
        
        try:
            keys_to_backup = [
                r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography",
                r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion"
            ]
            
            with open(backup_file, 'w', encoding='utf-16') as f:
                f.write("Windows Registry Editor Version 5.00\n\n")
                
                for key_path in keys_to_backup:
                    subprocess.run(
                        ['reg', 'export', key_path, 'temp.reg', '/y'],
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    
                    if os.path.exists('temp.reg'):
                        with open('temp.reg', 'r', encoding='utf-16') as temp:
                            f.write(temp.read())
                        os.remove('temp.reg')
            
            print(f"✅ Sauvegarde créée: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {str(e)}")
            return False
    
    def restore_registry_keys(self, backup_file: str = "hwid_backup.reg"):
        """Restaure les clés de registre depuis une sauvegarde"""
        if not self.is_admin():
            print("❌ Privilèges administrateur requis!")
            return False
        
        try:
            if not os.path.exists(backup_file):
                print(f"❌ Fichier de sauvegarde introuvable: {backup_file}")
                return False
            
            print(f"⚠️  ATTENTION: Cette opération va restaurer les clés de registre.")
            print(f"   Fichier: {backup_file}")
            confirm = input("   Continuer? (oui/non): ").strip().lower()
            
            if confirm not in ['oui', 'o', 'yes', 'y']:
                print("❌ Restauration annulée.")
                return False
            
            # Importer le fichier .reg
            result = subprocess.run(
                ['reg', 'import', backup_file],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                print(f"✅ Restauration réussie depuis: {backup_file}")
                print("ℹ️  Redémarrage recommandé pour appliquer les changements.")
                return True
            else:
                print(f"❌ Erreur lors de la restauration: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur lors de la restauration: {str(e)}")
            return False


def print_banner():
    """Affiche la bannière du programme"""
    banner = """
    +=============================================================+
    |                   HWID MANAGER v1.0                         |
    |          Hardware ID Information & Modification             |
    |                                                             |
    |  WARNING: Utilisation a des fins educatives uniquement      |
    |  Modifier le HWID peut violer les conditions d'utilisation  |
    +=============================================================+
    """
    print(banner)


def main():
    """Fonction principale en mode console"""
    print_banner()
    
    manager = HWIDManager()
    
    while True:
        print("\n" + "="*60)
        print("MENU PRINCIPAL")
        print("="*60)
        print("1. Afficher toutes les informations HWID")
        print("2. Modifier le Machine GUID")
        print("3. Modifier le Product ID")
        print("4. Modifier l'adresse MAC")
        print("5. Sauvegarder les clés de registre")
        print("6. Restaurer les clés de registre depuis une sauvegarde")
        print("7. Générer un nouveau HWID composite")
        print("8. Relancer en mode administrateur")
        print("0. Quitter")
        print("="*60)
        
        choice = input("\nVotre choix: ").strip()
        
        if choice == "1":
            print("\n📋 INFORMATIONS HWID ACTUELLES:")
            print("-" * 60)
            info = manager.get_all_hwid_info()
            for key, value in info.items():
                print(f"{key:.<30} {value}")
        
        elif choice == "2":
            print("\n🔧 MODIFICATION DU MACHINE GUID")
            custom = input("Entrer un GUID personnalisé (ou appuyez sur Entrée pour auto): ").strip()
            new_guid = custom if custom else None
            manager.modify_machine_guid(new_guid)
        
        elif choice == "3":
            print("\n🔧 MODIFICATION DU PRODUCT ID")
            custom = input("Entrer un Product ID personnalisé (ou appuyez sur Entrée pour auto): ").strip()
            new_id = custom if custom else None
            manager.modify_product_id(new_id)
        
        elif choice == "4":
            print("\n🌐 MODIFICATION DE L'ADRESSE MAC")
            custom_mac = input("Entrer une adresse MAC personnalisée (ou appuyez sur Entrée pour auto): ").strip()
            new_mac = custom_mac if custom_mac else None
            manager.spoof_mac_address(new_mac=new_mac)
        
        elif choice == "5":
            print("\n💾 SAUVEGARDE DES CLÉS DE REGISTRE")
            filename = input("Nom du fichier de sauvegarde (hwid_backup.reg): ").strip()
            filename = filename if filename else "hwid_backup.reg"
            manager.backup_registry_keys(filename)
        
        elif choice == "6":
            print("\n♻️  RESTAURATION DES CLÉS DE REGISTRE")
            filename = input("Nom du fichier de sauvegarde (hwid_backup.reg): ").strip()
            filename = filename if filename else "hwid_backup.reg"
            manager.restore_registry_keys(filename)
        
        elif choice == "7":
            print("\n🔑 NOUVEAU HWID COMPOSITE:")
            print(f"HWID: {manager.generate_composite_hwid()}")
        
        elif choice == "8":
            print("\n🔐 Relancement en mode administrateur...")
            manager.run_as_admin()
        
        elif choice == "0":
            print("\n👋 Au revoir!")
            break
        
        else:
            print("\n❌ Choix invalide!")
        
        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
