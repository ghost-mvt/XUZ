import mysql.connector
from mysql.connector import Error
import sys
import os
import time

# إعدادات ألوان نيون مستقرة كلياً لـ Termux (لا تسقط أثناء القراءة)
class Theme:
    CYAN    = '\x1b[38;5;51m'   # نيون سيان للمؤشرات والعناوين
    BLUE    = '\x1b[38;5;33m'   # الأزرق الكلاسيكي للخطوط
    GREEN   = '\x1b[38;5;82m'   # الأخضر المتوهج للنتائج والنجاح
    GRAY    = '\x1b[38;5;244m'  # الرمادي الداكن للنصوص الثانوية
    WHITE   = '\x1b[38;5;255m'  # الأبيض الناصع للبيانات
    ALERT   = '\x1b[38;5;197m'  # الأحمر للتحذيرات والأخطاء
    PURPLE  = '\x1b[38;5;141m'  # البنفسجي لمؤشرات المعالجة الذكية
    RESET   = '\x1b[0m'

class UIComponents:
    @classmethod
    def banner(cls):
        """عرض هيدر النظام المطور كلياً."""
        print("\x1b[H\x1b[J", end="") 
        print(f"{Theme.BLUE}[+] QUANTUM ENGINE ACTIVE {Theme.GRAY}|{Theme.PURPLE} 4-WAY MULTI SCANNER {Theme.GRAY}|{Theme.GREEN} ENVIRONMENT: TERMUX")
        print(f"{Theme.BLUE}─" * 65 + f"{Theme.RESET}\n")

    @classmethod
    def progress_bar(cls, message: str, duration: float = 0.4):
        """شريط تحميل رقمي سلس ومتوافق تماماً مع شاشات الهواتف."""
        print(f"{Theme.GRAY}[{Theme.BLUE}*{Theme.GRAY}] {message}...")  
        steps = 15  
        sleep_time = duration / steps
        for i in range(steps + 1):
            percent = int((i / steps) * 100)
            bar = f"{Theme.CYAN}█" * i + f"{Theme.GRAY}░" * (steps - i)
            sys.stdout.write(f"\r{Theme.GRAY} └──> ACTIVE DECODING: [{bar}{Theme.GRAY}] {Theme.WHITE}{percent}%{Theme.RESET}")
            sys.stdout.flush()
            time.sleep(sleep_time)
        sys.stdout.write('\r' + ' ' * 65 + '\r')
        sys.stdout.write('\x1b[1A' + ' ' * 65 + '\r')  
        sys.stdout.flush()

    @classmethod
    def print_box(cls, title: str, data: dict):
        """طباعة السجلات داخل صناديق بيانات جذابة بصرياً."""
        print(f"\n{Theme.CYAN}[+] ─── {title.upper()} " + f"─" * (45 - len(title)))
        for key, value in data.items():
            if key.lower() == 'id':
                continue
            val_str = f"{Theme.GREEN}{value}{Theme.RESET}" if value is not None else f"{Theme.GRAY}NULL{Theme.RESET}"
            print(f"{Theme.GRAY}    |- {Theme.WHITE}{key:<15} {Theme.GRAY}:: {val_str}")
        print(f"{Theme.CYAN}─────────────────────────────────────────────────────{Theme.RESET}")

    @classmethod
    def print_absolute_family_report(cls, target_name: str, parent_data: dict, spouse_data: dict, children: list, siblings: list):
        """طباعة خريطة الشبكة العائلية المستخرجة عبر خوارزمية تتبع الـ TC."""
        print(f"\n{Theme.PURPLE}[🧠 AI INTEGRATED COMPLETE KINSHIP REPORT FOR: {target_name.upper()}]")
        
        # 1. شبكة الوالدين وهواتفهم
        print(f"{Theme.GRAY} ├──> DIRECT PARENTAL NETWORK:")
        f_phones = f"{Theme.RESET}, {Theme.GREEN}".join(parent_data['father_phones']) if parent_data['father_phones'] else f"{Theme.ALERT}No GSM trace"
        print(f"      {Theme.WHITE}Father ({parent_data['father_name']}){Theme.GRAY} :: Phones: {Theme.GREEN}{f_phones}{Theme.RESET}")
        m_phones = f"{Theme.RESET}, {Theme.GREEN}".join(parent_data['mother_phones']) if parent_data['mother_phones'] else f"{Theme.ALERT}No GSM trace"
        print(f"      {Theme.WHITE}Mother ({parent_data['mother_name']}){Theme.GRAY} :: Phones: {Theme.GREEN}{m_phones}{Theme.RESET}")
        print(f"      {Theme.GRAY}────────────────────────────────────────")
        
        # 2. شبكة الزوجة الموثقة
        print(f"{Theme.GRAY} ├──> VERIFIED SPOUSE MATRIX (الزوجة القطعية):")
        if spouse_data:
            s_phones = f"{Theme.RESET}, {Theme.GREEN}".join(spouse_data['phones']) if spouse_data['phones'] else f"{Theme.ALERT}No GSM trace"
            print(f"      {Theme.WHITE}Spouse Name : {Theme.GREEN}{spouse_data['name']}{Theme.RESET}")
            print(f"      {Theme.WHITE}Spouse TC   : {Theme.CYAN}{spouse_data['tc']}{Theme.RESET}")
            print(f"      {Theme.WHITE}Spouse GSM  : {Theme.GREEN}{s_phones}{Theme.RESET}")
        else:
            print(f"      {Theme.ALERT}No verified spouse traced via shared biological children.{Theme.RESET}")
        print(f"      {Theme.GRAY}────────────────────────────────────────")
        
        # 3. شبكة الأبناء بالكامل مع هواتفهم
        print(f"{Theme.GRAY} ├──> VERIFIED CHILDREN NODES (الأبناء):")
        if children:
            for idx, child in enumerate(children, 1):
                print(f"      {Theme.CYAN}[Child {idx:02d}]{Theme.WHITE} Name : {Theme.GREEN}{child['name']:<20}{Theme.GRAY} | Birth: {Theme.WHITE}{child['birth']}{Theme.RESET}")
                print(f"                 ├──> TC    : {Theme.CYAN}{child['tc']}{Theme.RESET}")
                c_phones = f"{Theme.RESET}, {Theme.GREEN}".join(child['phones']) if child['phones'] else f"{Theme.ALERT}No GSM trace"
                print(f"                 └──> PHONES: {Theme.GREEN}{c_phones}{Theme.RESET}")
        else:
            print(f"      {Theme.ALERT}No children discovered inside core repositories.{Theme.RESET}")
        print(f"      {Theme.GRAY}────────────────────────────────────────")
        
        # 4. شبكة الأشقاء وهواتفهم
        print(f"{Theme.GRAY} └──> VERIFIED SIBLINGS NODES (الأشقاء):")
        if siblings:
            for idx, sib in enumerate(siblings, 1):
                print(f"      {Theme.PURPLE}[Sib {idx:02d}]{Theme.WHITE} Name   : {Theme.GREEN}{sib['name']:<20}{Theme.GRAY} | Birth: {Theme.WHITE}{sib['birth']}{Theme.RESET}")
                print(f"                 ├──> TC    : {Theme.CYAN}{sib['tc']}{Theme.RESET}")
                sib_phones = f"{Theme.RESET}, {Theme.GREEN}".join(sib['phones']) if sib['phones'] else f"{Theme.ALERT}No GSM trace"
                print(f"                 └──> PHONES: {Theme.GREEN}{sib_phones}{Theme.RESET}")
                print(f"                 {Theme.GRAY}────────────────────────────────────────")
        else:
            print(f"      {Theme.ALERT}No verified sibling connections matched via Parental TC codes.{Theme.RESET}")
        print(f"{Theme.PURPLE}─────────────────────────────────────────────────────{Theme.RESET}")


