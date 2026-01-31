# 🔐 HWID Manager - Gestionnaire d'Identifiant Matériel

Un outil complet pour afficher, analyser et modifier les identifiants matériels (HWID) sous Windows.

## ⚠️ AVERTISSEMENT IMPORTANT

**Ce programme est fourni à des fins éducatives uniquement.**

La modification du HWID peut:
- Violer les conditions d'utilisation de certains logiciels
- Contourner des protections anti-piratage (illégal)
- Causer des problèmes de stabilité système
- Invalider des licences logicielles

**Utilisez cet outil de manière responsable et légale.**

## 📋 Fonctionnalités

### Affichage d'Informations
- **Machine GUID**: Identifiant unique de la machine Windows
- **CPU ID**: Identifiant du processeur
- **Disk Serial**: Numéro de série du disque dur
- **Motherboard Serial**: Numéro de série de la carte mère
- **MAC Address**: Adresse MAC de la carte réseau
- **Windows Product ID**: ID produit Windows
- **Composite HWID**: Hash SHA-256 combinant tous les composants

### Modifications Disponibles
- ✅ Modifier le Machine GUID
- ✅ Modifier le Product ID Windows
- ✅ Générer de nouveaux identifiants aléatoires
- ✅ Sauvegarder/Restaurer les clés de registre
- ℹ️ Instructions pour modifier l'adresse MAC

## 🚀 Installation

### Prérequis
- Windows 10/11
- Python 3.8 ou supérieur
- Privilèges administrateur (pour les modifications)

### Installation des dépendances
```bash
# Aucune dépendance externe requise
# Le programme utilise uniquement des bibliothèques standard Python
```

## 💻 Utilisation

### Mode Console
```bash
python hwid_manager.py
```

Interface en ligne de commande avec menu interactif.

### Mode Graphique (Recommandé)
```bash
python hwid_gui.py
```

Interface graphique moderne avec thème sombre.

### Exécution en tant qu'Administrateur

**Important**: Pour modifier le HWID, vous devez exécuter le programme en tant qu'administrateur.

#### Méthode 1: Clic droit
1. Clic droit sur `hwid_gui.py` ou `hwid_manager.py`
2. Sélectionner "Exécuter en tant qu'administrateur"

#### Méthode 2: PowerShell Admin
```powershell
# Ouvrir PowerShell en tant qu'administrateur
cd C:\Users\jeuxc\Documents\SITE\hwid
python hwid_gui.py
```

#### Méthode 3: Depuis l'interface
Utiliser le bouton "🔐 Relancer en Admin" dans l'interface graphique.

## 📖 Guide d'Utilisation

### 1. Afficher les Informations HWID

```python
from hwid_manager import HWIDManager

manager = HWIDManager()
info = manager.get_all_hwid_info()

for key, value in info.items():
    print(f"{key}: {value}")
```

### 2. Modifier le Machine GUID

```python
# Génération automatique
manager.modify_machine_guid()

# GUID personnalisé
manager.modify_machine_guid("12345678-1234-1234-1234-123456789012")
```

### 3. Sauvegarder le Registre

```python
# Créer une sauvegarde avant modification
manager.backup_registry_keys("backup.reg")
```

### 4. Générer un HWID Composite

```python
hwid = manager.generate_composite_hwid()
print(f"HWID: {hwid}")
```

## 🔧 Composants du HWID

### Machine GUID
- **Emplacement**: `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid`
- **Format**: UUID (ex: `12345678-1234-1234-1234-123456789012`)
- **Utilisation**: Identifiant unique Windows

### Product ID
- **Emplacement**: `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProductId`
- **Format**: `XXXXX-XXXXX-XXXXX-XXXXX`
- **Utilisation**: Licence Windows

### CPU ID
- **Source**: WMIC (Windows Management Instrumentation)
- **Format**: Hexadécimal
- **Utilisation**: Identifiant processeur

### Disk Serial
- **Source**: WMIC diskdrive
- **Format**: Alphanumérique
- **Utilisation**: Numéro de série disque

### MAC Address
- **Source**: uuid.getnode()
- **Format**: `XX:XX:XX:XX:XX:XX`
- **Utilisation**: Adresse physique réseau

## 🛡️ Sécurité

### Sauvegarde Recommandée

Avant toute modification, créez une sauvegarde:

