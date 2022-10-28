import subprocess

out, err = subprocess.Popen("novelsave info 123",
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE).communicate()

try:
    out_out = out.decode('cp1252')
    err_out = err.decode('cp1252')
except UnicodeDecodeError:
    out_out = out.decode("utf-8")
    err_out = err.decode("utf-8")

print(out_out)
print(err_out)
