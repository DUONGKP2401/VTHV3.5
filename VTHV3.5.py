import threading
import base64
import os
import time
import re
import requests
import socket
import sys
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
from collections import Counter, defaultdict
from urllib.parse import urlparse, parse_qs
import random
import math

# Kiểm tra và cài đặt thư viện cần thiết
try:
    from faker import Faker
    from requests import session
    from colorama import Fore, Style
    import pystyle
except ImportError:
    os.system("pip install faker requests colorama bs4 pystyle rich")
    os.system("pip3 install requests pysocks")
    print('__Vui Lòng Chạy Lại Tool__')
    sys.exit()

# Tạo hoặc đọc khóa mã hóa bằng base64
secret_key = base64.urlsafe_b64encode(os.urandom(32))

# Mã hóa và giải mã dữ liệu bằng base64
def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(encrypted_data):
    return base64.b64decode(encrypted_data.encode()).decode()

# Màu sắc cho hiển thị
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xduong = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;39m"
end = '\033[0m'

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    # Sửa đổi ở đây: Phần này đã có hiệu ứng chạy chữ
    banner_text = f"""
{luc}████████╗ ██████╗░░ ██╗░░██╗░
{luc}╚══██╔══╝ ██╔══██╗░ ██║██╔╝░░
{luc}░░░██║░░░ ██║░░██║░ █████╔╝░░
{luc}░░░██║░░░ ██║░░██║░ ██╔═██╗░░
{luc}░░░██║░░░ ██║░░██║░ ██║░╚██╗░
{luc}░░░╚═╝░░░ ╚█████╔╝░ ╚═╝░░╚═╝░
{trang}══════════════════════════

{vang}Admin: DUONG PHUNG
{vang}Nhóm Zalo: https://zalo.me/g/ddxsyp497
{vang}Tele: @tankeko12
{trang}══════════════════════════
"""
    for char in banner_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(0.0001)

def get_ip_address():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        ip_address = ip_data['ip']
        return ip_address
    except Exception as e:
        print(f"{do}Lỗi khi lấy địa chỉ IP: {e}{trang}")
        return None

def display_ip_address(ip_address):
    if ip_address:
        banner()
        print(f"{trang}[{do}<>{trang}] {do}Địa chỉ IP : {vang}{ip_address}{trang}")
    else:
        print(f"{do}Không thể lấy địa chỉ IP của thiết bị.{trang}")

def luu_thong_tin_ip(ip, key, expiration_date):
    data = {ip: {'key': key, 'expiration_date': expiration_date.isoformat()}}
    encrypted_data = encrypt_data(json.dumps(data))

    with open('ip_key.json', 'w') as file:
        file.write(encrypted_data)

def tai_thong_tin_ip():
    try:
        with open('ip_key.json', 'r') as file:
            encrypted_data = file.read()
        data = json.loads(decrypt_data(encrypted_data))
        return data
    except FileNotFoundError:
        return None

def kiem_tra_ip(ip):
    data = tai_thong_tin_ip()
    if data and ip in data:
        expiration_date = datetime.fromisoformat(data[ip]['expiration_date'])
        if expiration_date > datetime.now():
            return data[ip]['key']
    return None

def generate_key_and_url(ip_address):
    ngay = int(datetime.now().day)
    key1 = str(ngay * 27 + 27)
    ip_numbers = ''.join(filter(str.isdigit, ip_address))
    key = f'VTH{key1}{ip_numbers}'
    expiration_date = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
    url = f'https://buffttfbinta.blogspot.com/2025/09/vth-v2-v3.html?m={key}'
    return url, key, expiration_date

def da_qua_gio_moi():
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return now >= midnight

def get_shortened_link_phu(url):
    try:
        token = "6725c7b50c661e3428736919"
        api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"

        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"status": "error", "message": "Không thể kết nối đến dịch vụ rút gọn URL."}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi rút gọn URL: {e}"}

