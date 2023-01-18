'''
Copy Write File Path to Clipboard

URL:

    http://github.com/khanrahan/copy-write-file-path-to-clipboard

Description:

    Copies the path of the selected Write File nodes in Batch.  The path will be just
    the Media Path and not include the resolved tokens from the Pattern field.  This is
    a limitation not overcome until Flame 2023.2

Menus:

    Right-click selected Write Nodes in Batch --> Copy... --> Write File Path to Clipboard

To Install:

    For all users, copy this file to:
    /opt/Autodesk/shared/python

    For a specific user, copy this file to:
    /opt/Autodesk/user/<user name>/python
'''

from __future__ import print_function

__title__ = "Copy Write File Path to Clipboard"
__version_info__ = (0, 2, 1)
__version__ = ".".join([str(num) for num in __version_info__])

MESSAGE_PREFIX = "[PYTHONHOOK]"

def message(string):
    """Print message to screen using MESSAGE_PREFIX global."""

    print(" ".join([MESSAGE_PREFIX, string]))

def send_to_clipboard(str_data):
    """Takes data in the form of a string and send it the system clipboard."""

    from PySide2 import QtWidgets

    qt_app_instance = QtWidgets.QApplication.instance()
    qt_app_instance.clipboard().setText(str_data)

def complete_pattern(pattern):
    """Complete the path pattern if incomplete.  Flame does the same for you.  It will
    complete the pattern with <frame> and <ext> if they are not present.
    
    The pattern must contain <frame> somewhere or it is appended, and <ext> is always
    appended if not present.  The <ext> token does not include the period but does
    magically cause a period to be added.
    """

    # Remove <ext> if present
    if pattern.endswith('<ext>'):
        pattern = pattern[:-5]

        # Remove hardcoded period if it was preceding <ext>
        if pattern.endswith('.'):
            pattern = pattern[:-1]

    # Append <frame> if not present
    if '<frame>' not in pattern:
        pattern += '<frame>'

    # Replace final period and <ext>
    pattern += '.<ext>'

    return pattern

def generate_frame_token(node):
    """Notation for the <frame> token is [#-#] and includes padding.  If the range is
    just a single frame, Flame just does # plus the padding.
    """

    padding = node.frame_padding.get_value()
    start = str(node.range_start.get_value()).zfill(padding)
    end = str(node.range_end.get_value()).zfill(padding)

    # Check for single frame or frame or range
    if start == end:  # single frame
        frame_token = start
    else:  # frame range
        frame_token = '[{}-{}]'.format(start, end)

    return frame_token

def generate_tokens(node):
    """Go gather all of the tokens into a dict."""

    import flame

    token_dict = {
        '<batch iteration>': flame.batch.current_iteration.name.get_value(),
        '<batch name>': flame.batch.name.get_value(),
        '<ext>': node.format_extension.get_value(),
        '<frame>': generate_frame_token(node),
        '<iteration>': flame.batch.current_iteration.name.get_value(),
        '<name>': node.name.get_value(),
        '<project>': flame.project.current_project.name,
        '<project nickname>': flame.project.current_project.nickname,
        '<shot name>': node.shot_name.get_value(),
    }

    return token_dict

def resolve_tokens(pattern, tokens):
    """Replace tokens with values."""

    resolved_pattern = pattern

    for token, value in tokens.items():
        resolved_pattern = resolved_pattern.replace(token, value)

    return resolved_pattern

def write_file_copy_path_old_school(selection):
    """Loop through selected Write File nodes, resolve the tokens, and append the path
    to a newline separated string of all paths.
    """

    import os

    message("{} v{}".format(__title__, __version__))
    message("Script called from {}".format(__file__))

    path_list = []

    for node in selection:

        path = node.media_path.get_value()
        pattern = complete_pattern(node.media_path_pattern.get_value())
        tokens = generate_tokens(node)

        pattern_resolved = resolve_tokens(pattern, tokens)

        full_path = os.path.join(path, pattern_resolved)
        path_list.append(full_path)

    # Shell output

    for item in path_list:
        message("Sending {} to clipboard.".format(item))

    # Send to clipboard

    paths = "\n".join(path_list)
    send_to_clipboard(paths)

    message("Done!")

def write_file_copy_path(selection):
    """Loop through selected Write File nodes, resolve the tokens, and append the path
    to a newline separated string of all paths.

    Starting on 2023.2, there is <PyWriteFileNode>.get_resolved_media_path()
    """

    import os

    message("{} v{}".format(__title__, __version__))
    message("Script called from {}".format(__file__))

    path_list = []

    for node in selection:

        full_path = node.get_resolved_media_path(show_extension = True)
        path_list.append(full_path)

    # Shell output

    for item in path_list:
        message("Sending {} to clipboard.".format(item))

    # Send to clipboard

    paths = "\n".join(path_list)
    send_to_clipboard(paths)

    message("Done!")

def scope_write_node(selection):
    import flame

    for node in selection:
        if node.type.get_value() == 'Write File':
            return True
    return False

def get_batch_custom_ui_actions():

    return [{'name': 'Copy...',
             'actions': [{'name': 'Write File Path to Clipboard',
                          'isVisible': scope_write_node,
                          'execute': write_file_copy_path_old_school,
                          'minimumVersion': '2021.1',
                          'maximumVersion': '2023.1'},
                         {'name': 'Write File Path to Clipboard',
                          'isVisible': scope_write_node,
                          'execute': write_file_copy_path,
                          'minimumVersion': '2023.2'}]}]
