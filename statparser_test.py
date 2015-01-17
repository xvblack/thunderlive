from statparser import *

parser = NginxRtmpStatParser("121.201.15.193/stat")
parser.update_stat()
streams = parser.stat.application(app_name="live").streams()
print find_one_by_name(streams, "akarin")