def check_key_main():
    ip_address = get_ip_address()
    display_ip_address(ip_address)

    if not ip_address:
        return False

    existing_key = kiem_tra_ip(ip_address)
    if existing_key:
        print(f"{trang}[{do}<>{trang}] {hong}Tool còn hạn, mời bạn dùng tool...{trang}")
        time.sleep(2)
        return True

    if da_qua_gio_moi():
        print(f"{vang}Quá giờ sử dụng tool !!!{trang}")
        return False

    url, key, expiration_date = generate_key_and_url(ip_address)

    print(f"{trang}[{do}<>{trang}] {luc}Nhập 1 Để Lấy Key {vang}( Free ){trang}")

    while True:
        try:
            choice = input(f"{trang}[{do}<>{trang}] {xduong}Nhập lựa chọn: {trang}")
            print(f"{trang}════════════════════════════════════════════════")
            if choice == "1":
                with ThreadPoolExecutor(max_workers=1) as executor:
                    yeumoney_future = executor.submit(get_shortened_link_phu, url)
                    yeumoney_data = yeumoney_future.result()

                if yeumoney_data and yeumoney_data.get('status') == "error":
                    print(yeumoney_data.get('message'))
                    return False
                else:
                    link_key_yeumoney = yeumoney_data.get('shortenedUrl')
                    print(f'{trang}[{do}<>{trang}] {hong}Link Để Vượt Key Là {xnhac}: {link_key_yeumoney}{trang}')

                while True:
                    keynhap = input(f'{trang}[{do}<>{trang}] {vang}Key Đã Vượt Là: {luc}')
                    if keynhap == key:
                        print(f'{luc}Key Đúng Mời Bạn Dùng Tool{trang}')
                        sleep(2)
                        luu_thong_tin_ip(ip_address, keynhap, expiration_date)
                        return True
                    else:
                        print(f'{trang}[{do}<>{trang}] {hong}Key Sai Vui Lòng Vượt Lại Link {xnhac}: {link_key_yeumoney}{trang}')
            else:
                print(f"{vang}Lựa chọn không hợp lệ, vui lòng nhập 1.{trang}")

        except (ValueError, KeyboardInterrupt):
            print(f"\n{trang}[{do}<>{trang}] {do}Cảm ơn bạn đã dùng Tool !!!{trang}")
            sys.exit()
    return False

# SECTION 1: UI & UTILITIES
# ==============================================================================
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.style import Style
    from rich.text import Text
    from rich.live import Live 
except ImportError:
    print("Thư viện 'rich' chưa được cài đặt. Vui lòng cài đặt lại.")
    sys.exit(1)

console = Console()
STYLE_SUCCESS, STYLE_ERROR, STYLE_WARNING, STYLE_INFO, STYLE_HEADER, STYLE_VALUE = \
    Style(color="green"), Style(color="red"), Style(color="yellow"), Style(color="cyan"), \
    Style(color="magenta", bold=True), Style(color="blue", bold=True)

def clear_console(): os.system("cls" if os.name == "nt" else "clear")

def show_header():
    header_string = "Tool Xworld Vua thoát hiểm V3 - admin: DUONG PHUNG -nhóm zalo: https://zalo.me/g/ddxsyp497  telegram: @tankeko12 -Lưu ý : Hãy quản lí vốn thật tốt; không tham lam, biết điểm dừng. Chúc bạn dùng tool vui vẻ!!"
    displayed_text = ""
    
    panel = Panel(Text(displayed_text, style=STYLE_HEADER, justify="center"), border_style="magenta", expand=False)
    
    with Live(panel, console=console, screen=False, transient=True, refresh_per_second=20) as live:
        for char in header_string:
            displayed_text += char
            panel = Panel(Text(displayed_text, style=STYLE_HEADER, justify="center"), border_style="magenta", expand=False)
            live.update(panel)
            time.sleep(0.01)
    
    console.print(panel) 
    console.print()


