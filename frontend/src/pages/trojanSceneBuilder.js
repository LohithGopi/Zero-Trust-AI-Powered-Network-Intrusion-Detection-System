import * as THREE from 'three';

/**
 * Deterministic pseudo-random helper so handcrafted plank & stone variations are repeatable
 */
function seededRandom(seed) {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453123;
  return x - Math.floor(x);
}

// ============================================================================
// SHARED SCENE GEOMETRY CONSTANTS (Left-to-Right Cinematic Composition)
// ============================================================================
// Gate is on the RIGHT; Horse starts on the LEFT facing directly along the road into the Gate.
export const GATE_ROTATION_Y = -1.22; // Faces left toward horse & angled ~20 deg toward camera
export const GATE_FORWARD_DIR = new THREE.Vector3(
  -Math.sin(GATE_ROTATION_Y), // +0.939 (points right into the city)
  0,
  -Math.cos(GATE_ROTATION_Y)  // -0.344 (points slightly deeper into scene)
).normalize();

export const GATE_CENTER_POS = new THREE.Vector3(4.6, 0, -0.75);
// Horse starts 8.6 units in front of the gate on the LEFT side of the screen: (-3.48, 0, +2.21)
export const HORSE_START_POS = new THREE.Vector3()
  .copy(GATE_CENTER_POS)
  .addScaledVector(GATE_FORWARD_DIR, -8.6);
// Horse destination inside the city street of Troy after passing through the open gate
export const HORSE_CITY_DEST_POS = new THREE.Vector3()
  .copy(GATE_CENTER_POS)
  .addScaledVector(GATE_FORWARD_DIR, 4.2);

// Horse local +Z points along GATE_FORWARD_DIR toward the gate on the right
export const HORSE_BASE_ROTATION_Y = GATE_ROTATION_Y + Math.PI; // ~ +1.92 rad

/**
 * Generates high-resolution procedural PBR wood plank textures (Diffuse, Bump, Roughness)
 */
export function createRealisticWoodMaterialSet() {
  const makeWoodVariant = (baseHex, darkHex, highlightHex, plankRows = 8, seedOffset = 1) => {
    const size = 512;
    const diffCanvas = document.createElement('canvas');
    const bumpCanvas = document.createElement('canvas');
    const roughCanvas = document.createElement('canvas');
    diffCanvas.width = bumpCanvas.width = roughCanvas.width = size;
    diffCanvas.height = bumpCanvas.height = roughCanvas.height = size;

    const dCtx = diffCanvas.getContext('2d');
    const bCtx = bumpCanvas.getContext('2d');
    const rCtx = roughCanvas.getContext('2d');

    dCtx.fillStyle = baseHex;
    dCtx.fillRect(0, 0, size, size);

    bCtx.fillStyle = '#808080';
    bCtx.fillRect(0, 0, size, size);

    rCtx.fillStyle = '#c8c8c8';
    rCtx.fillRect(0, 0, size, size);

    const rowHeight = size / plankRows;

    for (let row = 0; row < plankRows; row++) {
      const y0 = row * rowHeight;
      const toneShift = (seededRandom(row + seedOffset * 17) - 0.5) * 18;

      dCtx.fillStyle = toneShift > 0 ? highlightHex : darkHex;
      dCtx.globalAlpha = Math.abs(toneShift) / 95;
      dCtx.fillRect(0, y0, size, rowHeight);

      const fiberCount = 90;
      for (let f = 0; f < fiberCount; f++) {
        const fy = y0 + seededRandom(row * 300 + f + seedOffset) * rowHeight;
        const fh = 0.8 + seededRandom(row * 500 + f) * 2.2;
        const isDark = f % 2 === 0;
        dCtx.fillStyle = isDark ? darkHex : highlightHex;
        dCtx.globalAlpha = 0.06 + seededRandom(f * 13 + row) * 0.14;
        dCtx.fillRect(0, fy, size, fh);

        bCtx.fillStyle = isDark ? '#646464' : '#969696';
        bCtx.globalAlpha = 0.12;
        bCtx.fillRect(0, fy, size, fh);

        rCtx.fillStyle = isDark ? '#dedede' : '#b0b0b0';
        rCtx.globalAlpha = 0.1;
        rCtx.fillRect(0, fy, size, fh);
      }

      // Knots
      const knotCount = 1 + Math.floor(seededRandom(row * 41 + seedOffset) * 2);
      for (let k = 0; k < knotCount; k++) {
        const kx = 50 + seededRandom(row * 71 + k * 29 + seedOffset) * (size - 100);
        const ky = y0 + rowHeight * (0.28 + seededRandom(row * 97 + k) * 0.44);
        const rx = 10 + seededRandom(k * 19 + row) * 15;
        const ry = 4 + seededRandom(k * 31 + row) * 6;

        dCtx.save();
        dCtx.translate(kx, ky);
        dCtx.scale(rx / ry, 1);
        const grad = dCtx.createRadialGradient(0, 0, 1, 0, 0, ry);
        grad.addColorStop(0, '#140a04');
        grad.addColorStop(0.55, darkHex);
        grad.addColorStop(1, 'rgba(0,0,0,0)');
        dCtx.globalAlpha = 0.55;
        dCtx.fillStyle = grad;
        dCtx.beginPath();
        dCtx.arc(0, 0, ry, 0, Math.PI * 2);
        dCtx.fill();
        dCtx.restore();
      }

      // Plank seams & staggered joints
      dCtx.globalAlpha = 0.85;
      dCtx.strokeStyle = '#0e0703';
      dCtx.lineWidth = 2.6;
      dCtx.beginPath();
      dCtx.moveTo(0, y0);
      dCtx.lineTo(size, y0);
      dCtx.stroke();

      bCtx.globalAlpha = 0.9;
      bCtx.strokeStyle = '#181818';
      bCtx.lineWidth = 3.2;
      bCtx.beginPath();
      dCtx.moveTo(0, y0);
      dCtx.lineTo(size, y0);
      bCtx.stroke();

      const jointX = Math.floor(60 + seededRandom(row * 223 + seedOffset * 11) * (size - 120));
      dCtx.beginPath();
      dCtx.moveTo(jointX, y0);
      dCtx.lineTo(jointX, y0 + rowHeight);
      dCtx.stroke();

      bCtx.beginPath();
      bCtx.moveTo(jointX, y0);
      bCtx.lineTo(jointX, y0 + rowHeight);
      bCtx.stroke();
    }

    const diffTex = new THREE.CanvasTexture(diffCanvas);
    const bumpTex = new THREE.CanvasTexture(bumpCanvas);
    const roughTex = new THREE.CanvasTexture(roughCanvas);
    [diffTex, bumpTex, roughTex].forEach((t) => {
      t.wrapS = THREE.RepeatWrapping;
      t.wrapT = THREE.RepeatWrapping;
      t.anisotropy = 4;
    });

    return new THREE.MeshStandardMaterial({
      map: diffTex,
      bumpMap: bumpTex,
      bumpScale: 0.045,
      roughnessMap: roughTex,
      roughness: 0.82,
      metalness: 0.06
    });
  };

  const weatheredOakMat = makeWoodVariant('#6b4425', '#2e1a0b', '#875934', 8, 1);
  const warmHeartOakMat = makeWoodVariant('#784d2a', '#361f0d', '#946239', 9, 2);
  const agedWalnutMat = makeWoodVariant('#4a2d17', '#1d1006', '#633d20', 7, 3);
  const darkCharredTimberMat = makeWoodVariant('#331e0f', '#140a04', '#4a2c17', 6, 4);
  const dustyHoofMat = makeWoodVariant('#523924', '#26180d', '#6e5239', 6, 5);
  dustyHoofMat.roughness = 0.92;

  // Carved Greek Meander (Greek Key) relief band material
  const friezeCanvas = document.createElement('canvas');
  friezeCanvas.width = 512;
  friezeCanvas.height = 128;
  const fCtx = friezeCanvas.getContext('2d');
  fCtx.fillStyle = '#3b2311';
  fCtx.fillRect(0, 0, 512, 128);
  fCtx.strokeStyle = '#9c7432';
  fCtx.lineWidth = 6;
  fCtx.strokeRect(0, 10, 512, 108);
  fCtx.strokeStyle = '#8c6528';
  fCtx.lineWidth = 5;
  for (let x = 8; x < 512; x += 64) {
    fCtx.beginPath();
    fCtx.moveTo(x, 96);
    fCtx.lineTo(x, 30);
    fCtx.lineTo(x + 44, 30);
    fCtx.lineTo(x + 44, 76);
    fCtx.lineTo(x + 20, 76);
    fCtx.lineTo(x + 20, 50);
    fCtx.lineTo(x + 30, 50);
    fCtx.stroke();
  }
  const friezeTex = new THREE.CanvasTexture(friezeCanvas);
  friezeTex.wrapS = THREE.RepeatWrapping;
  friezeTex.wrapT = THREE.RepeatWrapping;

  const greekFriezeMat = new THREE.MeshStandardMaterial({
    map: friezeTex,
    bumpMap: friezeTex,
    bumpScale: 0.05,
    roughness: 0.65,
    metalness: 0.28
  });

  const ancientBronzeMat = new THREE.MeshStandardMaterial({
    color: 0x9c722c,
    roughness: 0.38,
    metalness: 0.82
  });

  const forgedIronMat = new THREE.MeshStandardMaterial({
    color: 0x232528,
    roughness: 0.55,
    metalness: 0.72
  });

  const recessedEyeMat = new THREE.MeshStandardMaterial({
    color: 0x170d06,
    roughness: 0.75,
    metalness: 0.05
  });

  const interiorTimberMat = agedWalnutMat.clone();
  interiorTimberMat.side = THREE.DoubleSide;

  return {
    plankMaterials: [weatheredOakMat, warmHeartOakMat, agedWalnutMat, darkCharredTimberMat],
    weatheredOakMat,
    warmHeartOakMat,
    agedWalnutMat,
    darkCharredTimberMat,
    dustyHoofMat,
    greekFriezeMat,
    ancientBronzeMat,
    forgedIronMat,
    recessedEyeMat,
    interiorTimberMat
  };
}

/**
 * Builds a realistic, anatomically proportioned 3D Ancient Greek Soldier (Hoplite)
 * or Trojan Gatekeeper with helmet, armor cuirass, tunic, greaves, shield, and spear.
 */
