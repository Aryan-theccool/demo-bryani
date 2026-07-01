import math, random
from pathlib import Path
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.transformations import rotation_matrix, translation_matrix, concatenate_matrices

OUT = Path('/home/user/biryani-ar-demo/assets')
OUT.mkdir(parents=True, exist_ok=True)
random.seed(8)

def mat(name, color, metallic=0.0, roughness=0.65):
    return PBRMaterial(name=name, baseColorFactor=color, metallicFactor=metallic, roughnessFactor=roughness)

copper = mat('hammered copper handi bowl', [0.72,0.36,0.14,1], metallic=.7, roughness=.34)
inner_copper = mat('dark copper inside', [0.46,0.22,0.10,1], metallic=.55, roughness=.44)
shadow = mat('dark underside shadow', [0.18,0.08,0.03,1], metallic=.1, roughness=.8)
rice_white = mat('white basmati rice', [0.96,0.91,0.73,1], roughness=.95)
rice_yellow = mat('saffron yellow rice', [1.0,0.72,0.18,1], roughness=.95)
rice_orange = mat('masala orange rice', [0.92,0.42,0.12,1], roughness=.95)
chicken_mat = mat('spiced chicken pieces', [0.67,0.31,0.13,1], roughness=.82)
chicken_dark = mat('charred masala marks', [0.22,0.09,0.035,1], roughness=.9)
egg_white = mat('boiled egg white', [1.0,0.96,0.82,1], roughness=.6)
yolk = mat('egg yolk', [1.0,0.75,0.20,1], roughness=.75)
leaf = mat('mint coriander leaves', [0.05,0.45,0.19,1], roughness=.9)
onion = mat('fried onion', [0.34,0.12,0.035,1], roughness=.9)
lemon = mat('lemon wedge', [0.84,0.93,0.20,1], roughness=.65)
raita_mat = mat('raita bowl white yogurt', [0.93,0.96,0.90,1], roughness=.4)

scene = trimesh.Scene()

def add(mesh, name, material, transform=None):
    mesh.visual = trimesh.visual.TextureVisuals(material=material)
    scene.add_geometry(mesh, node_name=name, geom_name=name, transform=transform)

# bowl outer/inner as revolution surfaces
segments = 96
rings = 12
verts=[]; faces=[]
for i in range(rings+1):
    t=i/rings
    y = -0.42 + t*0.62
    # flared handi bowl profile
    r = 0.38 + 1.05*(math.sin(t*math.pi/2)**0.72)
    if i==0: r=0.28
    for j in range(segments):
        a=2*math.pi*j/segments
        verts.append([r*math.cos(a), y, r*math.sin(a)*0.78])
for i in range(rings):
    for j in range(segments):
        faces.append([i*segments+j, i*segments+(j+1)%segments, (i+1)*segments+(j+1)%segments])
        faces.append([i*segments+j, (i+1)*segments+(j+1)%segments, (i+1)*segments+j])
outer=trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
add(outer,'copper serving handi bowl',copper)

# rim torus and base
rim=trimesh.creation.torus(major_radius=1.43, minor_radius=.035, major_segments=128, minor_segments=12)
rim.apply_scale([1,1,.78]); rim.apply_transform(rotation_matrix(math.pi/2,[1,0,0])); rim.apply_translation([0,.205,0])
add(rim,'thick copper rim',copper)
base=trimesh.creation.cylinder(radius=.48, height=.08, sections=96)
base.apply_scale([1,.55,1]); base.apply_translation([0,-.46,0])
add(base,'bowl foot ring',shadow)

# handles as vertical torus loops left/right
for side, sx in [('left',-1),('right',1)]:
    h=trimesh.creation.torus(major_radius=.34, minor_radius=.035, major_segments=64, minor_segments=10)
    h.apply_scale([.55,1.0,.20])
    # torus is around z axis in xy plane; rotate to vertical plane-ish and position
    h.apply_transform(rotation_matrix(math.pi/2,[0,1,0]))
    h.apply_translation([sx*1.48,.02,0])
    add(h,f'{side} copper handle loop',copper)

# rice mound ellipsoid
mound=trimesh.creation.uv_sphere(segments=96, ring_count=32)
mound.apply_scale([1.23,.32,.78]); mound.apply_translation([0,.28,0])
add(mound,'saffron rice mound',rice_yellow)

# individual rice grains on top
for i in range(180):
    x=random.uniform(-1.0,1.0); z=random.uniform(-.58,.58)
    if (x/1.1)**2+(z/.62)**2>1: continue
    y=.52 + random.uniform(-.03,.08) - .08*((x/1.1)**2+(z/.62)**2)
    grain=trimesh.creation.cylinder(radius=random.uniform(.009,.014), height=random.uniform(.065,.105), sections=8)
    color=random.choice([rice_white,rice_white,rice_yellow,rice_orange])
    R=rotation_matrix(random.uniform(0,math.pi), [random.random(),random.random(),random.random()])
    grain.apply_transform(R); grain.apply_translation([x,y,z])
    add(grain,f'basmati rice grain {i}',color)

