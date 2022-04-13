#!/usr/env python3
# -*- encoding: utf-8 -*-


''' Importing Modules '''
import os, platform, time
import requests, bs4, urllib3, colored


''' Coloring '''
	# for Style
cl_reset = colored.style.RESET
cl_bold = colored.attr("bold")
	# for Foreground
clfg_w = colored.fore.WHITE
clfg_r = colored.fore.LIGHT_RED
clfg_lg = colored.fore.LIGHT_GREEN
clfg_y = colored.fg(227)
clfg_b = colored.fore.BLUE
	# for Background
cl_bg_white = colored.back.WHITE
cl_bg_red = colored.back.LIGHT_RED
cl_bg_lgreen = colored.back.LIGHT_GREEN
cl_bg_yellow = colored.bg(227)
''' SETUP VARIABLE '''
sign_info = "{0}[{1}i{0}]".format(clfg_w,clfg_b)
sign_plus = "{0}[{1}+{0}]".format(clfg_w,clfg_lg)
sign_minus = "{0}[{1}-{0}]".format(clfg_w,clfg_r)
sign_proc = "{0}[*]".format(clfg_w)
sign_warn = "{0}[{1}!{0}]".format(clfg_w,clfg_r)
sign_input = "{0}[{1}>{0}]".format(clfg_w,clfg_y)


''' Banner '''
banner = '''{0}{1}
 ██╗   ██╗██████╗ ██╗     ██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗
 ██║   ██║██╔══██╗██║     ╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
 ██║   ██║██████╔╝██║█████╗╚███╔╝    ██║   ██████╔╝███████║██║        ██║   
 ██║   ██║██╔══██╗██║╚════╝██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   
 ╚██████╔╝██║  ██║███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   
  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝
 Coded by {2}Muhammad Rizky{1} [{2}XECTE-7{1}]
 version {2}1.1{1}

 URL-Xtract : Scrapping tool for extracting URL in a webpage
'''.format(cl_reset, clfg_w, clfg_r)


''' Clear Screen Function '''
def clr_scr():
	if platform.system() == 'Windows':
		os.system('cls')
	else:
		os.system('clear')


def utama():
	clr_scr()
	print(banner)
	# Getting Target URL
	try:
		target_url = str(input(f"{sign_input} Target URL : {clfg_lg}"))
		if target_url == '' or target_url == None:
			print(f"{sign_warn} Please specify Target URL")
			input(f"{clfg_w}[{clfg_y}Press ENTER to continue ...{clfg_w}]\n")
			utama()
		if 'http://' not in target_url and 'https://' not in target_url:
			print(f"{sign_warn} Please specify http:// or https://")
			input(f"{clfg_w}[{clfg_y}Press ENTER to continue ...{clfg_w}]\n")
			utama()
	except KeyboardInterrupt:
		print()
		exit()
	# Checking Page HTTP Response
	print(f"{sign_proc} Checking page response..")
	try:
		http_resp = requests.get(target_url)
		if http_resp.status_code == 200:
			print(f"{sign_plus} Continue -> Page response is [{int(http_resp.status_code)}]")
		else:
			print(f"{sign_warn} Error -> Page response is [{int(http_resp.status_code)}]")
			input(f"{clfg_w}[{clfg_y}Press ENTER to continue ...{clfg_w}]\n")
			utama()
	except:
		print(f"{sign_warn} Error when sending request")
		input(f"{clfg_w}[{clfg_y}Press ENTER to continue ...{clfg_w}]\n")
		utama()
	# Disabling SSL Waring
	#ssl_cert = './cert/cacert.pem'
	#req_res = requests.get(url, verify=ssl_cert)
	urllib3.disable_warnings(urllib3.exceptions.SSLError)
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	# Getting Page Data
	try:
		req_res = requests.get(target_url, verify=False)
		body_parser = bs4.BeautifulSoup(req_res.text, 'html.parser')
	except requests.exceptions.ConnectionError:
		print(f"{sign_warn} Connection timed out! Check your internet connection and try again..")
		input(f"{clfg_w}[{clfg_y}Press ENTER to continue ...{clfg_w}]\n")
		exit()
	except KeyboardInterrupt:
		print("{sign_warn} Keyboard interrupt detected, quitting..\n")
		print()
		exit()
	# Getting All Links Detected
	urls = []
		# Using HREF
	tag_a_links = body_parser.find_all('a')
	tag_area_links = body_parser.find_all('area')
	tag_base_links = body_parser.find_all('base')
	tag_link_links = body_parser.find_all('link')
		# Using SRC
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
	sterilized_urls = []
	# Separate HREF and SRC attribute tags
	for link in all_with_href:
		fix_link = link.get('href')
		if fix_link != None and fix_link[0] != '#' and fix_link[0:6] != 'mailto':
			if fix_link[0] == '/':
				fix_link = target_url + fix_link
			if fix_link not in sterilized_urls:
				sterilized_urls.append(fix_link)
			else:
				pass
	for link in all_with_src:
		fix_link = link.get('src')
		if fix_link != None and fix_link[0] != '#' and fix_link[0:6] != 'mailto':
			if fix_link[0] == '/':
				fix_link = target_url + fix_link
			if fix_link not in sterilized_urls:
				sterilized_urls.append(fix_link)
			else:
				pass
	# Sorting the List
	sterilized_urls.sort()
	print(f"{sign_plus} Found {len(sterilized_urls)} urls via {target_url}")
	print()
	# Asking for Show or Save
	try:
		print(f"{sign_input} (P) Print output // (S) Save output // (B) Both")
		final_option = str(input(f" ╰┈> {clfg_lg}"))
		if final_option.lower() == "p":
			for url in sterilized_urls:
				print(url)
		elif final_option.lower() == "s":
			filename = f"./saved/{target_url.split('/')[2]}-{time.strftime('%Y%m%d-%H%M%S')}.txt"
			buka_file = open(filename, 'a')
			for url in sterilized_urls:
				buka_file.write(f"{url.strip()}\n")
			buka_file.close()
			print(f"{sign_plusn} File saved to : {filename}")
		elif final_option.lower() == "b":
			filename = f"./saved/{target_url.split('/')[2]}-{time.strftime('%Y%m%d-%H%M%S')}.txt"
			buka_file = open(filename, 'a')
			for url in sterilized_urls:
				buka_file.write(f"{url.strip()}\n")
				print(url.strip())
			buka_file.close()
			print(f"{sign_plusn} File saved to : {filename}")
		else:
			print("[!] Invalid option. Saving file instead..")
			filename = f"./saved/{target_url.split('/')[2]}-{time.strftime('%Y%m%d-%H%M%S')}.txt"
			buka_file = open(filename, 'a')
			for url in sterilized_urls:
				buka_file.write(f"{url.strip()}\n")
			buka_file.close()
			print(f"{sign_plusn} File saved to : {filename}")
		print()
		input(f"{clfg_w}[{clfg_y}Press ENTER to continue ...{clfg_w}]\n")
		utama()
	except KeyboardInterrupt:
		print()
		exit()


if __name__ == '__main__':
	utama()
