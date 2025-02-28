import pandas as pd

# Dữ liệu
gamer_terms_data = {
    "Key": [
        "ks", "afk", "ez", "feed", "sp", "ad", "ap", "jg", "mid", "top", 
        "bot", "ulti", "cd", "gank", "poke", "kite", "cc", "ms", "hp", 
        "mp", "mana", "hack", "adc", "mm", "ksq", "lmao", "wtf", "omg", 
        "vl", "clgt", "vip", "noob", "pro", "smurf", "camp", "lag", 
        "ping", "flame", "tilt", "int", "rage", "roam", "push", "split", 
        "b", "heal", "dive", "snowball", "farm", "zone", "engage", 
        "disengage", "omw", "ff", "bg", "wp", "ns", "gg", "ff20", "pls", "ty"
    ],
    "Value": [
        "cướp mạng", "rời khỏi cuộc chơi", "dễ", "chết nhiều khiến đội địch có nhiều cơ hội", 
        "hỗ trợ", "attack damage", "ability power", "jungler", "đường giữa", "đường trên", 
        "đường dưới", "chiêu cuối", "cooldown", "hỗ trợ tấn công", "rỉa máu", "thả diều", 
        "crowd control", "movement speed", "máu", "mức năng lượng", "mức năng lượng", 
        "gian lận", "attack damage carry", "marksman", "kill steal nhanh", "cười lớn", 
        "cái quái gì thế", "trời ơi", "vãi", "cái l** gì thế", "rất tốt", "gà", 
        "giỏi", "người chơi giỏi nhưng tạo tài khoản cấp thấp", "chờ sẵn ở khu vực", 
        "giật, chậm", "độ trễ", "chửi bới đồng đội", "mất tinh thần", "chơi ngu", 
        "tức giận", "di chuyển hỗ trợ", "đẩy đường", "tách ra", "quay về căn cứ", 
        "hồi máu", "lao vào", "lăn cầu tuyết", "hái tài nguyên", "kiểm soát khu vực", 
        "bắt đầu giao tranh", "rút lui khỏi giao tranh", "đang đến", "đầu hàng", 
        "trận đấu tệ", "chơi tốt", "chiêu đẹp", "trận đấu tốt", "đầu hàng phút 20", 
        "làm ơn", "cảm ơn"
    ]
}

bad_words_data = {
    "Word": ["địt", "đụ", "đm", "dm", "địt", "đụ", "đm", "dm", "vãi", "djt",
    "clgt", "lồn", "loz", "lol", "cặc", "chó", "khốn nạn",
    "ngu", "phò", "đĩ", "điếm", "dâm", "hâm", "điên", "ngu",
    "láo", "đéo", "dell", "mẹ kiếp", "vkl", "vcl", "dmcs", "đờ mờ",
    "vđ", "vl", "fuck", "fck", "sml", "dương vật", "éo", 
    "tởm", "vãi lều", "đéo", "dell", "del", "âm hộ"
],
}

# Tạo DataFrame
gamer_terms_df = pd.DataFrame(gamer_terms_data)
bad_words_df = pd.DataFrame(bad_words_data)

# Ghi vào file Excel với 2 sheet
with pd.ExcelWriter("terms_and_words.xlsx") as writer:
    gamer_terms_df.to_excel(writer, sheet_name="GAMER_TERMS", index=False)
    bad_words_df.to_excel(writer, sheet_name="BAD_WORDS", index=False)

print("File created: terms_and_words.xlsx with 2 sheets")
