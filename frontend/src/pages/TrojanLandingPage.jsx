import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import {
  Shield,
  Lock,
  Key,
  ArrowLeft,
  GraduationCap,
  User,
  AlertCircle,
  X,
  Eye,
  EyeOff,
  ChevronDown,
  Layers,
  Cpu,
  FastForward
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import {
  buildUltraRealisticTrojanHorse,
  buildAncientTroyEnvironment,
  HORSE_START_POS,
  HORSE_CITY_DEST_POS,
  HORSE_BASE_ROTATION_Y,
  GATE_CENTER_POS
} from './trojanSceneBuilder';

/**
 * Deterministic Animation State Machine States:
 * EXTERIOR -> ENTERING_HORSE -> LOGIN -> AUTHENTICATING -> EXITING_HORSE -> OPENING_GATES -> ENTERING_CITY -> DASHBOARD
 */

/**
 * Reusable JNNCE College Emblem component with aspect-ratio preservation and graceful fallback.
 */
const CollegeEmblem = ({ sizeClass = 'h-11 w-11', imgClass = 'h-full w-full object-contain', alt }) => {
  const [imgError, setImgError] = useState(false);

  return (
    <div
      className={`${sizeClass} rounded-xl bg-[#131b2e]/90 border border-[#d4af37]/40 shadow-md p-1.5 flex items-center justify-center shrink-0 overflow-hidden`}
    >
      {!imgError ? (
        <img
          src="/jnnce_logo.png"
          alt={alt || 'Jawaharlal Nehru National College of Engineering (JNNCE), Shivamogga Official Emblem'}
          className={imgClass}
          loading="eager"
          onError={() => setImgError(true)}
        />
      ) : (
        <div className="flex flex-col items-center justify-center text-[#d4af37] text-center p-1">
          <GraduationCap className="h-5 w-5 stroke-[1.8]" />
          <span className="text-[8px] font-serif font-bold tracking-wider uppercase mt-0.5">JNNCE</span>
        </div>
      )}
    </div>
  );
};

export const TrojanLandingPage = ({ onSuccessLogin, onSwitchLanding }) => {
  const containerRef = useRef(null);
  const projectInfoRef = useRef(null);
  const { login } = useAuth();

  // Deterministic State Machine:
  // 'EXTERIOR' | 'ENTERING_HORSE' | 'LOGIN' | 'AUTHENTICATING' | 'EXITING_HORSE' | 'OPENING_GATES' | 'ENTERING_CITY' | 'DASHBOARD'
  const [sceneState, setSceneState] = useState('EXTERIOR');
  const [statusCaption, setStatusCaption] = useState('');
  const [webglAvailable, setWebglAvailable] = useState(true);
  const [fadeOverlayOpacity, setFadeOverlayOpacity] = useState(0);

  // Login Form States inside the Trojan Horse timber chamber
  const [selectedRole, setSelectedRole] = useState('Admin');
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [showPassword, setShowPassword] = useState(false);
  const [loginError, setLoginError] = useState('');
  const [showForgotModal, setShowForgotModal] = useState(false);

  // Refs to coordinate between React UI and Three.js animation loop without stale closures
  const sceneStateRef = useRef('EXTERIOR');
  const authSucceededRef = useRef(false);
  const dashboardTriggeredRef = useRef(false);
  const triggerEnterHorseRef = useRef(null);
  const triggerBackToExteriorRef = useRef(null);
  const triggerPostLoginVictoryRef = useRef(null);

  const updateSceneState = (nextState, caption = '') => {
    sceneStateRef.current = nextState;
    setSceneState(nextState);
    setStatusCaption(caption);
  };

  const completeToDashboard = () => {
    if (dashboardTriggeredRef.current) return;
    dashboardTriggeredRef.current = true;
    updateSceneState('DASHBOARD', '');
    if (onSuccessLogin) {
      onSuccessLogin();
    }
  };

  const handleRoleSelect = (roleName) => {
    if (sceneState === 'AUTHENTICATING') return;
    setSelectedRole(roleName);
    setLoginError('');
    if (roleName === 'Admin') {
      setUsername('admin');
      setPassword('admin123');
    } else {
      setUsername('analyst');
      setPassword('analyst123');
    }
  };

  const handleExploreProject = () => {
    projectInfoRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const handleTriggerLoginPortal = () => {
    if (sceneStateRef.current !== 'EXTERIOR') return;
    setLoginError('');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (triggerEnterHorseRef.current) {
      triggerEnterHorseRef.current();
    } else {
      updateSceneState('LOGIN', '');
    }
  };

  const handleBackToExterior = () => {
    if (sceneStateRef.current !== 'LOGIN') return;
    setLoginError('');
    if (triggerBackToExteriorRef.current) {
      triggerBackToExteriorRef.current();
    } else {
      updateSceneState('EXTERIOR', '');
    }
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    if (sceneStateRef.current !== 'LOGIN') return;

    setLoginError('');
    updateSceneState('AUTHENTICATING', 'Verifying Zero Trust Credentials...');

    try {
      await login(username, password, selectedRole);
      authSucceededRef.current = true;

      // Only after backend confirms valid authentication do we trigger the post-login sequence:
      // EXITING_HORSE (Phase B & C) -> OPENING_GATES (Phase D) -> ENTERING_CITY (Phase E & F) -> DASHBOARD
      if (triggerPostLoginVictoryRef.current) {
        triggerPostLoginVictoryRef.current();
      } else {
        completeToDashboard();
      }
    } catch (err) {
      // Remain inside the horse in LOGIN state and display error; do NOT move horse or open gates
      authSucceededRef.current = false;
      updateSceneState('LOGIN', '');
      setLoginError(err?.message || 'Invalid username or password credentials.');
    }
  };

  // Three.js Scene: Left = Trojan Horse, Center = Dusty Road, Right = City Wall & Scaean Gate of Troy
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const prefersReducedMotion =
      typeof window !== 'undefined' &&
      window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isMobileViewport = window.innerWidth < 768;

    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({
        antialias: !isMobileViewport,
        alpha: false,
        powerPreference: 'high-performance'
      });
    } catch (err) {
      console.warn('WebGL unavailable, falling back to static view:', err);
      setWebglAvailable(false);
      return;
    }

    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, isMobileViewport ? 1.5 : 2));
    renderer.shadowMap.enabled = !isMobileViewport;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.18;
    container.appendChild(renderer.domElement);

    // 1. Scene & Atmospheric Midnight Fog
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x060a12);
    scene.fog = new THREE.FogExp2(0x080e1a, 0.022);

    // 2. Wide-Angle Cinematic Camera Framing
    const camera = new THREE.PerspectiveCamera(
      48,
      container.clientWidth / container.clientHeight,
      0.1,
      190
    );

    const getExteriorCameraPos = () => {
      const w = container.clientWidth;
      if (w < 640) return new THREE.Vector3(0.2, 2.35, 14.5);
      if (w < 1024) return new THREE.Vector3(0.2, 2.25, 12.6);
      return new THREE.Vector3(0.2, 2.15, 11.2);
    };

    const getExteriorLookAt = () => {
      return new THREE.Vector3(0.35, 1.55, 0.15);
    };

    const initialCamPos = getExteriorCameraPos();
    const initialLookAt = getExteriorLookAt();
    camera.position.copy(initialCamPos);
    camera.lookAt(initialLookAt);

    // 3. Dual-Temperature Cinematic Lighting
    const hemiLight = new THREE.HemisphereLight(0x4b638e, 0x241911, 1.25);
    scene.add(hemiLight);

    const moonLight = new THREE.DirectionalLight(0x93c5fd, 2.1);
    moonLight.position.set(-10, 16, -8);
    moonLight.castShadow = !isMobileViewport;
    if (!isMobileViewport) {
      moonLight.shadow.mapSize.width = 2048;
      moonLight.shadow.mapSize.height = 2048;
      moonLight.shadow.camera.near = 1;
      moonLight.shadow.camera.far = 48;
      moonLight.shadow.camera.left = -12;
      moonLight.shadow.camera.right = 12;
      moonLight.shadow.camera.top = 10;
      moonLight.shadow.camera.bottom = -4;
      moonLight.shadow.bias = -0.0005;
    }
    scene.add(moonLight);

    const coolRimLight = new THREE.DirectionalLight(0x7dd3fc, 1.15);
    coolRimLight.position.set(-8.5, 6.0, 7.5);
    scene.add(coolRimLight);

    const horseFaceSpot = new THREE.SpotLight(0xfbbf24, 5.2, 26, Math.PI / 2.6, 0.45, 1.0);
    horseFaceSpot.position.set(-1.2, 4.8, 7.8);
    horseFaceSpot.target.position.set(HORSE_START_POS.x + 1.2, 2.4, HORSE_START_POS.z);
    scene.add(horseFaceSpot);
    scene.add(horseFaceSpot.target);

    const gateTorchLight = new THREE.PointLight(0xf59e0b, 4.2, 24, 1.15);
    gateTorchLight.position.set(GATE_CENTER_POS.x - 1.2, 2.4, GATE_CENTER_POS.z + 2.2);
    scene.add(gateTorchLight);

    const cityInteriorLight = new THREE.PointLight(0xff9d2e, 3.8, 26, 1.1);
    cityInteriorLight.position.set(GATE_CENTER_POS.x + 3.5, 2.8, GATE_CENTER_POS.z - 2.0);
    scene.add(cityInteriorLight);

    const interiorChamberLight = new THREE.PointLight(0xffb84d, 0.6, 5.5, 1.0);
    interiorChamberLight.position.set(0.15, 1.65, 0);

    const interiorFillLight = new THREE.PointLight(0xff9e3d, 0.3, 4.5, 1.1);
    interiorFillLight.position.set(-0.25, 1.35, 0);

    // 4. Build Ancient Troy
    const {
      leftGatePivot,
      rightGatePivot,
      gatekeepers,
      winchDrums,
      flameMeshes,
      hazePlanes
    } = buildAncientTroyEnvironment(scene, isMobileViewport);

    // 5. Build Monumental Wooden Trojan Horse
    const horseRoot = new THREE.Group();
    horseRoot.position.copy(HORSE_START_POS);
    horseRoot.rotation.y = HORSE_BASE_ROTATION_Y;
    horseRoot.add(interiorChamberLight);
    horseRoot.add(interiorFillLight);
    scene.add(horseRoot);

    const {
      leftHatchPivot,
      rightHatchPivot,
      soldiers,
      wheels
    } = buildUltraRealisticTrojanHorse(horseRoot);

    const loader = new GLTFLoader();
    loader.load(
      '/models/trojan_horse.glb',
      (gltf) => {
        const customModel = gltf.scene;
        customModel.scale.set(1.4, 1.4, 1.4);
        customModel.position.set(0, -1.1, 0);
        horseRoot.add(customModel);
      },
      undefined,
      () => {}
    );

    // 6. Atmospheric Ground Dust Motes
    const dustCount = prefersReducedMotion ? 25 : isMobileViewport ? 60 : 120;
    const dustGeo = new THREE.BufferGeometry();
    const dustPositions = new Float32Array(dustCount * 3);
    const dustSpeeds = new Float32Array(dustCount);

    for (let i = 0; i < dustCount; i++) {
      dustPositions[i * 3] = (Math.random() - 0.5) * 18;
      dustPositions[i * 3 + 1] = -1.18 + Math.random() * 3.2;
      dustPositions[i * 3 + 2] = -5 + Math.random() * 10;
      dustSpeeds[i] = 0.0015 + Math.random() * 0.003;
    }
    dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPositions, 3));

    const dustMat = new THREE.PointsMaterial({
      color: 0xd6b87c,
      size: isMobileViewport ? 0.038 : 0.045,
      transparent: true,
      opacity: 0.45,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });
    const dustParticles = new THREE.Points(dustGeo, dustMat);
    scene.add(dustParticles);

    // 7. Helper to compute exact World Coordinates
    const getHorsePointsWorld = () => {
      horseRoot.updateMatrixWorld(true);
      const hatchApproachWorld = horseRoot.localToWorld(new THREE.Vector3(-2.75, 1.46, 0));
      const hatchThresholdWorld = horseRoot.localToWorld(new THREE.Vector3(-1.18, 1.42, 0));
      const interiorCamWorld = horseRoot.localToWorld(new THREE.Vector3(-0.42, 1.42, 0));
      const interiorLookWorld = horseRoot.localToWorld(new THREE.Vector3(0.85, 1.36, 0));
      return {
        hatchApproachWorld,
        hatchThresholdWorld,
        interiorCamWorld,
        interiorLookWorld
      };
    };

    const easeInOutCubic = (x) =>
      x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;

    let animFrameId = null;

    // TRANSITION 1: EXTERIOR -> ENTERING_HORSE -> LOGIN
    triggerEnterHorseRef.current = () => {
      if (sceneStateRef.current !== 'EXTERIOR') return;

      const {
        hatchApproachWorld,
        hatchThresholdWorld,
        interiorCamWorld,
        interiorLookWorld
      } = getHorsePointsWorld();

      if (prefersReducedMotion) {
        if (leftHatchPivot && rightHatchPivot) {
          leftHatchPivot.rotation.y = Math.PI * 0.65;
          rightHatchPivot.rotation.y = -Math.PI * 0.65;
        }
        interiorChamberLight.intensity = 4.6;
        interiorFillLight.intensity = 2.6;
        camera.position.copy(interiorCamWorld);
        camera.lookAt(interiorLookWorld);
        updateSceneState('LOGIN', '');
        return;
      }

      updateSceneState('ENTERING_HORSE', 'Approaching Trojan Horse & Unsealing Concealed Hatch...');
      const startCamPos = camera.position.clone();
      const startLook = getExteriorLookAt();
      const duration = 2850;
      const startTime = performance.now();

      const stepEnter = (now) => {
        if (sceneStateRef.current !== 'ENTERING_HORSE') return;
        const rawT = Math.min((now - startTime) / duration, 1);
        const t = easeInOutCubic(rawT);

        if (rawT > 0.35 && rawT < 0.72) {
          setStatusCaption('Unsealing Concealed Timber Hatch...');
        } else if (rawT >= 0.72) {
          setStatusCaption('Entering Hollow Chamber — Greek Soldiers Concealed Inside...');
        }

        const doorProgress = Math.max(0, Math.min((rawT - 0.20) / 0.45, 1));
        const doorEase = easeInOutCubic(doorProgress);
        if (leftHatchPivot && rightHatchPivot) {
          leftHatchPivot.rotation.y = doorEase * (Math.PI * 0.65);
          rightHatchPivot.rotation.y = -doorEase * (Math.PI * 0.65);
        }

        if (rawT < 0.56) {
          const p1 = easeInOutCubic(rawT / 0.56);
          camera.position.lerpVectors(startCamPos, hatchApproachWorld, p1);
          const lookCur = new THREE.Vector3().lerpVectors(startLook, hatchThresholdWorld, p1);
          camera.lookAt(lookCur);
        } else {
          const p2 = easeInOutCubic((rawT - 0.56) / 0.44);
          camera.position.lerpVectors(hatchApproachWorld, interiorCamWorld, p2);
          camera.lookAt(interiorLookWorld);
        }

        interiorChamberLight.intensity = THREE.MathUtils.lerp(0.6, 4.6, t);
        interiorFillLight.intensity = THREE.MathUtils.lerp(0.3, 2.6, t);
        moonLight.intensity = THREE.MathUtils.lerp(2.1, 0.45, t);

        if (rawT < 1) {
          requestAnimationFrame(stepEnter);
        } else {
          updateSceneState('LOGIN', '');
        }
      };

      requestAnimationFrame(stepEnter);
    };

    // TRANSITION 2: LOGIN -> BACK TO EXTERIOR
    triggerBackToExteriorRef.current = () => {
      if (sceneStateRef.current !== 'LOGIN') return;

      const extPos = getExteriorCameraPos();
      const extLook = getExteriorLookAt();
      const { hatchApproachWorld, interiorLookWorld } = getHorsePointsWorld();

      if (prefersReducedMotion) {
        if (leftHatchPivot && rightHatchPivot) {
          leftHatchPivot.rotation.y = 0;
          rightHatchPivot.rotation.y = 0;
        }
        interiorChamberLight.intensity = 0.6;
        interiorFillLight.intensity = 0.3;
        moonLight.intensity = 2.1;
        camera.position.copy(extPos);
        camera.lookAt(extLook);
        updateSceneState('EXTERIOR', '');
        return;
      }

      updateSceneState('ENTERING_HORSE', 'Returning to Exterior Battlefield...');
      const startPos = camera.position.clone();
      const duration = 2000;
      const startTime = performance.now();

      const stepBack = (now) => {
        const rawT = Math.min((now - startTime) / duration, 1);
        const t = easeInOutCubic(rawT);

        if (rawT < 0.45) {
          const s1 = easeInOutCubic(rawT / 0.45);
          camera.position.lerpVectors(startPos, hatchApproachWorld, s1);
          camera.lookAt(interiorLookWorld);
        } else {
          const s2 = easeInOutCubic((rawT - 0.45) / 0.55);
          camera.position.lerpVectors(hatchApproachWorld, extPos, s2);
          const lookCur = new THREE.Vector3().lerpVectors(interiorLookWorld, extLook, s2);
          camera.lookAt(lookCur);
        }

        const closeT = easeInOutCubic(Math.max(0, Math.min((rawT - 0.35) / 0.55, 1)));
        if (leftHatchPivot && rightHatchPivot) {
          leftHatchPivot.rotation.y = THREE.MathUtils.lerp(Math.PI * 0.65, 0, closeT);
          rightHatchPivot.rotation.y = THREE.MathUtils.lerp(-Math.PI * 0.65, 0, closeT);
        }

        interiorChamberLight.intensity = THREE.MathUtils.lerp(4.6, 0.6, t);
        interiorFillLight.intensity = THREE.MathUtils.lerp(2.6, 0.3, t);
        moonLight.intensity = THREE.MathUtils.lerp(0.45, 2.1, t);

        if (rawT < 1) {
          requestAnimationFrame(stepBack);
        } else {
          updateSceneState('EXTERIOR', '');
        }
      };

      requestAnimationFrame(stepBack);
    };

    // TRANSITION 3: POST-LOGIN VICTORY SEQUENCE
    triggerPostLoginVictoryRef.current = () => {
      if (!authSucceededRef.current) return;

      if (prefersReducedMotion) {
        completeToDashboard();
        return;
      }

      const safetyTimeout = setTimeout(() => {
        completeToDashboard();
      }, 13500);

      updateSceneState(
        'EXITING_HORSE',
        'Authentication Verified — Greek Soldiers Prepare Inside the Trojan Horse...'
      );

      const {
        hatchApproachWorld,
        hatchThresholdWorld,
        interiorCamWorld,
        interiorLookWorld
      } = getHorsePointsWorld();
      const extPos = getExteriorCameraPos();
      const extLook = getExteriorLookAt();

      const exitDuration = 3000;
      const exitStart = performance.now();

      const runExitingHorse = (now) => {
        if (dashboardTriggeredRef.current) {
          clearTimeout(safetyTimeout);
          return;
        }
        const rawT = Math.min((now - exitStart) / exitDuration, 1);

        if (rawT < 0.38) {
          const reactT = easeInOutCubic(rawT / 0.38);
          interiorChamberLight.intensity = THREE.MathUtils.lerp(4.6, 6.4, reactT);
          interiorFillLight.intensity = THREE.MathUtils.lerp(2.6, 3.8, reactT);

          soldiers.forEach((s, idx) => {
            const sideDir = idx < 3 ? -1 : 1;
            s.headPivot.rotation.y = sideDir * reactT * 0.48;
            s.upperBody.rotation.x = reactT * 0.16;
            s.rightArmPivot.rotation.x = -0.45 - reactT * 0.42;
            s.leftArmPivot.rotation.x = -0.35 - reactT * 0.25;
          });

          camera.position.lerpVectors(
            interiorCamWorld,
            horseRoot.localToWorld(new THREE.Vector3(-0.62, 1.42, 0)),
            reactT * 0.5
          );
          camera.lookAt(interiorLookWorld);
        } else {
          setStatusCaption('Sealing Concealed Hatch — Preparing Trojan Horse Before the Gates of Troy...');
          const exitT = (rawT - 0.38) / 0.62;

          if (exitT < 0.45) {
            const p1 = easeInOutCubic(exitT / 0.45);
            camera.position.lerpVectors(interiorCamWorld, hatchApproachWorld, p1);
            const lookCur = new THREE.Vector3().lerpVectors(
              interiorLookWorld,
              hatchThresholdWorld,
              p1
            );
            camera.lookAt(lookCur);
          } else {
            const p2 = easeInOutCubic((exitT - 0.45) / 0.55);
            camera.position.lerpVectors(hatchApproachWorld, extPos, p2);
            const lookCur = new THREE.Vector3().lerpVectors(hatchThresholdWorld, extLook, p2);
            camera.lookAt(lookCur);
          }

          const sealT = easeInOutCubic(Math.max(0, Math.min((exitT - 0.35) / 0.55, 1)));
          if (leftHatchPivot && rightHatchPivot) {
            leftHatchPivot.rotation.y = THREE.MathUtils.lerp(Math.PI * 0.65, 0, sealT);
            rightHatchPivot.rotation.y = THREE.MathUtils.lerp(-Math.PI * 0.65, 0, sealT);
          }

          const fadeLightT = easeInOutCubic(exitT);
          interiorChamberLight.intensity = THREE.MathUtils.lerp(6.4, 0.5, fadeLightT);
          interiorFillLight.intensity = THREE.MathUtils.lerp(3.8, 0.2, fadeLightT);
          moonLight.intensity = THREE.MathUtils.lerp(0.45, 2.1, fadeLightT);
        }

        if (rawT < 1) {
          requestAnimationFrame(runExitingHorse);
        } else {
          startOpeningGates(safetyTimeout);
        }
      };

      requestAnimationFrame(runExitingHorse);
    };

    const startOpeningGates = (safetyTimeout) => {
      if (dashboardTriggeredRef.current) return;
      updateSceneState(
        'OPENING_GATES',
        'Trojan Gatekeepers Unbarring and Opening the Monumental Scaean Gate...'
      );

      const startCamPos = camera.position.clone();
      const startLook = getExteriorLookAt();
      const gateFocusCamPos = new THREE.Vector3(0.65, 2.15, 10.6);
      const gateFocusLook = new THREE.Vector3(1.15, 1.6, -0.15);

      const gateDuration = 3200;
      const gateStart = performance.now();

      const runOpeningGates = (now) => {
        if (dashboardTriggeredRef.current) {
          clearTimeout(safetyTimeout);
          return;
        }
        const rawT = Math.min((now - gateStart) / gateDuration, 1);
        const t = easeInOutCubic(rawT);

        camera.position.lerpVectors(startCamPos, gateFocusCamPos, t);
        const curLook = new THREE.Vector3().lerpVectors(startLook, gateFocusLook, t);
        camera.lookAt(curLook);

        const maxGateAngle = Math.PI * 0.56;
        if (leftGatePivot && rightGatePivot) {
          leftGatePivot.rotation.y = t * maxGateAngle;
          rightGatePivot.rotation.y = -t * maxGateAngle;
        }

        winchDrums.forEach(({ drum, sideSign }) => {
          drum.rotation.y = sideSign * rawT * Math.PI * 3.5;
        });

        gatekeepers.forEach((gk) => {
          const walkCycle = Math.sin(rawT * Math.PI * 10);
          gk.leftLegPivot.rotation.x = walkCycle * 0.42;
          gk.rightLegPivot.rotation.x = -walkCycle * 0.42;

          if (gk.role === 'pusher') {
            if (rawT < 0.76) {
              const pushProgress = easeInOutCubic(rawT / 0.76);
              gk.root.position.x = gk.sideSign * (0.85 + pushProgress * 0.95);
              gk.root.position.z = 0.82 - pushProgress * 1.05;
              gk.root.rotation.y = Math.PI - gk.sideSign * pushProgress * 0.65;
            } else {
              const clearProgress = easeInOutCubic((rawT - 0.76) / 0.24);
              gk.root.position.x = gk.sideSign * (1.8 + clearProgress * 0.55);
              gk.root.position.z = -0.23;
              gk.root.rotation.y = -gk.sideSign * (Math.PI / 2);
              gk.upperBody.rotation.x = THREE.MathUtils.lerp(0.48, 0.05, clearProgress);
            }
          } else if (gk.role === 'winch') {
            gk.upperBody.rotation.x = 0.25 + Math.sin(rawT * Math.PI * 8) * 0.12;
          }
        });

        cityInteriorLight.intensity = THREE.MathUtils.lerp(3.8, 6.8, t);

        if (rawT < 1) {
          requestAnimationFrame(runOpeningGates);
        } else {
          startEnteringCity(safetyTimeout, gateFocusCamPos, gateFocusLook);
        }
      };

      requestAnimationFrame(runOpeningGates);
    };

    const startEnteringCity = (safetyTimeout, startCamPos, startLook) => {
      if (dashboardTriggeredRef.current) return;
      updateSceneState(
        'ENTERING_CITY',
        'Transporting the Trojan Horse Through the Open Gates of Troy...'
      );

      const cityCamEnd = new THREE.Vector3(3.4, 2.45, 5.2);
      const cityLookEnd = new THREE.Vector3(
        HORSE_CITY_DEST_POS.x,
        1.85,
        HORSE_CITY_DEST_POS.z
      );

      const moveDuration = 4200;
      const moveStart = performance.now();
      let prevHorsePos = horseRoot.position.clone();

      const runEnteringCity = (now) => {
        if (dashboardTriggeredRef.current) {
          clearTimeout(safetyTimeout);
          return;
        }
        const rawT = Math.min((now - moveStart) / moveDuration, 1);
        const t = easeInOutCubic(rawT);

        horseRoot.position.lerpVectors(HORSE_START_POS, HORSE_CITY_DEST_POS, t);

        const stepDist = horseRoot.position.distanceTo(prevHorsePos);
        prevHorsePos.copy(horseRoot.position);
        const wheelRadius = 0.21;
        wheels.forEach((w) => {
          w.rotation.x += stepDist / wheelRadius;
        });

        horseFaceSpot.target.position.set(
          horseRoot.position.x + 0.8,
          2.2,
          horseRoot.position.z
        );

        camera.position.lerpVectors(startCamPos, cityCamEnd, t);
        const lookCur = new THREE.Vector3().lerpVectors(startLook, cityLookEnd, t);
        camera.lookAt(lookCur);

        if (rawT > 0.74) {
          setStatusCaption('Entering Troy — Launching Zero Trust Security Portal Dashboard...');
          const fadeT = (rawT - 0.74) / 0.26;
          setFadeOverlayOpacity(easeInOutCubic(fadeT));
        }

        if (rawT < 1) {
          requestAnimationFrame(runEnteringCity);
        } else {
          clearTimeout(safetyTimeout);
          completeToDashboard();
        }
      };

      requestAnimationFrame(runEnteringCity);
    };

    // 8. Main Render Loop
    const clock = new THREE.Clock();
    const animate = () => {
      animFrameId = requestAnimationFrame(animate);
      const elapsed = clock.getElapsedTime();

      const flicker = Math.sin(elapsed * 6.8) * 0.22 + Math.cos(elapsed * 12.1) * 0.12;
      gateTorchLight.intensity = 4.2 + flicker;

      if (!prefersReducedMotion) {
        if (sceneStateRef.current === 'LOGIN' || sceneStateRef.current === 'ENTERING_HORSE') {
          soldiers.forEach((s, idx) => {
            s.upperBody.position.y = 0.56 + Math.sin(elapsed * 2.1 + idx * 1.1) * 0.008;
            s.headPivot.rotation.y = Math.sin(elapsed * 0.9 + idx * 1.7) * 0.14;
            s.rightArmPivot.rotation.z = Math.sin(elapsed * 1.4 + idx) * 0.03;
          });
        }

        if (sceneStateRef.current === 'EXTERIOR') {
          gatekeepers.forEach((gk, idx) => {
            gk.headPivot.rotation.y = Math.sin(elapsed * 0.8 + idx * 1.5) * 0.12;
          });
        }

        flameMeshes.forEach((fm, idx) => {
          fm.scale.y = 1 + Math.sin(elapsed * 8.5 + idx * 1.7) * 0.07;
        });

        hazePlanes.forEach((hp) => {
          hp.mesh.position.x = hp.baseX + Math.sin(elapsed * hp.speed) * 1.6;
        });

        const dPos = dustGeo.attributes.position;
        const isHorseMoving = sceneStateRef.current === 'ENTERING_CITY';
        for (let i = 0; i < dustCount; i++) {
          let dx = dPos.getX(i) + dustSpeeds[i] * (isHorseMoving ? 2.2 : 0.6);
          let dy = dPos.getY(i) + dustSpeeds[i] * (isHorseMoving ? 0.9 : 0.35);
          if (dx > 9) dx = -9;
          if (dy > 2.4) dy = -1.18;
          dPos.setX(i, dx);
          dPos.setY(i, dy);
        }
        dPos.needsUpdate = true;
      }

      renderer.render(scene, camera);
    };
    animate();

    // 9. Responsive Resize Handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);

      if (sceneStateRef.current === 'EXTERIOR') {
        camera.position.copy(getExteriorCameraPos());
        camera.lookAt(getExteriorLookAt());
      }
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      if (animFrameId) cancelAnimationFrame(animFrameId);
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  const isExteriorVisible = sceneState === 'EXTERIOR';
  const isLoginVisible = sceneState === 'LOGIN' || sceneState === 'AUTHENTICATING';
  const isPostLoginCinematic =
    sceneState === 'EXITING_HORSE' ||
    sceneState === 'OPENING_GATES' ||
    sceneState === 'ENTERING_CITY';

  return (
    <div className="relative w-full min-h-screen bg-[#060a12] text-[#f5f0e6] overflow-x-hidden selection:bg-[#d4af37]/30 selection:text-[#f8f5ee]">
      {/* 1. FULL-VIEWPORT 3D SCENE */}
      <div
        ref={containerRef}
        id="canvas-container"
        aria-hidden="true"
        className="fixed inset-0 z-0 pointer-events-none"
      >
        {!webglAvailable && (
          <div className="w-full h-full bg-gradient-to-b from-[#060a12] via-[#10192b] to-[#090d16] flex items-center justify-center">
            <div className="w-96 h-96 rounded-full bg-[#d4af37]/10 blur-3xl" />
          </div>
        )}
      </div>

      {/* Smooth Scene-to-Dashboard Cross-Fade Overlay */}
      <div
        aria-hidden="true"
        style={{ opacity: fadeOverlayOpacity }}
        className="fixed inset-0 z-50 bg-[#060a12] pointer-events-none transition-opacity duration-300"
      />

      {/* Cinematic Sequence Status Banner */}
      {(statusCaption || isPostLoginCinematic) && (
        <div className="fixed bottom-7 left-1/2 -translate-x-1/2 z-40 flex flex-wrap items-center justify-center gap-3 px-4 w-full max-w-2xl">
          {statusCaption && (
            <div className="px-5 py-2.5 rounded-full bg-[#0c1322]/90 border border-[#d4af37]/50 text-[#f3e5ab] text-xs font-mono uppercase tracking-[0.15em] shadow-2xl flex items-center space-x-2.5 backdrop-blur-md">
              <span className="h-2 w-2 rounded-full bg-[#d4af37] animate-ping shrink-0" />
              <span>{statusCaption}</span>
            </div>
          )}

          {isPostLoginCinematic && (
            <button
              type="button"
              onClick={completeToDashboard}
              className="px-4 py-2 rounded-full bg-[#d4af37] hover:bg-[#e6c665] text-[#090d16] text-xs font-mono font-bold uppercase tracking-wider shadow-xl flex items-center space-x-1.5 cursor-pointer transition-all"
            >
              <span>Skip to Dashboard</span>
              <FastForward className="h-3.5 w-3.5" />
            </button>
          )}
        </div>
      )}

      {/* 2. EXTERIOR LANDING VIEW */}
      <div
        className={`relative z-10 min-h-screen flex flex-col justify-between transition-all duration-700 ease-out ${
          isExteriorVisible
            ? 'opacity-100 pointer-events-auto translate-y-0'
            : 'opacity-0 pointer-events-none -translate-y-3'
        }`}
      >
        {/* REGION A: TOP BRANDING BAR */}
        <header className="w-full border-b border-[#d4af37]/20 bg-[#060a12]/40 backdrop-blur-sm sticky top-0 z-30">
          <div className="max-w-7xl mx-auto px-4 sm:px-8 py-3 flex items-center justify-between gap-4">
            <div className="flex items-center space-x-3.5 min-w-0">
              <CollegeEmblem
                sizeClass="h-11 w-11 sm:h-12 sm:w-12"
                alt="JNNCE Official Emblem"
              />
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-serif font-bold text-xs sm:text-sm tracking-[0.08em] uppercase text-[#f8f5ee] truncate">
                    ZERO TRUST AI-POWERED NIDS
                  </span>
                  <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-[#d4af37]/15 text-[#e6c665] border border-[#d4af37]/40 shrink-0">
                    BATCH 34
                  </span>
                </div>
                <p className="text-[11px] sm:text-xs text-[#cbd5e1]/90 font-normal truncate mt-0.5">
                  JNNCE Shimoga • Dept of Information Science &amp; Engineering
                </p>
              </div>
            </div>

            {onSwitchLanding && (
              <button
                type="button"
                onClick={onSwitchLanding}
                className="px-3.5 py-2 rounded-xl text-xs font-mono font-semibold text-[#f3e5ab] bg-[#11192c]/70 hover:bg-[#192540]/90 border border-[#d4af37]/45 transition-all flex items-center space-x-2 cursor-pointer shrink-0"
              >
                <GraduationCap className="h-3.5 w-3.5 text-[#d4af37]" />
                <span>Academic Landing Page</span>
              </button>
            )}
          </div>
        </header>

        {/* REGION B: CENTERED JNNCE OFFICIAL CREST & ACADEMIC HERO BLOCK */}
        <main className="flex-1 flex items-center justify-center min-h-[calc(100vh-76px)] px-4 sm:px-8 py-6 pointer-events-none">
          <div className="max-w-2xl mx-auto w-full flex flex-col items-center text-center space-y-3 pointer-events-auto">
            <CollegeEmblem
              sizeClass="h-20 w-20 sm:h-24 sm:w-24 rounded-2xl p-2"
              alt="Jawaharlal Nehru National College of Engineering (JNNCE) Official Crest"
            />

            <div className="space-y-1 max-w-2xl">
              <p className="text-xs sm:text-sm font-bold uppercase tracking-[0.15em] text-[#e6c665] drop-shadow-[0_2px_10px_rgba(0,0,0,0.95)]">
                JAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING, SHIVAMOGGA
              </p>
              <p className="text-xs sm:text-sm font-semibold uppercase tracking-[0.13em] text-[#f8f5ee] drop-shadow-[0_2px_10px_rgba(0,0,0,0.95)]">
                DEPARTMENT OF INFORMATION SCIENCE AND ENGINEERING
              </p>
              <p className="text-xs text-[#e2e8f0] pt-0.5 drop-shadow-[0_2px_10px_rgba(0,0,0,0.95)]">
                Affiliated to Visvesvaraya Technological University (VTU), Belagavi • Approved by AICTE, New Delhi
              </p>
            </div>

            <div className="w-24 h-[1px] bg-gradient-to-r from-transparent via-[#d4af37]/80 to-transparent my-0.5" />

            <div className="flex flex-wrap items-center justify-center gap-3">
              <span className="inline-flex items-center space-x-1.5 px-3.5 py-1 rounded-full bg-[#11192c]/55 border border-[#d4af37]/45 text-xs font-mono font-semibold text-[#f3e5ab] backdrop-blur-xs">
                <GraduationCap className="h-3.5 w-3.5 text-[#d4af37]" />
                <span>FINAL YEAR B.E. ACADEMIC PROJECT (2023–2027)</span>
              </span>
              <span className="px-3.5 py-1 rounded-full bg-[#d4af37]/20 border border-[#d4af37]/50 text-xs font-mono font-bold text-[#e6c665] backdrop-blur-xs">
                PROJECT BATCH NO. 34
              </span>
            </div>

            <h1 className="font-serif text-2xl sm:text-4xl font-bold text-[#f8f5ee] tracking-tight leading-[1.15] max-w-2xl pt-1 drop-shadow-[0_4px_18px_rgba(0,0,0,0.95)]">
              Zero Trust AI-Powered Network Intrusion Detection System
            </h1>

            <p className="text-sm sm:text-base text-[#f5f0e6] leading-relaxed max-w-xl font-normal drop-shadow-[0_2px_10px_rgba(0,0,0,0.95)]">
              An academic project exploring Zero Trust network architecture, dataset preparation,
              and AI-based network intrusion detection.
            </p>

            <p className="text-xs sm:text-sm font-mono uppercase tracking-[0.11em] text-[#e6c665] max-w-xl leading-relaxed drop-shadow-[0_2px_10px_rgba(0,0,0,0.95)]">
              Phase 1 — Dataset Preparation, Zero Trust Architecture, and AI-Based Intrusion Detection Model
            </p>

            <div className="pt-2.5 flex flex-wrap items-center justify-center gap-3.5">
              <button
                type="button"
                id="enter-btn"
                onClick={handleTriggerLoginPortal}
                className="px-7 py-3.5 rounded-xl text-xs sm:text-sm font-bold uppercase tracking-[0.12em] text-[#090d16] bg-gradient-to-r from-[#d4af37] via-[#e6c665] to-[#d4af37] hover:brightness-110 shadow-xl shadow-[#d4af37]/25 transition-all flex items-center space-x-2.5 cursor-pointer active:scale-[0.98]"
              >
                <Shield className="h-4 w-4 stroke-[2.2]" />
                <span>ENTER SECURITY PORTAL</span>
              </button>

              <button
                type="button"
                onClick={handleExploreProject}
                className="px-6 py-3.5 rounded-xl text-xs sm:text-sm font-bold uppercase tracking-[0.12em] text-[#f3e5ab] bg-[#11192c]/60 hover:bg-[#192540]/80 border border-[#d4af37]/50 transition-all flex items-center space-x-2 cursor-pointer shadow-lg backdrop-blur-xs"
              >
                <span>ABOUT</span>
                <ChevronDown className="h-4 w-4 text-[#d4af37]" />
              </button>
            </div>
          </div>
        </main>

        {/* REGION C: ABOUT THE PROJECT SECTION */}
        <section
          ref={projectInfoRef}
          id="project-information"
          className="relative z-20 border-t border-[#d4af37]/25 bg-[#060a12]/55 backdrop-blur-md py-16 sm:py-20"
        >
          <div className="max-w-6xl mx-auto px-4 sm:px-8 space-y-14">
            <div className="space-y-6">
              <div className="text-center space-y-1.5">
                <span className="text-[11px] font-mono font-bold uppercase tracking-[0.2em] text-[#d4af37]">
                  ABOUT THE PROJECT
                </span>
                <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#f8f5ee]">
                  Problem Statement &amp; Proposed Zero Trust AI Solution
                </h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-6 rounded-2xl bg-[#0d1424]/85 border border-rose-500/30 space-y-3 shadow-lg">
                  <div className="flex items-center space-x-2.5 text-rose-400 font-mono text-xs font-bold uppercase tracking-wider">
                    <AlertCircle className="h-4 w-4 shrink-0" />
                    <span>Problem Statement</span>
                  </div>
                  <h3 className="text-base font-serif font-bold text-[#f8f5ee]">
                    Limitations of Perimeter-Based Network Defense
                  </h3>
                  <p className="text-xs sm:text-sm text-[#cbd5e1]/90 leading-relaxed">
                    Traditional perimeter-based network security models implicitly trust traffic once
                    inside the network boundary and rely on static rule signatures. As modern networks
                    scale, these legacy approaches struggle to detect evolving multi-vector cyber
                    intrusions, subtle anomalous flow patterns, and unauthorized lateral movement,
                    while raw intrusion datasets suffer from class imbalance, missing records, and
                    high-dimensional feature noise.
                  </p>
                </div>

                <div className="p-6 rounded-2xl bg-[#0d1424]/85 border border-[#d4af37]/40 space-y-3 shadow-lg">
                  <div className="flex items-center space-x-2.5 text-[#e6c665] font-mono text-xs font-bold uppercase tracking-wider">
                    <Shield className="h-4 w-4 shrink-0" />
                    <span>Proposed Solution</span>
                  </div>
                  <h3 className="text-base font-serif font-bold text-[#f8f5ee]">
                    Zero Trust Architecture + Deep Learning NIDS Pipeline
                  </h3>
                  <p className="text-xs sm:text-sm text-[#cbd5e1]/90 leading-relaxed">
                    This project delivers an integrated <strong>Zero Trust AI-Powered Network Intrusion Detection System (NIDS)</strong> that enforces <em>&ldquo;Never Trust, Always Verify&rdquo;</em> access control alongside automated dataset preprocessing and deep neural network traffic inspection. It standardizes benchmark intrusion datasets (<strong>NSL-KDD</strong>, <strong>CIC-IDS2017</strong>, and <strong>UNSW-NB15</strong>), trains a sequential <strong>LSTM</strong> deep learning classifier, and inspects live network flows with continuous role-based verification and immutable audit logging.
                  </p>
                </div>
              </div>
            </div>

            <div className="space-y-6 pt-6 border-t border-[#d4af37]/20">
              <div className="text-center space-y-1.5">
                <span className="text-[11px] font-mono font-bold uppercase tracking-[0.2em] text-[#d4af37]">
                  ACADEMIC &amp; TECHNICAL GOALS
                </span>
                <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#f8f5ee]">
                  Key Project Objectives
                </h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {[
                  {
                    num: '01',
                    title: 'Automated Dataset Ingestion & Cleaning',
                    desc: 'Ingest, validate, and preprocess benchmark intrusion datasets (NSL-KDD, CIC-IDS2017, and UNSW-NB15) by resolving missing values, removing duplicate records, and encoding categorical traffic attributes.'
                  },
                  {
                    num: '02',
                    title: 'Feature Standardization & Sequence Framing',
                    desc: 'Apply robust feature scaling, normalization, and dimensional alignment to transform raw network flow metrics into standardized input tensors suitable for sequential neural network learning.'
                  },
                  {
                    num: '03',
                    title: 'Zero Trust Access & Continuous Auditability',
                    desc: 'Enforce strict Zero Trust security principles with JWT session authentication, granular Role-Based Access Control (Admin and Analyst tiers), and tamper-evident security audit logs.'
                  },
                  {
                    num: '04',
                    title: 'Deep Learning Intrusion Model Training',
                    desc: 'Design and train a sequential Long Short-Term Memory (LSTM) deep neural network with configurable hyperparameters (epochs, batch size, learning rate, random seed) to accurately classify normal and malicious traffic.'
                  },
                  {
                    num: '05',
                    title: 'Real-Time Flow Detection & Comparative Analytics',
                    desc: 'Deploy trained models into an active passive flow detection engine to classify live network traffic, evaluate cross-dataset metrics (Accuracy, Precision, Recall, F1-Score), and trigger risk-graded alerts.'
                  }
                ].map((obj) => (
                  <div
                    key={obj.num}
                    className="p-5 rounded-2xl bg-[#0d1424]/80 border border-[#d4af37]/25 space-y-2.5 flex flex-col justify-between"
                  >
                    <div className="space-y-2">
                      <div className="flex items-center space-x-2.5">
                        <span className="px-2.5 py-0.5 rounded-md bg-[#d4af37]/15 border border-[#d4af37]/40 text-[#e6c665] font-mono text-xs font-bold">
                          OBJECTIVE {obj.num}
                        </span>
                      </div>
                      <h3 className="text-sm font-bold text-[#f8f5ee] pt-0.5">
                        {obj.title}
                      </h3>
                      <p className="text-xs text-[#cbd5e1]/85 leading-relaxed">
                        {obj.desc}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-6 pt-6 border-t border-[#d4af37]/20">
              <div className="text-center space-y-1.5">
                <span className="text-[11px] font-mono font-bold uppercase tracking-[0.2em] text-[#d4af37]">
                  INTRUSION DETECTION ENGINE
                </span>
                <h2 className="font-serif text-xl sm:text-2xl font-bold text-[#f8f5ee]">
                  AI Model Name &amp; Neural Network Architecture
                </h2>
              </div>

              <div className="p-6 rounded-2xl bg-[#0d1424]/85 border border-[#d4af37]/35 space-y-5 shadow-lg">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#d4af37]/20 pb-4">
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2 text-[#e6c665] text-xs font-mono uppercase tracking-wider">
                      <Cpu className="h-4 w-4" />
                      <span>Primary Deep Learning Model</span>
                    </div>
                    <h3 className="font-serif text-lg sm:text-xl font-bold text-[#f8f5ee]">
                      AI-Powered NIDS Sequential LSTM (<code className="text-[#e6c665] font-mono text-base">nids_lstm_sequential</code>)
                    </h3>
                    <p className="text-xs text-[#cbd5e1]/85">
                      Long Short-Term Memory (LSTM) Recurrent Neural Network • TensorFlow / Keras 3.x &amp; Calibrated Multi-Layer Perceptron (<code className="text-[#f3e5ab] font-mono">MLPClassifier(64, 32)</code>) Flow Classifier
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-2 shrink-0 font-mono text-[11px]">
                    <span className="px-3 py-1 rounded-lg bg-[#131c31] border border-[#d4af37]/35 text-[#f3e5ab]">
                      Total Params: <strong>29,637</strong>
                    </span>
                    <span className="px-3 py-1 rounded-lg bg-[#d4af37]/15 border border-[#d4af37]/40 text-[#e6c665]">
                      Optimizer: <strong>Adam (lr=0.001)</strong>
                    </span>
                  </div>
                </div>

                <div className="space-y-2.5">
                  <div className="flex items-center space-x-2 text-xs font-mono uppercase tracking-wider text-[#e6c665]">
                    <Layers className="h-4 w-4" />
                    <span>5-Stage Sequential Neural Architecture</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 font-mono text-xs pt-1">
                    <div className="p-4 rounded-xl bg-[#080d18]/90 border border-[#d4af37]/25 space-y-1.5">
                      <span className="text-[10px] text-[#e6c665] font-bold">STAGE 01 • INPUT</span>
                      <div className="font-bold text-[#f8f5ee] text-xs">Sequence Reshape</div>
                      <div className="text-[11px] text-[#cbd5e1]/80 font-sans">
                        Reshapes standardized flow features into 3D sequence tensors <code className="text-[#f3e5ab]">(Batch, 1, N)</code>.
                      </div>
                      <div className="text-[10px] text-[#94a3b8]">Shape: (None, 1, 42/22/15)</div>
                    </div>

                    <div className="p-4 rounded-xl bg-[#080d18]/90 border border-[#d4af37]/40 space-y-1.5">
                      <span className="text-[10px] text-[#e6c665] font-bold">STAGE 02 • RECURRENT</span>
                      <div className="font-bold text-[#f8f5ee] text-xs">64-Unit LSTM Layer</div>
                      <div className="text-[11px] text-[#cbd5e1]/80 font-sans">
                        Captures temporal and sequential flow dependencies via gated memory cells.
                      </div>
                      <div className="text-[10px] text-[#e6c665]">Params: 27,392</div>
                    </div>

                    <div className="p-4 rounded-xl bg-[#080d18]/90 border border-[#d4af37]/25 space-y-1.5">
                      <span className="text-[10px] text-[#e6c665] font-bold">STAGE 03 • REGULARIZER</span>
                      <div className="font-bold text-[#f8f5ee] text-xs">20% Dropout Layer</div>
                      <div className="text-[11px] text-[#cbd5e1]/80 font-sans">
                        Randomly deactivates 20% of recurrent activations (<code className="text-[#f3e5ab]">rate = 0.20</code>) to prevent overfitting.
                      </div>
                      <div className="text-[10px] text-[#94a3b8]">Params: 0</div>
                    </div>

                    <div className="p-4 rounded-xl bg-[#080d18]/90 border border-[#d4af37]/25 space-y-1.5">
                      <span className="text-[10px] text-[#e6c665] font-bold">STAGE 04 • HIDDEN DENSE</span>
                      <div className="font-bold text-[#f8f5ee] text-xs">Dense 32 (ReLU)</div>
                      <div className="text-[11px] text-[#cbd5e1]/80 font-sans">
                        Fully connected 32-neuron hidden layer with Rectified Linear Unit activation.
                      </div>
                      <div className="text-[10px] text-[#e6c665]">Params: 2,080</div>
                    </div>

                    <div className="p-4 rounded-xl bg-[#080d18]/90 border border-[#d4af37]/40 space-y-1.5">
                      <span className="text-[10px] text-[#e6c665] font-bold">STAGE 05 • OUTPUT HEAD</span>
                      <div className="font-bold text-[#f8f5ee] text-xs">Softmax Classifier</div>
                      <div className="text-[11px] text-[#cbd5e1]/80 font-sans">
                        Outputs multi-class intrusion probability distribution using Sparse Categorical Crossentropy.
                      </div>
                      <div className="text-[10px] text-[#e6c665]">Params: 165</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-4 flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-[#d4af37]/15 text-xs text-[#94a3b8]">
              <span>
                JNNCE Shimoga • Department of Information Science &amp; Engineering • Batch 34 (2023–2027)
              </span>
              <button
                type="button"
                onClick={handleTriggerLoginPortal}
                className="px-5 py-2.5 rounded-xl font-bold uppercase tracking-wider text-[#090d16] bg-[#d4af37] hover:bg-[#e5c158] transition-all flex items-center space-x-2 cursor-pointer"
              >
                <Lock className="h-3.5 w-3.5" />
                <span>Enter Security Portal</span>
              </button>
            </div>
          </div>
        </section>
      </div>

      {/* 3. INTERIOR TIMBER CHAMBER LOGIN VIEW */}
      <div
        id="dashboard-view"
        role="dialog"
        aria-modal="true"
        aria-label="Zero Trust Security Portal Login Inside Trojan Horse"
        className={`fixed inset-0 z-30 flex flex-col justify-between p-4 sm:p-6 transition-all duration-500 overflow-y-auto ${
          isLoginVisible
            ? 'opacity-100 pointer-events-auto scale-100'
            : 'opacity-0 pointer-events-none scale-95'
        }`}
      >
        <div className="max-w-6xl mx-auto w-full flex flex-wrap items-center justify-between gap-3 pt-1">
          <button
            type="button"
            onClick={handleBackToExterior}
            disabled={sceneState === 'AUTHENTICATING'}
            className="inline-flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-[#1c120c]/85 hover:bg-[#2a1b12] border border-[#d4af37]/40 text-xs sm:text-sm font-semibold text-[#f3e5ab] transition-all cursor-pointer shadow-md"
          >
            <ArrowLeft className="h-4 w-4 text-[#d4af37]" />
            <span>Back to Exterior</span>
          </button>

          <div className="px-3.5 py-1.5 rounded-full bg-[#1c120c]/80 border border-[#d4af37]/40 text-[11px] font-mono text-[#e6c665] uppercase tracking-wider shadow-md">
            Inside the Trojan Horse • Greek Soldiers Concealed Along the Ribs
          </div>

          <div className="flex items-center space-x-2.5 bg-[#1c120c]/85 px-3.5 py-1.5 rounded-xl border border-[#d4af37]/30">
            <CollegeEmblem sizeClass="h-7 w-7" alt="JNNCE Emblem" />
            <span className="font-serif font-bold text-xs sm:text-sm text-[#f8f5ee]">
              Zero Trust AI-Powered NIDS
            </span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-[#d4af37]/20 text-[#e6c665]">
              BATCH 34
            </span>
          </div>
        </div>

        <div className="max-w-[380px] w-full mx-auto my-auto py-4">
          <div className="bg-[#140d08]/84 backdrop-blur-md rounded-3xl p-6 sm:p-7 shadow-[0_24px_60px_rgba(0,0,0,0.85)] border border-[#d4af37]/45 space-y-5 text-[#f8f5ee]">
            <div className="text-center space-y-1.5">
              <div className="h-11 w-11 rounded-2xl bg-[#d4af37]/15 border border-[#d4af37]/45 text-[#e6c665] flex items-center justify-center mx-auto shadow-inner">
                <Lock className="h-5 w-5" />
              </div>
              <span className="text-[10px] font-mono font-bold uppercase tracking-[0.2em] text-[#e6c665] bg-[#d4af37]/15 px-3 py-0.5 rounded-full border border-[#d4af37]/35 inline-block">
                TROJAN CORE • SECURITY PORTAL
              </span>
              <h2 className="font-serif text-lg sm:text-xl font-bold text-[#f8f5ee]">
                Sign In to Unbar Troy&rsquo;s Gates
              </h2>
              <p className="text-[11px] text-[#d8d0c5]/85">
                JNNCE Dept. of ISE • Batch 34 Zero Trust Authentication
              </p>
            </div>

            <div className="grid grid-cols-2 gap-1.5 bg-[#0c0704]/90 p-1.5 rounded-xl border border-[#d4af37]/25 text-xs font-semibold">
              {['Admin', 'Analyst'].map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => handleRoleSelect(r)}
                  className={`py-2 rounded-lg transition-all text-center cursor-pointer ${
                    selectedRole === r
                      ? 'bg-gradient-to-r from-[#d4af37] to-[#e5c158] text-[#090d16] font-bold shadow-sm'
                      : 'text-[#cbd5e1] hover:text-[#f8f5ee]'
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>

            {loginError && (
              <div
                role="alert"
                className="p-3 rounded-xl bg-rose-950/90 border border-rose-500/50 text-rose-200 text-xs flex items-center space-x-2"
              >
                <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" />
                <span>{loginError}</span>
              </div>
            )}

            <form onSubmit={handleLoginSubmit} className="space-y-3.5 text-left">
              <div>
                <label
                  htmlFor="portal-username"
                  className="block text-xs font-semibold text-[#e6c665] mb-1"
                >
                  Username or Email
                </label>
                <div className="relative">
                  <User className="h-4 w-4 text-[#d4af37]/70 absolute left-3 top-2.5" />
                  <input
                    id="portal-username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    disabled={sceneState === 'AUTHENTICATING'}
                    autoComplete="username"
                    placeholder="admin"
                    className="w-full bg-[#0c0704]/90 border border-[#d4af37]/35 rounded-xl pl-9 pr-3 py-2.5 text-xs font-medium text-[#f8f5ee] placeholder-[#94a3b8]/50 focus:outline-none focus:ring-2 focus:ring-[#d4af37]"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1">
                  <label
                    htmlFor="portal-password"
                    className="block text-xs font-semibold text-[#e6c665]"
                  >
                    Password
                  </label>
                  <button
                    type="button"
                    onClick={() => setShowForgotModal(true)}
                    className="text-[11px] font-semibold text-[#d4af37] hover:underline cursor-pointer"
                  >
                    Credentials Help?
                  </button>
                </div>
                <div className="relative">
                  <Lock className="h-4 w-4 text-[#d4af37]/70 absolute left-3 top-2.5" />
                  <input
                    id="portal-password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    disabled={sceneState === 'AUTHENTICATING'}
                    autoComplete="current-password"
                    placeholder="••••••••"
                    className="w-full bg-[#0c0704]/90 border border-[#d4af37]/35 rounded-xl pl-9 pr-10 py-2.5 text-xs font-medium text-[#f8f5ee] placeholder-[#94a3b8]/50 focus:outline-none focus:ring-2 focus:ring-[#d4af37] font-mono"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((prev) => !prev)}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                    className="absolute right-3 top-2.5 text-[#d4af37]/80 hover:text-[#f8f5ee] cursor-pointer"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={sceneState === 'AUTHENTICATING'}
                className="w-full bg-gradient-to-r from-[#d4af37] via-[#e6c665] to-[#d4af37] hover:brightness-110 text-[#090d16] font-bold py-3 rounded-xl text-xs uppercase tracking-wider flex items-center justify-center space-x-2 shadow-lg shadow-[#d4af37]/20 transition-all active:scale-[0.99] cursor-pointer disabled:opacity-60"
              >
                <Key className="h-4 w-4 stroke-[2.2]" />
                <span>
                  {sceneState === 'AUTHENTICATING'
                    ? 'Verifying Credentials...'
                    : 'Authenticate & Open Gates of Troy'}
                </span>
              </button>
            </form>

            <div className="flex items-center justify-between pt-2 border-t border-[#d4af37]/20 text-[11px] font-mono text-[#cbd5e1]/80">
              <span>
                Zero Trust Role: <strong className="text-[#e6c665]">{selectedRole} Tier</strong>
              </span>
              <button
                type="button"
                onClick={handleBackToExterior}
                disabled={sceneState === 'AUTHENTICATING'}
                className="text-[#d4af37] hover:underline cursor-pointer"
              >
                ← Exit Horse
              </button>
            </div>
          </div>
        </div>

        <div className="text-center py-1 text-[11px] text-[#f3e5ab]/80 font-mono drop-shadow-[0_2px_8px_rgba(0,0,0,0.95)]">
          JAWAHARLAL NEHRU NATIONAL COLLEGE OF ENGINEERING, SHIVAMOGGA • BATCH NO. 34 (2023–2027)
        </div>
      </div>

      {/* Credentials Help Modal */}
      {showForgotModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-[#140d08] rounded-2xl max-w-sm w-full p-6 shadow-2xl border border-[#d4af37]/50 space-y-4 text-[#f8f5ee]">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-serif font-bold text-[#e6c665]">
                Zero Trust Portal Credentials
              </h3>
              <button
                type="button"
                onClick={() => setShowForgotModal(false)}
                className="text-[#cbd5e1] hover:text-white cursor-pointer"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <p className="text-xs text-[#d8d0c5]">
              Pre-configured academic demonstration accounts for Batch No. 34:
            </p>
            <div className="bg-[#0c0704] p-3.5 rounded-xl border border-[#d4af37]/30 text-xs font-mono space-y-1.5 text-[#f3e5ab]">
              <p>
                <strong>Admin:</strong> admin / admin123
              </p>
              <p>
                <strong>Analyst:</strong> analyst / analyst123
              </p>
            </div>
            <button
              type="button"
              onClick={() => setShowForgotModal(false)}
              className="w-full bg-[#d4af37] text-[#090d16] font-bold py-2 rounded-xl text-xs uppercase tracking-wider cursor-pointer"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
