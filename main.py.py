import subprocess
import re

# تلوين مخرجات الترمينال (ANSI Escape Codes)
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

def banner():
    subprocess.call('clear', shell=True)
    print(f"{BLUE}" + "="*50)
    print("""
    █████╗ ██╗     ███╗   ███╗███╗   ███╗
   ██╔══██╗██║     ████╗ ████║████╗ ████║
   ███████║██║     ██╔████╔██║██╔████╔██║
   ██╔══██║██║     ██║╚██╔╝██║██║╚██╔╝██║
   ██║  ██║███████╗██║ ╚═╝ ██║██║ ╚═╝ ██║
   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     ╚═╝
    """)
    print(f"       --- ALMM MAC-Changer v2.0 ---        ")
    print("="*50 + f"{RESET}\n")

def get_interface():
    # جلب كرت الشبكة الرئيسي النشط تلقائياً
    cmd = "ip route show default | awk '/default/ {print $5}'"
    try:
        interface_name = subprocess.check_output(cmd, shell=True).decode().strip()
        if interface_name:
            print(f"{GREEN}[+]{RESET} Detected active interface: {BLUE}{interface_name}{RESET}")
            return interface_name
        else:
            raise Exception
    except:
        print(f"{YELLOW}[!] Could not detect active interface automatically.{RESET}")
        return input(f"{GREEN}[?]{RESET} Enter network interface manually (e.g., eth0): ")

def get_arguments(interface):
    print("-"*50)
    while True:
        new_address = input(f"{GREEN}[?]{RESET} Enter your new MAC address: ").strip()
        
        # التحقق من أن الماك ادرس المدخل صيغته صحيحة (Regex)
        if re.match(r"^([0-9a-fA-F]{2}[:.-]){5}[0-9a-fA-F]{2}$", new_address):
            return interface, new_address
        else:
            print(f"{RED}[-] Invalid MAC address format. Try again (e.g., 00:11:22:33:44:55).{RESET}")

def mac_change(interface, new_mac):
    print("-"*50)
    print(f"{YELLOW}[*] Status: Changing MAC address for {interface} to {new_mac}...{RESET}")
    
    # تنفيذ الأوامر مع إخفاء المخرجات الجانبية لتظل الواجهة نظيفة
    subprocess.call(f"sudo ifconfig {interface} down", shell=True)
    subprocess.call(f"sudo ifconfig {interface} hw ether {new_mac}", shell=True)
    subprocess.call(f"sudo ifconfig {interface} up", shell=True)
    
    print(f"{GREEN}[+] MAC address changed successfully!{RESET}")
    print("-"*50)
    
    # استعراض الماك الجديد للتأكيد
    print(f"{BLUE}[*] Current Interface Details:{RESET}")
    subprocess.call(f"ifconfig {interface} | grep -E 'ether|inet '", shell=True)
    print(f"{BLUE}" + "="*50 + f"{RESET}")

# تشغيل البرنامج
if __name__ == "__main__":
    banner()
    active_interface = get_interface()
    interface_name, mac_address = get_arguments(active_interface)
    mac_change(interface_name, mac_address)