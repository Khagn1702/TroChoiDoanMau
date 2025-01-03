import pygame
import sys
import random
# Khởi tạo Pygame
pygame.init()
# Khởi tạo Pygame mixer
pygame.mixer.init()
# Tải các âm thanh
win = pygame.mixer.Sound("win.wav")  # Âm thanh khi người chơi thắng
lose = pygame.mixer.Sound("lose.wav")  # Âm thanh khi người chơi thua
button_click_sound = pygame.mixer.Sound("button_click.wav")  # Âm thanh khi nhấn nút
intro = pygame.mixer.Sound("intro.wav")
color_click_sound = pygame.mixer.Sound("color_click.wav")  # Âm thanh khi người chơi nhấn chọn màu
level_up_sound = pygame.mixer.Sound("level_up.wav")
# Biến kiểm soát trạng thái intro
intro_played = False  # Khai báo biến intro_played để kiểm soát âm thanh intro

# Kích thước cửa sổ
WIDTH, HEIGHT = 1000, 1000

# Màu sắc
MAGENTA = (255, 0, 255)  # Định nghĩa màu Magenta (tím hồng)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)  # Định nghĩa màu xanh lá cây
YELLOW = (255, 255, 0)
COLORS = [
    (255, 0, 0),  # Đỏ
    (0, 128, 0),  # Xanh lá cây đậm
    (0, 0, 255),  # Xanh dương
    (255, 165, 0),  # Cam
    (255, 255, 0),  # Vàng
    (128, 0, 128),  # Tím
    (0, 255, 255)  # Xanh da trời
]
# Màu nền menu và các nút
BUTTON_COLOR = (51, 51, 51)  # Màu xám cho các nút menu
HIGHLIGHT_COLOR = (0, 255, 255)  # Màu sáng cho mục đã chọn

# Tạo cửa sổ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trò Chơi Đoán Màu")

# Thay đổi font chữ
font_title = pygame.font.Font("InterTight-VariableFont_wght.ttf", 72)  # Tiêu đề
font_button = pygame.font.Font("InterTight-VariableFont_wght.ttf", 36) # Nút bấm
font_text = pygame.font.Font("InterTight-Italic-VariableFont_wght.ttf", 28)   # Chữ thường
# Các mục trong menu
menu_items = [
    ("              GIỚI THIỆU", "Giới thiệu về trò chơi"),
    ("              HƯỚNG DẪN", "Hướng dẫn cách chơi"),
    ("              CHẠY DEMO", "Chạy demo trò chơi"),
    ("              THOÁT", "Thoát trò chơi")
]

