import mysql.connector
from mysql.connector import Error
import sys
import os
import time

try:
    import tty
    import termios
except ImportError:
    tty = None

class Theme:
    RED_B   = '\x1b[38;5;196m'  # أحمر فوسفوري حاد للمؤشرات
    RED_D   = '\x1b[38;5;88m'   # أحمر داكن جداً للهياكل والحدود
    TEXT    = '\x1b[38;5;252m'  # رمادي فاتح للنصوص
    STEALTH = '\x1b[38;5;240m'  # رمادي معتم للمسارات
    WHITE   = '\x1b[38;5;255m'  # أبيض ناصع
    WARN    = '\x1b[38;5;130m'  # برتقالي محروق
    RESET   = '\x1b[0m'

class UIComponents:
    @classmethod
    def get_width(cls):
        try:
            return os.get_terminal_size().columns - 4
        except OSError:
            return 76

    @classmethod
    def clear_screen(cls):
        sys.stdout.write("\x1b[H\x1b[J")
        sys.stdout.flush()

    @classmethod
    def banner(cls):
        cls.clear_screen()
        w = cls.get_width()
        print(f" {Theme.RED_D}┌" + "─" * w + "┐")
        print(f" {Theme.RED_D}│ {Theme.RED_B}fso_reconstruct_engine_v7.0.0{Theme.STEALTH} // {Theme.WHITE}FSOCIETY_INTERNAL_NET".ljust(w + 14) + f"{Theme.RED_D}│")
        print(f" {Theme.RED_D}│ {Theme.STEALTH}STATUS: {Theme.TEXT}STREAM_LOAD_OK{Theme.STEALTH} :: {Theme.RED_D}ENV_CONTEXT: {Theme.TEXT}LIVE_TERMUX_KALI".ljust(w + 33) + f"{Theme.RED_D}│")
        print(f" {Theme.RED_D}└" + "─" * w + "┘{Theme.RESET}")

    @classmethod
    def progress_bar(cls, message: str, duration: float = 0.3):
        w = max(20, cls.get_width() - 30)
        sys.stdout.write(f"\n {Theme.STEALTH}[{Theme.RED_B}*{Theme.STEALTH}] {Theme.TEXT}INJECTING: {message.upper()}...\n")
        sys.stdout.flush()
        steps = 20  
        sleep_time = duration / steps
        for i in range(steps + 1):
            percent = int((i / steps) * 100)
            fill = int((i / steps) * w)
            bar = f"{Theme.RED_B}█" * fill + f"{Theme.STEALTH}·" * (w - fill)
            sys.stdout.write(f"\r {Theme.RED_D}[{bar}{Theme.RED_D}]─({Theme.WHITE}{percent:3d}%{Theme.RED_D})")
            sys.stdout.flush()
            time.sleep(sleep_time)
        sys.stdout.write('\r' + ' ' * (w + 20) + '\r')
        sys.stdout.write('\x1b[1A' + ' ' * (w + 20) + '\r')
        sys.stdout.flush()

    @classmethod
    def print_box(cls, title: str, data: dict):
        w = cls.get_width()
        print(f"\n {Theme.RED_D}┌── {Theme.WHITE}{title.upper()} " + f"─" * (w - len(title) - 5) + f"┐")
        for key, value in data.items():
            if key.lower() == 'id':
                continue
            val_str = f"{Theme.TEXT}{value}{Theme.RESET}" if value is not None else f"{Theme.WARN}[NO_RECORD]{Theme.RESET}"
            key_len = 18
            val_max_len = w - key_len - 6
            val_truncated = str(value)[:val_max_len] if value is not None else "[NO_RECORD]"
            val_display = f"{Theme.TEXT}{val_truncated:<{val_max_len}}{Theme.RESET}"
            print(f" {Theme.RED_D}│ {Theme.TEXT}{key:<{key_len}} {Theme.STEALTH}:: {val_display} {Theme.RED_D}│")
        print(f" {Theme.RED_D}└" + f"─" * w + f"┘{Theme.RESET}")

    @classmethod
    def print_absolute_family_report(cls, target_name: str, parent_data: dict, spouse_data: dict, 
                                   children: list, siblings: list, target_ikametgah: str = None, filters: dict = None):
        if filters is None:
            filters = {"address": True, "spouse": True, "children": True, "siblings": True, "sibling_phones": True}
        w = cls.get_width()   
        print(f"\n {Theme.RED_D}╔" + "═" * w + "╗")
        print(f" {Theme.RED_D}║ {Theme.WHITE}RELATIONAL DATA RECONSTRUCTION SCHEMA: {Theme.RED_B}{target_name.upper()}".ljust(w + 14) + f"{Theme.RED_D}║")
        print(f" {Theme.RED_D}╚" + "═" * w + "╝")
        
        if filters["address"] and target_ikametgah:
            print(f"  {Theme.STEALTH}[{Theme.RED_B}LBS_LOC{Theme.STEALTH}] {Theme.TEXT}TARGET COORD {Theme.STEALTH}» {Theme.TEXT}{target_ikametgah}")
            print(f"  {Theme.RED_D}╌" * w)

        print(f"  {Theme.RED_B}» {Theme.WHITE}PARENTAL NODES:")
        f_phones = f"{Theme.STEALTH}, {Theme.TEXT}".join(parent_data['father_phones']) if parent_data['father_phones'] else f"{Theme.WARN}EMPTY"
        print(f"    {Theme.STEALTH}├── {Theme.TEXT}Father : {Theme.WHITE}{parent_data['father_name']:<22} {Theme.STEALTH}[GSM: {Theme.TEXT}{f_phones}{Theme.STEALTH}]")
        if filters["address"] and parent_data.get('father_ikametgah'):
            print(f"    {Theme.STEALTH}│   └── LBS » {Theme.TEXT}{parent_data['father_ikametgah']}")
        
        m_phones = f"{Theme.STEALTH}, {Theme.TEXT}".join(parent_data['mother_phones']) if parent_data['mother_phones'] else f"{Theme.WARN}EMPTY"
        print(f"    {Theme.STEALTH}└── {Theme.TEXT}Mother : {Theme.WHITE}{parent_data['mother_name']:<22} {Theme.STEALTH}[GSM: {Theme.TEXT}{m_phones}{Theme.STEALTH}]")
        if filters["address"] and parent_data.get('mother_ikametgah'):
            print(f"        └── LBS » {Theme.TEXT}{parent_data['mother_ikametgah']}")
        print(f"  {Theme.RED_D}╌" * w)
        
        if filters["spouse"]:
            print(f"  {Theme.RED_B}» {Theme.WHITE}SPOUSE COMPILER LINK:")
            if spouse_data:
                s_phones = f"{Theme.STEALTH}, {Theme.TEXT}".join(spouse_data['phones']) if spouse_data['phones'] else f"{Theme.WARN}EMPTY"
                print(f"    {Theme.STEALTH}├── {Theme.TEXT}Name   : {Theme.WHITE}{spouse_data['name']}")
                print(f"    {Theme.STEALTH}├── {Theme.TEXT}ID/TC  : {Theme.WHITE}{spouse_data['tc']}")
                print(f"    {Theme.STEALTH}├── {Theme.TEXT}GSM    : {Theme.WHITE}{s_phones}")
                if filters["address"] and spouse_data.get('ikametgah'):
                    print(f"    {Theme.STEALTH}└── {Theme.TEXT}ADDR   : {Theme.WHITE}{spouse_data['ikametgah']}")
            else:
                print(f"    {Theme.STEALTH}└── {Theme.WARN}[!] {Theme.STEALTH}Zero civil matching results discovered.")
            print(f"  {Theme.RED_D}╌" * w)
        
        if filters["children"]:
            print(f"  {Theme.RED_B}» {Theme.WHITE}DESCENDANT MATRIX NODES:")
            if children:
                for idx, child in enumerate(children, 1):
                    print(f"    {Theme.STEALTH}[{Theme.RED_B}{idx:02d}{Theme.STEALTH}] {Theme.TEXT}CHILD {Theme.STEALTH}:: {Theme.WHITE}{child['name']:<22} {Theme.STEALTH}[DOB: {Theme.TEXT}{child['birth']}{Theme.STEALTH}]")
                    print(f"        {Theme.STEALTH}├── TC  : {Theme.TEXT}{child['tc']}")
                    c_phones = f"{Theme.STEALTH}, {Theme.TEXT}".join(child['phones']) if child['phones'] else f"{Theme.WARN}EMPTY"
                    print(f"        {Theme.STEALTH}├── GSM : {Theme.TEXT}{c_phones}")
                    if filters["address"] and child.get('ikametgah'):
                        print(f"        {Theme.STEALTH}└── LBS : {Theme.TEXT}{child['ikametgah']}")
            else:
                print(f"    {Theme.STEALTH}└── {Theme.WARN}[!] {Theme.STEALTH}No entries linked inside cluster fields.")
            print(f"  {Theme.RED_D}╌" * w)
        
        if filters["siblings"]:
            print(f"  {Theme.RED_B}» {Theme.WHITE}SIBLING EXTENSION CHAINS:")
            if siblings:
                for idx, sib in enumerate(siblings, 1):
                    print(f"    {Theme.STEALTH}[{Theme.RED_B}{idx:02d}{Theme.STEALTH}] {Theme.TEXT}SIB   {Theme.STEALTH}:: {Theme.WHITE}{sib['name']:<22} {Theme.STEALTH}[DOB: {Theme.TEXT}{sib['birth']}{Theme.STEALTH}]")
                    print(f"        {Theme.STEALTH}├── TC  : {Theme.TEXT}{sib['tc']}")
                    if filters["sibling_phones"]:
                        sib_phones = f"{Theme.STEALTH}, {Theme.TEXT}".join(sib['phones']) if sib['phones'] else f"{Theme.WARN}EMPTY"
                        print(f"        {Theme.STEALTH}├── GSM : {Theme.TEXT}{sib_phones}")
                    if filters["address"] and sib.get('ikametgah'):
                        print(f"        {Theme.STEALTH}└── LBS : {Theme.TEXT}{sib['ikametgah']}")
                    if idx < len(siblings):
                        print(f"        {Theme.RED_D}╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌ ╌")
            else:
                print(f"    {Theme.STEALTH}└── {Theme.WARN}[!] {Theme.STEALTH}No correlated sibling vectors found.")
        print(f" {Theme.RED_D}└" + "─" * w + f"┘{Theme.RESET}")

    @classmethod
    def read_key(cls):
        if not tty:
            return sys.stdin.read(1)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return ch3
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    @classmethod
    def interactive_menu(cls, options: list) -> int:
        current_idx = 0
        while True:
            cls.banner()
            w = cls.get_width()
            print(f"\n {Theme.STEALTH}[{Theme.RED_B}!{Theme.STEALTH}] {Theme.WHITE}MULTIPLE NODES DISCOVERED. SELECT ARCHIVE TARGET:")
            print(f" {Theme.RED_D}┌" + "─" * w + "┐")
            for idx, opt in enumerate(options):
                if idx == current_idx:
                    print(f" {Theme.RED_D}│ {Theme.RED_B}► {Theme.WHITE}{opt:<{w-3}} {Theme.RED_D}│")
                else:
                    print(f" {Theme.RED_D}│   {Theme.TEXT}{opt:<{w-3}} {Theme.RED_D}│")
            print(f" {Theme.RED_D}└" + "─" * w + "┘")
            print(f"\n {Theme.STEALTH}[ Use UP/DOWN arrows to navigate | Press ENTER to launch AI Reconstruction ]")
            
            key = cls.read_key()
            if key == 'A':
                current_idx = (current_idx - 1) % len(options)
            elif key == 'B':
                current_idx = (current_idx + 1) % len(options)
            elif key in ['\r', '\n']:
                return current_idx


