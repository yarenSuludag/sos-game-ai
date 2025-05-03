import copy  # Tahtanın kopyasını almak için kullanılır (Minimax için gerekli)
import tkinter as tk
from tkinter import messagebox

# 🎮 Tahta başlatılıyor: 3x3 boyutunda, tüm hücreler boş (' ')
board = [[' ' for _ in range(3)] for _ in range(3)]

# 🔢 Oyuncuların puanlarını tutan değişkenler
player1_score = 0  # Oyuncu 1 (insan)
player2_score = 0  # Oyuncu 2 (bilgisayar)

# ✅ Oyuncu sırasını tutan değişken: True → Oyuncu 1, False → Bilgisayar
player_turn = True

# 🪟 Tkinter GUI başlatılıyor
root = tk.Tk()
root.title("SOS Oyunu (Tkinter)")

# 🔤 Oyuncunun seçtiği harf (başlangıçta 'S')
selected_letter = tk.StringVar(value='S')

# 🧱 Tahtadaki butonları ve durum/sıralama etiketlerini tutan yapılar
grid_buttons = [[None for _ in range(3)] for _ in range(3)]
status_label = tk.Label(root, text="Oyuncu 1'in sırası", font=("Arial", 14))
score_label = tk.Label(root, text="Skor - Oyuncu: 0 | Bilgisayar: 0", font=("Arial", 12))


'''
# 🖨️ Tahtayı kullanıcıya okunabilir şekilde yazdıran fonksiyon
def print_board(board):
    print("\n  0   1   2")  # Sütun başlıkları
    print("-------------")
    for i in range(3):  # Her satır için döngü
        # Satır içeriğini çizgilerle biçimlendirerek yazdır
        row = f"{i}| {board[i][0]} | {board[i][1]} | {board[i][2]} |"
        print(row)
        print("-------------") '''

# 🔍 Belirli bir hücreye harf yerleştirildikten sonra oluşan SOS'ları sayar
def check_sos(board, row, col):
    sos_count = 0  # Bulunan SOS dizilerini sayar

    # ⬆️⬇️⬅️➡️↖️↘️↙️↗️ 8 yön: dikey, yatay ve çaprazlar
    # 8 yönün tamamına bakıyordu ama...
    # Aynı yönde iki kez bakmak riskliydi (çift sayma veya hiç saymama)
    directions = [
    (-1, 0),  # yukarı
    (0, -1),  # sola
    (-1, -1), # sol üst çapraz
    (-1, 1)   # sağ üst çapraz
]

    letter = board[row][col]  # Yerleştirilen harfi al

    # Eğer ortadaki harf 'O' ise, etrafında 'S' olup olmadığını kontrol et (S-O-S)
    if letter == 'O':
        for dr, dc in directions:
            # dr/dc = yön farkı (örneğin yukarı = -1, 0)
            r1, c1 = row - dr, col - dc  # ilk 'S'
            r2, c2 = row + dr, col + dc  # ikinci 'S'
            if 0 <= r1 < 3 and 0 <= c1 < 3 and 0 <= r2 < 3 and 0 <= c2 < 3:
                if board[r1][c1] == 'S' and board[r2][c2] == 'S':
                    sos_count += 1

    # Eğer harf 'S' ise, sonrasında 'O' ve 'S' sırasıyla varsa yine SOS olur
    elif letter == 'S':
        for dr, dc in directions:
            r1, c1 = row + dr, col + dc      # 'O'
            r2, c2 = row + 2 * dr, col + 2 * dc  # ikinci 'S'
            if 0 <= r1 < 3 and 0 <= c1 < 3 and 0 <= r2 < 3 and 0 <= c2 < 3:
                if board[r1][c1] == 'O' and board[r2][c2] == 'S':
                    sos_count += 1

    return sos_count  # Bulunan SOS dizilerinin sayısı