function buildAncientWarriorCharacter({
  pose = 'standing', // 'standing', 'seated', 'pushing', 'winch'
  tunicColor = 0x7f1d1d,
  plumeColor = 0x991b1b,
  hasShield = true,
  hasSpear = true,
  scale = 1.0
}) {
  const charGroup = new THREE.Group();
  charGroup.scale.setScalar(scale);

  const skinMat = new THREE.MeshStandardMaterial({
    color: 0xc69067,
    roughness: 0.68,
    metalness: 0.04
  });
  const bronzeArmorMat = new THREE.MeshStandardMaterial({
    color: 0xb08436,
    roughness: 0.35,
    metalness: 0.82
  });
  const leatherMat = new THREE.MeshStandardMaterial({
    color: 0x3b2212,
    roughness: 0.8,
    metalness: 0.08
  });
  const tunicMat = new THREE.MeshStandardMaterial({
    color: tunicColor,
    roughness: 0.88,
    metalness: 0.02
  });
  const plumeMat = new THREE.MeshStandardMaterial({
    color: plumeColor,
    roughness: 0.9
  });
  const woodShaftMat = new THREE.MeshStandardMaterial({
    color: 0x4e2f18,
    roughness: 0.8
  });
  const ironTipMat = new THREE.MeshStandardMaterial({
    color: 0x94a3b8,
    roughness: 0.3,
    metalness: 0.85
  });

  // Upper body pivot (for breathing, turning toward hatch, or leaning into gate)
  const upperBody = new THREE.Group();
  upperBody.position.set(0, 0.56, 0);
  charGroup.add(upperBody);

  // Sculpted Bronze Muscle Cuirass / Linothorax Torso
  const torso = new THREE.Mesh(
    new THREE.CylinderGeometry(0.145, 0.125, 0.38, 12),
    bronzeArmorMat
  );
  torso.scale.set(1.15, 1.0, 0.82);
  torso.position.y = 0.2;
  torso.castShadow = true;
  upperBody.add(torso);

  // Tunic skirt & leather pteruges strips at waist
  const skirt = new THREE.Mesh(
    new THREE.CylinderGeometry(0.13, 0.165, 0.22, 12),
    tunicMat
  );
  skirt.position.y = -0.02;
  upperBody.add(skirt);

  const belt = new THREE.Mesh(
    new THREE.CylinderGeometry(0.138, 0.138, 0.05, 12),
    leatherMat
  );
  belt.position.y = 0.04;
  upperBody.add(belt);

  // Shoulder Pauldrons
  [-0.17, 0.17].forEach((sx) => {
    const pauldron = new THREE.Mesh(
      new THREE.SphereGeometry(0.068, 10, 8),
      bronzeArmorMat
    );
    pauldron.scale.set(1.0, 0.75, 1.1);
    pauldron.position.set(sx, 0.36, 0);
    upperBody.add(pauldron);
  });

  // Head & Corinthian Bronze Helmet Group
  const headPivot = new THREE.Group();
  headPivot.position.set(0, 0.44, 0);
  upperBody.add(headPivot);

  const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.058, 0.08, 8), skinMat);
  neck.position.y = 0.02;
  headPivot.add(neck);

  const head = new THREE.Mesh(new THREE.SphereGeometry(0.095, 12, 12), skinMat);
  head.position.y = 0.11;
  headPivot.add(head);

  // Corinthian Bronze Helmet Bowl, Cheek Guards & Horsehair Crest
  const helmetBowl = new THREE.Mesh(
    new THREE.SphereGeometry(0.105, 14, 12),
    bronzeArmorMat
  );
  helmetBowl.position.set(0, 0.12, -0.005);
  headPivot.add(helmetBowl);

  // Cheek plates framing face
  [-0.065, 0.065].forEach((cx) => {
    const cheekGuard = new THREE.Mesh(
      new THREE.BoxGeometry(0.03, 0.11, 0.09),
      bronzeArmorMat
    );
    cheekGuard.position.set(cx, 0.075, 0.045);
    cheekGuard.rotation.y = cx > 0 ? -0.25 : 0.25;
    headPivot.add(cheekGuard);
  });

  // Helmet Horsehair Crest Holder & Plume
  const crestHolder = new THREE.Mesh(
    new THREE.BoxGeometry(0.025, 0.05, 0.22),
    bronzeArmorMat
  );
  crestHolder.position.set(0, 0.23, -0.01);
  headPivot.add(crestHolder);

  const horsehairPlume = new THREE.Mesh(
    new THREE.BoxGeometry(0.036, 0.09, 0.28),
    plumeMat
  );
  horsehairPlume.position.set(0, 0.28, -0.02);
  headPivot.add(horsehairPlume);

  // Left & Right Arms
  const leftArmPivot = new THREE.Group();
  leftArmPivot.position.set(-0.18, 0.34, 0);
  upperBody.add(leftArmPivot);

  const leftArm = new THREE.Mesh(
    new THREE.CylinderGeometry(0.042, 0.036, 0.32, 8),
    skinMat
  );
  leftArm.position.set(0, -0.14, 0.04);
  leftArm.rotation.x = -0.35;
  leftArmPivot.add(leftArm);

  // Round Bronze Hoplon Shield (Aspis) on Left Arm
  if (hasShield) {
    const shieldGroup = new THREE.Group();
    shieldGroup.position.set(-0.06, -0.16, 0.1);
    shieldGroup.rotation.y = -0.95;
    shieldGroup.rotation.x = 0.15;

    const shieldDisc = new THREE.Mesh(
      new THREE.CylinderGeometry(0.26, 0.26, 0.025, 20),
      bronzeArmorMat
    );
    shieldDisc.rotation.x = Math.PI / 2;
    shieldGroup.add(shieldDisc);

    const shieldRim = new THREE.Mesh(
      new THREE.TorusGeometry(0.26, 0.02, 8, 20),
      leatherMat
    );
    shieldGroup.add(shieldRim);

    leftArmPivot.add(shieldGroup);
  }

  const rightArmPivot = new THREE.Group();
  rightArmPivot.position.set(0.18, 0.34, 0);
  upperBody.add(rightArmPivot);

  const rightArm = new THREE.Mesh(
    new THREE.CylinderGeometry(0.042, 0.036, 0.32, 8),
    skinMat
  );
  rightArm.position.set(0, -0.14, 0.05);
  rightArm.rotation.x = -0.45;
  rightArmPivot.add(rightArm);

  // Dory Spear held in Right Hand
  if (hasSpear) {
    const spearGroup = new THREE.Group();
    spearGroup.position.set(0.02, -0.18, 0.12);
    spearGroup.rotation.x = 0.12;
    const shaft = new THREE.Mesh(
      new THREE.CylinderGeometry(0.014, 0.015, 1.35, 6),
      woodShaftMat
    );
    shaft.position.y = 0.25;
    spearGroup.add(shaft);

    const spearhead = new THREE.Mesh(
      new THREE.ConeGeometry(0.028, 0.14, 6),
      ironTipMat
    );
    spearhead.position.y = 0.96;
    spearGroup.add(spearhead);

    rightArmPivot.add(spearGroup);
  }

  // Legs (Thighs + Bronze Greaves on Shins + Sandals)
  const leftLegPivot = new THREE.Group();
  leftLegPivot.position.set(-0.085, 0.52, 0);
  charGroup.add(leftLegPivot);

  const rightLegPivot = new THREE.Group();
  rightLegPivot.position.set(0.085, 0.52, 0);
  charGroup.add(rightLegPivot);

  [leftLegPivot, rightLegPivot].forEach((legPiv, idx) => {
    const thigh = new THREE.Mesh(
      new THREE.CylinderGeometry(0.058, 0.048, 0.26, 8),
      skinMat
    );
    thigh.position.y = -0.13;
    legPiv.add(thigh);

    const shinGreave = new THREE.Mesh(
      new THREE.CylinderGeometry(0.046, 0.038, 0.26, 8),
      bronzeArmorMat
    );
    shinGreave.position.y = -0.37;
    legPiv.add(shinGreave);

    const boot = new THREE.Mesh(
      new THREE.BoxGeometry(0.065, 0.05, 0.12),
      leatherMat
    );
    boot.position.set(0, -0.5, 0.025);
    legPiv.add(boot);

    if (pose === 'seated') {
      thigh.rotation.x = -Math.PI / 2.3;
      thigh.position.set(0, -0.04, 0.11);
      shinGreave.position.set(0, -0.22, 0.22);
      boot.position.set(0, -0.35, 0.25);
    } else if (pose === 'pushing') {
      upperBody.rotation.x = 0.48;
      leftArmPivot.rotation.x = -1.1;
      rightArmPivot.rotation.x = -1.1;
      legPiv.rotation.x = idx === 0 ? -0.32 : 0.28;
    } else if (pose === 'winch') {
      upperBody.rotation.x = 0.25;
      leftArmPivot.rotation.x = -0.85;
      rightArmPivot.rotation.x = -0.85;
    }
  });

  return {
    root: charGroup,
    upperBody,
    headPivot,
    leftArmPivot,
    rightArmPivot,
    leftLegPivot,
    rightLegPivot
  };
}

/**
 * Builds the Monumental Wooden Trojan Horse on a low-profile wheeled timber siege platform,
 * with a concealed double-door hatch on its camera-facing (-X) flank and 6 visible 3D Greek
 * soldiers inside the hollow wooden ribcage chamber.
 */
