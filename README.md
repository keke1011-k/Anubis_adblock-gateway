自律型Raspberry Pi DNSシンクホール (Ad-block Gateway)

システム概要
Raspberry PiとBIND9(RPZ)を利用した、ネットワークレベルの広告・マルウェアブロックゲートウェイです。
一度ネットワークに導入すれば、端末側（スマホやPC）にアプリを入れることなく、ネットワーク全体の広告通信を根本から遮断します。

特徴（ビジネスメリット）
- 完全自律化（手間ゼロ）: PythonスクリプトとCronにより、深夜に最新のブロックリストを自動取得・更新。非IT層でもメンテナンスフリーで運用可能です。
- 高速・軽量: DNS要求に対して即座にNXDOMAINを返すため、通信トラフィックを削減し、ブラウジングが高速化します。
- セキュアな遠隔管理: Tailscaleを利用し、安全なリモートSSHアクセスと保守が可能です。

システム構成
- ハードウェア: Raspberry Pi
- DNSサーバー: BIND9
- ブロック方式: RPZ (Response Policy Zone)
- リスト更新: Python3 (StevenBlack hostsリストを利用)
- 定期実行: Cron
- リモート管理: Tailscale

構築に必要なコマンド

1. 必要なパッケージのインストール
sudo apt update
sudo apt install bind9 bind9utils bind9-doc python3

2. IPv4強制オプションの設定（IPv6エラー対策）
network unreachable エラーを防ぐため、IPv4通信を強制します。
sudo nano /etc/default/named
(OPTIONS="-u bind -4" と追記して保存)

3. BIND9とPythonスクリプトの配置
- /etc/bind/db.rpz のベースを作成。
- update_adblock.py を任意の場所に配置。

4. Cronへの自動実行登録
毎日深夜3時に最新のリストに更新し、DNSサーバーを停止させることなく反映させます。
crontab -e
(0 3 * * * python3 /path/to/update_adblock.py のように記述)