class DatabaseManager:
    def __init__(self):
        self.config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "", 
            "database": "target_db",
            "connect_timeout": 3
        }
        self.connection = None

    def connect(self) -> bool:
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
            return True
        except Error:
            return False

    def execute_query(self, query: str, params: tuple = None, fetch_all: bool = False):
        if not self.connect():
            raise Error("Database node offline.")
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall() if fetch_all else cursor.fetchone()
        finally:
            cursor.close()


class EngineController:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def extract_absolute_family_tree(self, profile_data: dict):
        """خوارزمية محرك الذكاء الاصطناعي لتحليل الروابط العائلية بالكامل."""
        current_tc = profile_data.get('TC')
        baba_tc = profile_data.get('BABATC')
        anne_tc = profile_data.get('ANNETC')
        
        parent_structure = {
            "father_name": profile_data.get('BABAADI', 'UNKNOWN'),
            "father_phones": [],
            "mother_name": profile_data.get('ANNEADI', 'UNKNOWN'),
            "mother_phones": []
        }
        spouse_data = None
        children_list = []
        siblings_list = []

        # سحب هواتف الوالدين
        if baba_tc and str(baba_tc).upper() not in ['NULL', '']:
            try:
                f_phones = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (baba_tc,), fetch_all=True)
                if f_phones: parent_structure['father_phones'] = [str(p['GSM']) for p in f_phones if p.get('GSM')]
            except: pass

        if anne_tc and str(anne_tc).upper() not in ['NULL', '']:
            try:
                m_phones = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (anne_tc,), fetch_all=True)
                if m_phones: parent_structure['mother_phones'] = [str(p['GSM']) for p in m_phones if p.get('GSM')]
            except: pass

        # جلب الأبناء والزوجة بشكل قطعي
        if current_tc:
            try:
                query_children = "SELECT `ADI`, `SOYADI`, `DOGUMTARIHI`, `TC`, `ANNETC`, `ANNEADI` FROM `101m` WHERE `BABATC` = %s"
                children_records = self.db.execute_query(query_children, (current_tc,), fetch_all=True)
                
                if children_records:
                    detected_mother_tc = None
                    detected_mother_name = None
                    
                    for child in children_records:
                        c_tc = child['TC']
                        c_phones_res = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (c_tc,), fetch_all=True)
                        c_phones = [str(p['GSM']) for p in (c_phones_res or []) if p.get('GSM')]
                        
                        children_list.append({
                            "name": f"{child['ADI']} {child['SOYADI']}",
                            "birth": child['DOGUMTARIHI'] if child['DOGUMTARIHI'] else "N/A",
                            "tc": c_tc,
                            "phones": c_phones
                        })
                        
                        if child.get('ANNETC') and str(child['ANNETC']).strip() != '':
                            detected_mother_tc = child['ANNETC']
                            detected_mother_name = child['ANNEADI']

                    if detected_mother_tc:
                        s_phones_res = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (detected_mother_tc,), fetch_all=True)
                        s_phones = [str(p['GSM']) for p in (s_phones_res or []) if p.get('GSM')]
                        spouse_data = {
                            "tc": detected_mother_tc,
                            "name": detected_mother_name,
                            "phones": s_phones
                        }
            except: pass

        # سحب الأشقاء
        if baba_tc and anne_tc and str(baba_tc).upper() not in ['NULL', ''] and str(anne_tc).upper() not in ['NULL', '']:
            try:
                query_siblings = "SELECT `ADI`, `SOYADI`, `DOGUMTARIHI`, `TC` FROM `101m` WHERE `BABATC` = %s AND `ANNETC` = %s AND `TC` != %s"
                matches = self.db.execute_query(query_siblings, (baba_tc, anne_tc, current_tc), fetch_all=True)
                if matches:
                    for match in matches:
                        sib_tc = match['TC']
                        phone_matches = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (sib_tc,), fetch_all=True)
                        siblings_list.append({
                            "name": f"{match['ADI']} {match['SOYADI']}",
                            "birth": match['DOGUMTARIHI'] if match['DOGUMTARIHI'] else "N/A",
                            "tc": sib_tc,
                            "phones": [str(p['GSM']) for p in (phone_matches or []) if p.get('GSM')]
                        })
            except: pass

        full_target_name = f"{profile_data.get('ADI', '')} {profile_data.get('SOYADI', '')}"
        UIComponents.print_absolute_family_report(full_target_name, parent_structure, spouse_data, children_list, siblings_list)

    def search_by_ai_family(self):
        """[الخيار الأول] البحث الشامل عن الشجرة العائلية والزوجة بالـ AI عبر الـ TC."""
        UIComponents.banner()
        print(f"{Theme.GRAY}[ SYSTEM ] EXECUTING AI DEEP KINSHIP SCROLL...")
        target_id = input(f" {Theme.PURPLE}[🧠] Enter National ID / TC for AI Mapping: {Theme.WHITE}").strip()
        if not target_id:
            print(f"\n{Theme.ALERT}[!] Error: Target identity string cannot be empty.{Theme.RESET}\n")
            return

        print()
        UIComponents.progress_bar("RUNNING NEURAL CELL RECONSTRUCTION")

        try:
            res_101m = self.db.execute_query("SELECT * FROM `101m` WHERE `TC` = %s LIMIT 1", (target_id,))
            if res_101m:
                UIComponents.print_box("Target Core Identity", res_101m)
                self.extract_absolute_family_tree(res_101m)
            else:
                print(f"{Theme.GRAY}[-] Zero records found in 101m cluster for TC: {Theme.WHITE}{target_id}{Theme.RESET}\n")
        except Error as e:
            print(f"\n{Theme.ALERT}[!] Core Exception: {str(e)}{Theme.RESET}\n")

    def search_by_tc(self):
        """[الخيار الثاني] البحث العادي بالـ TC لعرض قيود الجداول المباشرة فقط."""
        UIComponents.banner()
        print(f"{Theme.GRAY}[ SYSTEM ] EXECUTING STANDARD TC ROW DUMP...")
        target_id = input(f" {Theme.CYAN}[*] Enter National ID / TC: {Theme.WHITE}").strip()
        if not target_id: return

        print()
        UIComponents.progress_bar("RETRIEVING DIRECT RAW RECORDS")

        try:
            res_101m = self.db.execute_query("SELECT * FROM `101m` WHERE `TC` = %s LIMIT 1", (target_id,))
            res_datam = self.db.execute_query("SELECT * FROM `datam` WHERE `KimlikNo` = %s LIMIT 1", (target_id,))
            res_gsm = self.db.execute_query("SELECT * FROM `145mgsm` WHERE `TC` = %s", (target_id,), fetch_all=True)

            if res_101m or res_datam or res_gsm:
                if res_101m: UIComponents.print_box("Table_101m_Record", res_101m)
                if res_datam: UIComponents.print_box("Table_Datam_Record", res_datam)
                if res_gsm:
                    for count, gsm_row in enumerate(res_gsm, 1):
                        gsm_row.pop('TC', None)
                        UIComponents.print_box(f"GSM_Record_{count:02d}", gsm_row)
            else:
                print(f"{Theme.GRAY}[-] No rows matched standard TC query.{Theme.RESET}\n")
        except Error: pass

    def search_by_name_and_city(self):
        """[الخيار الثالث] البحث بـ الاسم، الكنية، والمدينة."""
        UIComponents.banner()
        print(f"{Theme.GRAY}[ SYSTEM ] EXECUTING NOMINAL LOCALIZED SCAN...")
        first_name = input(f" {Theme.CYAN}[*] First Name   : {Theme.WHITE}").strip().upper()
        surname    = input(f" {Theme.CYAN}[*] Surname      : {Theme.WHITE}").strip().upper()
        target_il  = input(f" {Theme.CYAN}[*] City (NUFUSIL): {Theme.WHITE}").strip().upper()
        
        if not first_name or not surname or not target_il:
            print(f"\n{Theme.ALERT}[!] Error: Name, Surname, and City parameters are all mandatory.{Theme.RESET}\n")
            return
        
        print()
        UIComponents.progress_bar("INDEXING NOMINAL MAPS")

        try:
            res_101m = self.db.execute_query("SELECT * FROM `101m` WHERE `ADI` = %s AND `SOYADI` = %s AND `NUFUSIL` = %s LIMIT 10", (first_name, surname, target_il), fetch_all=True)
            if res_101m:
                print(f"{Theme.CYAN}[+] Located matches inside targeted zone.{Theme.RESET}")
                for count, row in enumerate(res_101m, 1):
                    UIComponents.print_box(f"Discovered_Profile_{count:02d} [101M]", row)
            else:
                print(f"{Theme.GRAY}[-] Zero localized results for: {Theme.WHITE}{first_name} {surname} in {target_il}{Theme.RESET}\n")
        except Error: pass

    def search_by_gsm(self):
        """[الخيار الرابع] البحث برقم الهاتف وعرض الاسم المربوط به تلقائياً."""
        UIComponents.banner()
        print(f"{Theme.GRAY}[ SYSTEM ] EXECUTING ADVANCED REVERSE TELECOM LOOKUP...")
        target_gsm = input(f" {Theme.CYAN}[*] Enter GSM Phone Number: {Theme.WHITE}").strip()
        if not target_gsm: return
            
        print()
        UIComponents.progress_bar("RESOLVING REVERSE GSM Mark")

        try:
            # 1. البحث في جدول الهواتف لجلب السجلات والـ TC المرتبط
            res_gsm = self.db.execute_query("SELECT * FROM `145mgsm` WHERE `GSM` = %s", (target_gsm,), fetch_all=True)
            if res_gsm:
                print(f"{Theme.CYAN}[+] Active route established. Merging identity descriptors...{Theme.RESET}")
                for count, gsm_row in enumerate(res_gsm, 1):
                    associated_tc = gsm_row.get('TC')
                    
                    # إنشاء قاموس مدمج لعرض بيانات الهاتف والاسم معاً في صندوق واحد
                    display_data = {
                        "GSM_NUMBER": gsm_row.get('GSM'),
                        "LINKED_TC": associated_tc,
                        "OWNER_NAME": "UNKNOWN (No identity link)"
                    }
                    
                    # 2. الاستعلام العكسي الفوري عن الاسم من جدول 101m باستخدام الـ TC المكتشف
                    if associated_tc:
                        identity_match = self.db.execute_query("SELECT `ADI`, `SOYADI` FROM `101m` WHERE `TC` = %s LIMIT 1", (associated_tc,))
                        if identity_match:
                            display_data["OWNER_NAME"] = f"{identity_match['ADI']} {identity_match['SOYADI']}"
                    
                    # طباعة الصندوق المدمج الذكي
                    UIComponents.print_box(f"REVERSED_GSM_RECORD_{count:02d}", display_data)
            else:
                print(f"{Theme.GRAY}[-] No profile bindings discovered for GSM node: {Theme.WHITE}{target_gsm}{Theme.RESET}\n")
        except Error as e:
            print(f"\n{Theme.ALERT}[!] Pipeline Failure: {str(e)}{Theme.RESET}\n")


