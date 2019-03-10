from time import sleep
from urllib.parse import urlparse
import uiautomation as automation

def getCurrentApplication():
    # Getting Chrome Tab code copied with minor modification from stack overflow:
    # https://stackoverflow.com/questions/11645123/how-do-i-get-the-url-of-the-active-google-chrome-tab-in-windows
    # Thanks @proggeo(https://stackoverflow.com/users/7594271/proggeo)
    control = automation.GetForegroundControl()
    # If the current window is chromium based
    if(control.ClassName == "Chrome_WidgetWin_1"):
        address_control = automation.FindControl(control, lambda c, d: isinstance(c, automation.EditControl) and "Address and search bar" in c.Name)
        # Yeah its Google Chrome
        if(address_control):
            url = address_control.CurrentValue()
            domain = urlparse(url).netloc
            # We are on youtube
            if(domain == "www.youtube.com"):
                yt_control = automation.FindControl(control, lambda c, d: isinstance(c, automation.TabItemControl) and "- YouTube" in c.Name)
                # Probably on a video
                if(yt_control):
                    video_name = yt_control.Name[:-10]
                    return "YouTube - " + video_name
                # Might not be on a video
                else:
                    # Nevermind actually in a video
                    if("/watch?v=" in url):
                        return "YouTube - Unknown Video"
                    # Probably on the youtube homepage or something
                    else:
                        return "YouTube"
            else:
                return domain
        # Not Google Chrome
        else:
            if("— Atom" in control.Name):
                return "Atom"
            elif("Slack -" in control.Name):
                return "Slack"
            elif("- Discord" in control.Name):
                return "Discord"
            else:
                return control.Name
    # Other type of chromium based app
    elif(control.ClassName == "Chrome_WidgetWin_0"):
        spotify_test = automation.FindControl(control, lambda c, d: isinstance(c, automation.DocumentControl) and "Spotify" in c.Name)
        # Spotify
        if(spotify_test):
            return "Spotify"
        else:
            return control.Name
    # Not a chromium based window
    else:
        if(control.ClassName == "CabinetWClass"):
            file_exp_test = automation.FindControl(control, lambda c, d: isinstance(c, automation.TreeItemControl) and "OneDrive" in c.Name)
            if(file_exp_test and "This PC" in file_exp_test.GetNextSiblingControl().Name):
                return "File Explorer"
            else:
                return control.Name
        # Probably Native Microsoft Application
        elif(control.ClassName == "ApplicationFrameWindow"):
            enc_name = control.Name.encode("utf-8")
            if(b"- Mail" in enc_name):
                return "Mail"
            if(b"Microsoft Store" in enc_name):
                return "Microsoft Store"
            # Don't know what it is
            else:
                return str(enc_name)[2:-1]
        elif(control.ClassName == "vguiPopupWindow"):
            return control.Name
        else:
            if("- paint.net" in control.Name):
                return "Paint.net"
            else:
                return control.ClassName

if __name__ == '__main__':
    sleep(3)
    print(getCurrentApplication())
