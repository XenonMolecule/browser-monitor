from time import sleep
import uiautomation as automation

if __name__ == '__main__':
    sleep(3)
    # Getting Chrome Tab code copied with minor modification from stack overflow:
    # https://stackoverflow.com/questions/11645123/how-do-i-get-the-url-of-the-active-google-chrome-tab-in-windows
    # Thanks @proggeo(https://stackoverflow.com/users/7594271/proggeo)
    control = automation.GetFocusedControl()
    controlList = []
    while control:
        controlList.insert(0, control)
        control = control.GetParentControl()
    if len(controlList) == 1:
        control = controlList[0]
    else:
        control = controlList[1]
    # If the current window is chrome
    if(control.ClassName == "Chrome_WidgetWin_1"):
        address_control = automation.FindControl(control, lambda c, d: isinstance(c, automation.EditControl) and "Address and search bar" in c.Name)
        print(address_control.CurrentValue())
    else:
        print(control.ClassName)