class DatabaseManager:
    def __init__(self):
        self.config = {
            "host": "127.0.0.1",
            "user": "root",
            "password": "", 
            "database": "target_db",
            "connect_timeout": 5
        }
        self.connection = None

    def connect(self) -> bool:
        try:
            if self.connection and self.connection.is_connected():
                self.connection.ping(reconnect=True, attempts=3, delay=1)
                return True
            self.connection = mysql.connector.connect(**self.config)
            return True
        except Error:
            return False

    def execute_query(self, query: str, params: tuple = None, fetch_all: bool = False):
        if not self.connect():
            raise Error("Database core infrastructure unreachable.")
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            return cursor.fetchall() if fetch_all else cursor.fetchone()
        except Error as e: raise e
        finally: cursor.close()


class EngineController:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_ikametgah(self, tc):
        if not tc: return None
        try:
            result = self.db.execute_query("SELECT `Ikametgah` FROM `datam` WHERE `KimlikNo` = %s LIMIT 1", (tc,))
            return result['Ikametgah'] if result and result.get('Ikametgah') else "No verified data"
        except Error: return "Execution fault"

    def extract_absolute_family_tree(self, profile_data: dict, filters: dict = None):
        current_tc = profile_data.get('TC')
        baba_tc = profile_data.get('BABATC')
        anne_tc = profile_data.get('ANNETC')
        
        parent_structure = {
            "father_name": profile_data.get('BABAADI', 'UNKNOWN'), "father_phones": [], "father_ikametgah": "",
            "mother_name": profile_data.get('ANNEADI', 'UNKNOWN'), "mother_phones": [], "mother_ikametgah": ""
        }
        spouse_data = None
        children_list = []
        siblings_list = []

        if baba_tc:
            parent_structure['father_ikametgah'] = self.get_ikametgah(baba_tc)
            try:
                f_phones_res = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (baba_tc,), fetch_all=True)
                parent_structure['father_phones'] = [str(p['GSM']) for p in (f_phones_res or []) if p.get('GSM')]
            except Error: pass
            
        if anne_tc:
            parent_structure['mother_ikametgah'] = self.get_ikametgah(anne_tc)
            try:
                m_phones_res = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (anne_tc,), fetch_all=True)
                parent_structure['mother_phones'] = [str(p['GSM']) for p in (m_phones_res or []) if p.get('GSM')]
            except Error: pass

        if current_tc:
            try:
                query_children = "SELECT `ADI`, `SOYADI`, `DOGUMTARIHI`, `TC`, `ANNETC`, `ANNEADI` FROM `101m` WHERE `BABATC` = %s"
                children_records = self.db.execute_query(query_children, (current_tc,), fetch_all=True)
                if children_records:
                    detected_mother_tc, detected_mother_name = None, None
                    for child in children_records:
                        c_tc = child['TC']
                        c_phones_res = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (c_tc,), fetch_all=True)
                        children_list.append({
                            "name": f"{child['ADI']} {child['SOYADI']}", "birth": child['DOGUMTARIHI'] or "N/A", "tc": c_tc,
                            "phones": [str(p['GSM']) for p in (c_phones_res or []) if p.get('GSM')], "ikametgah": self.get_ikametgah(c_tc)
                        })
                        if child.get('ANNETC') and str(child['ANNETC']).strip() != '':
                            detected_mother_tc, detected_mother_name = child['ANNETC'], child['ANNEADI']
                    if detected_mother_tc:
                        s_phones_res = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (detected_mother_tc,), fetch_all=True)
                        spouse_data = {
                            "tc": detected_mother_tc, "name": detected_mother_name,
                            "phones": [str(p['GSM']) for p in (s_phones_res or []) if p.get('GSM')], "ikametgah": self.get_ikametgah(detected_mother_tc)
                        }
            except Error: pass

        if baba_tc and anne_tc and str(baba_tc).upper() not in ['NULL', ''] and str(anne_tc).upper() not in ['NULL', '']:
            try:
                query_siblings = "SELECT `ADI`, `SOYADI`, `DOGUMTARIHI`, `TC` FROM `101m` WHERE `BABATC` = %s AND `ANNETC` = %s AND `TC` != %s"
                matches = self.db.execute_query(query_siblings, (baba_tc, anne_tc, current_tc), fetch_all=True)
                if matches:
                    for match in matches:
                        sib_tc = match['TC']
                        phone_matches = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (sib_tc,), fetch_all=True)
                        siblings_list.append({
                            "name": f"{match['ADI']} {match['SOYADI']}", "birth": match['DOGUMTARIHI'] or "N/A", "tc": sib_tc,
                            "phones": [str(p['GSM']) for p in (phone_matches or []) if p.get('GSM')], "ikametgah": self.get_ikametgah(sib_tc)
                        })
            except Error: pass

        target_ikametgah = self.get_ikametgah(current_tc)
        UIComponents.print_absolute_family_report(
            f"{profile_data.get('ADI', '')} {profile_data.get('SOYADI', '')}", parent_structure, spouse_data, children_list, siblings_list, target_ikametgah, filters
        )

    def run_direct_ai_kinship(self, target_id: str):
        filters = {"address": True, "spouse": True, "children": True, "siblings": True, "sibling_phones": True}
        UIComponents.progress_bar("injecting target to kinship matrix core", duration=0.4)
        try:
            res_101m = self.db.execute_query("SELECT * FROM `101m` WHERE `TC` = %s LIMIT 1", (target_id,))
            if res_101m:
                combined_target_data = dict(res_101m)
                target_gsm_res = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (target_id,), fetch_all=True)
                combined_target_data['PHONES_GSM'] = ", ".join([str(p['GSM']) for p in target_gsm_res if p.get('GSM')]) if target_gsm_res else "No trace allocation"
                UIComponents.print_box("Target Descriptors Core", combined_target_data)
                self.extract_absolute_family_tree(res_101m, filters)
            else:
                print(f" {Theme.WARN}[!] Failure: Target allocation broken inside database fields.{Theme.RESET}\n")
        except Error as e:
            print(f"\n {Theme.WARN}[!] Core Critical Exception: {str(e)}{Theme.RESET}\n")

    def search_by_ai_family(self):
        UIComponents.banner()
        print(f"\n {Theme.STEALTH}[{Theme.RED_B}INPUT_REQ{Theme.STEALTH}] {Theme.TEXT}ENTER NATIONAL SIGNATURE VECTOR (TC):")
        target_id = input(f" {Theme.RED_D}fsociety_shell@root:~# {Theme.WHITE}").strip()
        if not target_id: return
        self.run_direct_ai_kinship(target_id)

    def search_by_tc(self, target_id: str = None):
        UIComponents.banner()
        if not target_id:
            print(f"\n {Theme.STEALTH}[{Theme.RED_B}INPUT_REQ{Theme.STEALTH}] {Theme.TEXT}ENTER LOOKUP SIGNATURE (TC):")
            target_id = input(f" {Theme.RED_D}fsociety_shell@root:~# {Theme.WHITE}").strip()
        if not target_id: return
        UIComponents.progress_bar("row dump internal database structures", duration=0.3)
        try:
            res_101m = self.db.execute_query("SELECT * FROM `101m` WHERE `TC` = %s LIMIT 1", (target_id,))
            res_datam = self.db.execute_query("SELECT * FROM `datam` WHERE `KimlikNo` = %s LIMIT 1", (target_id,))
            res_gsm = self.db.execute_query("SELECT * FROM `145mgsm` WHERE `TC` = %s", (target_id,), fetch_all=True)
            if res_101m or res_datam or res_gsm:
                if res_101m: UIComponents.print_box("Segment_Cluster_101m", res_101m)
                if res_datam: UIComponents.print_box("Segment_Cluster_Datam", res_datam)
                if res_gsm:
                    for count, gsm_row in enumerate(res_gsm, 1):
                        gsm_copy = dict(gsm_row); gsm_copy.pop('TC', None)
                        UIComponents.print_box(f"Telecom_Data_Node_{count:02d}", gsm_copy)
            else:
                print(f" {Theme.STEALTH}[{Theme.WARN}-{Theme.STEALTH}] {Theme.TEXT}No static row entries allocation discovered.{Theme.RESET}\n")
        except Error as e: print(f"\n {Theme.WARN}[!] Internal Failure: {str(e)}{Theme.RESET}\n")

    def search_by_name_and_city(self):
        UIComponents.banner()
        print(f"\n {Theme.STEALTH}╔═ [{Theme.RED_B}NOMINAL FILTER SPECIFICATIONS{Theme.STEALTH}]")
        first_name = input(f" {Theme.RED_D}╠═ {Theme.TEXT}FIRST NAME (OPTIONAL) : {Theme.WHITE}").strip().upper()
        surname    = input(f" {Theme.RED_D}╠═ {Theme.TEXT}SURNAME (OPTIONAL)    : {Theme.WHITE}").strip().upper()
        target_il  = input(f" {Theme.RED_D}╚═ {Theme.TEXT}NUFUSIL (OPTIONAL)    : {Theme.WHITE}").strip().upper()
        
        # حماية لمنع إدخال استعلام فارغ يسبب بطء النظام
        if not first_name and not surname and not target_il:
            print(f" {Theme.STEALTH}[{Theme.WARN}!{Theme.STEALTH}] {Theme.WARN}ERROR: AT LEAST ONE ARTIFACT IS REQUIRED FOR EXTRACTION.{Theme.RESET}\n")
            return
        
        UIComponents.progress_bar("streaming full database nominal records", duration=0.5)
        try:
            # بناء استعلام ديناميكي ذكي يتكيف مع المدخلات المتوفرة فقط
            query = "SELECT * FROM `101m` WHERE "
            conditions = []
            params = []
            
            if first_name:
                conditions.append("`ADI` = %s")
                params.append(first_name)
            if surname:
                conditions.append("`SOYADI` = %s")
                params.append(surname)
            if target_il:
                conditions.append("`NUFUSIL` = %s")
                params.append(target_il)
                
            query += " AND ".join(conditions)

            all_records = self.db.execute_query(query, tuple(params), fetch_all=True)
            
            if not all_records:
                print(f" {Theme.STEALTH}[{Theme.WARN}-{Theme.STEALTH}] {Theme.TEXT}Zero matches located.{Theme.RESET}\n")
                return

            filtered_records = all_records
            print(f" {Theme.STEALTH}[{Theme.RED_B}*{Theme.STEALTH}] {Theme.WHITE}TOTAL RECORD EXTRACTED: {Theme.RED_B}{len(all_records)} {Theme.WHITE}ROWS.")
            
            filter_choice = input(f" {Theme.STEALTH}[{Theme.RED_B}?{Theme.STEALTH}] {Theme.TEXT}APPLY LIVE MEMORY FILTER? (y/N): ").strip().lower()
            if filter_choice in ['y', 'yes']:
                print(f" {Theme.STEALTH}╔═ [{Theme.RED_B}ENTER VECTOR FILTER CRITERIA - LEAVE BLANK TO SKIP{Theme.STEALTH}]")
                f_baba  = input(f" {Theme.RED_D}╠═ {Theme.TEXT}FILTER BY FATHER NAME : {Theme.WHITE}").strip().upper()
                f_anne  = input(f" {Theme.RED_D}╠═ {Theme.TEXT}FILTER BY MOTHER NAME : {Theme.WHITE}").strip().upper()
                f_birth = input(f" {Theme.RED_D}╚═ {Theme.TEXT}FILTER BY BIRTH DATE  : {Theme.WHITE}").strip().upper()
                
                if f_baba:
                    filtered_records = [r for r in filtered_records if r.get('BABAADI') == f_baba]
                if f_anne:
                    filtered_records = [r for r in filtered_records if r.get('ANNEADI') == f_anne]
                if f_birth:
                    filtered_records = [r for r in filtered_records if r.get('DOGUMTARIHI') == f_birth]
                    
                print(f" {Theme.STEALTH}[{Theme.RED_B}*{Theme.STEALTH}] {Theme.WHITE}FILTER COMPLETED. SHOWING {Theme.RED_B}{len(filtered_records)}{Theme.WHITE}/{len(all_records)} MATCHES.")

            for count, row in enumerate(filtered_records, 1):
                current_tc = row.get('TC')
                display_profile = dict(row)
                if current_tc:
                    geo = self.db.execute_query("SELECT `Ikametgah` FROM `datam` WHERE `KimlikNo` = %s LIMIT 1", (current_tc,))
                    display_profile['IKAMETGAH'] = geo['Ikametgah'] if geo and geo.get('Ikametgah') else "No trace record"
                    gsm = self.db.execute_query("SELECT `GSM` FROM `145mgsm` WHERE `TC` = %s", (current_tc,), fetch_all=True)
                    display_profile['LINKED_GSM'] = ", ".join([str(p['GSM']) for p in gsm if p.get('GSM')]) if gsm else "No trace record"
                UIComponents.print_box(f"Nominal_Sync_Target_{count:02d}", display_profile)
                
        except Error as e: print(f"\n {Theme.WARN}[!] Operational Fault: {str(e)}{Theme.RESET}\n")

    def search_by_gsm(self, target_gsm: str = None):
        UIComponents.banner()
        if not target_gsm:
            print(f"\n {Theme.STEALTH}[{Theme.RED_B}INPUT_REQ{Theme.STEALTH}] {Theme.TEXT}ENTER TELECOM SIGNATURE (GSM):")
            target_gsm = input(f" {Theme.RED_D}fsociety_shell@root:~# {Theme.WHITE}").strip()
        if not target_gsm: return
            
        UIComponents.progress_bar("resolving reverse telecom signatures", duration=0.3)
        try:
            res_gsm = self.db.execute_query("SELECT * FROM `145mgsm` WHERE `GSM` = %s", (target_gsm,), fetch_all=True)
            if res_gsm:
                options_list, records_map = [], []
                for gsm_row in res_gsm:
                    associated_tc = gsm_row.get('TC')
                    owner_name = "UNRESOLVED NAME LAYER"
                    if associated_tc:
                        identity_match = self.db.execute_query("SELECT `ADI`, `SOYADI` FROM `101m` WHERE `TC` = %s LIMIT 1", (associated_tc,))
                        if identity_match: owner_name = f"{identity_match['ADI']} {identity_match['SOYADI']}"
                    options_list.append(f"TC: {associated_tc} | {owner_name}")
                    records_map.append(associated_tc)
                
                if len(options_list) > 1:
                    selected_index = UIComponents.interactive_menu(options_list)
                    self.run_direct_ai_kinship(records_map[selected_index])
                else:
                    self.run_direct_ai_kinship(records_map[0])
            else:
                print(f" {Theme.STEALTH}[{Theme.WARN}-{Theme.STEALTH}] {Theme.TEXT}No active footprint found for vector: {Theme.WHITE}{target_gsm}{Theme.RESET}\n")
        except Error as e: print(f"\n {Theme.WARN}[!] Reverse Pipeline Interrupted: {str(e)}{Theme.RESET}\n")