export function buildUltraRealisticTrojanHorse(group) {
  const mats = createRealisticWoodMaterialSet();
  const {
    plankMaterials,
    weatheredOakMat,
    warmHeartOakMat,
    agedWalnutMat,
    darkCharredTimberMat,
    dustyHoofMat,
    greekFriezeMat,
    ancientBronzeMat,
    forgedIronMat,
    recessedEyeMat,
    interiorTimberMat
  } = mats;

  let seedCounter = 1;
  const nextRand = () => seededRandom(seedCounter++);

  const createHandcraftedPlank = (w, h, d, matOverride = null) => {
    const mat =
      matOverride || plankMaterials[Math.floor(nextRand() * plankMaterials.length)];
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    return mesh;
  };

  // =========================================================================
  // 1. CONTACT SHADOWS & LOW-PROFILE WHEELED TIMBER SIEGE TRANSPORT PLATFORM
  // =========================================================================
  const shadowCanvas = document.createElement('canvas');
  shadowCanvas.width = 128;
  shadowCanvas.height = 128;
  const sCtx = shadowCanvas.getContext('2d');
  const sGrad = sCtx.createRadialGradient(64, 64, 6, 64, 64, 60);
  sGrad.addColorStop(0, 'rgba(0, 0, 0, 0.90)');
  sGrad.addColorStop(0.55, 'rgba(0, 0, 0, 0.48)');
  sGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
  sCtx.fillStyle = sGrad;
  sCtx.fillRect(0, 0, 128, 128);
  const contactShadowTex = new THREE.CanvasTexture(shadowCanvas);
  const contactShadowMat = new THREE.MeshBasicMaterial({
    map: contactShadowTex,
    transparent: true,
    depthWrite: false
  });

  const mainBodyShadow = new THREE.Mesh(new THREE.PlaneGeometry(3.8, 5.4), contactShadowMat);
  mainBodyShadow.rotation.x = -Math.PI / 2;
  mainBodyShadow.position.set(0, -1.235, 0.05);
  group.add(mainBodyShadow);

  // Heavy oak longitudinal siege runners beneath the hooves (keeps hooves fully visible!)
  [-0.68, 0.68].forEach((rx) => {
    const runner = createHandcraftedPlank(0.32, 0.11, 3.85, darkCharredTimberMat);
    runner.position.set(rx, -1.16, 0);
    group.add(runner);
  });

  // Cross-beams connecting the runners
  [-1.42, -0.45, 0.45, 1.42].forEach((cz) => {
    const crossBeam = createHandcraftedPlank(1.78, 0.09, 0.24, agedWalnutMat);
    crossBeam.position.set(0, -1.17, cz);
    group.add(crossBeam);
  });

  // Braided hemp tow ropes extending forward from the front cross-beam
  const ropeMat = new THREE.MeshStandardMaterial({ color: 0x856d47, roughness: 0.92 });
  [-0.45, 0.45].forEach((rx) => {
    const towRope = new THREE.Mesh(
      new THREE.CylinderGeometry(0.025, 0.025, 1.4, 8),
      ropeMat
    );
    towRope.rotation.x = Math.PI / 2 + 0.08;
    towRope.position.set(rx, -1.16, 2.55);
    group.add(towRope);
  });

  // 6 Low-Profile Iron-Rimmed Wooden Transport Wheels/Rollers (animated during Phase E)
  const wheels = [];
  const wheelZCoords = [-1.38, 0, 1.38];
  wheelZCoords.forEach((wz) => {
    [-0.88, 0.88].forEach((wx) => {
      const wheelGroup = new THREE.Group();
      wheelGroup.position.set(wx, -1.04, wz);

      const woodenDisc = new THREE.Mesh(
        new THREE.CylinderGeometry(0.21, 0.21, 0.12, 18),
        agedWalnutMat
      );
      woodenDisc.rotation.z = Math.PI / 2;
      woodenDisc.castShadow = true;
      wheelGroup.add(woodenDisc);

      const ironRim = new THREE.Mesh(
        new THREE.TorusGeometry(0.21, 0.022, 8, 20),
        forgedIronMat
      );
      ironRim.rotation.y = Math.PI / 2;
      wheelGroup.add(ironRim);

      // Cross spokes so wheel rotation is clearly visible when moving
      [0, Math.PI / 2].forEach((sa) => {
        const spoke = new THREE.Mesh(
          new THREE.BoxGeometry(0.14, 0.38, 0.045),
          darkCharredTimberMat
        );
        spoke.rotation.x = sa;
        wheelGroup.add(spoke);
      });

      const bronzeHub = new THREE.Mesh(
        new THREE.CylinderGeometry(0.06, 0.06, 0.16, 10),
        ancientBronzeMat
      );
      bronzeHub.rotation.z = Math.PI / 2;
      wheelGroup.add(bronzeHub);

      group.add(wheelGroup);
      wheels.push(wheelGroup);
    });
  });

  // =========================================================================
  // 2. FOUR ANATOMICALLY ARTICULATED EQUINE LEGS & MONUMENTAL WOODEN HOOVES
  // =========================================================================
  const legDefinitions = [
    { name: 'FrontLeft', x: -0.68, z: 1.25, isFront: true, stepOffsetZ: 0.12 },
    { name: 'FrontRight', x: 0.68, z: 1.25, isFront: true, stepOffsetZ: -0.08 },
    { name: 'RearLeft', x: -0.70, z: -1.32, isFront: false, stepOffsetZ: -0.08 },
    { name: 'RearRight', x: 0.70, z: -1.32, isFront: false, stepOffsetZ: 0.12 }
  ];

  legDefinitions.forEach(({ x, z, isFront, stepOffsetZ }) => {
    const legRoot = new THREE.Group();
    const sideSign = x < 0 ? -1 : 1;
    const baseZ = z + stepOffsetZ;

    // Contact shadow under each hoof
    const hoofZ = baseZ + (isFront ? 0.08 : -0.04);
    const hoofShadow = new THREE.Mesh(new THREE.PlaneGeometry(1.1, 1.1), contactShadowMat);
    hoofShadow.rotation.x = -Math.PI / 2;
    hoofShadow.position.set(x, -1.10, hoofZ);
    group.add(hoofShadow);

    // Monumental Splayed Wooden Hoof
    const hoofGroup = new THREE.Group();
    hoofGroup.position.set(x, -1.02, hoofZ);
    const hoofCore = new THREE.Mesh(
      new THREE.CylinderGeometry(0.24, 0.33, 0.24, 12),
      dustyHoofMat
    );
    hoofCore.scale.set(1.0, 1.0, 1.18);
    hoofCore.castShadow = true;
    hoofCore.receiveShadow = true;
    hoofGroup.add(hoofCore);

    for (let a = 0; a < 10; a++) {
      const ang = (a / 10) * Math.PI * 2;
      const stave = createHandcraftedPlank(0.08, 0.25, 0.06, dustyHoofMat);
      stave.position.set(Math.sin(ang) * 0.27, 0, Math.cos(ang) * 0.31);
      stave.rotation.y = ang;
      stave.rotation.x = 0.22;
      hoofGroup.add(stave);
    }

    const ironShoe = new THREE.Mesh(
      new THREE.CylinderGeometry(0.325, 0.34, 0.05, 14),
      forgedIronMat
    );
    ironShoe.scale.set(1.0, 1.0, 1.18);
    ironShoe.position.y = -0.09;
    hoofGroup.add(ironShoe);
    legRoot.add(hoofGroup);

    // Pastern & Fetlock Joint
    const fetlockZ = baseZ + (isFront ? -0.02 : -0.16);
    const pastern = createHandcraftedPlank(0.26, 0.28, 0.28, dustyHoofMat);
    pastern.position.set(x, -0.84, (hoofZ + fetlockZ) * 0.5);
    pastern.rotation.x = -0.28;
    legRoot.add(pastern);

    const fetlockJoint = new THREE.Mesh(
      new THREE.SphereGeometry(0.18, 12, 10),
      agedWalnutMat
    );
    fetlockJoint.scale.set(0.95, 0.85, 1.1);
    fetlockJoint.position.set(x, -0.68, fetlockZ);
    legRoot.add(fetlockJoint);

    // Cannon Bone
    const kneeOrHockY = isFront ? -0.04 : 0.06;
    const kneeOrHockZ = baseZ + (isFront ? 0.02 : -0.26);
    const cannonMidY = (-0.68 + kneeOrHockY) * 0.5;
    const cannonMidZ = (fetlockZ + kneeOrHockZ) * 0.5;
    const cannonGroup = new THREE.Group();
    cannonGroup.position.set(x, cannonMidY, cannonMidZ);
    cannonGroup.rotation.x = isFront ? 0.04 : 0.14;

    for (let s = 0; s < 8; s++) {
      const ang = (s / 8) * Math.PI * 2;
      const stave = createHandcraftedPlank(0.09, 0.66, 0.08);
      stave.position.set(Math.sin(ang) * 0.14, 0, Math.cos(ang) * 0.15);
      stave.rotation.y = ang;
      cannonGroup.add(stave);
    }
    [-0.2, 0.18].forEach((cy) => {
      const collar = new THREE.Mesh(
        new THREE.CylinderGeometry(0.195, 0.195, 0.045, 12),
        forgedIronMat
      );
      collar.position.y = cy;
      cannonGroup.add(collar);
    });
    legRoot.add(cannonGroup);

    // Knee / Hock Joint
    const jointGroup = new THREE.Group();
    jointGroup.position.set(x, kneeOrHockY, kneeOrHockZ);
    const jointBlock = new THREE.Mesh(
      new THREE.CylinderGeometry(0.22, 0.21, 0.36, 12),
      agedWalnutMat
    );
    jointBlock.rotation.z = Math.PI / 2;
    jointGroup.add(jointBlock);

    if (!isFront) {
      const hockPoint = createHandcraftedPlank(0.24, 0.22, 0.26, agedWalnutMat);
      hockPoint.position.set(0, 0.05, -0.12);
      hockPoint.rotation.x = 0.25;
      jointGroup.add(hockPoint);
    }
    const jointBoss = new THREE.Mesh(
      new THREE.CylinderGeometry(0.09, 0.09, 0.4, 10),
      ancientBronzeMat
    );
    jointBoss.rotation.z = Math.PI / 2;
    jointGroup.add(jointBoss);
    legRoot.add(jointGroup);

    // Upper Leg
    const shoulderOrHipY = 0.92;
    const shoulderOrHipZ = baseZ + (isFront ? 0.05 : -0.02);
    const upperMidY = (kneeOrHockY + shoulderOrHipY) * 0.5;
    const upperMidZ = (kneeOrHockZ + shoulderOrHipZ) * 0.5;

    const upperLegGroup = new THREE.Group();
    upperLegGroup.position.set(x, upperMidY, upperMidZ);
    upperLegGroup.rotation.x = isFront ? -0.05 : -0.26;

    for (let s = 0; s < 10; s++) {
      const ang = (s / 10) * Math.PI * 2;
      const rx = 0.22;
      const rz = isFront ? 0.25 : 0.31;
      const plank = createHandcraftedPlank(0.12, 0.92, 0.09);
      plank.position.set(Math.sin(ang) * rx, 0, Math.cos(ang) * rz);
      plank.rotation.y = ang;
      plank.rotation.z = Math.sin(ang) * 0.08;
      upperLegGroup.add(plank);
    }
    legRoot.add(upperLegGroup);

    // Shoulder / Haunch Plank Cladding
    const muscleGroup = new THREE.Group();
    muscleGroup.position.set(x * 1.06, 1.15, shoulderOrHipZ);
    const plankLayers = isFront ? 6 : 7;
    for (let p = 0; p < plankLayers; p++) {
      const py = -0.25 + p * 0.13;
      const pw = 0.16;
      const pd = (isFront ? 0.78 : 0.96) - p * 0.04;
      const mPlank = createHandcraftedPlank(pw, 0.125, pd);
      mPlank.position.set(
        sideSign * (0.08 - Math.abs(p - 3) * 0.015),
        py,
        (nextRand() - 0.5) * 0.03
      );
      mPlank.rotation.z = sideSign * (0.12 - p * 0.04);
      mPlank.rotation.y = sideSign * (isFront ? 0.12 : -0.1);
      muscleGroup.add(mPlank);
    }
    legRoot.add(muscleGroup);

    group.add(legRoot);
  });

  // =========================================================================
  // 3. COHERENT 3D WOODEN INTERIOR CHAMBER WITH VISIBLE GREEK SOLDIERS
  // =========================================================================
  // Note: Hatch opening is on the -X side (which faces +Z toward the camera when the
  // horse is on the LEFT facing the gate on the RIGHT).
  // Inside the chamber, the camera sits near x = -0.25 looking toward +X (the inner wall)
  // so Z spans left-to-right across the interior view!
  const interiorGroup = new THREE.Group();
  interiorGroup.position.set(0, 1.42, 0);
  group.add(interiorGroup);

  // Inner dark wooden hull shell (open on the -X hatch side)
  const innerShell = new THREE.Mesh(
    new THREE.CylinderGeometry(0.86, 0.82, 2.95, 18, 1, true, 0.35, Math.PI * 1.75),
    interiorTimberMat
  );
  innerShell.rotation.x = Math.PI / 2;
  innerShell.rotation.z = Math.PI / 2; // Open gap faces -X
  interiorGroup.add(innerShell);

  // Slatted timber floor deck & side benches for soldiers
  for (let fz = -1.35; fz <= 1.35; fz += 0.22) {
    const floorBoard = createHandcraftedPlank(1.52, 0.07, 0.19, agedWalnutMat);
    floorBoard.position.set(0, -0.58, fz);
    interiorGroup.add(floorBoard);
  }

  // Heavy structural oak cross-beams & curved hull ribs inside the horse
  for (let rz = -1.2; rz <= 1.2; rz += 0.4) {
    for (let a = 0; a < 9; a++) {
      const ang = -Math.PI * 0.65 + (a / 8) * Math.PI * 1.3; // Curves around +X, +Y, -Y
      const ribSeg = createHandcraftedPlank(0.09, 0.34, 0.11, darkCharredTimberMat);
      ribSeg.position.set(Math.cos(ang) * 0.78, Math.sin(ang) * 0.66, rz);
      ribSeg.rotation.z = ang - Math.PI / 2;
      interiorGroup.add(ribSeg);
    }
  }

  // Front and rear interior bulkheads with weapon racks
  [-1.42, 1.42].forEach((bz) => {
    const bulkhead = new THREE.Mesh(
      new THREE.CylinderGeometry(0.84, 0.84, 0.12, 14),
      interiorTimberMat
    );
    bulkhead.rotation.x = Math.PI / 2;
    bulkhead.position.set(0, 0, bz);
    interiorGroup.add(bulkhead);
  });

  // Two Hanging Bronze Oil Lamps illuminating the hidden Greek soldiers on both sides
  [-0.78, 0.78].forEach((lz) => {
    const lanternGroup = new THREE.Group();
    lanternGroup.position.set(0.28, 0.42, lz);
    const lanternCage = new THREE.Mesh(
      new THREE.OctahedronGeometry(0.11, 0),
      ancientBronzeMat
    );
    const lanternFlame = new THREE.Mesh(
      new THREE.SphereGeometry(0.065, 10, 10),
      new THREE.MeshBasicMaterial({ color: 0xffb84d })
    );
    lanternGroup.add(lanternCage);
    lanternGroup.add(lanternFlame);
    interiorGroup.add(lanternGroup);
  });

  // -------------------------------------------------------------------------
  // 6 THREE-DIMENSIONAL GREEK SOLDIERS (HOPLITES) HIDDEN INSIDE THE HORSE
  // Positioned on the left (z > 0.48), right (z < -0.48), and background of
  // the interior chamber so they frame the login form and are 100% visible!
  // -------------------------------------------------------------------------
  const soldiers = [];
  const soldierConfigs = [
    // Left side of interior view (toward front/neck of horse, z > 0)
    {
      x: 0.26,
      y: -0.55,
      z: 0.74,
      rotY: -Math.PI * 0.62,
      pose: 'standing',
      tunicColor: 0x881337,
      plumeColor: 0x991b1b,
      hasShield: true,
      hasSpear: true,
      scale: 0.92
    },
    {
      x: 0.44,
      y: -0.55,
      z: 0.46,
      rotY: -Math.PI * 0.52,
      pose: 'seated',
      tunicColor: 0x7c2d12,
      plumeColor: 0xb45309,
      hasShield: true,
      hasSpear: false,
      scale: 0.90
    },
    {
      x: -0.02,
      y: -0.55,
      z: 1.04,
      rotY: -Math.PI * 0.72,
      pose: 'standing',
      tunicColor: 0x1e3a8a,
      plumeColor: 0xd97706,
      hasShield: true,
      hasSpear: true,
      scale: 0.90
    },
    // Right side of interior view (toward rear/croup of horse, z < 0)
    {
      x: 0.26,
      y: -0.55,
      z: -0.74,
      rotY: -Math.PI * 0.38,
      pose: 'standing',
      tunicColor: 0x7f1d1d,
      plumeColor: 0x991b1b,
      hasShield: true,
      hasSpear: true,
      scale: 0.92
    },
    {
      x: 0.44,
      y: -0.55,
      z: -0.46,
      rotY: -Math.PI * 0.48,
      pose: 'seated',
      tunicColor: 0x1e3a8a,
      plumeColor: 0x991b1b,
      hasShield: true,
      hasSpear: true,
      scale: 0.90
    },
    {
      x: -0.02,
      y: -0.55,
      z: -1.04,
      rotY: -Math.PI * 0.28,
      pose: 'standing',
      tunicColor: 0x78350f,
      plumeColor: 0xb45309,
      hasShield: true,
      hasSpear: true,
      scale: 0.90
    }
  ];

  soldierConfigs.forEach((cfg) => {
    const warrior = buildAncientWarriorCharacter(cfg);
    warrior.root.position.set(cfg.x, cfg.y, cfg.z);
    warrior.root.rotation.y = cfg.rotY;
    warrior.baseRotY = cfg.rotY;
    interiorGroup.add(warrior.root);
    soldiers.push(warrior);
  });

  // =========================================================================
  // 4. ANATOMICAL EQUINE TORSO BARREL CLAD IN HUNDREDS OF OVERLAPPING PLANKS
  // =========================================================================
  const getTorsoProfile = (zNorm) => {
    const widthRx =
      0.92 -
      0.12 * Math.pow(zNorm - 0.15, 2) +
      0.08 * Math.exp(-Math.pow((zNorm + 0.65) * 3, 2)) +
      0.09 * Math.exp(-Math.pow((zNorm - 0.65) * 3, 2));
    const heightRy =
      0.74 -
      0.08 * Math.pow(zNorm, 2) +
      0.07 * Math.exp(-Math.pow((zNorm - 0.55) * 2.5, 2));
    const centerY =
      1.42 +
      0.08 * Math.sin(zNorm * Math.PI * 0.6) +
      (zNorm < -0.5 ? -0.12 * Math.pow((zNorm + 0.5) * 2, 2) : 0);
    return { widthRx, heightRy, centerY };
  };

  const circumferentialPlanks = 26;
  const axialSegments = 6;
  const zStart = -1.68;
  const zEnd = 1.62;
  const segLen = (zEnd - zStart) / axialSegments;

  for (let c = 0; c < circumferentialPlanks; c++) {
    const theta = (c / circumferentialPlanks) * Math.PI * 2;
    const cosT = Math.cos(theta);
    const sinT = Math.sin(theta);

    for (let s = 0; s < axialSegments; s++) {
      const z0 = zStart + s * segLen;
      const z1 = z0 + segLen;
      const zMid = (z0 + z1) * 0.5;
      const zNorm = zMid / 1.68;

      // Leave an opening on the camera-facing (-X) center flank for the concealed entrance hatch
      const isLeftSideOpening =
        cosT < -0.72 && Math.abs(sinT) < 0.62 && zMid > -0.58 && zMid < 0.58;
      if (isLeftSideOpening) continue;

      const { widthRx, heightRy, centerY } = getTorsoProfile(zNorm);
      const px = cosT * widthRx;
      const py = centerY + sinT * heightRy;

      const plankThick = 0.065 + (nextRand() - 0.5) * 0.018;
      const plankHeight = 0.21 + (nextRand() - 0.5) * 0.02;
      const plankLength = segLen + 0.04;

      const isLowerBelly = sinT < -0.65;
      const matChoice = isLowerBelly ? agedWalnutMat : null;
      const plank = createHandcraftedPlank(plankThick, plankHeight, plankLength, matChoice);

      plank.position.set(
        px + cosT * (nextRand() - 0.5) * 0.015,
        py + sinT * (nextRand() - 0.5) * 0.015,
        zMid
      );

      const normalAngle = Math.atan2(sinT / heightRy, cosT / widthRx);
      plank.rotation.z = normalAngle;

      const pPrev = getTorsoProfile((z0 - 0.05) / 1.68);
      const pNext = getTorsoProfile((z1 + 0.05) / 1.68);
      const dR = (pNext.widthRx - pPrev.widthRx) * cosT;
      plank.rotation.y = -Math.atan2(dR, segLen) + (nextRand() - 0.5) * 0.025;

      group.add(plank);
    }
  }

  // Carved Greek Meander Ornamental Girth & Breastplate Straps with Bronze Studs
  [-0.75, 0.72].forEach((strapZ) => {
    const { widthRx, heightRy, centerY } = getTorsoProfile(strapZ / 1.68);
    for (let a = 0; a < 24; a++) {
      const ang = (a / 24) * Math.PI * 2;
      const seg = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.16, 0.14), greekFriezeMat);
      seg.position.set(
        Math.cos(ang) * (widthRx + 0.03),
        centerY + Math.sin(ang) * (heightRy + 0.03),
        strapZ
      );
      seg.rotation.z = ang;
      group.add(seg);

      if (a % 2 === 0) {
        const stud = new THREE.Mesh(
          new THREE.SphereGeometry(0.028, 8, 8),
          ancientBronzeMat
        );
        stud.position.set(
          Math.cos(ang) * (widthRx + 0.055),
          centerY + Math.sin(ang) * (heightRy + 0.055),
          strapZ
        );
        group.add(stud);
      }
    }
  });

  // =========================================================================
  // 5. CONCEALED DOUBLE-DOOR TIMBER ENTRANCE HATCH ON CAMERA-FACING (-X) TORSO
  // =========================================================================
  const buildPlankedHatchDoor = (doorSign) => {
    // doorSign: -1 for rear-side door (z = -0.58), +1 for front-side door (z = +0.58)
    const pivot = new THREE.Group();
    pivot.position.set(-0.91, 1.42, doorSign * 0.58);

    const doorWidthZ = 0.57;
    const zCenterOffset = -doorSign * (doorWidthZ * 0.5);

    for (let r = 0; r < 6; r++) {
      const py = -0.38 + r * 0.15;
      const curvatureX = -Math.cos((py / 0.74) * 0.7) * 0.04;
      const hPlank = createHandcraftedPlank(0.08, 0.145, doorWidthZ - 0.01);
      hPlank.position.set(curvatureX, py, zCenterOffset);
      pivot.add(hPlank);
    }

    [-0.26, 0.26].forEach((hy) => {
      const ironStrap = new THREE.Mesh(
        new THREE.BoxGeometry(0.095, 0.05, doorWidthZ * 0.85),
        forgedIronMat
      );
      ironStrap.position.set(-0.04, hy, zCenterOffset);
      pivot.add(ironStrap);
    });

    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(0.065, 0.016, 8, 16),
      ancientBronzeMat
    );
    ring.rotation.y = Math.PI / 2;
    ring.position.set(-0.09, 0, -doorSign * 0.46);
    pivot.add(ring);

    group.add(pivot);
    return pivot;
  };

  const leftHatchPivot = buildPlankedHatchDoor(-1);
  const rightHatchPivot = buildPlankedHatchDoor(1);

  // =========================================================================
  // 6. MUSCULAR PECTORAL CHEST & ROUNDED HINDQUARTER CROUP CAPS
  // =========================================================================
  const chestGroup = new THREE.Group();
  chestGroup.position.set(0, 1.38, 1.62);
  for (let side of [-1, 1]) {
    for (let row = 0; row < 7; row++) {
      const ry = -0.42 + row * 0.14;
      const forwardCurve = Math.cos((ry / 0.6) * 0.9) * 0.24;
      const cPlank = createHandcraftedPlank(0.42, 0.135, 0.22);
      cPlank.position.set(side * 0.24, ry, forwardCurve);
      cPlank.rotation.y = side * 0.28;
      cPlank.rotation.x = -ry * 0.35;
      chestGroup.add(cPlank);
    }
    const boss = new THREE.Mesh(
      new THREE.CylinderGeometry(0.16, 0.18, 0.06, 16),
      ancientBronzeMat
    );
    boss.rotation.x = Math.PI / 2;
    boss.rotation.z = side * 0.28;
    boss.position.set(side * 0.44, 0.02, 0.22);
    chestGroup.add(boss);
  }
  const chestBelt = new THREE.Mesh(new THREE.BoxGeometry(1.18, 0.15, 0.28), greekFriezeMat);
  chestBelt.position.set(0, 0.02, 0.18);
  chestGroup.add(chestBelt);
  group.add(chestGroup);

  const croupGroup = new THREE.Group();
  croupGroup.position.set(0, 1.38, -1.66);
  for (let side of [-1, 1]) {
    for (let row = 0; row < 7; row++) {
      const ry = -0.4 + row * 0.14;
      const rearCurve = -Math.cos((ry / 0.6) * 0.9) * 0.22;
      const rPlank = createHandcraftedPlank(0.42, 0.135, 0.22);
      rPlank.position.set(side * 0.23, ry, rearCurve);
      rPlank.rotation.y = -side * 0.32;
      rPlank.rotation.x = ry * 0.38;
      croupGroup.add(rPlank);
    }
  }
  group.add(croupGroup);

  // =========================================================================
  // 7. GRACEFULLY CURVED ANATOMICAL NECK & LAYERED CARVED WOODEN MANE
  // =========================================================================
  const neckRings = 9;
  for (let n = 0; n < neckRings; n++) {
    const t = n / (neckRings - 1);
    const ny = 1.68 + t * 1.52;
    const nz = 1.28 + Math.sin(t * Math.PI * 0.65) * 0.76;
    const rx = THREE.MathUtils.lerp(0.56, 0.28, t);
    const rz = THREE.MathUtils.lerp(0.66, 0.36, t);
    const pitchX = -0.44 + t * 0.58;

    const ringGroup = new THREE.Group();
    ringGroup.position.set(0, ny, nz);
    ringGroup.rotation.x = pitchX;

    const stavesInRing = 14;
    for (let s = 0; s < stavesInRing; s++) {
      const ang = (s / stavesInRing) * Math.PI * 2;
      const stave = createHandcraftedPlank(0.13, 0.26, 0.08);
      stave.position.set(Math.sin(ang) * rx, 0, Math.cos(ang) * rz);
      stave.rotation.y = ang;
      ringGroup.add(stave);
    }

    const lockCount = 3;
    for (let l = 0; l < lockCount; l++) {
      const side = l === 0 ? 0 : l === 1 ? -1 : 1;
      const maneLock = createHandcraftedPlank(
        0.075,
        0.34 - t * 0.08,
        0.24 - t * 0.05,
        l % 2 === 0 ? agedWalnutMat : darkCharredTimberMat
      );
      maneLock.position.set(
        side * (0.09 + nextRand() * 0.05),
        0.08,
        -rz - 0.06 + (nextRand() - 0.5) * 0.03
      );
      maneLock.rotation.x = -0.38 - nextRand() * 0.18;
      maneLock.rotation.z = side * (0.28 + nextRand() * 0.12);
      maneLock.rotation.y = side * 0.18;
      ringGroup.add(maneLock);
    }

    group.add(ringGroup);
  }

  const neckCollar = new THREE.Mesh(
    new THREE.TorusGeometry(0.58, 0.045, 10, 24),
    ancientBronzeMat
  );
  neckCollar.position.set(0, 1.76, 1.34);
  neckCollar.rotation.x = Math.PI / 2 - 0.42;
  group.add(neckCollar);

  // =========================================================================
  // 8. SCULPTED EQUINE HEAD, MUZZLE, NOSTRILS, JAW & RECESSED EYES
  // =========================================================================
  const headGroup = new THREE.Group();
  headGroup.position.set(0, 3.24, 2.08);
  headGroup.rotation.x = 0.26;
  group.add(headGroup);

  for (let i = -3; i <= 3; i++) {
    const craniumPlank = createHandcraftedPlank(0.1, 0.48, 0.68);
    craniumPlank.position.set(
      i * 0.085,
      0.06 - Math.abs(i) * 0.025,
      -0.05 - Math.abs(i) * 0.02
    );
    craniumPlank.rotation.z = -i * 0.08;
    headGroup.add(craniumPlank);
  }

  [-1, 1].forEach((side) => {
    for (let c = 0; c < 4; c++) {
      const cheekPlank = createHandcraftedPlank(0.08, 0.14, 0.62 - c * 0.06);
      cheekPlank.position.set(
        side * (0.31 - c * 0.02),
        -0.08 - c * 0.08,
        0.06 + c * 0.04
      );
      cheekPlank.rotation.y = side * 0.16;
      cheekPlank.rotation.z = side * 0.1;
      headGroup.add(cheekPlank);
    }

    // Sculpted & Deeply Recessed Eye Socket (NO glowing lights)
    const eyeSocketGroup = new THREE.Group();
    eyeSocketGroup.position.set(side * 0.29, 0.11, 0.16);
    eyeSocketGroup.rotation.y = side * 0.22;

    const browRidge = createHandcraftedPlank(0.11, 0.07, 0.24, agedWalnutMat);
    browRidge.position.set(side * 0.02, 0.065, 0);
    browRidge.rotation.z = -side * 0.25;
    browRidge.rotation.x = 0.15;
    eyeSocketGroup.add(browRidge);

    const lowerLid = createHandcraftedPlank(0.09, 0.05, 0.2, agedWalnutMat);
    lowerLid.position.set(side * 0.01, -0.055, 0);
    eyeSocketGroup.add(lowerLid);

    const eyeCavity = new THREE.Mesh(
      new THREE.BoxGeometry(0.08, 0.09, 0.16),
      recessedEyeMat
    );
    eyeCavity.position.set(-side * 0.02, 0, 0);
    eyeSocketGroup.add(eyeCavity);

    const sculptedEyeball = new THREE.Mesh(
      new THREE.SphereGeometry(0.048, 12, 10),
      darkCharredTimberMat
    );
    sculptedEyeball.position.set(0, 0, 0);
    eyeSocketGroup.add(sculptedEyeball);

    headGroup.add(eyeSocketGroup);
  });

  for (let n = -2; n <= 2; n++) {
    const noseBridgePlank = createHandcraftedPlank(0.08, 0.12, 0.86);
    noseBridgePlank.position.set(
      n * 0.068,
      0.06 - Math.abs(n) * 0.03,
      0.52
    );
    noseBridgePlank.rotation.x = 0.18;
    noseBridgePlank.rotation.y = -n * 0.06;
    headGroup.add(noseBridgePlank);
  }

  const muzzleCore = createHandcraftedPlank(0.36, 0.28, 0.42, warmHeartOakMat);
  muzzleCore.position.set(0, -0.11, 0.86);
  muzzleCore.rotation.x = 0.15;
  headGroup.add(muzzleCore);

  [-1, 1].forEach((side) => {
    const nostrilRim = new THREE.Mesh(
      new THREE.TorusGeometry(0.058, 0.022, 8, 14),
      agedWalnutMat
    );
    nostrilRim.position.set(side * 0.15, -0.06, 1.02);
    nostrilRim.rotation.y = side * 0.55;
    nostrilRim.rotation.x = -0.3;
    headGroup.add(nostrilRim);

    const nostrilCavity = new THREE.Mesh(
      new THREE.SphereGeometry(0.048, 8, 8),
      recessedEyeMat
    );
    nostrilCavity.position.set(side * 0.135, -0.06, 1.0);
    headGroup.add(nostrilCavity);
  });

  for (let j = -1; j <= 1; j++) {
    const jawPlank = createHandcraftedPlank(0.12, 0.14, 0.78, agedWalnutMat);
    jawPlank.position.set(j * 0.095, -0.27, 0.56);
    jawPlank.rotation.x = 0.08;
    headGroup.add(jawPlank);
  }

  [-1, 1].forEach((side) => {
    const earGroup = new THREE.Group();
    earGroup.position.set(side * 0.21, 0.36, -0.24);
    earGroup.rotation.x = -0.18;
    earGroup.rotation.z = -side * 0.16;
    earGroup.rotation.y = side * 0.25;

    const earOuter = new THREE.Mesh(
      new THREE.ConeGeometry(0.095, 0.42, 7),
      agedWalnutMat
    );
    earOuter.castShadow = true;
    earGroup.add(earOuter);

    const earHollow = new THREE.Mesh(
      new THREE.ConeGeometry(0.055, 0.32, 6),
      recessedEyeMat
    );
    earHollow.position.set(0, -0.02, 0.035);
    earGroup.add(earHollow);

    headGroup.add(earGroup);
  });

  for (let f = -1; f <= 1; f++) {
    const forelock = createHandcraftedPlank(0.065, 0.1, 0.28, darkCharredTimberMat);
    forelock.position.set(f * 0.06, 0.3, -0.02);
    forelock.rotation.x = 0.42;
    forelock.rotation.y = f * 0.15;
    headGroup.add(forelock);
  }

  const noseband = new THREE.Mesh(
    new THREE.BoxGeometry(0.41, 0.055, 0.07),
    ancientBronzeMat
  );
  noseband.position.set(0, -0.02, 0.76);
  headGroup.add(noseband);

  [-1, 1].forEach((side) => {
    const bitRing = new THREE.Mesh(
      new THREE.TorusGeometry(0.065, 0.015, 8, 16),
      ancientBronzeMat
    );
    bitRing.rotation.y = Math.PI / 2;
    bitRing.position.set(side * 0.21, -0.21, 0.82);
    headGroup.add(bitRing);

    const cheekStrap = new THREE.Mesh(
      new THREE.BoxGeometry(0.03, 0.045, 0.72),
      ancientBronzeMat
    );
    cheekStrap.position.set(side * 0.28, -0.04, 0.42);
    cheekStrap.rotation.x = 0.32;
    cheekStrap.rotation.y = -side * 0.14;
    headGroup.add(cheekStrap);
  });

  // =========================================================================
  // 9. LONG CARVED WOODEN TAIL (Layered Curved Timber Strands)
  // =========================================================================
  const tailRoot = new THREE.Group();
  tailRoot.position.set(0, 1.48, -1.86);
  tailRoot.rotation.x = 0.22;
  group.add(tailRoot);

  for (let t = 0; t < 22; t++) {
    const layer = Math.floor(t / 5);
    const spread = ((t % 5) - 2) * 0.075;
    const strandLen = 0.55 + (t % 3) * 0.12;
    const strand = createHandcraftedPlank(
      0.068,
      strandLen,
      0.065,
      t % 2 === 0 ? agedWalnutMat : darkCharredTimberMat
    );
    const yPos = -0.24 - layer * 0.34;
    const zPos = -0.06 - Math.sin(layer * 0.6) * 0.14;
    strand.position.set(spread * (1 + layer * 0.22), yPos, zPos);
    strand.rotation.x = 0.16 - layer * 0.09;
    strand.rotation.z = spread * 0.85;
    tailRoot.add(strand);
  }

  return {
    leftHatchPivot,
    rightHatchPivot,
    interiorGroup,
    soldiers,
    wheels
  };
}

