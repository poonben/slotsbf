from random import choice, shuffle


# ---------------------------------------------------------------------------- #
def pick_status():
    status_options = [
        "https://www.facebook.com/jharriswebdev #freelance #webdev #100DaysOfCode #techjobs",
         "If you were a triangle you'd be acute one.",
        "eBay is so useless. I tried to look up lighters and all they had was 13,749 matches.",
        "(┛ಠ_ಠ)┛彡┻━┻",
        "Check out my creator's portfolio here: jharriswebdev.com #freelance #webdeveloper #coding #100DaysOfCode",
        "My creator is kind of funny, too. Check him out: @jheeeeezy #bot",
        "@jheeeeezy is the one that created me! Check him out!",
        "Follow me here too:  https://www.facebook.com/jharriswebdev !!! #freelance #webdev #100DaysOfCode #techjobs",
        "Beep boop boop bmmmmmmmmm *~*laser sounds*~* beep",
        "Best bot in the biz, baby! #bot #webdev #coding #python",
        "*- Does robot dance to future music -*",
        "Share a meme with me!",
        "Go like: https://www.facebook.com/jharriswebdev #freelance #webdev #100DaysOfCode #techjobs",
        "これは英語ではありません！",
        "@jheeeeezy can create a bot for you, too! #bot #freelance #hitmeup #work",
        "jharriswebdev.com #freelance #webdev",
        "Go like the Facebook Page: https://www.facebook.com/jharriswebdev !!! #freelance #webdev #100DaysOfCode #techjobs"
    ]
    shuffle(status_options)
    return choice(status_options)


# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    pick_status()