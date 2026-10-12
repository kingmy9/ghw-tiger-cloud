import json, subprocess, sys
p = subprocess.Popen(["tiger","mcp","start"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
i=0
def rpc(method, params=None, notify=False):
    global i
    msg={"jsonrpc":"2.0","method":method}
    if params is not None: msg["params"]=params
    if not notify:
        i+=1; msg["id"]=i
    p.stdin.write(json.dumps(msg)+"\n"); p.stdin.flush()
    if notify: return None
    while True:
        line=p.stdout.readline()
        if not line: return None
        r=json.loads(line)
        if r.get("id")==i: return r
rpc("initialize",{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"hark-agent","version":"1.0"}})
rpc("notifications/initialized",notify=True)
cmd=sys.argv[1]
if cmd=="list":
    r=rpc("tools/list",{})
    for t in r["result"]["tools"]: print(t["name"], "-", t.get("description","")[:100].replace("\n"," "))
elif cmd=="schema":
    r=rpc("tools/list",{})
    for t in r["result"]["tools"]:
        if t["name"]==sys.argv[2]: print(json.dumps(t["inputSchema"],indent=1))
else:
    r=rpc("tools/call",{"name":cmd,"arguments":json.loads(sys.argv[2]) if len(sys.argv)>2 else {}})
    print(json.dumps(r.get("result",r),indent=1,ensure_ascii=False)[:4000])
p.terminate()
