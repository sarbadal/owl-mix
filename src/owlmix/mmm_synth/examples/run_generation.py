from ..generator import MMMDataGenerator
 
 
# FMCG
gen = MMMDataGenerator("mmm_synth/config/presets/config_fmcg.yaml")
df = gen.generate()
 
print(df.head())