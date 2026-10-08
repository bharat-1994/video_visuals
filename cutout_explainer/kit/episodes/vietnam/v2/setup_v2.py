"""Registers everything v2 into the scene_v2 registries: BG, ASSETS, CAST, CUSTOM, AMBIENCE, FX.
Run after film_v2.py has seeded scene_v2 from v1's scene.py (film_v2 imports this module)."""
import sys, os
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
from scene_v2 import BG, ASSETS, CAST, CUSTOM, AMBIENCE, FX
from episodes.vietnam.v2 import assets_v2 as AV, fx_v2 as FV

# ---------------- cast (section 5) ----------------
for _w in ("lan", "minh", "bunny", "us_official", "cn_official"):
    CAST[_w] = (lambda w: lambda s=1.0: AV.v2cast(w, s))(_w)

# ---------------- props (section 7) ----------------
PROPS = ("city_card", "rank_podium", "shop_front", "factory_modern", "sewing_machine", "wafer", "microscope",
         "laptop", "whiteboard", "chalk_text", "tv_screen", "carton", "cargo_plane", "road_sign", "trophy",
         "vault_door", "food_stall", "empty_chairs", "loudspeaker_pole", "compass", "sneaker", "solar_panel")
for _k in PROPS:
    if hasattr(AV, _k): ASSETS[_k] = getattr(AV, _k)

# ---------------- backgrounds (section 6): every bg_* defined in assets_v2 (not the lib helpers) ----------------
_LIB_BGS = {"bg_flat", "bg_room", "bg_sky_ground", "bg_spotlight", "bg_sunset", "bg_dark", "bg_paddy", "bg_kitchen", "bg_congress"}
for _k in dir(AV):
    if _k.startswith("bg_") and _k not in _LIB_BGS and callable(getattr(AV, _k)): BG[_k[3:]] = getattr(AV, _k)

# P2 items not built fall back to the listed alias (noted in REPORT_v2.md)
ALIAS = {"office_1980s": "office", "ruins": "dark", "engine_room": "factory", "renovation": "construction",
         "hanoi_street_1990": "hanoi_1986", "harvest_gold": "paddy", "harvest_poor": "paddy", "beijing_1978": "hanoi_1986",
         "embassy": "meeting_room", "government_hall": "meeting_room", "expo_hall": "meeting_room",
         "signing_table": "meeting_room", "trophy_stage": "meeting_room", "night_city": "night", "seoul_hq": "city",
         "drone_view": "paddy", "north_vn_hills": "paddy", "rice_to_factory": "paddy", "samsung_campus": "city",
         "factory_gate": "room", "garment_hall": "room", "small_workshop": "room", "design_studio": "office",
         "air_cargo": "port_day", "border": "sky", "sea_lanes": "port_day", "race_track": "sky",
         "casino_table": "room", "vault": "dark", "vhs_rewind": "dark", "kitchen_wall": "kitchen"}
ALIASED = []
for _n, _a in sorted(ALIAS.items()):
    if _n not in BG and _a in BG:
        BG[_n] = BG[_a]; ALIASED.append(_n)

# ---------------- ambience per background (sections 3.4 / 6) ----------------
AMB = {"hanoi_1986": ("crowd_murmur", -24), "hanoi_today": ("street_traffic", -22), "market": ("crowd_murmur", -22),
       "meeting_room": ("office_hum", -26), "assembly_hall": ("factory_line", -20), "samsung_hall": ("factory_line", -20),
       "port_day": ("harbor", -22), "port_night": ("harbor", -22), "warehouse": ("factory_line", -26),
       "construction": ("construction", -20), "lab": ("office_hum", -26), "cleanroom": ("cleanroom_hum", -20),
       "foxconn_campus": ("crowd_murmur", -24), "sunrise": ("wind_ambience", -24), "coop_yard": ("wind_ambience", -22),
       "boxing_ring": ("crowd_murmur", -20), "newsroom": ("office_hum", -26), "state_store": ("office_hum", -26),
       "office_1980s": ("office_hum", -26), "ruins": ("wind_ambience", -20), "engine_room": ("factory_line", -22),
       "renovation": ("construction", -24), "hanoi_street_1990": ("street_traffic", -26),
       "harvest_gold": ("wind_ambience", -22), "harvest_poor": ("wind_ambience", -22), "beijing_1978": ("street_traffic", -26),
       "embassy": ("office_hum", -26), "government_hall": ("office_hum", -26), "expo_hall": ("office_hum", -26),
       "signing_table": ("office_hum", -26), "trophy_stage": ("office_hum", -26), "night_city": ("night_crickets", -24),
       "seoul_hq": ("office_hum", -26), "drone_view": ("wind_ambience", -24), "north_vn_hills": ("wind_ambience", -24),
       "rice_to_factory": ("wind_ambience", -24), "samsung_campus": ("factory_line", -26), "factory_gate": ("factory_line", -22),
       "garment_hall": ("sewing", -20), "small_workshop": ("office_hum", -26), "design_studio": ("office_hum", -26),
       "air_cargo": ("jet_idle", -24), "border": ("street_traffic", -24), "sea_lanes": ("harbor", -24),
       "race_track": ("wind_ambience", -24), "casino_table": ("crowd_murmur", -24), "vault": ("office_hum", -28)}
for _n, _v in AMB.items():
    if _n in BG: AMBIENCE[_n] = _v

# ---------------- custom shot functions + fx layers (sections 8-9) ----------------
CUSTOM.update(FV.CUSTOM2)
FX.update(FV.FX2)
