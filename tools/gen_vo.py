import re, json, hashlib, os, subprocess, numpy as np, soundfile as sf, warnings, random
warnings.filterwarnings('ignore')
from scipy.signal import fftconvolve, butter, sosfilt, resample_poly
from kk import synth, voice
src=open('/home/claude/book/index.html').read()
lines=set()
role={'dd':'dd','mm':'mm','s1':'sh','s3':'sh'}
for m in re.finditer(r"R\.say\((dd|mm|s1|s3),'([^']*)'(,\{[^}]*\})?\)",src):
    if m.group(3) and 'sfx' in m.group(3): continue
    lines.add((role[m.group(1)],m.group(2)))
for m in re.finditer(r"R\.narr\('([^']*)'",src): lines.add(('n',m.group(1)))
mono=re.search(r"const MONO=\[(.*?)\];",src).group(1)
for t in re.findall(r"'([^']*)'",mono): lines.add(('ddt',t))
poke=re.search(r"const POKE=\{(.*?)\};",src).group(1)
for who,arr in re.findall(r"'(豆豆|毛毛|小羊)':\[(.*?)\]",poke):
    for t in re.findall(r"'([^']*)'",arr): lines.add(({'豆豆':'dd','毛毛':'mm','小羊':'sh'}[who],t))
lines=sorted(lines)
print(len(lines),'lines')
# voice casting: (kokoro voice, speed, pitch factor, gain, reverb wet, lowpass)
CAST={'n':('zf_xiaoxiao',.92,1.0,1.0,.07,None),'dd':('zm_yunxia',.96,1.07,1.0,.05,None),
      'ddt':('zm_yunxia',.84,1.05,.78,.16,5200),'mm':('zf_xiaoyi',1.0,1.1,1.0,.05,None),'sh':('zf_xiaoyi',1.06,1.2,.95,.05,None)}
SR=24000
rng=np.random.default_rng(7)
ir=rng.standard_normal(int(SR*.45))*np.exp(-np.linspace(0,7,int(SR*.45)));ir/=np.abs(ir).sum()/6
def clean(t):
    t=t.replace('「','').replace('」','').replace('——','，').replace('—','，').replace('～','。').replace('（梦话）','')
    t=re.sub(r'^…+','',t);t=t.replace('……','，')
    return t.strip('，') or t
def pitch(a,f):
    if abs(f-1)<1e-3: return a
    up,down=int(round(1000/f)),1000   # resample to fewer samples => higher pitch & faster
    return resample_poly(a,up,down)
os.makedirs('/home/claude/book/vo',exist_ok=True)
manifest={}
for r,t in lines:
    v,sp,pf,g,wet,lp=CAST[r]
    random.seed(hash((r,t))%9999);jit=1+random.uniform(-.03,.03)
    txt=clean(t)
    if r=='sh' and txt.startswith('咩'): txt=txt.replace('咩','咩～').replace('～～','～')
    a,_=synth(txt,v,speed=sp*jit/pf)
    a=pitch(a,pf)
    if lp: a=sosfilt(butter(4,lp,'low',fs=SR,output='sos'),a)
    a=a+fftconvolve(a,ir)[:len(a)]*wet*4
    # trim silence, pad naturally
    nz=np.where(np.abs(a)>0.01)[0]
    if len(nz): a=a[max(0,nz[0]-480):nz[-1]+1200]
    rms=np.sqrt(np.mean(a**2))+1e-9;a=a*(0.075*g/rms);a=np.clip(a,-.97,.97)
    a=np.concatenate([np.zeros(int(SR*.06)),a,np.zeros(int(SR*.12))])
    key=f'{r}|{t}';h=hashlib.md5(key.encode()).hexdigest()[:10];f=f'{r}_{h}.mp3'
    sf.write('/tmp/x.wav',a,SR)
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i','/tmp/x.wav','-ac','1','-ar','24000','-b:a','48k',f'/home/claude/book/vo/{f}'],check=True)
    manifest[key]={'f':f,'d':round(len(a)/SR,2)}
json.dump(manifest,open('/home/claude/book/vo/vo.json','w'),ensure_ascii=False,indent=0)
print('done',sum(m['d'] for m in manifest.values()),'sec')