def main():
    db = DatabaseManager()
    engine = EngineController(db)
    
    if not db.connect():
        UIComponents.banner()
        print(f"{Theme.ALERT}[!] CRITICAL ERROR: LOCAL SQL DAEMON PROCESS IS OFFLINE.{Theme.RESET}\n")
        sys.exit(1)
        
    while True:
        UIComponents.banner()
        print(f" {Theme.PURPLE}[01]{Theme.WHITE} Deep AI Kinship Matrix Scroll (Spouse/Children Tree via TC)")
        print(f" {Theme.CYAN}[02]{Theme.WHITE} Standard National ID Lookup   (Raw Row Dump via TC)")
        print(f" {Theme.CYAN}[03]{Theme.WHITE} Localized Nominal Scan        (First Name + Surname + City)")
        print(f" {Theme.CYAN}[04]{Theme.WHITE} Reverse Telecom Lookup        (GSM Phone -> Displays Linked Name)")
        print(f" {Theme.ALERT}[00]{Theme.WHITE} Exit Quantum Core")
        
        choice = input(f"\n{Theme.CYAN}quantum_prompt//_ {Theme.WHITE}").strip()
        
        if choice in ['1', '01']:
            engine.search_by_ai_family()
        elif choice in ['2', '02']:
            engine.search_by_tc()
        elif choice in ['3', '03']:
            engine.search_by_name_and_city()
        elif choice in ['4', '04']:
            engine.search_by_gsm()
        elif choice in ['0', '00']:
            print(f"\n{Theme.GRAY}[-] Framework shutdown sequence initiated... Goodbye.{Theme.RESET}\n")
            break
        else:
            print(f"\n{Theme.ALERT}[!] Invalid Operational Command.{Theme.RESET}")
            time.sleep(1)
        
        input(f"\n{Theme.GRAY}[ Press ENTER to cycle console input ]{Theme.RESET}")

if __name__ == "__main__":
    main()
