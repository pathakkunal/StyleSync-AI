import os

def polish_dashboard():
    file_path = "dashboard.html"
    if not os.path.exists(file_path):
        print("❌ dashboard.html not found!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Force Branding Updates
    replacements = {
        "MerchFlow AI": "StyleSync AI",
        "MerchFlow": "StyleSync",
        "bg-primary": "bg-emerald-600",
        "text-primary": "text-emerald-500",
        "border-primary": "border-emerald-500",
        "from-primary": "from-emerald-500",
        "to-primary": "to-emerald-500",
        "hover:bg-primary": "hover:bg-emerald-500",
        "hover:text-primary": "hover:text-emerald-400"
    }

    for old, new in replacements.items():
        html = html.replace(old, new)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print("✅ Dashboard UI polished: Emerald Green Theme & StyleSync Branding applied.")

if __name__ == "__main__":
    polish_dashboard()
