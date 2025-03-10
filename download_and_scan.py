import os
import time
import clamd
from io import BytesIO

host = os.environ['CLAMAV_HOST'] if 'CLAMAV_HOST' in os.environ else '127.0.0.1'
port = os.environ['CLAMAV_PORT'] if 'CLAMAV_PORT' in os.environ else 3310

print(f'{host}:{port}')

cd = clamd.ClamdNetworkSocket(host, port)

# waiting for clamav container to get ready
while True:
  try:
    response = cd.ping()
    if response == 'PONG':
      break
    else:
      print('waiting for clamd to be ready')
    time.sleep(1)
  except Exception as e:
    print(e)

try:
  with open('download_and_scan.py', "rb") as fh:
    print('scanning file...')
    buf = BytesIO(fh.read())
    scan_result = cd.instream(buf)
    print(scan_result)
finally:
  cd.shutdown()