/**
 * Builds the Right-Side Fortified City Wall & Monumental Scaean Gate of Troy,
 * the Center Dusty Approach Road, 4 Visible 3D Trojan Gatekeepers operating the
 * gate panels & winches, and the Colonnaded City Street & Acropolis beyond the gate.
 */
export function buildAncientTroyEnvironment(scene, isMobileViewport) {
  const envGroup = new THREE.Group();
  scene.add(envGroup);

  let seed = 101;
  const rand = () => seededRandom(seed++);

  // =========================================================================
  // 1. PROCEDURAL TEXTURES FOR STONE MASONRY, BATTLEFIELD EARTH & HAZE
  // =========================================================================
  const stoneCanvas = document.createElement('canvas');
  const stoneBumpCanvas = document.createElement('canvas');
  stoneCanvas.width = stoneBumpCanvas.width = 512;
  stoneCanvas.height = stoneBumpCanvas.height = 512;
  const stCtx = stoneCanvas.getContext('2d');
  const sbCtx = stoneBumpCanvas.getContext('2d');

  stCtx.fillStyle = '#262d3b';
  stCtx.fillRect(0, 0, 512, 512);
  sbCtx.fillStyle = '#808080';
  sbCtx.fillRect(0, 0, 512, 512);

  const courses = 10;
  const courseH = 512 / courses;
  for (let r = 0; r < courses; r++) {
    const y = r * courseH;
    let x = 0;
    while (x < 512) {
      const bw = 48 + Math.floor(rand() * 68);
      const shade = 34 + Math.floor(rand() * 24);
      stCtx.fillStyle = `rgb(${shade}, ${shade + 5}, ${shade + 14})`;
      stCtx.fillRect(x + 2, y + 2, bw - 4, courseH - 4);

      sbCtx.fillStyle = `rgb(${115 + Math.floor(rand() * 35)}, ${115 + Math.floor(rand() * 35)}, ${115 + Math.floor(rand() * 35)})`;
      sbCtx.fillRect(x + 3, y + 3, bw - 6, courseH - 6);

      stCtx.strokeStyle = '#11151d';
      stCtx.lineWidth = 3;
      stCtx.strokeRect(x, y, bw, courseH);

      sbCtx.strokeStyle = '#222222';
      sbCtx.lineWidth = 4;
      sbCtx.strokeRect(x, y, bw, courseH);
      x += bw;
    }
  }
  const stoneTex = new THREE.CanvasTexture(stoneCanvas);
  const stoneBumpTex = new THREE.CanvasTexture(stoneBumpCanvas);
  [stoneTex, stoneBumpTex].forEach((t) => {
    t.wrapS = THREE.RepeatWrapping;
    t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(3, 2);
  });

  const fortressWallMat = new THREE.MeshStandardMaterial({
    map: stoneTex,
    bumpMap: stoneBumpTex,
    bumpScale: 0.08,
    roughness: 0.9,
    metalness: 0.04
  });

  const distantStoneMat = new THREE.MeshStandardMaterial({
    map: stoneTex,
    roughness: 0.94,
    metalness: 0.02,
    color: 0x1e2636
  });

  const terracottaRoofMat = new THREE.MeshStandardMaterial({
    color: 0x45271f,
    roughness: 0.86,
    metalness: 0.05
  });

  // Dusty Battlefield Ground Plane
  const groundCanvas = document.createElement('canvas');
  groundCanvas.width = 512;
  groundCanvas.height = 512;
  const gCtx = groundCanvas.getContext('2d');
  gCtx.fillStyle = '#1a1511';
  gCtx.fillRect(0, 0, 512, 512);

  for (let i = 0; i < 900; i++) {
    const gx = rand() * 512;
    const gy = rand() * 512;
    const gr = 1 + rand() * 14;
    gCtx.fillStyle = i % 2 === 0 ? '#261f18' : '#120f0c';
    gCtx.globalAlpha = 0.16;
    gCtx.beginPath();
    gCtx.arc(gx, gy, gr, 0, Math.PI * 2);
    gCtx.fill();
  }
  const groundTex = new THREE.CanvasTexture(groundCanvas);
  groundTex.wrapS = THREE.RepeatWrapping;
  groundTex.wrapT = THREE.RepeatWrapping;
  groundTex.repeat.set(7, 7);

  const groundMat = new THREE.MeshStandardMaterial({
    map: groundTex,
    bumpMap: groundTex,
    bumpScale: 0.04,
    roughness: 0.95,
    metalness: 0.02
  });

  const ground = new THREE.Mesh(new THREE.CircleGeometry(75, 64), groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -1.25;
  ground.receiveShadow = true;
  envGroup.add(ground);

  // =========================================================================
  // 2. RIGHT SIDE: MONUMENTAL WALLS OF TROY, SCAEAN GATE & CITY BEYOND
  // =========================================================================
  // All gate & wall elements are placed in `troyComplex`, centered at GATE_CENTER_POS
  // and rotated by GATE_ROTATION_Y so:
  // - Local +Z points outward along the approach road toward the horse on the LEFT.
  // - Local -Z points inward through the gateway into the city of Troy on the RIGHT.
  const troyComplex = new THREE.Group();
  troyComplex.position.set(GATE_CENTER_POS.x, -1.25, GATE_CENTER_POS.z);
  troyComplex.rotation.y = GATE_ROTATION_Y;
  envGroup.add(troyComplex);

  const flameMeshes = [];

  // 2a. Dusty Approach Road with Parallel Wheel Ruts from Horse (local z = +10) through Gate into City (local z = -14)
  const roadCanvas = document.createElement('canvas');
  roadCanvas.width = 256;
  roadCanvas.height = 512;
  const rdCtx = roadCanvas.getContext('2d');
  rdCtx.fillStyle = '#2b2219';
  rdCtx.fillRect(0, 0, 256, 512);
  // Wheel tracks along the road
  rdCtx.strokeStyle = '#140f0a';
  rdCtx.lineWidth = 14;
  [82, 174].forEach((rx) => {
    rdCtx.beginPath();
    rdCtx.moveTo(rx, 0);
    rdCtx.lineTo(rx, 512);
    rdCtx.stroke();
  });
  const roadTex = new THREE.CanvasTexture(roadCanvas);
  roadTex.wrapS = THREE.RepeatWrapping;
  roadTex.wrapT = THREE.RepeatWrapping;
  roadTex.repeat.set(1, 5);

  const roadMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(3.5, 26),
    new THREE.MeshStandardMaterial({
      map: roadTex,
      roughness: 0.94,
      metalness: 0.02
    })
  );
  roadMesh.rotation.x = -Math.PI / 2;
  roadMesh.position.set(0, 0.012, -1.0);
  roadMesh.receiveShadow = true;
  troyComplex.add(roadMesh);

  // 2b. Monumental Scaean Gate Archway & Flanking Bastion Towers
  // Gateway clear opening is 3.8 units wide (x in [-1.9, +1.9]) and 5.6 units high (y in [0, 5.6])
  // so the 4.9-unit tall Trojan Horse rolls through with generous clearance!
  const buildBastionTower = (localX, localZ, width = 3.2, height = 7.8) => {
    const tGroup = new THREE.Group();
    tGroup.position.set(localX, 0, localZ);

    const shaft = new THREE.Mesh(
      new THREE.BoxGeometry(width, height, width),
      fortressWallMat
    );
    shaft.position.y = height / 2;
    shaft.castShadow = !isMobileViewport;
    shaft.receiveShadow = true;
    tGroup.add(shaft);

    const crown = new THREE.Mesh(
      new THREE.BoxGeometry(width * 1.08, 0.45, width * 1.08),
      fortressWallMat
    );
    crown.position.y = height + 0.18;
    tGroup.add(crown);

    for (let m = -1; m <= 1; m++) {
      const merlon = new THREE.Mesh(
        new THREE.BoxGeometry(width * 0.25, 0.48, 0.36),
        fortressWallMat
      );
      merlon.position.set(m * (width * 0.34), height + 0.62, width * 0.48);
      tGroup.add(merlon);
    }

    // Wall torch & glowing watchtower slit on front face (+Z)
    const slit = new THREE.Mesh(
      new THREE.PlaneGeometry(0.28, 0.8),
      new THREE.MeshBasicMaterial({ color: 0xffaa33 })
    );
    slit.position.set(0, height * 0.68, width / 2 + 0.03);
    tGroup.add(slit);
    flameMeshes.push(slit);

    // Burning torch sconce on lower tower face flanking the gate
    const torchFlame = new THREE.Mesh(
      new THREE.ConeGeometry(0.18, 0.42, 8),
      new THREE.MeshBasicMaterial({ color: 0xff9922 })
    );
    torchFlame.position.set(localX > 0 ? -width * 0.32 : width * 0.32, 3.2, width / 2 + 0.22);
    tGroup.add(torchFlame);
    flameMeshes.push(torchFlame);

    troyComplex.add(tGroup);
  };

  // Left (-X) and Right (+X) Gatehouse Bastion Towers framing the 3.8-unit wide Scaean Gate
  buildBastionTower(-3.55, 0, 3.3, 8.0);
  buildBastionTower(3.55, 0, 3.3, 8.0);

  // Outer Curtain Walls extending from the Gatehouse Towers
  const buildCurtainWall = (width, height, depth, localX, localZ, rotY = 0) => {
    const wGroup = new THREE.Group();
    wGroup.position.set(localX, 0, localZ);
    wGroup.rotation.y = rotY;

    const lowerWall = new THREE.Mesh(
      new THREE.BoxGeometry(width, height * 0.65, depth * 1.25),
      fortressWallMat
    );
    lowerWall.position.y = height * 0.325;
    lowerWall.receiveShadow = true;
    wGroup.add(lowerWall);

    const upperWall = new THREE.Mesh(
      new THREE.BoxGeometry(width, height * 0.38, depth),
      fortressWallMat
    );
    upperWall.position.y = height * 0.82;
    wGroup.add(upperWall);

    const merlonCount = Math.floor(width / 0.95);
    for (let m = 0; m < merlonCount; m++) {
      const mx = -width / 2 + 0.48 + m * 0.95;
      const merlon = new THREE.Mesh(
        new THREE.BoxGeometry(0.52, 0.45, depth * 0.45),
        fortressWallMat
      );
      merlon.position.set(mx, height + 0.22, depth * 0.25);
      wGroup.add(merlon);
    }

    troyComplex.add(wGroup);
  };

  buildCurtainWall(14.0, 6.2, 2.4, -11.8, -1.2, 0.18);
  buildCurtainWall(14.0, 6.2, 2.4, 11.8, -1.2, -0.18);
  buildBastionTower(-18.5, -2.5, 3.1, 7.2);
  buildBastionTower(18.5, -2.5, 3.1, 7.2);

  // High Stone Lintel Bridge & Crenellated Guard Gallery above the Scaean Gate (y = 5.65 to 7.35)
  const gateLintel = new THREE.Mesh(
    new THREE.BoxGeometry(4.2, 1.55, 2.6),
    fortressWallMat
  );
  gateLintel.position.set(0, 6.42, 0);
  troyComplex.add(gateLintel);

  for (let m = -2; m <= 2; m++) {
    const gateMerlon = new THREE.Mesh(
      new THREE.BoxGeometry(0.46, 0.45, 0.42),
      fortressWallMat
    );
    gateMerlon.position.set(m * 0.78, 7.42, 1.05);
    troyComplex.add(gateMerlon);
  }

  // -------------------------------------------------------------------------
  // 2c. HEAVY PIVOTED WOODEN & BRONZE DOUBLE DOORS OF THE SCAEAN GATE
  // Pivoted at x = -1.90 and x = +1.90 so they swing inward (-Z) smoothly!
  // -------------------------------------------------------------------------
  const gateTimberMat = new THREE.MeshStandardMaterial({
    color: 0x3b2211,
    roughness: 0.84,
    metalness: 0.1
  });
  const gateBronzeMat = new THREE.MeshStandardMaterial({
    color: 0x8f6829,
    roughness: 0.42,
    metalness: 0.8
  });

  const buildCityGateLeaf = (sideSign) => {
    // sideSign: -1 for left gate leaf (hinged at x = -1.90), +1 for right gate leaf (hinged at x = +1.90)
    const leafPivot = new THREE.Group();
    leafPivot.position.set(sideSign * 1.9, 0, 0.25);

    const leafWidth = 1.88;
    const leafHeight = 5.5;
    const xCenter = -sideSign * (leafWidth * 0.5);

    const timberPanel = new THREE.Mesh(
      new THREE.BoxGeometry(leafWidth, leafHeight, 0.28),
      gateTimberMat
    );
    timberPanel.position.set(xCenter, leafHeight * 0.5, 0);
    timberPanel.castShadow = !isMobileViewport;
    timberPanel.receiveShadow = true;
    leafPivot.add(timberPanel);

    // Vertical timber plank ribs on gate face
    for (let p = 0; p < 5; p++) {
      const px = -sideSign * (0.2 + p * 0.37);
      const rib = new THREE.Mesh(
        new THREE.BoxGeometry(0.08, leafHeight - 0.1, 0.32),
        gateTimberMat
      );
      rib.position.set(px, leafHeight * 0.5, 0);
      leafPivot.add(rib);
    }

    // Heavy horizontal bronze reinforcement straps & boss studs
    [0.8, 2.0, 3.2, 4.4].forEach((by) => {
      const strap = new THREE.Mesh(
        new THREE.BoxGeometry(leafWidth - 0.04, 0.16, 0.34),
        gateBronzeMat
      );
      strap.position.set(xCenter, by, 0);
      leafPivot.add(strap);
    });

    // Heavy timber push-bar jutting out at waist height for the Trojan gatekeepers
    const pushBar = new THREE.Mesh(
      new THREE.BoxGeometry(leafWidth * 0.75, 0.12, 0.24),
      gateBronzeMat
    );
    pushBar.position.set(xCenter, 1.05, 0.22);
    leafPivot.add(pushBar);

    troyComplex.add(leafPivot);
    return leafPivot;
  };

  const leftGatePivot = buildCityGateLeaf(-1);
  const rightGatePivot = buildCityGateLeaf(1);

  // -------------------------------------------------------------------------
  // 2d. FOUR VISIBLE 3D TROJAN GATEKEEPERS & WINCH MECHANISMS AT THE GATE
  // -------------------------------------------------------------------------
  const gatekeepers = [];

  // Two Gatekeepers pushing the heavy wooden gate panels open (positioned in front of each door leaf)
  [-1, 1].forEach((sideSign) => {
    const pusher = buildAncientWarriorCharacter({
      pose: 'pushing',
      tunicColor: 0x1e3a8a,
      plumeColor: 0xd97706,
      hasShield: false,
      hasSpear: false,
      scale: 0.96
    });
    // Positioned at the inner edge of each gate panel facing inward (-Z) to push the doors open
    pusher.root.position.set(sideSign * 0.85, 0, 0.82);
    pusher.root.rotation.y = Math.PI; // Faces -Z (into the gate panels)
    pusher.sideSign = sideSign;
    pusher.role = 'pusher';
    pusher.startPos = pusher.root.position.clone();
    troyComplex.add(pusher.root);
    gatekeepers.push(pusher);
  });

  // Two Gatekeepers operating bronze-and-timber capstan winches flanking the gateway
  const winchDrums = [];
  [-1, 1].forEach((sideSign) => {
    const winchGroup = new THREE.Group();
    winchGroup.position.set(sideSign * 2.45, 0, 1.85);
    troyComplex.add(winchGroup);

    const base = new THREE.Mesh(
      new THREE.CylinderGeometry(0.28, 0.32, 0.22, 10),
      fortressWallMat
    );
    base.position.y = 0.11;
    winchGroup.add(base);

    const drum = new THREE.Group();
    drum.position.y = 0.55;
    const cylinder = new THREE.Mesh(
      new THREE.CylinderGeometry(0.18, 0.18, 0.65, 10),
      gateTimberMat
    );
    drum.add(cylinder);

    // Capstan levers
    [0, Math.PI / 2].forEach((ang) => {
      const bar = new THREE.Mesh(
        new THREE.CylinderGeometry(0.03, 0.03, 1.15, 6),
        gateBronzeMat
      );
      bar.rotation.z = Math.PI / 2;
      bar.rotation.y = ang;
      bar.position.y = 0.18;
      drum.add(bar);
    });
    winchGroup.add(drum);
    winchDrums.push({ drum, sideSign });

    // Gatekeeper stationed at the capstan winch bar
    const operator = buildAncientWarriorCharacter({
      pose: 'winch',
      tunicColor: 0x0f766e,
      plumeColor: 0xf59e0b,
      hasShield: false,
      hasSpear: false,
      scale: 0.96
    });
    operator.root.position.set(sideSign * 2.45, 0, 2.38);
    operator.root.rotation.y = Math.PI * 0.85 * sideSign;
    operator.sideSign = sideSign;
    operator.role = 'winch';
    operator.startPos = operator.root.position.clone();
    troyComplex.add(operator.root);
    gatekeepers.push(operator);
  });

  // -------------------------------------------------------------------------
  // 2e. COLONNADED ANCIENT CITY STREET & ACROPOLIS BEYOND THE GATES (local z < 0)
  // Visible straight through the open Scaean Gate and above the battlements!
  // -------------------------------------------------------------------------
  const windowLightMat = new THREE.MeshBasicMaterial({ color: 0xffb347 });

  // Colonnaded street buildings flanking the main avenue inside Troy (local z = -2.5 to -16)
  for (let s = 0; s < 5; s++) {
    const lz = -3.0 - s * 2.7;
    [-1, 1].forEach((sideSign) => {
      const lx = sideSign * 3.4;

      // Doric street column with burning brazier
      const col = new THREE.Mesh(
        new THREE.CylinderGeometry(0.22, 0.26, 4.2, 10),
        fortressWallMat
      );
      col.position.set(lx * 0.72, 2.1, lz);
      troyComplex.add(col);

      // Street torch flame illuminating the interior avenue
      const streetFlame = new THREE.Mesh(
        new THREE.ConeGeometry(0.14, 0.34, 6),
        windowLightMat
      );
      streetFlame.position.set(lx * 0.65, 2.8, lz);
      troyComplex.add(streetFlame);
      flameMeshes.push(streetFlame);

      // Multi-story Trojan stone building behind the colonnade
      const bh = 4.5 + (s % 3) * 1.4;
      const bw = 2.4;
      const bd = 2.2;
      const bldg = new THREE.Group();
      bldg.position.set(lx * 1.35, 0, lz);

      const body = new THREE.Mesh(new THREE.BoxGeometry(bw, bh, bd), distantStoneMat);
      body.position.y = bh / 2;
      bldg.add(body);

      const roof = new THREE.Mesh(
        new THREE.ConeGeometry(bw * 0.78, 1.05, 4),
        terracottaRoofMat
      );
      roof.rotation.y = Math.PI / 4;
      roof.position.y = bh + 0.5;
      bldg.add(roof);

      const win = new THREE.Mesh(new THREE.PlaneGeometry(0.26, 0.42), windowLightMat);
      win.position.set(-sideSign * (bw / 2 + 0.02), bh * 0.68, 0);
      win.rotation.y = -sideSign * (Math.PI / 2);
      bldg.add(win);

      troyComplex.add(bldg);
    });
  }

  // Additional terraced city buildings rising behind the walls
  const extraBuildings = isMobileViewport ? 14 : 26;
  for (let b = 0; b < extraBuildings; b++) {
    const bx = (rand() - 0.5) * 28;
    if (Math.abs(bx) < 4.5) continue; // Keep central street clear
    const bz = -4.0 - rand() * 14.0;
    const bw = 1.8 + rand() * 2.2;
    const bd = 1.8 + rand() * 2.2;
    const bh = 4.2 + rand() * 4.5;

    const bldg = new THREE.Group();
    bldg.position.set(bx, (-bz - 3) * 0.16, bz);

    const body = new THREE.Mesh(new THREE.BoxGeometry(bw, bh, bd), distantStoneMat);
    body.position.y = bh / 2;
    bldg.add(body);

    const roof = new THREE.Mesh(
      new THREE.ConeGeometry(Math.max(bw, bd) * 0.76, 0.95, 4),
      terracottaRoofMat
    );
    roof.rotation.y = Math.PI / 4;
    roof.position.y = bh + 0.45;
    bldg.add(roof);

    const win = new THREE.Mesh(new THREE.PlaneGeometry(0.24, 0.36), windowLightMat);
    win.position.set(0, bh * 0.72, bd / 2 + 0.03);
    bldg.add(win);

    troyComplex.add(bldg);
  }

  // Elevated Acropolis Hill & Temple of Athena Silhouette rising above Troy's walls
  const acropolisGroup = new THREE.Group();
  acropolisGroup.position.set(0, 7.2, -16.5);

  const citadelRock = new THREE.Mesh(
    new THREE.CylinderGeometry(5.5, 8.2, 5.2, 12),
    distantStoneMat
  );
  citadelRock.position.y = -2.5;
  acropolisGroup.add(citadelRock);

  const stylobate = new THREE.Mesh(
    new THREE.BoxGeometry(7.2, 0.55, 4.4),
    fortressWallMat
  );
  stylobate.position.y = 0.25;
  acropolisGroup.add(stylobate);

  for (let c = 0; c < 8; c++) {
    const cx = -3.1 + (c / 7) * 6.2;
    const col = new THREE.Mesh(
      new THREE.CylinderGeometry(0.17, 0.21, 2.4, 10),
      fortressWallMat
    );
    col.position.set(cx, 1.7, 1.85);
    acropolisGroup.add(col);
  }

  const cella = new THREE.Mesh(
    new THREE.BoxGeometry(5.0, 2.3, 2.8),
    distantStoneMat
  );
  cella.position.set(0, 1.65, 0);
  acropolisGroup.add(cella);

  const entablature = new THREE.Mesh(
    new THREE.BoxGeometry(7.3, 0.4, 4.4),
    fortressWallMat
  );
  entablature.position.y = 3.05;
  acropolisGroup.add(entablature);

  const pediment = new THREE.Mesh(
    new THREE.ConeGeometry(5.2, 1.3, 4),
    terracottaRoofMat
  );
  pediment.rotation.y = Math.PI / 4;
  pediment.scale.set(1.0, 1.0, 0.62);
  pediment.position.y = 3.88;
  acropolisGroup.add(pediment);

  troyComplex.add(acropolisGroup);

  // =========================================================================
  // 3. CENTER APPROACH DETAILS (Torch Stands & Scattered Stones Flanking Road)
  // =========================================================================
  const rockMat = new THREE.MeshStandardMaterial({
    color: 0x2c2723,
    roughness: 0.92,
    metalness: 0.04
  });

  // Flanking Iron Torch Stands along the sides of the approach road (local |x| > 2.3 so road is 100% clear)
  [3.6, 6.8].forEach((lz) => {
    [-2.55, 2.55].forEach((lx) => {
      const bGroup = new THREE.Group();
      bGroup.position.set(lx, 0, lz);

      const bowl = new THREE.Mesh(
        new THREE.CylinderGeometry(0.28, 0.12, 0.22, 10),
        new THREE.MeshStandardMaterial({ color: 0x1e2024, roughness: 0.6, metalness: 0.7 })
      );
      bowl.position.y = 0.85;
      bGroup.add(bowl);

      const post = new THREE.Mesh(
        new THREE.CylinderGeometry(0.04, 0.05, 0.85, 8),
        bowl.material
      );
      post.position.y = 0.42;
      bGroup.add(post);

      const fire = new THREE.Mesh(
        new THREE.ConeGeometry(0.2, 0.45, 8),
        new THREE.MeshBasicMaterial({ color: 0xff9d2e })
      );
      fire.position.y = 1.08;
      bGroup.add(fire);
      flameMeshes.push(fire);

      troyComplex.add(bGroup);
    });
  });

  // Scattered stones outside the road margins (|local x| > 2.4)
  for (let i = 0; i < (isMobileViewport ? 18 : 36); i++) {
    const side = i % 2 === 0 ? -1 : 1;
    const lx = side * (2.5 + rand() * 5.5);
    const lz = 1.5 + rand() * 11.0;
    const rock = new THREE.Mesh(
      new THREE.DodecahedronGeometry(0.09 + rand() * 0.18, 1),
      rockMat
    );
    rock.scale.set(1.2, 0.65, 1.0);
    rock.position.set(lx, 0.04, lz);
    rock.rotation.set(rand(), rand(), rand());
    troyComplex.add(rock);
  }

  // =========================================================================
  // 4. MEDITERRANEAN NIGHT SKY: STARFIELD, MOON & VOLUMETRIC HAZE
  // =========================================================================
  const starCount = isMobileViewport ? 140 : 320;
  const starGeo = new THREE.BufferGeometry();
  const starPositions = new Float32Array(starCount * 3);
  for (let s = 0; s < starCount; s++) {
    starPositions[s * 3] = (rand() - 0.5) * 95;
    starPositions[s * 3 + 1] = 8 + rand() * 34;
    starPositions[s * 3 + 2] = -26 - rand() * 25;
  }
  starGeo.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
  const starMat = new THREE.PointsMaterial({
    color: 0xe2e8f0,
    size: 0.14,
    transparent: true,
    opacity: 0.65,
    depthWrite: false
  });
  envGroup.add(new THREE.Points(starGeo, starMat));

  // Textured Moon in Upper Sky
  const moonGroup = new THREE.Group();
  moonGroup.position.set(-10.5, 13.5, -30);
  const moonDisc = new THREE.Mesh(
    new THREE.SphereGeometry(1.4, 24, 24),
    new THREE.MeshBasicMaterial({ color: 0xeff6ff })
  );
  const moonHalo = new THREE.Mesh(
    new THREE.SphereGeometry(2.8, 24, 24),
    new THREE.MeshBasicMaterial({
      color: 0x93c5fd,
      transparent: true,
      opacity: 0.14,
      depthWrite: false
    })
  );
  moonGroup.add(moonDisc);
  moonGroup.add(moonHalo);
  envGroup.add(moonGroup);

  // Volumetric Mist / Haze Planes
  const mistCanvas = document.createElement('canvas');
  mistCanvas.width = 256;
  mistCanvas.height = 256;
  const mCtx = mistCanvas.getContext('2d');
  const mGrad = mCtx.createRadialGradient(128, 128, 10, 128, 128, 120);
  mGrad.addColorStop(0, 'rgba(148, 163, 184, 0.20)');
  mGrad.addColorStop(0.5, 'rgba(71, 85, 105, 0.09)');
  mGrad.addColorStop(1, 'rgba(15, 23, 42, 0)');
  mCtx.fillStyle = mGrad;
  mCtx.fillRect(0, 0, 256, 256);
  const mistTex = new THREE.CanvasTexture(mistCanvas);

  const hazePlanes = [];
  const hazeConfigs = [
    { x: -4, y: 1.4, z: -7.5, w: 18, h: 6.0, speed: 0.16 },
    { x: 5, y: 1.6, z: -8.5, w: 20, h: 6.5, speed: -0.13 },
    { x: 0, y: 2.5, z: -14.0, w: 28, h: 8.0, speed: 0.1 }
  ];
  hazeConfigs.forEach((cfg) => {
    const hMat = new THREE.MeshBasicMaterial({
      map: mistTex,
      transparent: true,
      opacity: 0.5,
      depthWrite: false
    });
    const plane = new THREE.Mesh(new THREE.PlaneGeometry(cfg.w, cfg.h), hMat);
    plane.position.set(cfg.x, cfg.y, cfg.z);
    envGroup.add(plane);
    hazePlanes.push({ mesh: plane, baseX: cfg.x, speed: cfg.speed });
  });

  return {
    envGroup,
    troyComplex,
    leftGatePivot,
    rightGatePivot,
    gatekeepers,
    winchDrums,
    flameMeshes,
    hazePlanes
  };
}
