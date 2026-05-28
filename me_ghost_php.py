import mysql.connector
import sys
import os
import time
import subprocess
import shutil

# Professional Dark Gray & Blue Palette
B_BRIGHT = '\033[94m'  # أزرق غامق مشع للمؤشرات
B_DARK   = '\033[34m'  # أزرق كلاسيكي هادئ للخطوط
GRAY     = '\033[90m'  # رمادي داكن للنصوص الثانوية
WHITE    = '\033[97m'  # أبيض ناصع للمخرجات والبيانات
ALERT    = '\033[91m'  # أحمر خفيف للتنبيهات والأخطاء
RESET    = '\033[0m'

def banner():
    # تنظيف الشاشة بطريقة متوافقة تماماً مع Linux و Termux دون استدعاء أوامر النظام مباشرة
    print("\033[H\033[J", end="")
    print(f"{B_DARK}[+] CORE ENGINE ACTIVE {GRAY}|{B_BRIGHT} DB_NODE: 127.0.0.1 {GRAY}|{WHITE} ACCESS: GRANTED")
    print(f"{B_DARK}─"*70 + f"{RESET}\n")

def progress_bar(message, duration=2):
    """شريط تحميل خفيف وثابت في سطر واحد ويختفي تماماً فور اكتماله لتفادي مشاكل الحجم"""
    print(f"{GRAY}[{B_DARK}*{GRAY}] {message}...")  
    steps = 15  
    sleep_time = duration / steps
    
    for i in range(steps + 1):
        percent = int((i / steps) * 100)
        filled_length = int(steps * i // steps)
        bar = f"{B_BRIGHT}█" * filled_length + f"{GRAY}░" * (steps - filled_length)
        
        sys.stdout.write(f"\r{GRAY} └──> LOADING: [{bar}{GRAY}] {WHITE}{percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(sleep_time)
    
    # مسح أسطر التحميل كلياً من واجهة الـ Terminal عابر للمنصات
    sys.stdout.write('\r' + ' ' * 60 + '\r')
    sys.stdout.write('\033[1A' + ' ' * 60 + '\r')  
    sys.stdout.flush()

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="", 
        database="target_db",
        connect_timeout=3
    )

def check_mysql_status():
    """التحقق من حالة اتصال خادم قاعدة البيانات"""
    try:
        conn = connect_db()
        if conn.is_connected():
            conn.close()
            return True
    except mysql.connector.Error:
        return False

def start_mysql_automatically():
    """محاولة تفعيل السيرفر تلقائياً بديناميكية متوافقة مع أنظمة إدارة الخدمات في Linux و Termux"""
    print(f"{B_BRIGHT}[*] Optimizing framework environmental variables...{RESET}")
    is_termux = os.path.exists('/data/data/com.termux')
    
    try:
        if is_termux:
            # تفعيل السيرفر لبيئة Termux
            subprocess.Popen(["mariadbd-safe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # تفعيل السيرفر لأنظمة Linux / Kali / Ubuntu
            if shutil.which("systemctl"):
                # إذا كان النظام يعتمد على systemd
                subprocess.Popen(["sudo", "systemctl", "start", "mariadb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif shutil.which("service"):
                # كخيار بديل إذا كان يعتمد على init.d
                subprocess.Popen(["sudo", "service", "mysql", "start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                # الكاشف الأخير لـ MySQL المستقلة
                subprocess.Popen(["mysqld_safe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(4)  # منح السيرفر الوقت الكافي لتشغيل الـ Socket
        return check_mysql_status()
    except Exception:
        return False

def print_record_box(title, data):
    """طباعة البيانات المستخرجة داخل صندوق منسق ومنظم"""
    print(f"\n{B_BRIGHT}» {WHITE}{title} {GRAY}" + "─"*(60 - len(title)))
    for key, value in data.items():
        if key.lower() == 'id':
            continue
        val_str = str(value) if value is not None else "NULL"
        print(f"{GRAY}  {B_BRIGHT}{key:<18} {GRAY}:: {WHITE}{val_str}")
    print(f"{GRAY}─"*65 + f"{RESET}")

def search_by_id():
    banner()
    print(f"{GRAY}[ SYSTEM ] RUNNING IDENTITY SEARCH...")
    target_id = input(f" {B_BRIGHT}[*] Enter National ID / TC: {WHITE}").strip()
    
    if not target_id:
        print(f"\n{ALERT}[!] Error: Input identity string cannot be empty.{RESET}\n")
        return

    print()
    progress_bar("FETCHING STORAGE NODES", duration=2)

    try:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        
        query_101m = "SELECT * FROM `101m` WHERE `TC` = %s LIMIT 1"
        cursor.execute(query_101m, (target_id,))
        res_101m = cursor.fetchone()
        
        query_datam = "SELECT * FROM `datam` WHERE `KimlikNo` = %s LIMIT 1"
        cursor.execute(query_datam, (target_id,))
        res_datam = cursor.fetchone()

        query_gsm = "SELECT * FROM `145mgsm` WHERE `TC` = %s"
        cursor.execute(query_gsm, (target_id,))
        res_gsm = cursor.fetchall()
        
        if res_101m or res_datam or res_gsm:
            print(f"{B_BRIGHT}[+] Match found in system repositories.{RESET}")
            
            if res_101m:
                print_record_box("Table_101m_Record", res_101m)
                    
            if res_datam:
                print_record_box("Table_Datam_Record", res_datam)

            if res_gsm:
                count = 1
                for gsm_row in res_gsm:
                    if 'TC' in gsm_row:
                        del gsm_row['TC']
                    print_record_box(f"Table_145mgsm_Record_{count:02d}", gsm_row)
                    count += 1
        else:
            print(f"{GRAY}[-] No matching records found for: {WHITE}{target_id}{RESET}\n")
            
    except mysql.connector.Error:
        print(f"\n{ALERT}[!] Database Error: Connection Lost. Ensure MySQL service is alive.{RESET}\n")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def search_by_name():
    banner()
    print(f"{GRAY}[ SYSTEM ] RUNNING NOMINAL SEARCH...")
    first_name = input(f" {B_BRIGHT}[*] First Name   : {WHITE}").strip().upper()
    surname    = input(f" {B_BRIGHT}[*] Surname      : {WHITE}").strip().upper()
    target_il  = input(f" {GRAY}[*] City / NUFUSIL (Optional): {WHITE}").strip().upper()
    
    if not first_name or not surname:
        print(f"\n{ALERT}[!] Error: Name fields are required.{RESET}\n")
        return
    
    print()
    progress_bar("SCANNING NOMINAL RECORDS", duration=2)

    try:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        
        if target_il:
            query_101m = "SELECT * FROM `101m` WHERE `ADI` = %s AND `SOYADI` = %s AND `NUFUSIL` = %s LIMIT 10"
            cursor.execute(query_101m, (first_name, surname, target_il))
        else:
            query_101m = "SELECT * FROM `101m` WHERE `ADI` = %s AND `SOYADI` = %s LIMIT 10"
            cursor.execute(query_101m, (first_name, surname))
        res_101m = cursor.fetchall()
        
        full_name_pattern = f"{first_name} {surname}"
        if target_il:
            query_datam = "SELECT * FROM `datam` WHERE `AdSoyad` LIKE %s AND `Ikametgah` LIKE %s LIMIT 10"
            il_pattern = f"%{target_il}%"
            cursor.execute(query_datam, (full_name_pattern, il_pattern))
        else:
            query_datam = "SELECT * FROM `datam` WHERE `AdSoyad` LIKE %s LIMIT 10"
            cursor.execute(query_datam, (full_name_pattern,))
        res_datam = cursor.fetchall()
        
        if res_101m or res_datam:
            print(f"{B_BRIGHT}[+] Matches recovered from storage buffer.{RESET}")
            
            discovered_tcs = set()
            count = 1
            for row in res_101m:
                print_record_box(f"Record_{count:02d} [101M]", row)
                if row.get('TC'):
                    discovered_tcs.add(row['TC'])
                count += 1
                
            for row in res_datam:
                print_record_box(f"Record_{count:02d} [DATAM]", row)
                if row.get('KimlikNo'):
                    discovered_tcs.add(row['KimlikNo'])
                count += 1
                
            for current_tc in discovered_tcs:
                query_gsm = "SELECT * FROM `145mgsm` WHERE `TC` = %s"
                cursor.execute(query_gsm, (current_tc,))
                res_gsm = cursor.fetchall()
                
                if res_gsm:
                    gsm_count = 1
                    for gsm_row in res_gsm:
                        if 'TC' in gsm_row:
                            del gsm_row['TC']
                        print_record_box(f"Linked_GSM_Record_{gsm_count:02d} [For TC: {current_tc}]", gsm_row)
                        gsm_count += 1
        else:
            print(f"{GRAY}[-] Zero results returned for specified query.{RESET}\n")
            
    except mysql.connector.Error:
        print(f"\n{ALERT}[!] Database Error: Connection Lost. Ensure MySQL service is alive.{RESET}\n")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def search_by_gsm():
    banner()
    print(f"{GRAY}[ SYSTEM ] RUNNING GSM PROTOCOL SEARCH...")
    target_gsm = input(f" {B_BRIGHT}[*] Enter GSM Number: {WHITE}").strip()
    
    if not target_gsm:
        print(f"\n{ALERT}[!] Error: GSM field cannot be empty.{RESET}\n")
        return
        
    print()
    progress_bar("CORRELATING NETWORK ID", duration=2)

    try:
        connection = connect_db()
        cursor = connection.cursor(dictionary=True)
        
        query_gsm = "SELECT * FROM `145mgsm` WHERE `GSM` = %s"
        cursor.execute(query_gsm, (target_gsm,))
        res_gsm = cursor.fetchall()
        
        if res_gsm:
            print(f"{B_BRIGHT}[+] GSM Match found. Extracting identity relations...{RESET}")
            
            count = 1
            associated_tcs = set()
            for gsm_row in res_gsm:
                if gsm_row.get('TC'):
                    associated_tcs.add(gsm_row['TC'])
                if 'TC' in gsm_row:
                    del gsm_row['TC']
                print_record_box(f"Table_145mgsm_Record_{count:02d}", gsm_row)
                count += 1
            
            for current_tc in associated_tcs:
                print(f"\n{GRAY}[🔍] Fetching profile details for TC: {WHITE}{current_tc}{GRAY}...{RESET}")
                
                query_101m = "SELECT * FROM `101m` WHERE `TC` = %s LIMIT 1"
                cursor.execute(query_101m, (current_tc,))
                res_101m = cursor.fetchone()
                
                query_datam = "SELECT * FROM `datam` WHERE `KimlikNo` = %s LIMIT 1"
                cursor.execute(query_datam, (current_tc,))
                res_datam = cursor.fetchone()
                
                if res_101m:
                    print_record_box(f"Linked_Profile_[101M]", res_101m)
                if res_datam:
                    print_record_box(f"Linked_Profile_[DATAM]", res_datam)
        else:
            print(f"{GRAY}[-] No records found for GSM: {WHITE}{target_gsm}{RESET}\n")
            
    except mysql.connector.Error:
        print(f"\n{ALERT}[!] Database Error: Connection Lost. Ensure MySQL service is alive.{RESET}\n")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    banner()
    
    # تشغيل الفحص الأولي للتحقق من سلامة البورتات المحلية وتطابق النظام
    progress_bar("INITIALIZING ENGINE & VERIFYING NODES", duration=2)
    
    if not check_mysql_status():
        print(f"{ALERT}[!] LOCAL DATABASE OFFLINE DETECTED")
        print(f"{GRAY}──────────────────────────────────────────────────────────────────────")
        ans = input(f"{WHITE}[?] Do you want to start MySQL automatically? ({B_BRIGHT}y{WHITE}/{ALERT}n{WHITE}) [{B_BRIGHT}y{WHITE}]: ").strip().lower()
        
        if ans in ['y', 'yes', '']:
            print(f"{GRAY}──────────────────────────────────────────────────────────────────────")
            if start_mysql_automatically():
                print(f"{B_BRIGHT}[+] SUCCESS: MySQL Server linked successfully.{RESET}")
                print(f"{GRAY}──────────────────────────────────────────────────────────────────────\n")
                time.sleep(1)
            else:
                print(f"\n{ALERT}[!] CRITICAL: Failed to wake MySQL daemon process automatically.{RESET}")
                print(f"{WHITE}[*] Please ensure MySQL daemon is pre-installed or try launching it manually.\n")
                sys.exit(1)
        else:
            print(f"\n{GRAY}[-] Aborted by user. Exiting engine framework...{RESET}\n")
            sys.exit(0)
        
    print(f" {B_BRIGHT}[01]{WHITE} Search via Identity Protocol (ID / TC)")
    print(f" {B_BRIGHT}[02]{WHITE} Search via Nominal Protocol (NAME / SURNAME)")
    print(f" {B_BRIGHT}[03]{WHITE} Search via GSM Protocol (PHONE NUMBER)")
    choice = input(f"\n{B_BRIGHT}sys_prompt//_ {WHITE}").strip()
    
    if choice in ['1', '01']:
        search_by_id()
    elif choice in ['2', '02']:
        search_by_name()
    elif choice in ['3', '03']:
        search_by_gsm()
    else:
        print(f"\n{GRAY}[-] Exiting console interface...{RESET}\n")
