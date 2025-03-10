# Test if the shutdown method actuall shuts down the clamd process
# and makes the container stop

import clamd

from io import BytesIO

cd = clamd.ClamdNetworkSocket()
print(cd.ping())
print(cd.version())

with open('freskdesk_tickets_2019.csv', "rb") as fh:
  buf = BytesIO(fh.read())
  scan_result = cd.instream(buf)
  print(scan_result)

print(cd.stats())
cd.shutdown()