# 🧩 Tahta dolu mu kontrol eden fonksiyon
def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':  # Hâlâ boş hücre varsa tahta dolmamıştır
                return False
    return True  # Hiç boş hücre kalmadıysa oyun biter

# 🎯 Tahtadaki tüm olası hamleleri döner: her boş hücreye 'S' ve 'O' denenebilir
def get_possible_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                moves.append((i, j, 'S'))  # S harfiyle dene
                moves.append((i, j, 'O'))  # O harfiyle dene
    return moves

# 📈 Tahtayı puan olarak değerlendirir (AI için avantajlı mı?)
def evaluate_score(board):
    # 🧮 Bu fonksiyon sadece oyun sonundaki durumu değerlendirir
    ai_score = 0
    player_score = 0

    # Her hücreye bakarak oyuncu kimse ona puan yaz
    for i in range(3):
        for j in range(3):
            if board[i][j] != ' ':
                sos = check_sos(board, i, j)

                # 🧠 Basit kural:
                # Harfi yerleştiren AI ise (maximize eden), AI puan alır
                # Rakip yerleştirdiyse, oyuncu puan alır
                # Bunu anlamak için tahmin yürütüyoruz:
                # 'O' harflerini çoğunlukla AI yerleştiriyor gibi varsayalım
                if board[i][j] == 'S':
                    player_score += sos
                else:
                    ai_score += sos

    return ai_score - player_score  # AI avantajlıysa pozitif değer döner

# 🧠 Yapay zekanın karar verdiği ana algoritma: minimax + alpha-beta budama
def minimax(board, depth, alpha, beta, maximizing_player, is_ai_turn):

    # ⛔ 1. Durum: Oyun bitmiş mi veya derinlik sınırına gelinmiş mi?
    # Derinlik sıfırsa veya tahtada hamle kalmamışsa artık durur ve değerlendirme yapılır
    if depth == 0 or is_board_full(board):
        return evaluate_score(board), None  # Skor döner, hamle yok çünkü bitti

    # 📝 En iyi hamleyi burada saklayacağız
    best_move = None

    # 👾 Eğer maximizing_player True ise → bu yapay zekânın (bilgisayarın) sırası demek
    if maximizing_player:
        max_eval = float('-inf')  # Başlangıçta en düşük değeri kabul ediyoruz

        # 🧩 Tüm olası hamleleri deniyoruz: her boş yere 'S' ve 'O' koy
        for move in get_possible_moves(board):
            i, j, letter = move  # hamle: satır, sütun, ve konulacak harf

            # 🪞 Tahtanın kopyasını çıkarıyoruz (orijinal tahtayı değiştirmemek için)
            new_board = copy.deepcopy(board)

            # 📌 Bu hamleyi uyguluyoruz
            new_board[i][j] = letter

            # 🧮 Bu hamle sonucunda kaç tane SOS oluştu? (örneğin 1 puanlık bir hamle mi?)
            score = check_sos(new_board, i, j)

            # 🔁 Şimdi rakibin (minimizer = oyuncu) sırası olacak
            eval, _ = minimax(new_board, depth - 1, alpha, beta, False, False)

            # AI bir SOS oluşturduysa, bunu skora ekliyoruz
            if is_ai_turn:
                eval += score  # AI puanı
            else:
                eval -= score  # Oyuncu puanı


            # 💡 Eğer bu değerlendirme önceki maksimumdan büyükse, en iyi skoru ve hamleyi güncelle
            if eval > max_eval:
                max_eval = eval
                best_move = move

            # 🔪 Alpha-Beta budaması için alpha'yı güncelle
            alpha = max(alpha, eval)

            # ❌ Eğer alpha >= beta olursa, bu alt dalları kesmek güvenlidir (daha iyi hamle bulunamaz)
            if beta <= alpha:
                break  # budama yapılır

        return max_eval, best_move

    # 🙋‍♂️ Eğer sıra oyuncudaysa (minimizing player), AI'ye en kötü sonucu getirecek hamleyi bulmak ister
    else:
        min_eval = float('inf')  # Başlangıçta en büyük değeri kabul ediyoruz

        for move in get_possible_moves(board):
            i, j, letter = move
            new_board = copy.deepcopy(board)
            new_board[i][j] = letter
            score = check_sos(new_board, i, j)

            # Şimdi tekrar AI'nin sırası olacak
            eval, _ = minimax(new_board, depth - 1, alpha, beta, True, True)

            # Kullanıcı bir SOS yaptıysa, bu AI için kötü → skordan çıkarılır
            if is_ai_turn:
                eval += score  # AI puanı
            else:
                eval -= score  # Oyuncu puanı

            if eval < min_eval:
                min_eval = eval
                best_move = move

            beta = min(beta, eval)
            if beta <= alpha:
                break  # budama yapılır

        return min_eval, best_move


