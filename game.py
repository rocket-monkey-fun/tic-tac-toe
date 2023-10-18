import dearpygui.dearpygui as dpg
import colors

player_1_selected_icon = []
player_1_name = []
player_2_selected_icon = []
player_2_name = []

game_step = [0]
board = [[9, 9, 9], [9, 9, 9], [9, 9, 9]]

def player_name(sender, app_data):
    if sender == "player_1_name":
        player_1_name.clear()
        player_1_name.append(app_data)
    if sender == "player_2_name":
        player_2_name.clear()
        player_2_name.append(app_data)

def player_icon(sender, app_data):
    if sender == "player_1_icon_o":
        dpg.configure_item("player_1_icon_o", background_color = colors.retro_turqoise)
        dpg.configure_item("player_1_icon_x", background_color = colors.retro_red)
        dpg.configure_item("player_2_icon_o", show = True, background_color = colors.retro_red)
        dpg.configure_item("player_2_icon_x", show = True, background_color = colors.retro_turqoise)
        player_1_selected_icon.clear()
        player_2_selected_icon.clear()
        player_1_selected_icon.append("image_o")
        player_2_selected_icon.append("image_x")

    else:
        dpg.configure_item("player_1_icon_o", background_color = colors.retro_red)
        dpg.configure_item("player_1_icon_x", background_color = colors.retro_turqoise)
        dpg.configure_item("player_2_icon_o", show = True, background_color = colors.retro_turqoise)
        dpg.configure_item("player_2_icon_x", show = True, background_color = colors.retro_red)
        player_1_selected_icon.clear()
        player_2_selected_icon.clear()
        player_1_selected_icon.append("image_x")
        player_2_selected_icon.append("image_o")

def start_game(sender, app_data):
    if len(player_1_selected_icon) != 0 and len(player_1_name) != 0 and len(player_2_name) != 0:
        dpg.configure_item("welcome_screen", show = False)
        dpg.configure_item("game_screen", show = True)
        dpg.set_primary_window("game_screen", True)
        dpg.set_value("hint_text", value = f"Player 1 ({player_1_name[0]}) to play...")
    else:
        dpg.configure_item("start_game_popup", show = True)

def change_texture(sender, app_data, user_data):
    game_step[0] += 1

    if game_step[0] % 2 != 0:
        dpg.configure_item(sender, texture_tag = player_1_selected_icon[0], enabled = False)
        dpg.set_value("hint_text", value = f"Player 2 ({player_2_name[0]}) to play...")
        check_result(user_data, image_to_check = player_1_selected_icon[0])
    if game_step[0] % 2 == 0:
        dpg.configure_item(sender, texture_tag = player_2_selected_icon[0], enabled = False)
        dpg.set_value("hint_text", value = f"Player 1 ({player_1_name[0]}) to play...")
        check_result(user_data, image_to_check = player_2_selected_icon[0])
        
def check_result(user_data, image_to_check):
    row = int(user_data[0]) - 1
    column = int(user_data[1]) - 1

    board[row].pop((column))

    if image_to_check == "image_o":
        board[row].insert(column, 0)
    if image_to_check == "image_x":
        board[row].insert(column, 1)

    print(board)

    check_scenario(user_data, row, column)

def check_scenario(user_data, row, column):
    print(user_data)
    if user_data == "11":
        print("yey2")
        if board[row][column] == board[row][column + 1] and board[row][column] == board[row][column + 2]:
            print("yey")

dpg.create_context()

width_blank, height_blank, channels_blank, data_blank = dpg.load_image("blank.png")
width_x, height_x, channels_x, data_x = dpg.load_image("x.png")
width_o, height_o, channels_o, data_o = dpg.load_image("o.png")

with dpg.texture_registry():
    dpg.add_static_texture(width = width_x, height = height_x, default_value = data_x, tag = "image_x")
    dpg.add_static_texture(width = width_o, height = height_o, default_value = data_o, tag = "image_o")
    dpg.add_static_texture(width = width_blank, height = height_blank, default_value = data_blank, tag = "image_blank")

dpg.create_viewport(title = 'Tic-Tac-Toe', width = 600, height = 600, small_icon = "icon.ico", large_icon = "icon.ico", resizable = True)


with dpg.window(label = "Welcome screen", pos = (100, 100), show = True, tag = "welcome_screen"):
    with dpg.tree_node(label = "Player 1:", default_open = True, bullet = True, leaf = True):
        with dpg.tree_node(label = "Name:", default_open = True, bullet = True, leaf = True):
            dpg.add_input_text(hint = "Enter name...", width = 150, callback = player_name, tag = "player_1_name")
        with dpg.tree_node(label = "Icon:", default_open = True, bullet = True, leaf = True):
            with dpg.group(horizontal = True):
                dpg.add_image_button("image_o", width = 75, height = 75, callback = player_icon, tag = "player_1_icon_o")
                dpg.add_image_button("image_x", width = 75, height = 75, callback = player_icon, tag = "player_1_icon_x")

    with dpg.tree_node(label = "Player 2:", default_open = True, bullet = True, leaf = True):
        with dpg.tree_node(label = "Name:", default_open = True, bullet = True, leaf = True):
            dpg.add_input_text(hint = "Enter name...", width = 150, callback = player_name, tag = "player_2_name")
        with dpg.tree_node(label = "Icon:", default_open = True, bullet = True, leaf = True):
            with dpg.group(horizontal = True):
                dpg.add_image_button("image_o", width = 75, show = False, height = 75, tag = "player_2_icon_o")
                dpg.add_image_button("image_x", width = 75, show = False, height = 75, tag = "player_2_icon_x")

    with dpg.theme(tag = "button_theme"):
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, colors.retro_blue_dark)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, colors.retro_blue_dark)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, colors.retro_blue_light)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 40)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 40, 20)

    dpg.add_button(label = "Start game", callback = start_game, tag = "start_game_button")
    dpg.bind_item_theme(dpg.last_item(), "button_theme")

with dpg.window(label = "Game screen", pos = (100, 100), show = False, tag = "game_screen"):
    for row in range(1, 4):
        with dpg.group(horizontal = True):
            for column in range(1, 4):
                dpg.add_image_button("image_blank", width = 150, height = 150, callback = change_texture, user_data = f"{row}{column}", tag = f"button{row}_{column}")
    dpg.add_text("Player to play...", tag = "hint_text")

with dpg.window(label = "Wait!", popup = True, show = False, no_title_bar = True, pos = (100, 100), tag = "start_game_popup"):
    dpg.add_text("Please enter usernames and select icons.", pos = (10, 40))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("welcome_screen", True)
dpg.start_dearpygui()
dpg.destroy_context()