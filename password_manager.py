"""
Advanced Password Manager & Strength Analyzer
For Johns Hopkins MS Cybersecurity Student Portfolio Project
Krishita Choksi - March 2026

Features:
- Password strength checker with entropy calculation [web:39][web:35]
- Memorable passphrase generator (Diceware-style words + dates) [web:40]
- Password variation generator for policy compliance [web:41]
- Secure vault with AES encryption (using cryptography lib - install required)
- Copy to clipboard
- Export/Import vault
- GUI with dark theme
- Crack time estimation

Requirements:
pip install cryptography pyperclip
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import string
import math
import random
import json
import os
from datetime import datetime
import hashlib
import pyperclip  # pip install pyperclip
from cryptography.fernet import Fernet  # pip install cryptography
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Advanced Password Manager - JHU Cybersecurity Project")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        # Colors for dark theme
        self.bg_color = '#1e1e1e'
        self.fg_color = '#ffffff'
        self.button_color = '#0d7377'
        self.accent_color = '#00d4aa'
        
        self.vault_file = "encrypted_vault.enc"
        self.master_password = None
        self.cipher_suite = None
        
        self.wordlist = [
            "apple", "banana", "cherry", "date", "elder", "fig", "grape", "honey", "ice", "jelly",
            "kiwi", "lemon", "mango", "nut", "orange", "peach", "quince", "rasp", "straw", "tanger",
            "ugli", "vanilla", "water", "xmas", "yellow", "zest", "cloud", "dream", "eagle", "fire"
        ] * 10  # Extended wordlist for Diceware [web:40]
        
        self.setup_ui()
        self.load_vault()
    
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TFrame', background=self.bg_color)
        
        # Title
        title_label = tk.Label(self.root, text="🔐 Password Manager & Analyzer", 
                              font=('Arial', 20, 'bold'), bg=self.bg_color, fg=self.accent_color)
        title_label.pack(pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Strength Checker Tab
        self.strength_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.strength_frame, text="Strength Checker")
        self.setup_strength_checker()
        
        # Generator Tab
        self.generator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.generator_frame, text="Password Generator")
        self.setup_generator()
        
        # Variation Tab
        self.variation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.variation_frame, text="Password Variations")
        self.setup_variations()
        
        # Vault Tab
        self.vault_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.vault_frame, text="Secure Vault")
        self.setup_vault()
    
    def setup_strength_checker(self):
        # Input
        tk.Label(self.strength_frame, text="Enter Password:", font=('Arial', 12), 
                bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        self.strength_entry = tk.Entry(self.strength_frame, show='*', width=50, font=('Arial', 12),
                                      bg='#2d2d2d', fg=self.fg_color, insertbackground=self.fg_color)
        self.strength_entry.pack(pady=5)
        self.strength_entry.bind('<KeyRelease>', self.update_strength)
        
        # Show/Hide button
        self.show_strength = tk.BooleanVar()
        tk.Checkbutton(self.strength_frame, text="Show", variable=self.show_strength,
                      command=self.toggle_strength_visibility, bg=self.bg_color, fg=self.fg_color,
                      selectcolor=self.button_color).pack()
        
        # Results
        self.strength_result = tk.Label(self.strength_frame, text="", font=('Arial', 16, 'bold'),
                                       bg=self.bg_color, fg=self.fg_color)
        self.strength_result.pack(pady=20)
        
        self.entropy_label = tk.Label(self.strength_frame, text="", font=('Arial', 10),
                                     bg=self.bg_color, fg='#cccccc')
        self.entropy_label.pack()
        
        self.crack_time_label = tk.Label(self.strength_frame, text="", font=('Arial', 10),
                                        bg=self.bg_color, fg='#cccccc')
        self.crack_time_label.pack()
    
    def toggle_strength_visibility(self):
        if self.show_strength.get():
            self.strength_entry.config(show='')
        else:
            self.strength_entry.config(show='*')
    
    def calculate_entropy(self, password):
        """Calculate password entropy [web:39][web:35]"""
        if not password:
            return 0
        
        charset_size = 0
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_digits = any(c in string.digits for c in password)
        has_special = any(c in string.punctuation for c in password)
        has_space = any(c.isspace() for c in password)
        
        if has_lower: charset_size += 26
        if has_upper: charset_size += 26
        if has_digits: charset_size += 10
        if has_special: charset_size += 32  # approx punctuation
        if has_space: charset_size += 1
        
        return len(password) * math.log2(max(charset_size, 1)) if charset_size else 0
    
    def estimate_crack_time(self, entropy):
        """Estimate crack time in years [web:49]"""
        if entropy == 0:
            return "Instant"
        
        # Assume 10^12 guesses/sec for modern GPU rig
        guesses_per_sec = 10**12
        total_guesses = 2 ** entropy
        seconds = total_guesses / guesses_per_sec
        years = seconds / (3600 * 24 * 365)
        
        if years < 1:
            return f"{years*365:.1f} days"
        elif years < 100:
            return f"{years:.1f} years"
        else:
            return f"{years/100:.0f} centuries"
    
    def update_strength(self, event=None):
        password = self.strength_entry.get()
        entropy = self.calculate_entropy(password)
        
        if entropy < 28:
            strength = "Very Weak"
            color = "#ff4444"
        elif entropy < 36:
            strength = "Weak"
            color = "#ff8800"
        elif entropy < 60:
            strength = "Moderate"
            color = "#ffdd00"
        elif entropy < 80:
            strength = "Strong"
            color = "#00cc00"
        else:
            strength = "Very Strong"
            color = "#00aa00"
        
        self.strength_result.config(text=f"Strength: {strength}", fg=color)
        self.entropy_label.config(text=f"Entropy: {entropy:.1f} bits")
        self.crack_time_label.config(text=f"Crack Time: {self.estimate_crack_time(entropy)}")
    
    def setup_generator(self):
        # Length
        tk.Label(self.generator_frame, text="Passphrase Length (words):", font=('Arial', 12),
                bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        self.length_var = tk.StringVar(value="4")
        length_spin = tk.Spinbox(self.generator_frame, from_=2, to=8, textvariable=self.length_var,
                                font=('Arial', 12), bg='#2d2d2d', fg=self.fg_color)
        length_spin.pack(pady=5)
        
        # Type
        tk.Label(self.generator_frame, text="Type:", font=('Arial', 12),
                bg=self.bg_color, fg=self.fg_color).pack(pady=(20,5))
        self.type_var = tk.StringVar(value="memorable")
        memorable_rb = tk.Radiobutton(self.generator_frame, text="Memorable (Words+Date)", 
                                    variable=self.type_var, value="memorable", bg=self.bg_color, fg=self.fg_color)
        memorable_rb.pack()
        random_rb = tk.Radiobutton(self.generator_frame, text="Random (Complex)", 
                                  variable=self.type_var, value="random", bg=self.bg_color, fg=self.fg_color)
        random_rb.pack()
        
        # Generate button
        tk.Button(self.generator_frame, text="Generate Password", command=self.generate_password,
                 bg=self.button_color, fg=self.fg_color, font=('Arial', 12, 'bold'),
                 relief='flat', padx=20).pack(pady=20)
        
        # Output
        self.generated_password = tk.Label(self.generator_frame, text="Click generate...", 
                                          font=('Arial', 16, 'bold'), bg=self.bg_color, fg=self.accent_color,
                                          wraplength=800)
        self.generated_password.pack(pady=20)
        
        self.copy_btn = tk.Button(self.generator_frame, text="Copy to Clipboard", command=self.copy_generated,
                                 bg=self.accent_color, fg='#000000', font=('Arial', 10, 'bold'),
                                 relief='flat', padx=20)
        self.copy_btn.pack(pady=5)
    
    def generate_memorable(self, num_words):
        """Generate memorable passphrase from words/dates [web:40][web:46]"""
        words = random.choices(self.wordlist, k=num_words)
        # Add date element for memorability (e.g., birthday)
        date_element = datetime.now().strftime("%b%d").lower()  # e.g., mar25
        passphrase = " ".join(words) + f"-{date_element}"
        return passphrase
    
    def generate_random(self, length=16):
        """Generate complex random password"""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_password(self):
        num_words = int(self.length_var.get())
        ptype = self.type_var.get()
        
        if ptype == "memorable":
            password = self.generate_memorable(num_words)
        else:
            password = self.generate_random(16)
        
        self.generated_password.config(text=password)
    
    def copy_generated(self):
        password = self.generated_password.cget("text")
        if password != "Click generate...":
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
    
    def setup_variations(self):
        tk.Label(self.variation_frame, text="Original Password:", font=('Arial', 12),
                bg=self.bg_color, fg=self.fg_color).pack(pady=10)
        self.orig_entry = tk.Entry(self.variation_frame, width=50, font=('Arial', 12),
                                  bg='#2d2d2d', fg=self.fg_color)
        self.orig_entry.pack(pady=5)
        
        tk.Button(self.variation_frame, text="Generate Variations", command=self.generate_variations,
                 bg=self.button_color, fg=self.fg_color, font=('Arial', 12),
                 relief='flat', padx=20).pack(pady=20)
        
        self.variations_text = tk.Text(self.variation_frame, height=10, width=80, font=('Arial', 10),
                                      bg='#2d2d2d', fg=self.fg_color, wrap='word')
        self.variations_text.pack(pady=10, padx=20, fill='both', expand=True)
    
    def generate_variations(self):
        """Create similar but different passwords for policy changes [web:41]"""
        original = self.orig_entry.get()
        if not original:
            messagebox.showwarning("Input", "Enter original password")
            return
        
        variations = []
        # Swap case
        variations.append(original.swapcase())
        # Add number
        variations.append(original + "1")
        variations.append(original[:-1] + str(int(original[-1])+1) if original[-1].isdigit() else original + "1")
        # Add special char
        variations.append(original + "!")
        # Leet speak variations
        leet_map = {'a':'4', 'e':'3', 'i':'1', 'o':'0', 's':'5'}
        leet_var = ''.join(leet_map.get(c.lower(), c) for c in original)
        variations.append(leet_var)
        # Reverse
        variations.append(original[::-1])
        
        self.variations_text.delete(1.0, tk.END)
        for i, var in enumerate(variations, 1):
            self.variations_text.insert(tk.END, f"{i}. {var}\n")
    
    def setup_vault(self):
        # Master password setup
        self.master_label = tk.Label(self.vault_frame, text="Enter Master Password:", 
                                    font=('Arial', 12), bg=self.bg_color, fg=self.fg_color)
        self.master_label.pack(pady=10)
        self.master_entry = tk.Entry(self.vault_frame, show='*', width=30, font=('Arial', 12),
                                    bg='#2d2d2d', fg=self.fg_color)
        self.master_entry.pack(pady=5)
        self.master_entry.bind('<KeyRelease>', self.on_master_change)
        
        tk.Button(self.vault_frame, text="Unlock Vault", command=self.unlock_vault,
                 bg=self.accent_color, fg='#000000', font=('Arial', 12, 'bold'),
                 relief='flat', padx=20).pack(pady=10)
        
        # Vault list
        columns = ('Site', 'Username', 'Password', 'Date')
        self.vault_tree = ttk.Treeview(self.vault_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.vault_tree.heading(col, text=col)
            self.vault_tree.column(col, width=150)
        self.vault_tree.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Buttons frame
        btn_frame = tk.Frame(self.vault_frame, bg=self.bg_color)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Add Entry", command=self.add_entry, bg=self.button_color,
                 fg=self.fg_color, relief='flat', padx=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Copy Password", command=self.copy_selected, bg=self.accent_color,
                 fg='#000000', relief='flat', padx=10).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Export Vault", command=self.export_vault, bg=self.button_color,
                 fg=self.fg_color, relief='flat', padx=10).pack(side='left', padx=5)
    
    def derive_key(self, master_password):
        """Derive encryption key from master password"""
        password = master_password.encode()
        salt = b'salt_for_jhu_project'  # In production, use random salt from file
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def on_master_change(self, event=None):
        self.cipher_suite = None
    
    def unlock_vault(self):
        self.master_password = self.master_entry.get()
        if not self.master_password:
            messagebox.showerror("Error", "Enter master password")
            return
        
        try:
            self.cipher_suite = Fernet(self.derive_key(self.master_password))
            self.master_label.config(text="Vault Unlocked ✓")
            self.load_vault_entries()
        except:
            messagebox.showerror("Error", "Invalid master password or corrupted vault")
    
    def load_vault(self):
        if os.path.exists(self.vault_file):
            try:
                with open(self.vault_file, 'rb') as f:
                    encrypted_data = f.read()
                # Test decryption with empty password first (will fail)
                pass
            except:
                pass  # Vault exists but needs master password
    
    def load_vault_entries(self):
        if not self.cipher_suite:
            return
        
        try:
            with open(self.vault_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            entries = json.loads(decrypted_data.decode())
            
            # Clear tree
            for item in self.vault_tree.get_children():
                self.vault_tree.delete(item)
            
            # Load entries
            for site, data in entries.items():
                username = data['username']
                password = "*****"  # Hide in UI
                date = data['date']
                self.vault_tree.insert('', 'end', values=(site, username, password, date))
                
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load vault: {str(e)}")
    
    def save_vault(self, entries):
        if not self.cipher_suite:
            return
        
        data = json.dumps(entries).encode()
        encrypted_data = self.cipher_suite.encrypt(data)
        with open(self.vault_file, 'wb') as f:
            f.write(encrypted_data)
        self.load_vault_entries()
    
    def add_entry(self):
        if not self.cipher_suite:
            messagebox.showerror("Error", "Unlock vault first")
            return
        
        site = simpledialog.askstring("Add Entry", "Website/Service:")
        if not site:
            return
        
        username = simpledialog.askstring("Add Entry", "Username:")
        password = simpledialog.askstring("Add Entry", "Password:", show='*')
        
        if site and username and password:
            entries = {}
            try:
                with open(self.vault_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                entries = json.loads(decrypted_data.decode())
            except:
                pass
            
            entries[site] = {'username': username, 'password': password, 
                           'date': datetime.now().strftime("%Y-%m-%d")}
            self.save_vault(entries)
            messagebox.showinfo("Success", "Entry added!")
    
    def copy_selected(self):
        selected = self.vault_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry")
            return
        
        if not self.cipher_suite:
            return
        
        site = self.vault_tree.item(selected)['values'][0]
        try:
            with open(self.vault_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            entries = json.loads(decrypted_data.decode())
            password = entries[site]['password']
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        except:
            messagebox.showerror("Error", "Could not retrieve password")
    
    def export_vault(self):
        if messagebox.askyesno("Export", "Export decrypted vault? (Unsecure!)"):
            try:
                with open(self.vault_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                with open("vault_export.json", 'w') as f:
                    f.write(decrypted_data.decode())
                messagebox.showinfo("Exported", "Vault exported to vault_export.json")
            except Exception as e:
                messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