def main():
    db = DatabaseManager()
    engine = EngineController(db)
    
    if not db.connect():
        UIComponents.banner()
        print(f" {Theme.STEALTH}[{Theme.WARN}CRIT_FAULT{Theme.STEALTH}] {Theme.WARN}LOCAL DATABASE INSTANCE OFFLINE. CORE TERMINATED.{Theme.RESET}\n")
        sys.exit(1)

    if len(sys.argv) > 1:
        argument = sys.argv[1].strip()
        if argument.isdigit():
            if len(argument) == 10: engine.search_by_gsm(argument); sys.exit(0)
            elif len(argument) == 11: engine.search_by_tc(argument); sys.exit(0)
            else: sys.exit(1)
        else: sys.exit(1)
        
    while True:
        UIComponents.banner()
        print(f"  {Theme.RED_D}├── [{Theme.RED_B}01{Theme.RED_D}] {Theme.WHITE}INTEGRATED RELATIONAL TREE MATRIX {Theme.STEALTH}(AI Deep Kinship)")
        print(f"  {Theme.RED_D}├── [{Theme.RED_B}02{Theme.RED_D}] {Theme.TEXT}STANDARD ID EXTRACTOR ROW DUMP    {Theme.STEALTH}(Direct TC Lookup)")
        print(f"  {Theme.RED_D}├── [{Theme.RED_B}03{Theme.RED_D}] {Theme.TEXT}NOMINAL INDEX PIPELINE EXPLORER   {Theme.STEALTH}(Name + City)")
        print(f"  {Theme.RED_D}├── [{Theme.RED_B}04{Theme.RED_D}] {Theme.TEXT}REVERSE TELECOM REGISTRY PARSER   {Theme.STEALTH}(GSM Reverse Trace)")
        print(f"  {Theme.RED_D}└── [{Theme.WARN}00{Theme.RED_D}] {Theme.STEALTH}SHUTDOWN SYSTEM EXECUTIONS FRAMEWORK")
        
        choice = input(f"\n {Theme.RED_D}fsociety_shell@{Theme.RED_B}fso_core{Theme.STEALTH}:~# {Theme.WHITE}").strip()
        
        if choice in ['1', '01']: engine.search_by_ai_family()
        elif choice in ['2', '02']: engine.search_by_tc()
        elif choice in ['3', '03']: engine.search_by_name_and_city()
        elif choice in ['4', '04']: engine.search_by_gsm()
        elif choice in ['0', '00']: break
        else: time.sleep(0.4)
        
        input(f"\n{Theme.STEALTH}[ Press ENTER to flash console buffer ]{Theme.RESET}")

if __name__ == "__main__":
    main()
