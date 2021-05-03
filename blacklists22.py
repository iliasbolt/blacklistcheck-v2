import os
import dns.resolver
import dns
import xlsxwriter
import webbrowser
from datetime import date
import multiprocessing

#git clone https://github.com/jmcnamara/XlsxWriter.git

def ips_count():
  try:
    c = open('ips.txt','r')
    tt = c.readlines()
    bb = list()
    counter = 0
    if tt == "":
      print("Please enter the ips :")
      exit()
      c.close()
    for ip in tt:
      counter = counter + 1

    return counter,tt
  except Exception:
    print('error in ips_count function')
    import sys
    print(sys.exc_info()[0])
    import traceback
    print(traceback.format_exc())
  

def checker(ip):
    bls = ["b.barracudacentral.org", 
    "bl.spamcop.net", 
    "zen.spamhaus.org"]
    blacklisted = []
    spm_type = ""
    #print('inside checker')
    #print(ip)
    for bl in bls:
        try: 
            my_resolver = dns.resolver.Resolver()
            my_resolver.timeout = 20
            my_resolver.lifetime = 240

            query = '.'.join(reversed(str(ip).split("."))) + "." + bl
            dd = query.replace('\n','')
            query = dd
            #print('->>>> '+query)
            reader = ""
            if bl == "zen.spamhaus.org":
                        ##open terminale and check for spamhause cheet
                stream = os.popen("nslookup "+query)
                reader = stream.read()
                
                        #print("ping "+query)
                        #print('#####')
                        #print(reader)
                spm_type = ""
                if reader.find('127.0.0.2') != -1:
                    spm_type = "SBL"
                if reader.find('127.0.0.3') != -1:
                    spm_type = "SBL && CSS"
                if reader.find('127.0.0.4') != -1:
                    spm_type = "XBL"
                if reader.find('127.0.0.9') != -1:
                    spm_type = "SBL DROP/EDROP"
                if reader.find('127.0.0.10') != -1:
                    spm_type = "PBL -> ISP Maintained"
                if reader.find('127.0.0.11') != -1:
                    spm_type = "PBL -> Spamhaus Maintained"
            #print(spm_type)
                

            answer = my_resolver.query(query, "A")
            answer_txt = my_resolver.query(query, "TXT")
            
            
            #register output
            print(f"\t\there {bl} -> {ip}")
            blacklisted.append(f"{ip}&{bl}&{spm_type}")
            spm_type = ""
            #r.write(f"{bl}")
            
        
            
        except dns.exception.Timeout:
            print("TimedOut ")
            continue 
        except dns.resolver.NXDOMAIN:
                print("nXDOMAIN  --- >  that need to check OUT !!!!")
        except dns.name.EmptyLabel:
                print("EMPTYLABEL") 
        except dns.resolver.NoNameservers:
            print ('not listed ...')
        except dns.resolver.NoAnswer:
            print ('not listed ...')

    return blacklisted


def proccessing():

    print('ilias.balhi@gmail.com & https://github.com/iliasbolt & V1.1 2021')
    print('#############- - START - -################')
    my_email = "balhi.ilias@yandex.com"
    phone_number = "+73647236234"
    msg = "sdhfjshdbcvjsdbsd"

    bls = ["b.barracudacentral.org", 
    "bl.spamcop.net", 
    "zen.spamhaus.org"]
    try:
      f = open('ips.txt','r')
      ips = f.readlines()
      if ips == "":
        print("Please enter the ips :")
        exit()

      r = open("blacklist_log.txt","a")
    except Exception:
      import sys
      print(sys.exc_info()[0])
      import traceback
      print(traceback.format_exc())

    blacklisted = []
    #cnttt = int(ips_count()[0])
    ############################## IPS &&& The  ormal code 
    #for ip in ips:
    #('----- > '+ips)
    #les_IP = []
    with multiprocessing.Pool(processes=10) as pool:
        result = pool.map(checker,ips,)
        blacklisted = result
            #print(checker(ip))
    ### spamhause 
    #input('hhh2222')
    
    r.write('\n')
    r.write('\t'+str(date.today()))
    r.write('\n\n')
    for n in blacklisted:
      r.write(str(n))
      r.write('\n')
    r.close()
    print("end of procesing start of EXCEl :) !")
    for n in blacklisted:
        print("-- > "+str(n))
        print("\n")
    #print(blacklisted)

    workbook = xlsxwriter.Workbook('checkBlacklistPy.xlsx')
    worksheet = workbook.add_worksheet()
    c=1
    ok = []
    for i in blacklisted:
      x = str(i).split('&')
      print(x)
      #print(x[0])
      #print(x[1])
      #print(x[2])
      #print(x[3])
      worksheet.write('A'+str(c),x[0])
      worksheet.write('B'+str(c),x[1])
      worksheet.write('C'+str(c),x[2])
      ff = x[1]
      if str(ff).find('spamhaus') != -1:
        worksheet.write_url('D'+str(c),'https://www.spamhaus.org/query/ip/'+i[0],tip="Delisting")
        webbrowser.open_new_tab('https://www.spamhaus.org/query/ip/'+i[0])
      if str(ff).find('barracudacentral') != -1:
        worksheet.write_url('D'+str(c),'https://anonym.to/?http://www.barracudacentral.org/rbl/removal-request/'+i[0]+'&address='+i[0]+'\&email='+my_email+'&phone='+phone_number+'&ir_code=&submit=submit+request',tip="Delisting")
        webbrowser.open_new_tab('https://anonym.to/?http://www.barracudacentral.org/rbl/removal-request/'+i[0]+'&address='+i[0]+'\&email='+my_email+'&phone='+phone_number+'&ir_code=&submit=submit+request')
      c = c+1
      #print(i[0]+''+i[1]+''+i[2] )"""
      

    workbook.close()
      



if __name__ == "__main__":
  try:
    cnt = ips_count()[0]
    data = ips_count()[1]
    proccessing()
  except Exception:
    print('error in processing function')
    import sys
    print(sys.exc_info()[0])
    import traceback
    print(traceback.format_exc())
  finally:
    import sys
    print("\n\n\n")
    print('ilias.balhi@gmail.com & https://github.com/iliasbolt & V1.1 2021')
    print("\n\n\n")
    print('##### ----- DONE -------- ####')
    print(sys.exc_info()[0])
    import traceback
    print(traceback.format_exc())
