import urllib.request
import os

# 1. 外部の広告ブロックリスト（hosts形式）を取得
url = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"
response = urllib.request.urlopen(url)
data = response.read().decode('utf-8')

# 2. RPZファイルのヘッダー（SOAレコード）を準備
rpz_file = "/etc/bind/db.rpz"
header = """$TTL 60
@ IN SOA localhost. root.localhost. ( 2026091201 3600 1800 604800 86400 )
  IN NS localhost.

"""

with open(rpz_file, "w") as f:
    f.write(header)

    # 3. リストを1行ずつ解析し、RPZ形式に変換して書き込み
    for line in data.splitlines():
        # "0.0.0.0"で始まる行（ブロック対象）だけを抽出
        if line.startswith("0.0.0.0") and "0.0.0.0 0.0.0.0" not in line:
            domain = line.split()[1]

            # BIND9が読める形式（ドメイン名 IN CNAME .）に変換
            f.write(f"{domain} IN CNAME .\n")

# 4. BIND9に最新リストを再読み込みさせる
os.system("sudo rndc reload")