def ve_tro_choi(guesses, results, current_guess, round_size, show_answer, secret_colors, level):
    screen.fill(BLACK)
    # Hiển thị Level ở trên cùng với màu vàng
    level_text = font_title.render(f"Level {level}", True, (255, 255, 0))  # Màu vàng
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 20))

    # Vẽ một đường gạch ngang dưới "Level"
    pygame.draw.line(screen, WHITE, (10, 90), (WIDTH - 10, 90), 3)

    # Tính toán chiều dài viền cho phần "Chọn màu"
    total_width_choose = round_size * 70 - 20  # Chiều rộng cần thiết cho các vòng màu (kể cả khoảng cách)
    pygame.draw.rect(screen, GRAY, (10, 150, total_width_choose + 20, 120), border_radius=10)  # Viền cho "Chọn màu"
    title_text = font_text.render(f"Chọn màu (1-{round_size})", True, WHITE)
    screen.blit(title_text, (20, 160))

    # Vẽ các vòng màu
    x = 20
    y = 215  # Di chuyển xuống dưới một chút để không bị che bởi chữ "Chọn màu"
    spacing = 70
    for i, color in enumerate(COLORS[:round_size]):
        pygame.draw.circle(screen, color, (x + 25, y), 20)
        color_text = font_text.render(str(i + 1), True, WHITE)
        screen.blit(color_text, (x + 20, y + 30))
        x += spacing

    # Nút xem kết quả
    pygame.draw.rect(screen, GRAY, (20, 700, 150, 50), border_radius=10)
    button_text = font_button.render("Kết Quả", True, WHITE)
    screen.blit(button_text, (30, 710))

    # Nút thoát
    pygame.draw.rect(screen, GRAY, (WIDTH - 170, 700, 150, 50), border_radius=10)
    exit_button_text = font_button.render("Thoát", True, WHITE)
    screen.blit(exit_button_text, (WIDTH - 110 - exit_button_text.get_width() // 2, 710))  # Căn chỉnh nút "Thoát"

    # Di chuyển phần "Đoán màu" xuống dưới một chút
    center_x = WIDTH // 2
    y = 350  # Di chuyển phần đoán xuống dưới (vị trí y đã thay đổi)
    for guess, result in zip(guesses, results):
        x = center_x - (len(guess) * 35)
        for color in guess:
            pygame.draw.circle(screen, COLORS[color - 1], (x, y), 20)
            x += 70

        # Vẽ hình tròn cho số lượng đúng
        for i in range(result):  # Vẽ số lượng tròn đúng
            pygame.draw.circle(screen, WHITE, (x, y), 10)  # Vẽ các tròn đại diện cho đúng
            x += 30  # Điều chỉnh khoảng cách giữa các hình tròn

        y += 50

    # Hiển thị màu đang nhập
    if current_guess:
        total_width = len(current_guess) * 70 - 20  # Chiều rộng tổng cộng của các vòng màu
        x = (WIDTH - total_width) // 2  # Tính toán vị trí x để căn giữa
        for color in current_guess:
            pygame.draw.circle(screen, COLORS[color - 1], (x, y), 20)
            x += 70

    # Tính toán chiều dài viền cho phần "Đáp án"
    total_width_answer = len(secret_colors) * 70 - 20  # Chiều rộng cần thiết cho các vòng màu trong đáp án
    if show_answer:
        x = 20  # Đặt vị trí x ở góc bên trái
        answer_text_y = HEIGHT - 200  # Điều chỉnh y để tránh bị che bởi các vòng màu
        answer_text = font_text.render("Đáp án:", True, WHITE)
        screen.blit(answer_text, (x, answer_text_y))

        # Viền cho phần đáp án
        pygame.draw.rect(screen, GRAY, (15, HEIGHT - 200, total_width_answer + 20, 120),
                         border_radius=10)  # Viền cho "Đáp án"

        colors_y = answer_text_y + 40  # Đặt khoảng cách giữa "Đáp án:" và các vòng màu
        for color in secret_colors:
            pygame.draw.circle(screen, COLORS[color - 1], (x + 25, colors_y), 20)
            x += 50

    pygame.display.flip()


def hien_thi_game_over(secret_colors):
    screen.fill(BLACK)

    # Hiển thị "Game Over!" ở giữa màn hình
    result_text = font_title.render("Game Over!", True, (255, 0, 0))
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 100))

    # Hiển thị "Đáp án đúng:" ở dưới "Game Over!"
    answer_text = font_text.render("Đáp án đúng:", True, WHITE)
    screen.blit(answer_text, (WIDTH // 2 - answer_text.get_width() // 2, HEIGHT // 2))

    # Hiển thị đáp án màu
    center_x = WIDTH // 2
    y = HEIGHT // 2 + 60
    x = center_x - (len(secret_colors) * 35)
    for color in secret_colors:
        pygame.draw.circle(screen, COLORS[color - 1], (x, y), 20)
        x += 100

    # Phát âm thanh khi kết thúc trò chơi (Game Over)
    lose.play()  # Phát âm thanh thua

    pygame.display.flip()
    pygame.time.delay(3000)  # Chờ trong 3 giây trước khi quay lại menu

    lose.stop()  # Dừng âm thanh lose sau khi game over

    main_menu()  # Quay lại menu chính


# Cập nhật phần game_loop
def vong_lap_trong_tro_choi():
    global intro_played
    intro.stop()  # Dừng âm thanh intro khi vào mục "Giới thiệu"
    intro_played = False  # Đặt lại intro_played
    running = True
    round_sizes = [4, 5, 6, 7]
    round_index = 0
    level = 1  # Gán giá trị cho level

    secret_colors = [random.randint(1, round_sizes[round_index]) for _ in range(round_sizes[round_index])]
    guesses = []
    results = []
    current_guess = []
    attempts = 0
    max_attempts = 10
    show_answer = False  # Biến để theo dõi trạng thái hiển thị đáp án

    while running:
        ve_tro_choi(guesses, results, current_guess, round_sizes[round_index], show_answer, secret_colors, level)
        if attempts >= max_attempts:
            hien_thi_game_over(secret_colors)
            lose.play()  # Phát âm thanh thua khi game over
            running = False
            continue

        if len(results) > 0 and results[-1] == round_sizes[round_index]:
            if round_index == len(round_sizes) - 1:
                result_text = font_title.render("You Win!", True, (0, 255, 0))
                screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2))
                win.play()  # Phát âm thanh khi người chơi hoàn thành toàn bộ trò chơi
                pygame.display.flip()
                pygame.time.delay(3000)
                running = False
            else:
                round_index += 1
                level += 1  # Tăng level khi chuyển sang vòng mới
                secret_colors = [random.randint(1, round_sizes[round_index]) for _ in range(round_sizes[round_index])]
                guesses = []
                results = []
                current_guess = []
                attempts = 0
                show_answer = False  # Ẩn đáp án khi chuyển vòng mới
                level_up_sound.play()  # Phát âm thanh khi lên level mới
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra nhấn nút "Kết Quả"
                if 20 <= event.pos[0] <= 170 and 700 <= event.pos[1] <= 750:
                    button_click_sound.play()  # Phát âm thanh khi nhấn nút
                    show_answer = not show_answer
                # Kiểm tra nhấn nút "Thoát"
                if WIDTH - 170 <= event.pos[0] <= WIDTH - 20 and 700 <= event.pos[1] <= 750:
                    button_click_sound.play()  # Phát âm thanh khi nhấn nút
                    main_menu()  # Quay lại menu khi nhấn "Thoát"
                    return


            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Nhấn ESC để quay lại menu
                    button_click_sound.play()  # Phát âm thanh khi nhấn ESC
                    main_menu()  # Quay lại menu khi ESC được nhấn
                    return
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]:
                    color_index = event.key - pygame.K_1 + 1
                    if color_index <= round_sizes[round_index]:
                        current_guess.append(color_index)
                        color_click_sound.play()  # Phát âm thanh khi chọn màu

                    if len(current_guess) == round_sizes[round_index]:
                        guesses.append(current_guess)
                        correct = sum(
                            [1 for i in range(round_sizes[round_index]) if current_guess[i] == secret_colors[i]])
                        results.append(correct)
                        current_guess = []
                        attempts += 1

    main_menu()  # Quay lại menu chính khi kết thúc game

