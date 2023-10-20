import dearpygui.dearpygui as dpg
import colors

player_1_selected_icon = []
player_1_name = []
player_1_score_value = [0]
player_2_selected_icon = []
player_2_name = []
player_2_score_value = [0]

game_step = [0]
board_row = [[9, 9, 9], [9, 9, 9], [9, 9, 9]]
board_column = [[9, 9, 9], [9, 9, 9], [9, 9, 9]]

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
        dpg.set_value("player_1_score", value = f"Player 1 ({player_1_name[0]}) score:")
        dpg.set_value("player_2_score", value = f"Player 2 ({player_2_name[0]}) score:")
    else:
        dpg.configure_item("start_game_popup", show = True)

def change_texture(sender, app_data, user_data):
    game_step[0] += 1

    if game_step[0] % 2 != 0:
        dpg.configure_item(sender, texture_tag = player_1_selected_icon[0], enabled = False)
        dpg.set_value("hint_text", value = f"Player 2 ({player_2_name[0]}) to play...")
        check_result(user_data, image_to_check = player_1_selected_icon[0], player = 1, playername = player_1_name[0])
    if game_step[0] % 2 == 0:
        dpg.configure_item(sender, texture_tag = player_2_selected_icon[0], enabled = False)
        dpg.set_value("hint_text", value = f"Player 1 ({player_1_name[0]}) to play...")
        check_result(user_data, image_to_check = player_2_selected_icon[0], player = 2, playername = player_2_name[0])
        
def check_result(user_data, image_to_check, player, playername):
    row = int(user_data[0]) - 1
    column = int(user_data[1]) - 1

    board_row[row].pop((column))
    board_column[column].pop((row))

    if image_to_check == "image_o":
        board_row[row].insert(column, 0)
        board_column[column].insert(row, 0)
    if image_to_check == "image_x":
        board_row[row].insert(column, 1)
        board_column[column].insert(row, 1)

    print(board_row)
    print(board_column)

    check_row(player, playername)

def check_row(player, playername):
    game = "on"
    while game == "on":
        for row in range(0, 3):
            if board_row[row][0] == board_row[row][1] and board_row[row][0] == board_row[row][2] and sum(board_row[row]) != 27:
                print("win1")
                game = "off"
                the_end(player, playername, state = "win")
                break
        if game == "off":
            break

        for column in range(0, 3):
            if board_column[column][0] == board_column[column][1] and board_column[column][0] == board_column[column][2] and sum(board_column[column]) != 27:
                print("win2")
                game = "off"
                the_end(player, playername, state = "win")
                break 
            if game == "off":
                break 

        if board_row[0][0] == board_row[1][1] and board_row[0][0] == board_row[2][2] and board_row[0][0] + board_row[1][1] + board_row[2][2] != 27:
            print("win3")
            game = "off"
            the_end(player, playername, state = "win")
        if game == "off":
            break

        if board_row[2][0] == board_row[1][1] and board_row[2][0] == board_row[0][2] and board_row[2][0] + board_row[1][1] + board_row[0][2] != 27:
            print("win4")
            game = "off"
            the_end(player, playername, state = "win")
        if game == "off":
            break

        if game_step[0] == 9:
            the_end(player, playername, state = "draw")

        game = "off"

def the_end(player, playername, state):
    for row in range(1, 4):
        for column in range(1, 4):
            dpg.configure_item(f"button{row}_{column}", enabled = False)
    
    dpg.set_value("hint_text", value = "The end!")

    if state == "win":
        dpg.set_value("winner", value = f"Player {player} ({playername}) wins!")
        if player == 1:
            player_1_score_value[0] += 1
            dpg.set_value("player_1_score_value", player_1_score_value[0])
        if player == 2:
            player_2_score_value[0] += 1
            dpg.set_value("player_2_score_value", player_2_score_value[0])

    if state == "draw":
        dpg.set_value("winner", value = f"You both loose!")

    dpg.configure_item("the_end_popup", show = True)
    
