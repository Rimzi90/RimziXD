#!/usr/bin/env python3
try:
    import requests, json, time, os, sys, urllib.parse
    from rich.console import Console
    from bs4 import BeautifulSoup
    from rich.panel import Panel
    from rich import print as printf
    from requests.exceptions import RequestException
except (ModuleNotFoundError) as e:
    __import__('sys').exit(f"Error: {str(e).capitalize()}!")

LOOPING, STOP, GROUPS = 0, False, []

class MAIN:

    def __init__(self):
        global STOP, LOOPING
        try:
            self.BANNER()
            printf(Panel(f"[bold white]Please fill in the name of the group you want to search for. You can use[bold red] commas[bold white] to search for\nmultiple groups. Example: [bold green]Termux, Kali Linux", width=59, style="bold orange4", title="[bold orange4][ Question ]", subtitle="[bold orange4]╭───────", subtitle_align="left"))
            self.QUERY = Console().input("[bold orange4]   ╰─> ")
            if len(self.QUERY) != 0:
                printf(Panel(f"[bold white]Searching for WhatsApp groups. Use[bold green] CTRL + C[bold white] to stop the search.\nDo not use[bold red] CTRL + Z[bold white]!", width=59, style="bold orange4", title="[bold orange4][ Note ]"))
                for NAME in self.QUERY.split(','):
                    try:
                        printf(f"[bold orange4]   ──>[bold white] SEARCHING[bold green] {str(NAME)[:30].upper()}[bold white] GROUP...   ", end='\r')
                        time.sleep(3.0)
                        while (bool(STOP) != True):
                            try:
                                self.SEARCH_GROUPS(query=NAME)
                            except (RequestException):
                                printf(f"[bold orange4]   ──>[bold yellow] NETWORK ERROR!          ", end='\r')
                                time.sleep(5.0)
                                continue
                            except (Exception) as e:
                                printf(f"[bold orange4]   ──>[bold red] {str(e).upper()}!", end='\r')
                                time.sleep(5.0)
                                continue
                        LOOPING = 0
                        STOP = False
                        continue
                    except (KeyboardInterrupt):
                        printf(f"[bold orange4]   ──>[bold yellow] SEARCH CANCELED!          ", end='\r')
                        time.sleep(2.0)
                        break
                if len(GROUPS) != 0:
                    self.FILE_NAME = (f'Temporary/{str(NAME).replace(" ", "").capitalize()}_{int(time.time())}.json')
                    with open(self.FILE_NAME, 'w', encoding='utf-8') as W:
                        json.dump(GROUPS, W, ensure_ascii=False, indent=4)
                    W.close()
                    printf(Panel(f"[bold white]Search completed. Found[bold red] {len(GROUPS)}[bold white] groups.\nSaved in:[bold green] {self.FILE_NAME}", width=59, style="bold orange4", title="[bold orange4][ Done ]"))
                    sys.exit()
                else:
                    printf(Panel(f"[bold red]No groups found with that name. Try another search term!", width=59, style="bold orange4", title="[bold orange4][ Not Found ]"))
                    sys.exit()
            else:
                printf(Panel(f"[bold red]Group name cannot be empty!", width=59, style="bold orange4", title="[bold orange4][ Empty Input ]"))
                sys.exit()
        except (Exception) as e:
            printf(Panel(f"[bold red]{str(e).capitalize()}!", width=59, style="bold orange4", title="[bold orange4][ Error ]"))
            sys.exit()

    def SEARCH_GROUPS(self, query):
        global LOOPING, STOP, GROUPS
        with requests.Session() as session:
            data = {
                "group_no": "{}".format(int(LOOPING)),
                "search": True,
                "keyword": "{}".format(query),
            }
            session.headers.update({
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Referer": "https://groupda1.link/add/group/search",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html, */*; q=0.01",
                "Content-Length": "{}".format(len(urllib.parse.urlencode(data))),
                "Host": "groupda1.link",
                "Origin": "https://groupda1.link",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/127.0.0.0 Safari/537.36",
            })
            response = session.post("https://groupda1.link/add/group/loadresult", data=data)
            if response.status_code != 200 or len(response.text) == 0:
                printf(f"[bold orange4]   ──>[bold red] NO CURSOR FOUND!             ", end='\r')
                time.sleep(3.0)
                STOP = True
                return
            else:
                self.SOUP = BeautifulSoup(response.text, 'html.parser')

                for self.MAINDIV in self.SOUP.find_all('div', class_='maindiv'):
                    self.MAINDIV_TAG = self.MAINDIV.find('a', href=True)
                    self.LINK = self.MAINDIV_TAG['href']
                    self.TITLE = self.MAINDIV_TAG['title']

                    self.MAINDIV_DESCRIPTION_TAG = self.MAINDIV.find('p', class_='descri')
                    self.DESCRIPTION = self.MAINDIV_DESCRIPTION_TAG.get_text(strip=True) if self.MAINDIV_DESCRIPTION_TAG else 'No description available'
                    self.GROUP_ID = self.LINK.split('/')[-1]
                    self.GROUP_NAME = self.TITLE.replace('Whatsapp group invite link: ', '')
                    self.GROUP_LINK = f"https://chat.whatsapp.com/{self.GROUP_ID}"

                    if str(self.GROUP_ID) not in GROUPS:
                        printf(Panel(f"""[bold white]Group Name :[bold green] {self.GROUP_NAME}
[bold white]ID         :[bold red] {self.GROUP_ID}
[bold white]Link       :[bold red] {self.GROUP_LINK}
[bold white]Description:[bold green] {self.DESCRIPTION}""", width=59, style="bold orange4", title="[bold orange4][ Success ]"))

                        GROUPS.append({
                            'Link': f'{self.GROUP_LINK}',
                            'Name': f"{self.GROUP_NAME}",
                            'Code': f"{self.GROUP_ID}",
                            'Description': f"{self.DESCRIPTION}"
                        })
                        printf(f"[bold orange4]   ──>[bold white] Collected[bold green] {str(self.GROUP_ID)[:15]}[bold white]/[bold red]{len(GROUPS)}[bold white]/[bold green]{LOOPING}[bold white] Group!   ", end='\r')
                        time.sleep(0.007)
                    else:
                        continue

                LOOPING += 1
                return

    def BANNER(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        printf(Panel(r"""[bold red]● [bold yellow]● [bold green]●[/]
[bold red] __      __.__            __          ____ ___         
/  \    /  \  |__ _____ _/  |_  _____|    |   \______  
\   \/\/   /  |  \\__  \\   __\/  ___/    |   /\____ \ 
 \        /|   Y  \/ __ \|  |  \___ \|    |  / |  |_> >
[bold white]  \__/\  / |___|  (____  /__| /____  >______/  |   __/ 
       \/       \/     \/          \/          |__|    
       [underline green]WhatsApp Group Finder - Coded by RIMZI""", width=59, style="bold orange4"))
        return

if __name__ == '__main__':
    try:
        os.system('git pull')
        MAIN()
    except (Exception) as e:
        printf(Panel(f"[bold red]{str(e).capitalize()}!", width=59, style="bold orange4", title="[bold orange4][ Error ]"))
        sys.exit()
    except (KeyboardInterrupt):
        sys.exit()