def gioi_thieu():
    global intro_played
    intro.stop()  # Dừng âm thanh intro khi vào mục "Giới thiệu"
    intro_played = False  # Đặt lạ # Dừng âm thanh intro khi vào mục "Giới thiệu"
    running = True
    while running:
        screen.fill(BLACK)

        # Tiêu đề lớn "GIỚI THIỆU"
        title_text = font_title.render("GIỚI THIỆU", True, YELLOW)
        screen.blit(title_text, (50, 100))  # Căn trái cho tiêu đề lớn

        # Nội dung giới thiệu
        intro_text = """
        ĐẶC TẢ ĐỀ TÀI

        Nội dung bài toán:

        “Đoản màu” được thể hiện: có từ 4 đến 7 màu, người chơi một lần đoán 4 màu, có 10 lần đoán.
        Máy sẽ đánh giá mỗi lần đoán và cho biết số vị trí đoán đúng.
        Sau 10 lần đoán máy sẽ cho kết quả người chơi thắng hay thua.

        YÊU CẦU CỦA ĐỀ TÀI

        Nắm vững cơ sở lý thuyết về cấu trúc dữ liệu. Các giải thuật sắp xếp.
        Chương trình cần có các chức năng sau đối với các giải thuật:

        Đọc dữ liệu từ file văn bản, xuất ra file văn bản.

        Cho biết số lần đổi chỗ của các giải thuật.

        So sánh các giải thuật với nhau.
        """

        # Vẽ các dòng nội dung từ trái sang phải
        intro_lines = intro_text.strip().split('\n')
        y_offset = 180
        for line in intro_lines:
            line_text = font_text.render(line, True, WHITE)
            screen.blit(line_text, (20, y_offset))  # Căn trái cho văn bản
            y_offset += 40  # Điều chỉnh khoảng cách giữa các dòng

        # Hiển thị hướng dẫn phía dưới
        footer_text = font_text.render("Nhấn ESC để quay lại menu", True, CYAN)
        screen.blit(footer_text, (WIDTH // 2 - footer_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

        # Kiểm tra sự kiện thoát (nhấn ESC)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Nhấn ESC để quay lại menu
                    running = False

    main_menu()  # Quay lại menu chính khi ESC được nhấn

def huong_dan():
    global intro_played
    intro.stop()
    intro_played = False
    running = True
    scroll_offset = 0  # Biến theo dõi vị trí cuộn màn hình
    while running:
        screen.fill(BLACK)

        # Tiêu đề lớn "HƯỚNG DẪN"
        title_text = font_title.render("HƯỚNG DẪN", True, YELLOW)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))  # Căn giữa tiêu đề

        # Nội dung hướng dẫn
        instructions_text = """
        1. MÔ TẢ TRÒ CHƠI:

        Trò chơi Đoán Màu yêu cầu người chơi đoán một chuỗi màu sắc từ 4 đến 7 màu. 
        Mỗi lần người chơi sẽ đoán 4 màu, và trò chơi cho phép 10 lần đoán. 
        Mỗi lần đoán, trò chơi sẽ phản hồi bằng cách cho biết số lượng màu sắc và vị trí đoán đúng.

        2. LUẬT CHƠI:

        - Người chơi chỉ được chọn từ một danh sách các màu có sẵn. 
        - Mỗi lần đoán, bạn sẽ phải chọn 4 màu trong số các màu được cung cấp.
        - Sau mỗi lần đoán, trò chơi sẽ phản hồi với số lượng màu và vị trí đúng.
        - Người chơi có tổng cộng 10 lượt đoán để đoán chính xác chuỗi màu của máy.

        3. CÁCH CHƠI:

        - Người chơi nhập màu từ bàn phim số (1 đến 7)
        - Nhấn kết quả nếu như bạn không đoán được.

        4. MỤC TIÊU:

        - Đoán đúng chuỗi màu trong ít lần đoán nhất.
        - Có 10 lần đoán để bạn có thể thử nghiệm chiến lược và dự đoán.
        """

        # Vẽ các dòng hướng dẫn từ trái sang phải với cuộn màn hình
        instructions_lines = instructions_text.strip().split('\n')
        y_offset = 180 - scroll_offset  # Sử dụng scroll_offset để cuộn màn hình
        for line in instructions_lines:
            line_text = font_text.render(line, True, WHITE)
            screen.blit(line_text, (20, y_offset))  # Căn trái cho văn bản
            y_offset += 40  # Điều chỉnh khoảng cách giữa các dòng

        # Hiển thị hướng dẫn phía dưới
        footer_text = font_text.render("Nhấn ESC để quay lại menu", True, CYAN)
        screen.blit(footer_text, (WIDTH // 2 - footer_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

        # Kiểm tra sự kiện thoát (nhấn ESC) và cuộn màn hình
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Nhấn ESC để quay lại menu
                    running = False
                elif event.key == pygame.K_DOWN:  # Cuộn xuống
                    scroll_offset += 40
                elif event.key == pygame.K_UP:  # Cuộn lên
                    scroll_offset -= 40
                    if scroll_offset < 0:  # Ngừng cuộn lên khi đến đầu trang
                        scroll_offset = 0

    main_menu()  # Quay lại menu chính khi ESC được nhấn

def ve_menu(selected_index):
    screen.fill(BLACK)

    # Vẽ khung viền xung quanh toàn bộ menu
    pygame.draw.rect(screen, GRAY, (10, 10, WIDTH - 20, HEIGHT - 20), 10)  # Viền khung ngoài (độ dày = 10)

    # Tiêu đề trên cùng: TRƯỜNG ĐẠI HỌC BẠC LIÊU
    university_text = font_title.render("TRƯỜNG ĐẠI HỌC BẠC LIÊU", True, YELLOW)
    screen.blit(university_text, (WIDTH // 2 - university_text.get_width() // 2, 50))  # Vị trí phía trên

    # Vẽ đường gạch ngang dưới "TRƯỜNG ĐẠI HỌC BẠC LIÊU"
    pygame.draw.line(screen, GRAY, (20, 145), (WIDTH - 20, 145), 5)  # Vẽ đường gạch ngang

    # Tiêu đề chính: TRÒ CHƠI ĐOÁN MÀU
    title_text = font_title.render("TRÒ CHƠI ĐOÁN MÀU", True, YELLOW)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))  # Vị trí dưới tiêu đề trường

    # Các mục menu
    for i, (item, description) in enumerate(menu_items):
        # Kiểm tra nếu mục này được chọn
        if i == selected_index:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (300, 320 + i * 60, 400, 50), border_radius=10)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, (300, 320 + i * 60, 400, 50), border_radius=10)

        # Render chữ với màu vàng cho các mục menu
        button_text = font_button.render(item, True, YELLOW)  # Đổi màu chữ trong menu thành vàng
        screen.blit(button_text, (400 - button_text.get_width() // 2, 330 + i * 60))

    # Mô tả cho mục được chọn (giữ màu trắng cho mô tả này nếu cần)
    description_text = font_text.render(menu_items[selected_index][1], True, WHITE)  # Mô tả màu trắng
    screen.blit(description_text, (WIDTH // 2 - description_text.get_width() // 2, 600))

    # Hiển thị hướng dẫn phía dưới
    footer_text = font_text.render("Chọn chức năng như thanh menu hoặc nhấn ESC để thoát", True, GREEN)
    screen.blit(footer_text, (WIDTH // 2 - footer_text.get_width() // 2, HEIGHT - 100))

    # Thêm thông tin GVHD, SVTH, MSSV, MSDT vào phía trên phần hiển thị phía dưới
    info_text = "GVHD: Ths.Trần Phước Nghĩa\nSVTH: Nguyễn Trường Khang\nMSSV: 227480201058\nMSDT: DA1 - TH014"
    lines = info_text.split("\n")

    # Tính toán kích thước cho khung viền (dựa vào chiều dài thông tin) và thêm padding
    max_width = max([font_text.size(line)[0] for line in lines])  # Lấy chiều rộng của dòng dài nhất
    padding = 30  # Cộng thêm padding cho chiều rộng
    width_with_padding = max_width + padding  # Chiều rộng khung viền thêm padding
    height = len(lines) * 40  # Tính chiều cao của khung viền dựa trên số dòng

    # Vẽ khung viền quanh thông tin (sử dụng chiều rộng mới)
    pygame.draw.rect(screen, GRAY,
                     (WIDTH // 2 - width_with_padding // 2 - 10, 680 - 10, width_with_padding + 20, height + 20), 5)

    # Vẽ từng dòng thông tin, cách xa phần mô tả mục được chọn một chút
    for index, line in enumerate(lines):
        # Tạo các phần tử dòng thông tin với các từ cần đổi màu
        parts = line.split(": ")
        label = font_text.render(parts[0] + ": ", True, GREEN)  # Từ GVHD, SVTH, MSSV, MSDT
        value = font_text.render(parts[1], True, WHITE)  # Giá trị như "Ths Trần Phước Nghĩa"...

        screen.blit(label, (WIDTH // 2 - width_with_padding // 2 + 10, 680 + index * 40))  # Vị trí cho nhãn
        screen.blit(value, (
        WIDTH // 2 - width_with_padding // 2 + 10 + label.get_width(), 680 + index * 40))  # Vị trí cho giá trị

    pygame.display.flip()


def main_menu():
    global intro_played  # Dùng lại biến toàn cục
    running = True
    selected_index = 0

    if not intro_played:
        intro.play()  # Phát intro nếu chưa phát
        intro_played = True  # Đánh dấu là âm thanh đã phát

    while running:
        ve_menu(selected_index)  # Sửa tên hàm draw_menu thành ve_menu

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 300 <= event.pos[0] <= 700:
                    if 320 <= event.pos[1] <= 370:
                        button_click_sound.play()  # Phát âm thanh khi nhấn nút "Giới thiệu"
                        gioi_thieu()  # Sửa tên hàm show_intro thành gioi_thieu
                    elif 380 <= event.pos[1] <= 430:
                        button_click_sound.play()  # Phát âm thanh khi nhấn nút "Hướng dẫn"
                        huong_dan()  # Sửa tên hàm show_instructions thành huong_dan
                    elif 440 <= event.pos[1] <= 490:
                        button_click_sound.play()  # Phát âm thanh khi nhấn nút "Chạy Demo"
                        vong_lap_trong_tro_choi()  # Sửa tên hàm game_loop thành vong_lap_trong_tro_choi
                    elif 500 <= event.pos[1] <= 550:
                        button_click_sound.play()  # Phát âm thanh khi nhấn nút "Thoát"
                        pygame.quit()
                        sys.exit()  # Mục "Thoát"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)  # Di chuyển lên
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)  # Di chuyển xuống
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:  # Mục "Giới thiệu"
                        button_click_sound.play()  # Phát âm thanh khi nhấn "Giới thiệu"
                        gioi_thieu()  # Sửa tên hàm show_intro thành gioi_thieu
                    elif selected_index == 1:  # Mục "Hướng dẫn"
                        button_click_sound.play()  # Phát âm thanh khi nhấn "Hướng dẫn"
                        huong_dan()  # Sửa tên hàm show_instructions thành huong_dan
                    elif selected_index == 2:  # Mục "Chạy Demo"
                        button_click_sound.play()  # Phát âm thanh khi nhấn "Chạy Demo"
                        vong_lap_trong_tro_choi()  # Sửa tên hàm game_loop thành vong_lap_trong_tro_choi
                    elif selected_index == 3:  # Mục "Thoát"
                        button_click_sound.play()  # Phát âm thanh khi nhấn "Thoát"
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_ESCAPE:  # Thoát khi nhấn ESC
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main_menu()
