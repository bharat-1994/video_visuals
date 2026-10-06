import json,time,sys
sys.path.insert(0,'build')
from commons import search
vq=["Maldives aerial","atoll aerial","Fiji lagoon","Bora Bora","Seychelles beach","Sri Lanka beach","Kerala backwaters","Kochi Chinese fishing nets","dhow sailing","traditional sailing boat","outrigger canoe","lava flowing into ocean","underwater volcano","plate tectonics animation","Indian Ocean","Arabian Sea","coral polyps","coral spawning","coral time-lapse","sea anemone","plankton","coral reef fish Maldives","Indian flag waving","flag waving","airplane takeoff","airplane landing island","cargo ship","ship at sea","cable laying ship","desalination","water drops slow motion","rain on sea","thunderstorm lightning","cyclone landfall","coconut tree beach","coconut harvest","fish market","fisherman net throwing","pole and line fishing","tuna fishing","sunrise ocean","sunset palm","beach drone sunset","clear water shallow","snorkeling","scuba diving reef","moray eel","hawksbill turtle","stingray","octopus","dancers India","Kolkali","Kerala dance","mosque","Kerala village","Kerala boat","Kochi","Mumbai harbour","Gujarat coast","Oman dhow","wind turbines sea","rising sea level","coastal erosion","flooding coast","ocean heat","satellite sea surface temperature","climate change ocean","glacier melting","tourism beach resort","tourists beach","plastic ocean","mangrove","sea birds colony","tern","frigatebird","noddy tern"]
cat={}
for q in vq:
    cat['V:'+q]=search(q,'video',12); time.sleep(2.2); print('V',q,len(cat['V:'+q]),flush=True)
json.dump(cat,open('build/catalog2.json','w'),indent=1)
