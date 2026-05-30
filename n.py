import mysql.connector
from mysql.connector import Error
import sys
import os
import time

# إعدادات ألوان نيون مستقرة كلياً لـ Termux
class Theme:
    CYAN    = '\x1b[38;5;51m'   # نيون سيان
    BLUE    = '\x1b[38;5;33m'   # أزرق
    GREEN   = '\x1b[38;5;82m'   # أخضر
    GRAY    = '\x1b[38;5;244m'  # رمادي
    WHITE   = '\x1b[38;5;255m'  # أبيض
    ALERT   = '\x1b[38;5;197m'  # أحمر
    PURPLE  = '\x1b[38;5;141m'  # بنفسجي
    RESET   = '\x1b[0m'

class UIComponents:
    @classmethod
    def banner(cls):
        print("\x1b[H\x1b[J", end="") 
        print(f"{Theme.BLUE}[+] QUANTUM ENGINE ACTIVE {Theme.GRAY}|{Theme.PURPLE} 4-WAY MULTI SCANNER + GEO {Theme.GRAY}|{Theme.GREEN} ENVIRONMENT: TERMUX")
        print(f"{Theme.BLUE}─" * 65 + f"{Theme.RESET}\n")

    @classmethod
    def progress_bar(cls, message: str, duration: float = 0.4):
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
        print(f"\n{Theme.CYAN}[+] ─── {title.upper()} " + f"─" * (45 - len(title)))
        for key, value in data.items():
            if key.lower() == 'id':
                continue
            val_str = f"{Theme.GREEN}{value}{Theme.RESET}" if value is not None else f"{Theme.GRAY}NULL{Theme.RESET}"
            print(f"{Theme.GRAY}    |- {Theme.WHITE}{key:<15} {Theme.GRAY}:: {val_str}")
        print(f"{Theme.CYAN}─────────────────────────────────────────────────────{Theme.RESET}")

    @classmethod
    def print_absolute_family_report(cls, target_name: str, parent_data: dict, spouse_data: dict, 
                                   children: list, siblings: list, target_ikametgah: str = None):
        """طباعة خريطة الشبكة العائلية الكاملة مع عناوين السكن"""
        print(f"\n{Theme.PURPLE}[🧠 AI INTEGRATED COMPLETE KINSHIP REPORT FOR: {target_name.upper()}]")
        
        # عنوان المستهدف
        if target_ikametgah:
            print(f"{Theme.CYAN}[🏠] TARGET RESIDENCE : {Theme.WHITE}{target_ikametgah}{Theme.RESET}")
            print(f"{Theme.GRAY}────────────────────────────────────────")

        # 1. الوالدين
        print(f"{Theme.GRAY} ├──> DIRECT PARENTAL NETWORK:")
        f_phones = f"{Theme.RESET}, {Theme.GREEN}".join(parent_data['father_phones']) if parent_data['father_phones'] else f"{Theme.ALERT}No GSM trace"
        print(f"      {Theme.WHITE}Father ({parent_data['father_name']}){Theme.GRAY} :: Phones: {Theme.GREEN}{f_phones}{Theme.RESET}")
        if parent_data.get('father_ikametgah'):
            print(f"      {Theme.CYAN}       └──> Address: {Theme.WHITE}{parent_data['father_ikametgah']}{Theme.RESET}")
        
        m_phones = f"{Theme.RESET}, {Theme.GREEN}".join(parent_data['mother_phones']) if parent_data['mother_phones'] else f"{Theme.ALERT}No GSM trace"
        print(f"      {Theme.WHITE}Mother ({parent_data['mother_name']}){Theme.GRAY} :: Phones: {Theme.GREEN}{m_phones}{Theme.RESET}")
        if parent_data.get('mother_ikametgah'):
            print(f"      {Theme.CYAN}       └──> Address: {Theme.WHITE}{parent_data['mother_ikametgah']}{Theme.RESET}")
        print(f"      {Theme.GRAY}────────────────────────────────────────")
        
        # 2. الزوجة
        print(f"{Theme.GRAY} ├──> VERIFIED SPOUSE MATRIX:")
        if spouse_data:
            s_phones = f"{Theme.RESET}, {Theme.GREEN}".join(spouse_data['phones']) if spouse_data['phones'] else f"{Theme.ALERT}No GSM trace"
            print(f"      {Theme.WHITE}Spouse Name : {Theme.GREEN}{spouse_data['name']}{Theme.RESET}")
            print(f"      {Theme.WHITE}Spouse TC   : {Theme.CYAN}{spouse_data['tc']}{Theme.RESET}")
            print(f"      {Theme.WHITE}Spouse GSM  : {Theme.GREEN}{s_phones}{Theme.RESET}")
            if spouse_data.get('ikametgah'):
                print(f"      {Theme.CYAN}       └──> Address: {Theme.WHITE}{spouse_data['ikametgah']}{Theme.RESET}")
        else:
            print(f"      {Theme.ALERT}No verified spouse traced via shared biological children.{Theme.RESET}")
        print(f"      {Theme.GRAY}────────────────────────────────────────")
        
        # 3. الأبناء
        print(f"{Theme.GRAY} ├──> VERIFIED CHILDREN NODES:")
        if children:
            for idx, child in enumerate(children, 1):
                print(f"      {Theme.CYAN}[Child {idx:02d}]{Theme.WHITE} Name : {Theme.GREEN}{child['name']:<20}{Theme.GRAY} | Birth: {Theme.WHITE}{child['birth']}{Theme.RESET}")
                print(f"                 ├──> TC    : {Theme.CYAN}{child['tc']}{Theme.RESET}")
                c_phones = f"{Theme.RESET}, {Theme.GREEN}".join(child['phones']) if child['phones'] else f"{Theme.ALERT}No GSM trace"
                print(f"                 ├──> Phones: {Theme.GREEN}{c_phones}{Theme.RESET}")
                if child.get('ikametgah'):
                    print(f"                 └──> Address: {Theme.WHITE}{child['ikametgah']}{Theme.RESET}")
        else:
            print(f"      {Theme.ALERT}No children discovered inside core repositories.{Theme.RESET}")
        print(f"      {Theme.GRAY}────────────────────────────────────────")
        
        # 4. الأشقاء
        print(f"{Theme.GRAY} └──> VERIFIED SIBLINGS NODES:")
        if siblings:
            for idx, sib in enumerate(siblings, 1):
                print(f"      {Theme.PURPLE}[Sib {idx:02d}]{Theme.WHITE} Name   : {Theme.GREEN}{sib['name']:<20}{Theme.GRAY} | Birth: {Theme.WHITE}{sib['birth']}{Theme.RESET}")
                print(f"                 ├──> TC    : {Theme.CYAN}{sib['tc']}{Theme.RESET}")
                sib_phones = f"{Theme.RESET}, {Theme.GREEN}".join(sib['phones']) if sib['phones'] else f"{Theme.ALERT}No GSM trace"
                print(f"                 ├──> Phones: {Theme.GREEN}{sib_phones}{Theme.RESET}")
                if sib.get('ikametgah'):
                    print(f"                 └──> Address: {Theme.WHITE}{sib['ikametgah']}{Theme.RESET}")
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

    def get_ikametgah(self, tc):
        """جلب عنوان السكن من جدول datam"""
        if not tc:
            return "No address data"
        try:
            result = self.db.execute_query("SELECT `Ikametgah` FROM `datam` WHERE `KimlikNo` = %s LIMIT 1", (tc,))
            if result and result.get('Ikametgah'):
                return result['Ikametgah']
            return "No verified address"
        except:
            return "Address lookup failed"

    def extract_absolute_family_tree(self, profile_data: dict):
        """خوارزمية الذكاء الاصطناعي لاستخراج الشجرة العائلية + العناوين"""
        current_tc = profile_data.get('TC')
        baba_tc = profile_data.get('BABATC')
        anne_tc = profile_data.get('ANNETC')
        
        parent_structure = {
            "father_name": profile_data.get('BABAADI', 'UNKNOWN'),
            "father_phones": [],
            "father_ikametgah": "",
            "mother_name": profile_data.get('ANNEADI', 'UNKNOWN'),
            "mother_phones": [],
            "mother_ikametgah": ""
        }
        spouse_data = None
        children_list = []
        siblings_list = []

        # عناوين الوالدين
        if baba_tc:
            parent_structure['father_ikametgah'] = self.get_ikametgah(baba_tc)
        if anne_tc:
            parent_structure['mother_ikametgah'] = self.get_ikametgah(anne_tc)

        # جلب الأبناء والزوجة
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
                        c_ikametgah = self.get_ikametgah(c_tc)
                        
                        children_list.append({
                            "name": f"{child['ADI']} {child['SOYADI']}",
                            "birth": child['DOGUMTARIHI'] if child['DOGUMTARIHI'] else "N/A",
                            "tc": c_tc,
                            "phones": c_phones,
                            "ikametgah": c_ikametgah
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
                            "phones": s_phones,
                            "ikametgah": self.get_ikametgah(detected_mother_tc)
                        }
            except: pass

        # جلب الأشقاء
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
                            "phones": [str(p['GSM']) for p in (phone_matches or []) if p.get('GSM')],
                            "ikametgah": self.get_ikametgah(sib_tc)
                        })
            except: pass

        # عنوان المستهدف
        target_ikametgah = self.get_ikametgah(current_tc)

        full_target_name = f"{profile_data.get('ADI', '')} {profile_data.get('SOYADI', '')}"
        UIComponents.print_absolute_family_report(
            full_target_name, parent_structure, spouse_data, children_list, siblings_list, target_ikametgah
        )

    # باقي الدوال بدون تغيير (search_by_ai_family, search_by_tc, ...)

    def search_by_ai_family(self):
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
        UIComponents.banner()
        print(f"{Theme.GRAY}[ SYSTEM ] EXECUTING NOMINAL LOCALIZED SCAN + GEO...")
        first_name = input(f" {Theme.CYAN}[*] First Name   : {Theme.WHITE}").strip().upper()
        surname    = input(f" {Theme.CYAN}[*] Surname      : {Theme.WHITE}").strip().upper()
        target_il  = input(f" {Theme.CYAN}[*] City (NUFUSIL): {Theme.WHITE}").strip().upper()
        
        if not first_name or not surname or not target_il:
            print(f"\n{Theme.ALERT}[!] Error: Name, Surname, and City parameters are all mandatory.{Theme.RESET}\n")
            return
        
        print()
        UIComponents.progress_bar("INDEXING NOMINAL & GEOLOCATION MAPS")

        try:
            res_101m = self.db.execute_query("SELECT * FROM `101m` WHERE `ADI` = %s AND `SOYADI` = %s AND `NUFUSIL` = %s LIMIT 10", 
                                           (first_name, surname, target_il), fetch_all=True)
            if res_101m:
                print(f"{Theme.CYAN}[+] Located matches inside targeted zone. Correlating Ikametgah nodes...{Theme.RESET}")
                for count, row in enumerate(res_101m, 1):
                    current_tc = row.get('TC')
                    display_profile = dict(row)
                    display_profile['IKAMETGAH'] = "No verified data inside datam storage"
                    
                    if current_tc:
                        geo_match = self.db.execute_query("SELECT `Ikametgah` FROM `datam` WHERE `KimlikNo` = %s LIMIT 1", (current_tc,))
                        if geo_match and geo_match.get('Ikametgah'):
                            display_profile['IKAMETGAH'] = geo_match['Ikametgah']
                    
                    UIComponents.print_box(f"Localized_Profile_{count:02d} [101M + DATAM]", display_profile)
            else:
                print(f"{Theme.GRAY}[-] Zero localized results for: {Theme.WHITE}{first_name} {surname} in {target_il}{Theme.RESET}\n")
        except Error as e: 
            print(f"\n{Theme.ALERT}[!] Database Error inside Geo compiler: {str(e)}{Theme.RESET}\n")

    def search_by_gsm(self):
        UIComponents.banner()
        print(f"{Theme.GRAY}[ SYSTEM ] EXECUTING ADVANCED REVERSE TELECOM LOOKUP...")
        target_gsm = input(f" {Theme.CYAN}[*] Enter GSM Phone Number: {Theme.WHITE}").strip()
        if not target_gsm: return
            
        print()
        UIComponents.progress_bar("RESOLVING REVERSE GSM MARK")

        try:
            res_gsm = self.db.execute_query("SELECT * FROM `145mgsm` WHERE `GSM` = %s", (target_gsm,), fetch_all=True)
            if res_gsm:
                print(f"{Theme.CYAN}[+] Active route established. Merging identity descriptors...{Theme.RESET}")
                for count, gsm_row in enumerate(res_gsm, 1):
                    associated_tc = gsm_row.get('TC')
                    display_data = {
                        "GSM_NUMBER": gsm_row.get('GSM'),
                        "LINKED_TC": associated_tc,
                        "OWNER_NAME": "UNKNOWN (No identity link)"
                    }
                    if associated_tc:
                        identity_match = self.db.execute_query("SELECT `ADI`, `SOYADI` FROM `101m` WHERE `TC` = %s LIMIT 1", (associated_tc,))
                        if identity_match:
                            display_data["OWNER_NAME"] = f"{identity_match['ADI']} {identity_match['SOYADI']}"
                    
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
        print(f" {Theme.PURPLE}[01]{Theme.WHITE} Deep AI Kinship Matrix Scroll (Spouse/Children Tree + Address)")
        print(f" {Theme.CYAN}[02]{Theme.WHITE} Standard National ID Lookup")
        print(f" {Theme.CYAN}[03]{Theme.WHITE} Localized Nominal Scan + GEO")
        print(f" {Theme.CYAN}[04]{Theme.WHITE} Reverse Telecom Lookup")
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