def new_game():
    for row in range(1, 4):
        for column in range(1, 4):
            dpg.configure_item(f"button{row}_{column}", texture_tag = "image_blank", enabled = True)

    for i in range(0, 3):
        for j in range(0, 3):
                board_row[i].pop(0)
                board_row[i].append(9)
                board_column[i].pop(0)
                board_column[i].append(9)

    dpg.set_value("hint_text", value = f"Player 1 ({player_1_name[0]}) to play...")

    game_step.clear()
    game_step.append(0)

def reset_game():
    new_game()
    player_1_selected_icon.clear()
    player_1_name.clear()
    player_1_score_value.clear
    player_1_score_value.append(0)

    player_2_selected_icon.clear()
    player_2_name.clear()
    player_2_score_value.clear()
    player_2_score_value.append(0)

    dpg.configure_item("welcome_screen", show = True)
    dpg.configure_item("game_screen", show = False)
    dpg.set_primary_window("welcome_screen", True)
    dpg.set_value("player_1_name", value = "")
    dpg.set_value("player_2_name", value = "")
    dpg.configure_item("player_1_icon_o", background_color = (0, 0, 0, 0))
    dpg.configure_item("player_1_icon_x", background_color = (0, 0, 0, 0))
    dpg.configure_item("player_2_icon_o", show = False, background_color = (0, 0, 0, 0))
    dpg.configure_item("player_2_icon_x", show = False, background_color = (0, 0, 0, 0))

####################################################################################################################################################################################    

dpg.create_context()

width_blank, height_blank, channels_blank, data_blank = dpg.load_image("blank.png")
width_x, height_x, channels_x, data_x = dpg.load_image("x.png")
width_o, height_o, channels_o, data_o = dpg.load_image("o.png")

with dpg.texture_registry():
    dpg.add_static_texture(width = width_x, height = height_x, default_value = data_x, tag = "image_x")
    dpg.add_static_texture(width = width_o, height = height_o, default_value = data_o, tag = "image_o")
    dpg.add_static_texture(width = width_blank, height = height_blank, default_value = data_blank, tag = "image_blank")

dpg.create_viewport(title = 'Tic-Tac-Toe', width = 550, height = 675, small_icon = "icon.ico", large_icon = "icon.ico", resizable = False)

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
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 40, 10)

    dpg.add_button(label = "Start game", callback = start_game, tag = "start_game_button")
    dpg.bind_item_theme(dpg.last_item(), "button_theme")

with dpg.window(label = "Game screen", pos = (100, 100), show = False, tag = "game_screen"):
    for row in range(1, 4):
        with dpg.group(horizontal = True):
            for column in range(1, 4):
                dpg.add_image_button("image_blank", width = 150, height = 150, callback = change_texture, user_data = f"{row}{column}", tag = f"button{row}_{column}")
    dpg.add_text("Player to play...", tag = "hint_text")

    with dpg.group(horizontal = True):
        dpg.add_button(label = "New game", callback = new_game, tag = "new_game_button")
        dpg.bind_item_theme(dpg.last_item(), "button_theme")
        dpg.add_button(label = "Reset game", callback = reset_game, tag = "reset_game_button")
        dpg.bind_item_theme(dpg.last_item(), "button_theme")

    with dpg.tree_node(label = "Score:", default_open = True, bullet = True, leaf = True):
        with dpg.group(horizontal = True):
            dpg.add_text("Player 1:", tag = "player_1_score")
            dpg.add_text("0", tag = "player_1_score_value")
        with dpg.group(horizontal = True):
            dpg.add_text("Player 2:", tag = "player_2_score")
            dpg.add_text("0", tag = "player_2_score_value")

with dpg.window(label = "Wait!", no_resize = True, popup = True, show = False, no_title_bar = True, pos = (100, 100), tag = "start_game_popup"):
    dpg.add_text("Please enter usernames and select icons.", pos = (10, 40))

with dpg.window(label = "The end!", autosize=True, no_resize = True, modal = True, popup = True, show = False, no_title_bar = True, pos = (100, 100), tag = "the_end_popup"):
    dpg.add_text(f"Player wins!", tag = "winner")
    dpg.add_button(label = "Close", callback = lambda: dpg.configure_item("the_end_popup", show = False), tag = "close_button")
    dpg.bind_item_theme(dpg.last_item(), "button_theme")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("welcome_screen", True)
dpg.start_dearpygui()
dpg.destroy_context()