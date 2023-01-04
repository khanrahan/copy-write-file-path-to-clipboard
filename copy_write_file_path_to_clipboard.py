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
__version_info__ = (0,1,0)
__version__ = ".".join([str(num) for num in __version_info__])

MESSAGE_PREFIX = "[PYTHONHOOK]"

def message(string):
    """ """

    print(" ".join([MESSAGE_PREFIX, string]))

def send_to_clipboard(str_data):
    """Takes data in the form of a string and send it the system clipboard."""

    from PySide2 import QtWidgets

    qt_app_instance = QtWidgets.QApplication.instance()
    qt_app_instance.clipboard().setText(str_data)

def batch_write_file_copy_path(selection):
    """
    Until 2023.2, will not be able to get full resolved path.  Only the root path before
    the use of tokens.
    """

    message("{} v{}".format(__title__, __version__))
    message("Script called from {}".format(__file__))

    path_list = [node.media_path.get_value() for node in selection]

    # Convert path list to string with new line

    paths = "\n".join(path_list)

    # Add clips to clipboard

    for item in path_list:
        message("Sending {} to clipboard.".format(item))

    send_to_clipboard(paths)

    message("Done!")

def scope_write_node(selection):
    import flame

    for node in selection:
        if isinstance(node,flame.PyNode):
            if hasattr(node, 'media_path'):
                return True
    return False

def get_batch_custom_ui_actions():

    return [{'name': 'Copy...',
             'actions': [{ 'name': 'Write File Path to Clipboard',
                           'isVisible': scope_write_node,
                           'execute': batch_write_file_copy_path,
                           'minimumVersion': '2021.1'}]}]
