from statparser import *

parser = NginxRtmpStatParser("121.201.15.193/stat")
parser.update_stat()
streams = parser.stat.application(app_name="live").streams()
print streams[0]