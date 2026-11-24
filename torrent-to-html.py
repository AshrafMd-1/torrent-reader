import sys, os, json, hashlib

class B:
    def __init__(self, d): self.d=d; self.i=0
    def parse(self):
        c=self.d[self.i:self.i+1]
        if c==b'd': return self.dict()
        if c==b'l': return self.list()
        if c==b'i': return self.int()
        return self.str()
    def int(self):
        self.i+=1; j=self.d.index(b'e', self.i); n=int(self.d[self.i:j]); self.i=j+1; return n
    def str(self):
        j=self.d.index(b':', self.i); n=int(self.d[self.i:j]); s=self.d[j+1:j+1+n]; self.i=j+1+n; return s
    def list(self):
        self.i+=1; out=[]
        while self.d[self.i:self.i+1]!=b'e': out.append(self.parse())
        self.i+=1; return out
    def dict(self):
        self.i+=1; out={}
        while self.d[self.i:self.i+1]!=b'e':
            k=self.str(); out[k]=self.parse()
        self.i+=1; return out

def s(x):
    if isinstance(x, bytes):
        for e in ('utf-8','cp1252'):
            try: return x.decode(e)
            except Exception: pass
        return x.decode('latin-1','replace')
    if isinstance(x, list): return [s(y) for y in x]
    return x

path = sys.argv[1]
out  = sys.argv[2]
raw = open(path,'rb').read()
t = B(raw).parse()
info = t[b'info']

# infohash = sha1 of the bencoded info dict (v1)
i0 = raw.index(b'4:infod') + 6
probe = B(raw); probe.i = i0; probe.parse()
infohash = hashlib.sha1(raw[i0:probe.i]).hexdigest()

trackers = []
seen = set()
def add(tr):
    tr = s(tr).strip()
    if tr and tr not in seen:
        seen.add(tr); trackers.append(tr)
for tr in t.get(b'announce-list', []):
    for x in tr: add(x)
if b'announce' in t: add(t[b'announce'])

files = []
if b'files' in info:
    for f in info[b'files']:
        files.append([s(p) for p in f[b'path']] + [f[b'length']])
else:
    files.append([s(info[b'name']), info[b'length']])

data = {
    "name": s(info[b'name']),
    "infohash": infohash,
    "totalSize": sum(f[-1] for f in files),
    "pieceLength": info.get(b'piece length', 0),
    "pieceCount": len(info.get(b'pieces', b'')) // 20,
    "private": bool(info.get(b'private', 0)),
    "createdBy": s(t.get(b'created by', b'')),
    "creationDate": t.get(b'creation date', 0),
    "comment": s(t.get(b'comment', b'')),
    "trackers": trackers,
    "files": [[f[:-1], f[-1]] for f in files],
}

tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html')).read()
html = tpl.replace('/*__DATA__*/null', json.dumps(data, separators=(',',':'), ensure_ascii=False))
with open(out, 'w', encoding='utf-8') as fh:
    fh.write(html)
print("wrote", out, len(html), "bytes")