# 🤖 Bilgisayarın en iyi hamleyi yapmasını sağlar
def make_ai_move():
   # print("\n🤖 Bilgisayar düşünüyor...")
    global player2_score, player_turn  # player_turn burada eksik

    # 🧠 minimax fonksiyonu ile AI en iyi hamleyi arıyor
    # depth → arama derinliği (ne kadar ileriyi görebileceğini belirler)
    # -inf, inf → başlangıçta herhangi bir skor sınırlaması olmadığını gösterir
    # True → bu tur AI'nin (maksimize eden oyuncu) sırası
       # 🧮 Kalan boş hücre sayısı kadar derinliğe bak → tüm olasılıkları kontrol eder
    depth = sum(row.count(' ') for row in board)

    # 🧠 Derinlik dinamik: kalan hamle sayısı kadar
    _, best_move = minimax(board, depth, float('-inf'), float('inf'), True, True)


    # ✅ Eğer geçerli bir en iyi hamle bulunduysa:
    if best_move:
        i, j, letter = best_move  # En iyi hamlenin detaylarını al (konum ve harf)

        # ⬇️ Hamleyi tahtaya uygula
        board[i][j] = letter

        # ⚙️ Bu hamle sonucunda kaç SOS oluştu? Puanı hesapla
        sos = check_sos(board, i, j)

        # 🌟 Global değişkeni kullanarak bilgisayarın puanını güncelle
        global player2_score
        player2_score += sos # Bilgisayar skoru güncellenir
        grid_buttons[i][j].config(text=letter, state='disabled') # Buton devre dışı bırakılır
        update_score()
        if sos == 0:
            player_turn = True # Sıra oyuncuya geçer
        else:
            status_label.config(text=f"Bilgisayar {sos} puan aldı!")
        if is_board_full(board):
            end_game()


        # 🖨️ Bilgisayarın yaptığı hamleyi ve aldığı puanı kullanıcıya bildir
       # print(f"🤖 Bilgisayar {i},{j} konumuna '{letter}' koydu. {sos} puan aldı. Toplam: {player2_score}")

# 🔃 Skor etiketini günceller (GUI ekranında)
def update_score():
    score_label.config(text=f"Skor - Oyuncu: {player1_score} | Bilgisayar: {player2_score}")

# 👤 Oyuncunun butona tıklamasıyla hamle yapılır ve bu fonksiyon çalışır
def player_move(i, j):
    global player1_score, player_turn
    if board[i][j] != ' ' or not player_turn:
        return  # Hücre doluysa veya sırası değilse hiçbir şey yapma
    letter = selected_letter.get() # Oyuncunun seçtiği harf alınır
    board[i][j] = letter
    grid_buttons[i][j].config(text=letter, state='disabled') # Hücreye harf yazılır ve pasif yapılır
    sos = check_sos(board, i, j)
    player1_score += sos
    update_score()

    if sos == 0:
        player_turn = False # Skor alınmadıysa sıra bilgisayara geçer
        status_label.config(text="Bilgisayarın sırası")
        root.after(500, make_ai_move) # 500ms sonra bilgisayar hamlesi yapılır
    else:
        status_label.config(text=f"Oyuncu {sos} puan aldı!")
    if is_board_full(board):
        end_game() # Oyun biterse sonucu göster


