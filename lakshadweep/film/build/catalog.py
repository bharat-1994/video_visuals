import json,time,sys
sys.path.insert(0,'build')
from commons import search
vq=["ocean waves","sea waves beach","tropical beach","coconut palm","fishing boat","fishermen","tuna","dhow","sailing ship","lighthouse","sunset sea","underwater coral","sea turtle","manta ray","tropical cyclone","hurricane satellite","aerial island","drone beach","Kerala","India fishing","Kochi","harbor","sailing vessel replica","Indian Navy","ISS timelapse Earth","atoll","lagoon","coral bleaching","school of fish","clouds timelapse","monsoon","rope making","coconut","seaweed","jellyfish","reef fish","dolphin","seagull","palm trees wind","tidal","stormy sea","storm waves","night sky stars timelapse","sailing"]
iq=["Lakshadweep","Kavaratti","Agatti","Minicoy","Kalpeni","Bangaram","Androth","Amini island","Kadmat","Lakshadweep lagoon","Lakshadweep coral","Lakshadweep mosque","Lakshadweep fishing","Lakshadweep island aerial","Arakkal","Tipu Sultan","Portuguese carrack","Kannur fort","Vasco da Gama","Madras Presidency","Indian independence 1947","Sardar Patel","Cheraman Juma Mosque","Ubaid","Kolkali","coir","Minicoy lava dance","Kochi harbour","Lakshadweep ship","Lakshadweep Agatti airport"]
cat={}
for q in vq:
    cat['V:'+q]=search(q,'video',15); time.sleep(2.5); print('V',q,len(cat['V:'+q]),flush=True)
for q in iq:
    cat['I:'+q]=search(q,'bitmap',15); time.sleep(2.5); print('I',q,len(cat['I:'+q]),flush=True)
json.dump(cat,open('build/catalog.json','w'),indent=1)
