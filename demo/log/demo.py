#!/usr/bin/env python3



def main():
    options = ["entry 1", "entry 2", "entry 3"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    print(f"You have selected {options[menu_entry_index]}!")

if __name__ == "__main__":
    main()