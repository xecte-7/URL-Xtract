#!/usr/bin/env python3
# -*- encode: utf-8 -*-

try:
    import os, platform, datetime
    import argparse, requests, bs4, urllib3, colored
except:
    print("[-] Error: Fail importing one or more modules!")
    exit()

''' VARIABLE WARNA '''
	# for Style
cl_reset = colored.style.RESET
cl_bold = colored.attr("bold")
	# for Foreground
clfg_w = colored.fore.WHITE
clfg_r = colored.fore.LIGHT_RED
clfg_lg = colored.fore.LIGHT_GREEN
clfg_y = colored.fg(227)
	# for Background
cl_bg_white = colored.back.WHITE
cl_bg_red = colored.back.LIGHT_RED
cl_bg_lgreen = colored.back.LIGHT_GREEN
cl_bg_yellow = colored.bg(227)

''' ARGUMENTS '''
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="specify the url to start crawling", type=str)
parser.add_argument("--output", help="save result to txt file", type=str)
args = parser.parse_args()
''' CHECKUP '''
if args.url == None:
    print("[-] URL Error: Specify URL to start crawling!")
    exit()

tool_banner = """{0}{1}
  ▄• ▄▌▄▄▄  ▄▄▌        ▐▄• ▄ ▄▄▄▄▄▄▄▄   ▄▄▄·  ▄▄· ▄▄▄▄▄
  █▪██▌▀▄ █·██•  ▄▄▄▄▄  █▌█▌▪•██  ▀▄ █·▐█ ▀█ ▐█ ▌▪•██  
  █▌▐█▌▐▀▀▄ ██▪    ▪·   ·██·  ▐█.▪▐▀▀▄ ▄█▀▀█ ██ ▄▄ ▐█.▪
  ▐█▄█▌▐█•█▌▐█▌▐▌      ▪▐█·█▌ ▐█▌·▐█•█▌▐█ ▪▐▌▐███▌ ▐█▌·
   ▀▀▀ .▀  ▀.▀▀▀       •▀▀ ▀▀ ▀▀▀ .▀  ▀ ▀  ▀ ·▀▀▀  ▀▀▀
                 {2}(v1.0){1}
  Url scrapping tool coded by {3}Muhammad Rizky [Dr-3AM]{0}
""".format(cl_reset, clfg_w, clfg_y, clfg_r)

def tool_extract(url):
    ''' Disabling SSL Warning'''
    #ssl_cert = './cert/cacert.pem'
    #req_res = requests.get(url, verify=ssl_cert)
    urllib3.disable_warnings(urllib3.exceptions.SSLError)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ''' Getting page data '''
    try:
        req_res = requests.get(url, verify=False)
        body_parser = bs4.BeautifulSoup(req_res.text, 'html.parser')
    except requests.exceptions.ConnectionError:
        print("[-] Error: Connection timed out! Check your internet connection and try again..")
        exit()
    except KeyboardInterrupt:
        print("[-] Keyboard interrupt detected, quitting..")
        exit()
    ''' Managing all links '''
    urls = []
        # With HREF
    tag_a_links = body_parser.find_all('a')
    tag_area_links = body_parser.find_all('area')
    tag_base_links = body_parser.find_all('base')
    tag_link_links = body_parser.find_all('link')
        # With SRC
    tag_audio_links = body_parser.find_all('audio')
    tag_embed_links = body_parser.find_all('embed')
    tag_iframe_links = body_parser.find_all('iframe')
    tag_img_links = body_parser.find_all('img')
    tag_input_links = body_parser.find_all('input')
    tag_script_links = body_parser.find_all('script')
    tag_source_links = body_parser.find_all('source')
    tag_track_links = body_parser.find_all('track')
    tag_video_links = body_parser.find_all('video')
        # Combine
    all_with_href = tag_a_links + tag_area_links + tag_base_links + tag_link_links
    all_with_src = tag_audio_links + tag_embed_links + tag_iframe_links + tag_img_links + tag_input_links + tag_script_links + tag_source_links + tag_track_links + tag_video_links
    sterilize_urls = []
    ''' Separate href and src attribute tags '''
    for link in all_with_href:
        fix_link = link.get('href')
        if fix_link != None and fix_link[0] != '#' and fix_link[0:6] != 'mailto':
            if fix_link[0] == '/':
                fix_link = url + fix_link
            if fix_link not in sterilize_urls:
                sterilize_urls.append(fix_link)
            else:
                pass
    for link in all_with_src:
        fix_link = link.get('src')
        if fix_link != None and fix_link[0] != '#' and fix_link[0:6] != 'mailto':
            if fix_link[0] == '/':
                fix_link = url + fix_link
            if fix_link not in sterilize_urls:
                sterilize_urls.append(fix_link)
            else:
                pass
    ''' Sorting and output '''
    sterilize_urls.sort()
    print(f"[+] Found {len(sterilize_urls)} urls via {url} \n")
    ''' Final Movement '''
    if args.output != None and args.output != '':
        count = 1
        for url in sterilize_urls:
            print(f"[{count}] {url}")
            count += 1
        # Save File
        print("")
        filename = f"{args.output}.txt"
        open_file = open('./output/'+filename, 'w+')
        open_file.write(f"### RESULT FOR {url} ###\n")
        for url in sterilize_urls:
            open_file.write(f"{url} \n")
        open_file.close()
        print(f"[+] File saved as './output/{filename}'\n")
    else:
        psq = input("[>] Show on screen (P) / Save (S) / Quit (Q) : ")
        if psq in ['P','p','show','print']:
            count = 1
            for url in sterilize_urls:
                print(f"[{count}] {url}")
                count += 1
        elif psq in ['S', 's', 'save'] or psq == '':
            time = datetime.datetime.now()
            filename = f"{time.year}-{time.month}-{time.day}_{time.hour}-{time.minute}-{time.second}_{time.microsecond}.txt"
            open_file = open('./output/'+filename, 'a')
            open_file.write(f"### RESULT FOR {url} ###\n")
            for url in sterilize_urls:
                open_file.write(f"{url} \n")
            open_file.close()
            print(f"[+] File saved as './output/{filename}'\n")
        elif psq in ['Q', 'q']:
            exit()
    
def tool_main():
    #if platform.system() == "Windows":
    #    os.system('cls')
    #else:
    #    os.system('clear')
    print(tool_banner)
    tool_extract(args.url)

if __name__ == '__main__':
    tool_main()