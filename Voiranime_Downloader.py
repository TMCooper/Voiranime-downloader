# installer un proxy via Yui pour eviter que le captcha repères les activité de haute fréquences et facilité la resolution de celle ci

from function.__init__ import *

def main():
    original_url = "https://v5.voiranime.com/anime/komi-san-wa-komyushou-desu/komi-san-wa-komyushou-desu-01-vostfr/"

    # Yui.requesting_anime(original_url)
    Thoru.captcha(original_url)

if __name__ == "__main__":
    main()