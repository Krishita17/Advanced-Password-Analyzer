# 🔐 Advanced Password Analyzer & Manager

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=yellow)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/YOURUSERNAME/Advanced-Password-Analyzer?style=social)](https://github.com/YOURUSERNAME/Advanced-Password-Analyzer)

A professional-grade **Password Manager & Security Analyzer** built in Python with Tkinter GUI. Designed for cybersecurity students and professionals, it combines password strength evaluation (entropy + crack-time estimation), memorable passphrase generation (Diceware-style with dates), policy-compliant variations, and a secure AES-encrypted vault [web:39][web:40][web:35].


- # 🔐 Advanced Password Analyzer & Manager

A professional-grade Password Manager & Security Analyzer built in Python with advanced encryption, password strength evaluation, and comprehensive vault management.

## ✨ Enhanced Features

- **Strength Checker**: Entropy calculation, crack-time estimation
- **Memorable Generator**: Diceware words + personal dates
- **Secure Vault**: AES-256 encryption
- **🆕 Password History**: Track password changes
- **🆕 CSV Import/Export**: Bulk backup/restore
- **🆕 Delete Functionality**: Secure entry removal
- **🆕 Clipboard Auto-Clear**: 30-second security timeout

## 🚀 Quick Start

```bash
git clone https://github.com/Krishita17/Advanced-Password-Analyzer.git
cd Advanced-Password-Analyzer
pip install -r requirements.txt
python password_manager.py

| Feature | Security Level | Memorability |
|---------|----------------|--------------|
| Strength Checker | High (Entropy) | N/A [web:35] |
| Memorable Gen | Medium-High | High [web:40] |
| Random Gen | Very High | Low |
| Vault | AES-256 | N/A |

## 🎯 Demo Screenshots

*(Add screenshots: strength meter, generator tab, vault unlocked)*

## 🚀 Quick Start

1. **Clone & Install**:
   ```bash
   git clone https://github.com/YOURUSERNAME/Advanced-Password-Analyzer.git
   cd Advanced-Password-Analyzer
   pip install -r requirements.txt  # cryptography pyperclip
   ```

2. **Run**:
   
   ```bash
   python password_manager.py
   ```

3. **Usage**:
    - Analyze any password's strength in real-time
    - Generate "correct-horse-mar25" style passphrases
    - Create variations for your company's policy
    - Store/retrieve encrypted entries with master password

## 🛠️ Technical Highlights (Cybersecurity Focus)

- **Entropy**: $H = L \times \log_2(C)$ where $L$ = length, $C$ = charset size [web:39]
- **Crack Time**: $2^H / 10^{12}$ seconds (modern GPU benchmark)
- **Key Derivation**: PBKDF2-HMAC-SHA256 (100k iterations)
- **Encryption**: Fernet (AES-128-CBC + HMAC-SHA256)
- **No Persistence**: Clipboard clears automatically; local-only storage


## 📊 Security Audit Checklist

- [x] No plaintext storage
- [x] Secure random (secrets/crypto)
- [x] No hard-coded secrets
- [x] Input validation
- [x] Compliant with OWASP password guidelines


## 🔒 Future Enhancements

- Biometric unlock (face_recognition)
- TOTP 2FA integration
- Browser extension
- Cloud sync (end-to-end encrypted)
- zxcvbn realistic guessing [web:1]


## 📸 Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐
│   Tkinter GUI   │───▶│   Encryption     │
│  (Dark Theme)   │    │   (Fernet/AES)   │
└──────────┬──────┘    └────────┬─────────┘
           │                    │
           ▼                    ▼
┌──────────┼──────┐    ┌────────┼─────────┐
│Strength │Vault  │    │JSON File│ (enc)  │
│Analyzer │Storage│    │         │        │
└──────────┘      └───▶└─────────┘        │
                                          │
                                 ┌─────────▼─────────┐
                                 │ Disk (encrypted)   │
                                 └────────────────────┘
```


## 🤝 Contributing

1. Fork \& PR
2. Add tests: `pytest`
3. Follow PEP8: `black .`

## 📄 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- Built for [Johns Hopkins MS Cybersecurity](https://isi.jhu.edu/) portfolio
- Inspired by Diceware [web:40] \& OWASP guidelines
- Icons: [Icons8](https://icons8.com/)

**⭐ Star if useful!** Questions? Open an issue.
