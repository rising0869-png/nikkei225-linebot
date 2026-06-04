import gspread

gc = gspread.service_account(
    filename="bot-498411-78d452146270.json"
)

sheet = gc.open("日経平均225").sheet1

rows = sheet.get_all_records()

keyword = input("検索：")

found = False

for row in rows:
    code = str(row["銘柄コード"])
    name = row["銘柄名"]

    if keyword in code or keyword in name:
        print(f"\n{code}")
        print(name)
        print(f"業種：{row['業種']}")
        found = True

if not found:
    print("見つかりませんでした")