```bash
# Via l'interface
Menu > Sauvegarder Registre

# Via console
python hwid_manager.py
# Choisir option 5
```

### Restauration

Pour restaurer une sauvegarde:

```bash
# Double-cliquer sur le fichier .reg
# OU
reg import hwid_backup.reg
```

### Point de Restauration Windows

Créez un point de restauration système avant modification:

```powershell
# PowerShell Admin
Checkpoint-Computer -Description "Avant modification HWID"
```

## 🎨 Interface Graphique

### Thème
- **Couleurs**: Catppuccin Mocha (thème sombre)
- **Police**: Segoe UI (interface), Consolas (données)
- **Style**: Moderne, minimaliste

### Fonctionnalités GUI
- ✅ Actualisation en temps réel
- ✅ Journal d'activité
- ✅ Dialogues de modification
- ✅ Copie dans le presse-papiers
- ✅ Indicateur de statut admin

## 📁 Structure du Projet

```
hwid/
├── hwid_manager.py      # Module principal (logique)
├── hwid_gui.py          # Interface graphique
├── README.md            # Documentation
└── hwid_backup.reg      # Sauvegarde (généré)
```

## 🔍 Cas d'Usage Légitimes

### Développement
- Tester des systèmes de licence
- Développer des protections anti-piratage
- Analyser les identifiants matériels

### Administration Système
- Gérer des parcs de machines
- Identifier des machines en réseau
- Diagnostiquer des problèmes matériels

### Sécurité
- Recherche en cybersécurité
- Tests de pénétration autorisés
- Audit de sécurité

## ⚖️ Aspects Légaux

### Utilisations Interdites
- ❌ Contourner des protections anti-piratage
- ❌ Utiliser des logiciels piratés
- ❌ Créer de faux comptes
- ❌ Contourner des bannissements

### Utilisations Autorisées
- ✅ Recherche éducative
- ✅ Tests sur vos propres systèmes
- ✅ Développement de logiciels
- ✅ Administration système légitime

## 🐛 Dépannage

### Erreur: "Privilèges administrateur requis"
**Solution**: Exécuter le programme en tant qu'administrateur

### Erreur: "Impossible d'ouvrir la clé de registre"
**Solution**: 
1. Vérifier les privilèges admin
2. Désactiver temporairement l'antivirus
3. Vérifier que la clé existe

### L'adresse MAC ne change pas
**Solution**: 
- Certaines cartes réseau ne supportent pas le changement MAC
- Utiliser des outils dédiés (TMAC, Technitium MAC Address Changer)

### Le GUID revient à l'ancienne valeur
**Solution**: 
- Windows peut restaurer certaines valeurs
- Créer un script de modification au démarrage

## 📚 Ressources

### Documentation Microsoft
- [Machine GUID](https://docs.microsoft.com/en-us/windows/win32/api/sysinfoapi/)
- [Product ID](https://docs.microsoft.com/en-us/windows/deployment/volume-activation/)
- [WMI Reference](https://docs.microsoft.com/en-us/windows/win32/wmisdk/)

### Outils Complémentaires
- **WMIC**: Windows Management Instrumentation Command-line
- **Regedit**: Éditeur de registre Windows
- **DevManView**: Gestionnaire de périphériques avancé

## 🤝 Contribution

Ce projet est à des fins éducatives. Les contributions sont les bienvenues:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit les changements (`git commit -m 'Ajout fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est fourni "tel quel" sans garantie d'aucune sorte.

**L'auteur décline toute responsabilité pour:**
- Dommages système
- Violations de licences
- Utilisations illégales
- Pertes de données

## 👨‍💻 Auteur

Créé à des fins éducatives et de recherche.

## 🔄 Changelog

### Version 1.0 (2026-01-31)
- ✅ Interface console complète
- ✅ Interface graphique moderne
- ✅ Modification Machine GUID
- ✅ Modification Product ID
- ✅ Sauvegarde registre
- ✅ Génération HWID composite
- ✅ Support mode administrateur

## 📞 Support

Pour toute question ou problème:
1. Vérifier la documentation
2. Consulter la section Dépannage
3. Créer une issue sur GitHub

---

**Rappel**: Utilisez cet outil de manière responsable et éthique. La modification du HWID doit être effectuée uniquement sur vos propres systèmes et dans un cadre légal.
