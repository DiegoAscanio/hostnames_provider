import sys, getopt, csv
import django

def feed(file_name):
    django.setup()
    from hostnames.models import Host
    with open(file_name, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        for h,m,i in spamreader:
            #print(hostname,mac_address,ip_address)
            h = Host(hostname=h,mac_address=m,ip_address=i)
            h.save()
            

feed(sys.argv[1]) if __name__ == "__main__" and len(sys.argv) == 2 else print('Usage: python feeder.py <csv_file>')