# irregular chicken chunks
for i,(x,z,s) in enumerate([(-.58,-.18,.22),(-.18,.18,.18),(.33,-.12,.20),(.62,.18,.17),(.05,-.34,.16)]):
    ch=trimesh.creation.icosphere(subdivisions=2, radius=1)
    # noise vertices
    v=ch.vertices.copy();
    rng=np.random.default_rng(i+4)
    v *= (1 + rng.normal(0,.10,v.shape))
    ch.vertices=v
    ch.apply_scale([s*1.35,s*.62,s*.9]); ch.apply_translation([x,.58,z])
    add(ch,f'3d spiced chicken chunk {i+1}',chicken_mat)
    # char marks small dark flattened spheres
    for k in range(3):
        mark=trimesh.creation.uv_sphere(segments=16, ring_count=8)
        mark.apply_scale([s*.26,s*.035,s*.12])
        mark.apply_translation([x+random.uniform(-s*.5,s*.5), .58+s*.33, z+random.uniform(-s*.3,s*.3)])
        add(mark,f'char masala spot {i}-{k}',chicken_dark)

# egg half on rim
for i,(x,z,ang) in enumerate([(.72,-.36,-.35)]):
    ew=trimesh.creation.uv_sphere(segments=32, ring_count=16)
    ew.apply_scale([.23,.07,.16]); ew.apply_translation([x,.66,z])
    add(ew,'half boiled egg white',egg_white)
    yo=trimesh.creation.uv_sphere(segments=24, ring_count=12)
    yo.apply_scale([.105,.028,.075]); yo.apply_translation([x,.725,z])
    add(yo,'egg yolk',yolk)

# leaves as flattened green ellipses
for i in range(26):
    x=random.uniform(-.95,.95); z=random.uniform(-.52,.52)
    if (x/1.12)**2+(z/.62)**2>1: continue
    lf=trimesh.creation.uv_sphere(segments=16, ring_count=8)
    lf.apply_scale([.055,.008,.025])
    lf.apply_transform(rotation_matrix(random.uniform(0,math.pi), [0,1,0]))
    lf.apply_translation([x,.68+random.uniform(-.02,.04),z])
    add(lf,f'mint coriander leaf {i}',leaf)

# fried onion strips thin curved-ish cylinders
for i in range(38):
    x=random.uniform(-1.0,1.0); z=random.uniform(-.58,.58)
    if (x/1.1)**2+(z/.62)**2>1: continue
    st=trimesh.creation.cylinder(radius=.012, height=random.uniform(.12,.22), sections=8)
    st.apply_scale([1,.45,1])
    st.apply_transform(rotation_matrix(math.pi/2,[1,0,0]))
    st.apply_transform(rotation_matrix(random.uniform(0,math.pi),[0,1,0]))
    st.apply_translation([x,.70,z])
    add(st,f'fried onion strip {i}',onion)

# lemon wedge (small yellow quarter-like wedge)
lem=trimesh.creation.uv_sphere(segments=24, ring_count=12)
lem.apply_scale([.20,.06,.11]); lem.apply_translation([-.80,.57,.38])
add(lem,'lemon wedge garnish',lemon)

# small side raita bowl on plate/base
plate=trimesh.creation.cylinder(radius=1.75, height=.035, sections=128)
plate.apply_scale([1,.45,1]); plate.apply_translation([0,-.52,0])
add(plate,'round serving plate under bowl',mat('dark wooden table shadow plate',[0.24,0.13,0.07,1],roughness=.9))
raita_bowl=trimesh.creation.cylinder(radius=.34, height=.16, sections=48)
raita_bowl.apply_scale([1,.45,1]); raita_bowl.apply_translation([-1.25,-.36,.55])
add(raita_bowl,'small raita bowl',copper)
raita=trimesh.creation.cylinder(radius=.29, height=.025, sections=48)
raita.apply_scale([1,.45,1]); raita.apply_translation([-1.25,-.26,.55])
add(raita,'raita yogurt surface',raita_mat)

# Set camera/lights metadata-ish
scene.camera = trimesh.scene.Camera(resolution=(1200,900), fov=(45,45))
scene.camera_transform = trimesh.transformations.translation_matrix([0,1.2,4.2]) @ trimesh.transformations.rotation_matrix(math.radians(-12), [1,0,0])

# export glb
out=OUT/'biryani_plate_3d.glb'
out.write_bytes(trimesh.exchange.gltf.export_glb(scene))
print(out, out.stat().st_size)