# ==============================================================================
# SECTION 2: CONFIGURATION
# ==============================================================================
CONFIG_FILE = "config.json"
def load_or_create_config():
    if os.path.exists(CONFIG_FILE):
        if console.input(f"🔎 Đã tìm thấy file config. Dùng lại? ([bold green]Y[/bold green]/n): ").strip().lower() in ["y", "yes", ""]:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                if all(k in config for k in ["stop_profit", "stop_loss", "max_lose_streak", "rounds_before_break", "break_duration_rounds"]):
                    return config

    console.print("⚠️ Không tìm thấy config hoặc config cũ. Vui lòng tạo mới.", style=STYLE_WARNING)
    config = {
        "url_game": console.input(f"[{STYLE_INFO}]Nhập Link Game:[/] ").strip(),
        "bet_type": console.input(f"[{STYLE_INFO}]Nhập Loại Tiền cược (BUILD/USDT/WORLD):[/] ").strip().upper(),
        "base_bet": float(console.input(f"[{STYLE_INFO}]Nhập Số Tiền Cược cơ bản:[/] ").strip()),
        "rounds_before_break": int(console.input(f"[{STYLE_INFO}]Chơi bao nhiêu ván thì nghỉ (nhập 0 để không nghỉ):[/] ").strip()),
        "break_duration_rounds": int(console.input(f"[{STYLE_INFO}]Nghỉ bao nhiêu ván rồi chơi tiếp:[/] ").strip()),
        "multiplier": float(console.input(f"[{STYLE_INFO}]Nhập Cấp số nhân sau khi thua:[/] ").strip()),
        "max_lose_streak": int(console.input(f"[{STYLE_WARNING}]Nhập Giới hạn chuỗi thua để DỪNG/RESET (ví dụ: 5):[/] ").strip()),
        "stop_profit": float(console.input(f"[{STYLE_SUCCESS}]Nhập Số LÃI mục tiêu để DỪNG (ví dụ: 50):[/] ").strip()),
        "stop_loss": float(console.input(f"[{STYLE_ERROR}]Nhập Mức LỖ tối đa để DỪNG (ví dụ: 100):[/] ").strip())
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f: json.dump(config, f, indent=4)
    console.print(f"✅ Đã lưu config vào file [bold cyan]{CONFIG_FILE}[/bold cyan]", style=STYLE_SUCCESS)
    return config

# ==============================================================================
# SECTION 3: PREDICTION LOGIC (PREDICTOR V23 - DIVERSIFIED JURY)
# ==============================================================================
def choose_safe_room(recent_100, recent_10, win_streak=0, lose_streak=0):
    try:
        full_history = [int(r["killed_room_id"]) for r in recent_100 if "killed_room_id" in r] if isinstance(recent_100, list) else []
        
        if len(full_history) < 25:
            candidate_rooms = list(range(1, 9))
            if len(full_history) > 0:
                last_killed = full_history[0]
                if last_killed in candidate_rooms:
                    candidate_rooms.remove(last_killed)
            if len(full_history) > 1:
                second_last_killed = full_history[1]
                if second_last_killed in candidate_rooms:
                    candidate_rooms.remove(second_last_killed)
            if not candidate_rooms:
                candidate_rooms = list(range(1, 9))
            return random.choice(candidate_rooms), ""

        # LỚP 1: PHÂN TÍCH TRẠNG THÁI NÂNG CAO
        player_momentum = "TRUNG LẬP"
        if win_streak >= 3: player_momentum = "THẮNG LỚN"
        elif win_streak > 0: player_momentum = "ĐANG THẮNG"
        elif lose_streak >= 4: player_momentum = "KHỦNG HOẢNG"
        elif lose_streak > 0: player_momentum = "ĐANG THUA"

        game_pattern = "HỖN LOẠN"
        analysis_segment = full_history[:30]
        std_dev = math.sqrt(sum([(x - sum(analysis_segment) / len(analysis_segment)) ** 2 for x in analysis_segment]) / len(analysis_segment))
        top_3_freq_ratio = sum(c for _, c in Counter(analysis_segment).most_common(3)) / len(analysis_segment)

        if std_dev < 2.15: game_pattern = "CÓ CẦU"
        elif top_3_freq_ratio > 0.55: game_pattern = "BỆT/CỤM"

        # LỚP 2: KHỞI TẠO PHIẾU BẦU NGUY HIỂM
        danger_votes = {room: 0 for room in range(1, 9)}
        danger_votes[full_history[0]] += 1 # Phòng vừa ra luôn có 1 phiếu

        # LỚP 3: HỘI ĐỒNG CHUYÊN GIA ("GRAND JURY")
        # --- DANH SÁCH CHUYÊN GIA ---
        def _get_coldest_rooms(h):
            gaps = {r: h.index(r) if r in h else len(h) for r in range(1, 9)}
            max_gap = max(gaps.values())
            return {r for r, g in gaps.items() if g == max_gap}

        def _get_transition_rooms(h):
            if len(h) < 2: return set()
            transitions = defaultdict(Counter)
            for i in range(len(h) - 1): transitions[h[i+1]][h[i]] += 1
            if h[0] in transitions and transitions[h[0]]:
                return {transitions[h[0]].most_common(1)[0][0]}
            return set()

        def _get_parity_rooms(h):
            if len(h) < 3: return set()
            parities = [r % 2 for r in h[:3]]
            if parities[0] == parities[1] == parities[2]:
                return {r for r in range(1, 9) if r % 2 == parities[0]}
            return set()
            
        def _get_sequence_rooms(h):
            if len(h) < 2: return set()
            h1, h2 = h[0], h[1]
            diff = h1 - h2
            if abs(diff) in [1, 2]:
                if 1 <= h1 + diff <= 8: return {h1 + diff}
            return set()

        def _get_mirror_rooms(h):
            return {9 - h[0]}

        def _get_frequent_recent_rooms(h):
            recent_segment = h[:8]
            counts = Counter(recent_segment)
            return {room for room, count in counts.items() if count > 1}

        # --- MA TRẬN CHIẾN LƯỢC SIÊU THÍCH ỨNG (2D) ---
        cg = _get_coldest_rooms; tr = _get_transition_rooms; pr = _get_parity_rooms
        sq = _get_sequence_rooms; mr = _get_mirror_rooms; fr = _get_frequent_recent_rooms
        
        strategy_matrix = {
            ("ĐANG THUA", "HỖN LOẠN"): [cg, fr], ("ĐANG THUA", "BỆT/CỤM"):  [cg, tr, fr], ("ĐANG THUA", "CÓ CẦU"): [cg, tr, pr],
            ("KHỦNG HOẢNG", "HỖN LOẠN"): [cg], ("KHỦNG HOẢNG", "BỆT/CỤM"):  [cg, fr], ("KHỦNG HOẢNG", "CÓ CẦU"): [cg, tr],
            ("TRUNG LẬP", "HỖN LOẠN"): [tr, mr, fr], ("TRUNG LẬP", "BỆT/CỤM"):  [tr, fr, sq], ("TRUNG LẬP", "CÓ CẦU"): [tr, sq, pr, mr],
            ("ĐANG THẮNG", "HỖN LOẠN"): [tr, mr, fr], ("ĐANG THẮNG", "BỆT/CỤM"):  [tr, sq, fr], ("ĐANG THẮNG", "CÓ CẦU"): [tr, sq, pr],
            ("THẮNG LỚN", "HỖN LOẠN"): [tr, mr, sq], ("THẮNG LỚN", "BỆT/CỤM"):  [tr, sq, fr], ("THẮNG LỚN", "CÓ CẦU"): [tr, sq, mr, pr],
        }

        # LỚP 4: THAM VẤN VÀ BỎ PHIẾU
        active_strategy = (player_momentum, game_pattern)
        specialists_to_consult = strategy_matrix.get(active_strategy, [tr, cg, fr])

        for specialist in specialists_to_consult:
            for room in specialist(full_history):
                danger_votes[room] += 1
        
        # LỚP 5: RA QUYẾT ĐỊNH & ĐA DẠNG HÓA
        min_danger_votes = min(danger_votes.values())
        safest_rooms = [room for room, votes in danger_votes.items() if votes == min_danger_votes]
        
        final_choice = random.choice(safest_rooms)
        
        status_string = f"State: [bold cyan]{player_momentum}[/bold cyan] | Pattern: [bold magenta]{game_pattern}[/bold magenta]"
        if len(safest_rooms) > 1:
             status_string += f" | Options: {len(safest_rooms)}"

        return final_choice, status_string

    except Exception as e:
        return random.randint(1, 8), "[bold red]Lỗi phân tích, chọn ngẫu nhiên![/bold red]"


# ==============================================================================
# SECTION 4: API & DATA HANDLING
# ==============================================================================
def make_api_request(session, method, url, max_retries=3, **kwargs):
    base_delay = 1
    for attempt in range(max_retries):
        time.sleep(random.uniform(0.1, 0.5))
        try:
            response = session.request(method, url, timeout=10, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if attempt == max_retries - 1: return None
            time.sleep((base_delay * 2 ** attempt) + random.uniform(0, 1))
    return None

def get_wallet_balance(session, url, bet_type):
    resp = make_api_request(session, "GET", url)
    if not resp or resp.get("code") not in [0, 200]: return None
    wallet = resp.get("data", {}).get("cwallet")
    if wallet is None: return None
    key_map = {"USDT": "ctoken_kusdt", "WORLD": "ctoken_kther", "BUILD": "ctoken_contribute"}
    balance_str = wallet.get(key_map.get(bet_type))
    return float(balance_str) if balance_str is not None else None

def generate_summary_table(session_state, round_data, config, room_names_map):
    BET_TYPE, MAX_LOSE_STREAK = config["bet_type"], config["max_lose_streak"]
    win_rate = (session_state['wins'] / (session_state['wins'] + session_state['losses']) * 100) if (session_state['wins'] + session_state['losses']) > 0 else 0

    summary_table = Table(title=f"[bold]Bảng Tóm Tắt Phiên Chơi[/]", show_header=True, header_style="bold magenta")
    summary_table.add_column("Chỉ Số", width=15); summary_table.add_column("Thống Kê")
    summary_table.add_row("Ván Gần Nhất", f"#{round_data.get('issue_id', 'N/A')}")
    summary_table.add_row("Hành động", round_data.get('action', Text("---")))

    result = round_data.get('result')
    if result:
        killed_room_id = result.get('killed_room_id', 'N/A')
        killed_room_name = room_names_map.get(str(killed_room_id), '?')
        summary_table.add_row("Phòng Sát Thủ", f"{killed_room_id} ({killed_room_name})")

    if round_data.get('final_balance') is not None:
        summary_table.add_row("Số dư Hiện tại", f"{round_data.get('final_balance', 0):.4f} {BET_TYPE}")

    summary_table.add_row("Kết quả", round_data.get('outcome', Text("---")))
    summary_table.add_row("Tiền cược", f"{round_data.get('bet_amount', 0):.4f} {BET_TYPE}")
    profit_text = Text(f"{round_data.get('round_profit', 0):+.4f}", style=STYLE_SUCCESS if round_data.get('round_profit', 0) >= 0 else STYLE_ERROR)
    summary_table.add_row("Lời/Lỗ Vòng", profit_text)
    total_profit_text = Text(f"{session_state.get('cumulative_profit', 0):+.4f}", style=STYLE_SUCCESS if session_state.get('cumulative_profit', 0) >= 0 else STYLE_ERROR)
    summary_table.add_row("Tổng Lời/Lỗ", total_profit_text)
    summary_table.add_row("Thắng/Thua", f"{session_state['wins']}/{session_state['losses']} ({win_rate:.2f}%)")
    summary_table.add_row("Chuỗi thắng", f"{session_state['win_streak']} (Max: {session_state['max_win_streak']})")
    summary_table.add_row("Chuỗi thua", f"[red]{session_state['lose_streak']}[/red]/{MAX_LOSE_STREAK}")
    return summary_table

# ==============================================================================
# SECTION 5: MAIN LOGIC
# ==============================================================================
def main():
    if not check_key_main():
        return

    clear_console(); show_header(); config = load_or_create_config()
    try:
        params = parse_qs(urlparse(config["url_game"]).query)
        user_id, secret_key = params.get("userId", [None])[0], params.get("secretKey", [None])[0]
        if not user_id or not secret_key: raise ValueError("Invalid Link")
    except (ValueError, IndexError, TypeError):
        console.print("[red]LỖI: Link game không hợp lệ.[/red]"); return

    BET_TYPE = config["bet_type"]
    BASE_BET = config["base_bet"]
    MULTIPLIER = config["multiplier"]
    STOP_PROFIT = config["stop_profit"]
    STOP_LOSS = config["stop_loss"]
    MAX_LOSE_STREAK = config["max_lose_streak"]
    ROUNDS_BEFORE_BREAK = config.get("rounds_before_break", 0)
    BREAK_DURATION = config.get("break_duration_rounds", 0)

    ROOM_NAMES = {"1":"Nhà Kho", "2":"Phòng Họp", "3":"PhGĐ", "4":"PhTròChuyện", "5":"PhGiámSát", "6":"VănPhòng", "7":"PhTàiVụ", "8":"PhNhânSự"}

    API_BASE = "https://api.escapemaster.net/escape_game"
    URL_USER_INFO = "https://user.3games.io/user/regist?is_cwallet=1"
    URL_BET = f"{API_BASE}/bet"
    URL_RECENT_10 = f"{API_BASE}/recent_10_issues?asset={BET_TYPE}"
    URL_RECENT_100 = f"{API_BASE}/recent_issues?limit=100&asset={BET_TYPE}"

    title = "[bold cyan]Cấu Hình Hoạt Động[/]"
    text = (f"Loại Tiền Cược : {BET_TYPE}\nCược Cơ Bản    : {BASE_BET}\nCấp số nhân    : x{MULTIPLIER}\n"
            f"[cyan]Nghỉ giải lao   : Sau {ROUNDS_BEFORE_BREAK} ván, nghỉ {BREAK_DURATION} ván[/cyan]\n"
            f"[yellow]Giới hạn thua   : {MAX_LOSE_STREAK} ván[/yellow]\n"
            f"[green]Mục tiêu Lãi   : +{STOP_PROFIT}[/green]\n[red]Ngưỡng Cắt Lỗ  : -{STOP_LOSS}[/red]")
    console.print(Panel(Text(text, style="white"), title=title, border_style="cyan", expand=False))

    api_session = requests.Session()
    api_session.headers.update({"user-id": user_id, "user-secret-key": secret_key, "user-agent": "Mozilla/5.0"})

    console.print("🔄 [italic]Đang quét số dư ban đầu làm mốc...[/italic]")
    initial_balance = get_wallet_balance(api_session, URL_USER_INFO, BET_TYPE)
    if initial_balance is None:
        console.print("❌ [red]Không thể lấy số dư ban đầu. Vui lòng kiểm tra lại Link Game và kết nối.[/red]")
        return
    console.print(f"✅ [green]Số dư ban đầu được ghi nhận: [bold]{initial_balance:.4f} {BET_TYPE}[/bold][/green]\n")

    session_state = { "round": 0, "wins": 0, "losses": 0, "cumulative_profit": 0.0, "lose_streak": 0, "win_streak": 0, "max_win_streak": 0, "last_known_issue_id": None, "last_bet_on": None, "balance_before_bet": initial_balance, "initial_balance": initial_balance, "rounds_played_since_break": 0, "rounds_to_skip": 0 }

    initial_round_data = {
        'issue_id': 'N/A',
        'action': Text("---"),
        'result': {'killed_room_id': 'N/A'},
        'final_balance': initial_balance,
        'outcome': Text("Đang chờ ván đầu tiên...", style="dim"),
        'bet_amount': 0,
        'round_profit': 0
    }
    initial_table = generate_summary_table(session_state, initial_round_data, config, ROOM_NAMES)

    with Live(initial_table, console=console, screen=False, vertical_overflow="visible", refresh_per_second=10) as live:
        while True:
            try:
                resp10 = make_api_request(api_session, "GET", URL_RECENT_10)
                if not resp10 or not resp10.get("data"):
                    console.print("[yellow]Không thể lấy lịch sử 10 ván, đang chờ...[/yellow]", end="\r"); time.sleep(5); continue
                recent_10_hist = resp10["data"]

                latest_result = recent_10_hist[0]
                latest_issue_id = str(latest_result.get("issue_id"))

                if latest_issue_id != session_state["last_known_issue_id"]:
                    session_state["round"] += 1
                    console.print(f"\n--- Vòng {session_state['round']}: Xử lý kết quả ván #{latest_issue_id} ---", style="bold yellow")

                    round_data = {"issue_id": latest_issue_id, "bet_amount": 0, "round_profit": 0, "result": latest_result, "action": Text("---"), "outcome": Text("Không cược", style="dim")}
                    last_bet = session_state.get("last_bet_on")

                    if last_bet and str(last_bet["issue_id"]) == latest_issue_id:
                        killed_room_id = latest_result.get("killed_room_id")
                        bet_room = last_bet['room']
                        bet_amount = last_bet['amount']
                        balance_before = session_state['balance_before_bet']

                        console.print("[cyan]... Đang đồng bộ số dư từ máy chủ ...[/cyan]", end="\r"); time.sleep(10)
                        final_balance = get_wallet_balance(api_session, URL_USER_INFO, BET_TYPE)
                        console.print(" " * 60, end="\r")

                        is_win = (killed_room_id is not None and int(killed_room_id) != int(bet_room))
                        round_profit = 0

                        if is_win:
                            round_data["outcome"] = Text("THẮNG", style=STYLE_SUCCESS)
                            session_state.update({"wins": session_state["wins"]+1, "lose_streak": 0, "win_streak": session_state["win_streak"]+1})
                            session_state["max_win_streak"] = max(session_state["max_win_streak"], session_state["win_streak"])
                            if final_balance is not None and balance_before is not None: round_profit = final_balance - balance_before
                        else:
                            round_data["outcome"] = Text("THUA", style=STYLE_ERROR)
                            session_state.update({"losses": session_state["losses"]+1, "lose_streak": session_state["lose_streak"]+1, "win_streak": 0})
                            round_profit = -bet_amount

                        if final_balance is not None:
                            session_state["cumulative_profit"] = final_balance - session_state["initial_balance"]

                        bet_room_name = ROOM_NAMES.get(str(bet_room), '?')
                        action_text = Text(f"Đã cược Phòng {bet_room} ({bet_room_name})", style=STYLE_INFO)
                        round_data.update({ "bet_amount": bet_amount, "action": action_text, "round_profit": round_profit, "final_balance": final_balance })
                        session_state["rounds_played_since_break"] += 1

                    if session_state["round"] > 1 or (session_state["round"] == 1 and last_bet):
                        updated_table = generate_summary_table(session_state, round_data, config, ROOM_NAMES)
                        live.update(updated_table)

                    if session_state['lose_streak'] > 0 and session_state['lose_streak'] >= MAX_LOSE_STREAK:
                        console.print(Panel(f"BẠN ĐÃ THUA LIÊN TIẾP {session_state['lose_streak']} VÁN!", title="[bold yellow]ĐẠT GIỚI HẠN CHUỖI THUA[/bold yellow]", border_style="yellow"))
                        choice = console.input("Bạn muốn [bold green]Chơi tiếp[/bold green] (reset tiền cược) hay [bold red]Nghỉ[/bold red]? (mặc định là Chơi tiếp) [C/N]: ").strip().lower()
                        if choice in ['n', 'nghi']:
                            console.print("[yellow]Bot đã dừng theo yêu cầu của người dùng.[/yellow]"); return
                        else:
                            session_state['lose_streak'] = 0
                            console.print("[green]Đã reset tiền cược về mức ban đầu. Tiếp tục chơi...[/green]\n")

                    if session_state['cumulative_profit'] >= STOP_PROFIT:
                        console.print(Panel(f"✅ ĐÃ ĐẠT MỤC TIÊU LỢI NHUẬN! (Tổng lãi: {session_state['cumulative_profit']:.4f} {BET_TYPE})", title="[bold green]DỪNG TOOL[/bold green]", border_style="green")); return
                    if session_state['cumulative_profit'] <= -STOP_LOSS:
                        console.print(Panel(f"❌ ĐÃ CHẠM NGƯỠNG CẮT LỖ! (Tổng lỗ: {session_state['cumulative_profit']:.4f} {BET_TYPE})", title="[bold red]DỪNG TOOL[/bold red]", border_style="red")); return

                    session_state["last_known_issue_id"] = latest_issue_id

                    if ROUNDS_BEFORE_BREAK > 0 and session_state["rounds_played_since_break"] >= ROUNDS_BEFORE_BREAK:
                        console.print(Panel(f"Đã chơi {session_state['rounds_played_since_break']} ván. Tạm nghỉ {BREAK_DURATION} ván.", title="[bold yellow]BẮT ĐẦU NGHỈ GIẢI LAO[/bold yellow]", border_style="yellow"))
                        session_state["rounds_to_skip"] = BREAK_DURATION
                        session_state["rounds_played_since_break"] = 0

                    if session_state["rounds_to_skip"] > 0:
                        console.print(f"☕ [yellow]Đang trong thời gian nghỉ. Bỏ qua cược ván này. Còn lại {session_state['rounds_to_skip']-1} ván nghỉ.[/yellow]")
                        session_state["rounds_to_skip"] -= 1
                        session_state["last_bet_on"] = None
                        time.sleep(5)
                        continue

                    next_round_id = int(latest_issue_id) + 1

                    current_balance = get_wallet_balance(api_session, URL_USER_INFO, BET_TYPE)

                    if current_balance is None:
                        console.print(f"⚠️ Không thể xác minh số dư, tạm bỏ qua ván #{next_round_id} để đảm bảo an toàn.", style=STYLE_WARNING)
                        session_state["last_bet_on"] = None; time.sleep(10); continue

                    session_state['balance_before_bet'] = current_balance
                    console.print(f"💰 Số dư hiện tại: [bold green]{current_balance:.4f} {BET_TYPE}[/bold green] | Chuẩn bị cho ván: [bold]#{next_round_id}[/bold]")

                    resp100 = make_api_request(api_session, "GET", URL_RECENT_100)
                    recent_100_hist = resp100.get("data") if resp100 and resp100.get("data") else []

                    predicted_room, status_string = choose_safe_room(recent_100_hist, recent_10_hist, session_state['win_streak'], session_state['lose_streak'])

                    if status_string: console.print(status_string)
                    console.print("🤖 [italic]BOT V3.5 đang phân tích và đặt cược...[/italic]")

                    bet_amount = round(BASE_BET * (MULTIPLIER ** session_state["lose_streak"]), 4)

                    if bet_amount > current_balance:
                        console.print(f"⚠️ Không đủ số dư ({current_balance:.4f}). Cần {bet_amount:.4f}. Bỏ qua ván.", style=STYLE_WARNING)
                        session_state["last_bet_on"] = None
                    else:
                        predicted_room_name = ROOM_NAMES.get(str(predicted_room), "?")
                        console.print(f"✅ Cược [bold blue]{bet_amount:.4f} {BET_TYPE}[/bold blue] vào phòng [bold blue]{predicted_room} ({predicted_room_name})[/bold blue] cho ván [bold]#{next_round_id}[/bold]...")

                        bet_payload = { "asset_type": BET_TYPE, "user_id": int(user_id), "room_id": predicted_room, "bet_amount": bet_amount }
                        bet_response = make_api_request(api_session, "POST", URL_BET, json=bet_payload)

                        if bet_response and bet_response.get("code") == 0:
                            session_state["last_bet_on"] = {"issue_id": next_round_id, "room": predicted_room, "amount": bet_amount}
                            console.print("✅ Đặt cược thành công!", style="green")
                        else:
                            console.print(f"❌ Đặt cược thất bại! Phản hồi: {bet_response}", style="red")
                            session_state["last_bet_on"] = None
                else:
                    console.print(f"[yellow]... Chờ kết quả ván #{int(latest_issue_id) + 1} ...[/yellow]", end="\r")
                    time.sleep(3)
            except Exception as e:
                console.print(f"\n[red]Gặp lỗi trong vòng lặp chính: {e}. Đang thử lại sau 10 giây...[/red]")
                time.sleep(10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\nBot đã dừng bởi người dùng.", style="bold yellow")
    except Exception as e:
        console.print(f"\nĐã xảy ra lỗi không mong muốn:", style=STYLE_ERROR)
        console.print_exception(show_locals=False)
