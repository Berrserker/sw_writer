import dearpygui.dearpygui as dpg
from lupa import LuaRuntime
import re

dpg.create_context()

lua = LuaRuntime(unpack_returned_tuples=True)

# Initialize Lua version (default 5.3, you can change it)
lua_version = "5.3"

# Predefined semantic functions and additional dictionary
lua_semantics = {
    "print": "Outputs text to the console",
    "math.sqrt": "Returns the square root of a number",
    "string.len": "Returns the length of a string",
    "os.time": "Returns the current time",
}

autocomplete_dict = list(lua_semantics.keys())

# Lua keywords and reserved words for syntax highlighting
lua_keywords = [
    "and", "break", "do", "else", "elseif", "end", "false", "for", "function",
    "if", "in", "local", "nil", "not", "or", "repeat", "return", "then", "true",
    "until", "while"
]


# Function to execute Lua code
def run_lua_code(sender, data):
    lua_code = dpg.get_value("LuaEditor")
    try:
        output = lua.execute(lua_code)
        dpg.set_value("LuaOutput", f"Result: {output}")
    except Exception as e:
        dpg.set_value("LuaOutput", f"Error: {str(e)}")


# Function to update autocomplete suggestions
def update_autocomplete(sender, data):
    text = dpg.get_value("LuaEditor")
    suggestions = [key for key in autocomplete_dict if key.startswith(text.split()[-1])]
    dpg.set_items("AutocompleteList", suggestions)
    highlight_syntax()


# Function to select an autocomplete suggestion
def apply_autocomplete(sender, data):
    selected_item = dpg.get_value("AutocompleteList")
    if selected_item:
        current_text = dpg.get_value("LuaEditor").rsplit(' ', 1)[0]
        dpg.set_value("LuaEditor", f"{current_text} {selected_item}")
        highlight_syntax()


# Function to highlight Lua syntax
def highlight_syntax():
    lua_code = dpg.get_value("LuaEditor")
    highlighted_code = lua_code

    # Highlight keywords
    for keyword in lua_keywords:
        highlighted_code = re.sub(rf"\b{keyword}\b", f"[Keyword]{keyword}[/Keyword]", highlighted_code)

    # Highlight functions
    for function in lua_semantics.keys():
        highlighted_code = re.sub(rf"\b{function}\b", f"[Function]{function}[/Function]", highlighted_code)

    # Display highlighted code (currently just for display)
    dpg.set_value("SyntaxHighlightedCode", highlighted_code)


try:
    with dpg.window(label="Tutorial"):
        dpg.add_text("Lua Code Editor")
        dpg.add_input_text(label="LuaEditor", multiline=True, width=500, height=300, callback=update_autocomplete, on_enter=True)
        dpg.add_button(label="Run Lua Code", callback=run_lua_code)
        dpg.add_listbox(autocomplete_dict, width=200, height=100, callback=apply_autocomplete)
        dpg.add_text("Output:")
        dpg.add_input_text(label="LuaOutput", multiline=True, readonly=True, width=500, height=200)
        dpg.add_text(f"Lua Version: {lua_version}")
        dpg.add_text("Syntax Highlighted Code:")
        dpg.add_input_text(label="SyntaxHighlightedCode", multiline=True, readonly=True, width=500, height=300)

        # dpg.add_checkbox(label="Radio Button1", tag="R1")
        # dpg.add_checkbox(label="Radio Button2", source="R1")
        #
        # dpg.add_input_text(label="Text Input 1")
        # dpg.add_input_text(label="Text Input 2")
        # dpg.add_input_text(label="Text Input 3", source=dpg.last_item(), password=True)
except Exception as e:
    print(e)

dpg.create_viewport(title='SW_builder', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()