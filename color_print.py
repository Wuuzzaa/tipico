
"""
Enable colored print messages on the terminal.

Ensure to add "ResetAll" (ResetAll = "\033[0m") at the end of every printmethod. Otherwise all following print calls
will have the same configs.

From: https://godoc.org/github.com/whitedevops/colors
"""
ResetAll = "\033[0m"

Bold       = "\033[1m"
Dim        = "\033[2m"
Underlined = "\033[4m"
Blink      = "\033[5m"
Reverse    = "\033[7m"
Hidden     = "\033[8m"

ResetBold       = "\033[21m"
ResetDim        = "\033[22m"
ResetUnderlined = "\033[24m"
ResetBlink      = "\033[25m"
ResetReverse    = "\033[27m"
ResetHidden     = "\033[28m"

Default      = "\033[39m"
Black        = "\033[30m"
Red          = "\033[31m"
Green        = "\033[32m"
Yellow       = "\033[33m"
Blue         = "\033[34m"
Magenta      = "\033[35m"
Cyan         = "\033[36m"
LightGray    = "\033[37m"
DarkGray     = "\033[90m"
LightRed     = "\033[91m"
LightGreen   = "\033[92m"
LightYellow  = "\033[93m"
LightBlue    = "\033[94m"
LightMagenta = "\033[95m"
LightCyan    = "\033[96m"
White        = "\033[97m"

BackgroundDefault      = "\033[49m"
BackgroundBlack        = "\033[40m"
BackgroundRed          = "\033[41m"
BackgroundGreen        = "\033[42m"
BackgroundYellow       = "\033[43m"
BackgroundBlue         = "\033[44m"
BackgroundMagenta      = "\033[45m"
BackgroundCyan         = "\033[46m"
BackgroundLightGray    = "\033[47m"
BackgroundDarkGray     = "\033[100m"
BackgroundLightRed     = "\033[101m"
BackgroundLightGreen   = "\033[102m"
BackgroundLightYellow  = "\033[103m"
BackgroundLightBlue    = "\033[104m"
BackgroundLightMagenta = "\033[105m"
BackgroundLightCyan    = "\033[106m"
BackgroundWhite        = "\033[107m"


def print_red(text):
    print(f"{Red}{text} {ResetAll}")


if __name__ == "__main__":
    print_red("some text in red")
    print("nicht mehr rot")