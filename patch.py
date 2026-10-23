import os,re,glob
from PIL import Image,ImageDraw
R=os.path.dirname(os.path.abspath(__file__))+'/../'
A=R+'android/app/src/main/'
# manifest: ล็อกแนวนอน
p=A+'AndroidManifest.xml';m=open(p).read()
if 'screenOrientation' not in m:
    m=m.replace('<activity','<activity android:screenOrientation="sensorLandscape" android:keepScreenOn="true"',1)
open(p,'w').write(m)
# ชื่อแอป
p=A+'res/values/strings.xml';s=open(p,encoding='utf8').read()
s=re.sub(r'(<string name="app_name">)[^<]*',r'\1เกาะร้าง',s);s=re.sub(r'(<string name="title_activity_main">)[^<]*',r'\1เกาะร้าง',s)
open(p,'w',encoding='utf8').write(s)
# เต็มจอ (immersive)
pk=[d for d in glob.glob(A+'java/**/MainActivity.java',recursive=True)][0]
open(pk,'w').write('''package com.islandsurvival.game;
import android.os.Bundle;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;
public class MainActivity extends BridgeActivity {
  private void hide(){WindowCompat.setDecorFitsSystemWindows(getWindow(),false);WindowInsetsControllerCompat c=WindowCompat.getInsetsController(getWindow(),getWindow().getDecorView());c.hide(WindowInsetsCompat.Type.systemBars());c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);}
  @Override public void onCreate(Bundle b){super.onCreate(b);hide();}
  @Override public void onWindowFocusChanged(boolean f){super.onWindowFocusChanged(f);if(f)hide();}
}
''')
# ไอคอน
full=Image.open(R+'res/full.png').convert('RGBA');fg=Image.open(R+'res/fg.png').convert('RGBA')
dens={'mdpi':(48,108),'hdpi':(72,162),'xhdpi':(96,216),'xxhdpi':(144,324),'xxxhdpi':(192,432)}
for d,(a,b) in dens.items():
    o=A+'res/mipmap-%s/'%d;os.makedirs(o,exist_ok=True)
    ic=full.resize((a,a),Image.LANCZOS);ic.save(o+'ic_launcher.png')
    mk=Image.new('L',(a*4,a*4),0);ImageDraw.Draw(mk).ellipse((0,0,a*4-1,a*4-1),fill=255);mk=mk.resize((a,a),Image.LANCZOS)
    rd=ic.copy();rd.putalpha(mk);rd.save(o+'ic_launcher_round.png')
    fg.resize((b,b),Image.LANCZOS).save(o+'ic_launcher_fg.png')
x='<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android"><background android:drawable="@color/ic_bg2"/><foreground android:drawable="@mipmap/ic_launcher_fg"/></adaptive-icon>\n'
os.makedirs(A+'res/mipmap-anydpi-v26',exist_ok=True)
for n in ['ic_launcher.xml','ic_launcher_round.xml']:open(A+'res/mipmap-anydpi-v26/'+n,'w').write(x)
open(A+'res/values/ic_bg2.xml','w').write('<?xml version="1.0" encoding="utf-8"?><resources><color name="ic_bg2">#2a6f86</color></resources>')
print('patched')