# 🏁 Oyun bitince sonucu gösterir ve pencereyi kapatır
def end_game():
    if player1_score > player2_score:
        message = "Oyuncu 1 kazandı!"
    elif player2_score > player1_score:
        message = "Bilgisayar kazandı!"
    else:
        message = "Berabere!"
    messagebox.showinfo("Oyun Bitti", message)
    root.quit() # Uygulama kapanır

# 🧱 GUI bileşenlerini oluştur: harf seçimi, durum, skor ve butonlar
letter_frame = tk.Frame(root)
tk.Radiobutton(letter_frame, text='S', variable=selected_letter, value='S').pack(side='left')
tk.Radiobutton(letter_frame, text='O', variable=selected_letter, value='O').pack(side='left')
# Eskisi:
# status_label.pack()
# score_label.pack()

# Yenisi:
status_label.grid(row=0, column=0, columnspan=3, pady=(10, 0))
score_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
letter_frame.grid(row=2, column=0, columnspan=3)

# 🧮 3x3 butonlu tahta oluştur
for i in range(3):
    for j in range(3):
        btn = tk.Button(root, text=' ', font=("Arial", 24), width=3, height=1, command=lambda i=i, j=j: player_move(i, j))
        btn.grid(row=i + 3, column=j)
        grid_buttons[i][j] = btn

# 🚀 Tkinter ana döngüsünü başlatılır (GUI çalışır)
root.mainloop()



'''
# 🎮 Oyunun ana döngüsü
while True:
    print_board(board)  # Her turda tahtayı göster

    # Kimin sırası olduğunu göster
    print(f"\n{'Oyuncu 1' if player_turn else 'Bilgisayar'}'in sırası")

    if player_turn:  # Oyuncunun sırasıysa
        try:
            # Kullanıcıdan satır ve sütun al
            row, col = map(int, input("Satır ve sütun gir (örnek: 0 1): ").split())

            # Geçerli mi kontrol et
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print("⛔ Geçersiz konum! 0-2 arasında sayı girin.")
                continue

            if board[row][col] != ' ':
                print("⛔ Bu hücre zaten dolu!")
                continue

            # Kullanıcıdan harf al
            letter = input("Harf gir (S veya O): ").upper()
            if letter not in ['S', 'O']:
                print("⛔ Sadece 'S' veya 'O' girilebilir.")
                continue

            board[row][col] = letter  # Hamle uygula
            sos_formed = check_sos(board, row, col)

            if sos_formed > 0:
                player1_score += sos_formed
                print(f"✔️ Oyuncu 1 {sos_formed} puan aldı! Toplam: {player1_score}")
            else:
                player_turn = not player_turn  # Puan alınmadıysa sıra değişsin

        except ValueError:
            print("⛔ Lütfen sadece sayı girin! Örneğin: 0 2")
            continue

    else:  # Bilgisayarın sırasıysa
        make_ai_move()
        player_turn = not player_turn  # Bilgisayar hamle yaptıktan sonra sıra değişir

    # Oyun bitmiş mi? Tahta dolduysa
    if is_board_full(board):
        print_board(board)
        print("\n🎉 Oyun bitti!")
        print(f"🧑‍🎮 Oyuncu 1 Puan: {player1_score}")
        print(f"🤖 Bilgisayar Puan: {player2_score}")

        if player1_score > player2_score:
            print("🏆 Oyuncu 1 kazandı!")
        elif player2_score > player1_score:
            print("🏆 Bilgisayar kazandı!")
        else:
            print("🤝 Berabere!")
        break  # Döngü sonlanır, oyun biter '''
