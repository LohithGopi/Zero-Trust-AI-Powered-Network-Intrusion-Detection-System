import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { 
  Lock, ArrowRight, Shield, ArrowLeft, Key, 
  Activity, CheckCircle2, User, AlertCircle 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const TrojanTransition = ({ onBackToLanding, onSuccessLogin, onExploreDashboard, initialMode = 'login' }) => {
  const containerRef = useRef(null);
  const { login } = useAuth();

  const [isInsideCore, setIsInsideCore] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);
  
  // Login Form States inside Core
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [selectedRole, setSelectedRole] = useState('Admin');
  const [loginError, setLoginError] = useState('');
  const [loading, setLoading] = useState(false);

  // References for Three.js animation control
  const triggerTransitionRef = useRef(null);
  const resetTransitionRef = useRef(null);

  const handleRoleSelect = (roleName) => {
    setSelectedRole(roleName);
    if (roleName === 'Admin') {
      setUsername('admin');
      setPassword('admin123');
    } else {
      setUsername('analyst');
      setPassword('analyst123');
    }
  };

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setLoginError('');
    setLoading(true);
    try {
      await login(username, password, selectedRole);
      if (onSuccessLogin) {
        onSuccessLogin();
      }
    } catch (err) {
      setLoginError(err?.message || 'Invalid credentials.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // Scene & Camera
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
      60,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0x10b981, 2.5, 50);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    // Low-poly Trojan Horse Group
    const horseGroup = new THREE.Group();
    const woodMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x8b5a2b, 
      roughness: 0.7, 
      metalness: 0.1 
    });
    const glowingCoreMaterial = new THREE.MeshBasicMaterial({ 
      color: 0x10b981, 
      wireframe: true 
    });

    // Body
    const bodyGeo = new THREE.BoxGeometry(2.2, 1.4, 3.5);
    const bodyMesh = new THREE.Mesh(bodyGeo, woodMaterial);
    bodyMesh.position.y = 0.5;
    horseGroup.add(bodyMesh);

    // Neck & Head
    const neckGeo = new THREE.BoxGeometry(0.8, 1.5, 0.8);
    const neckMesh = new THREE.Mesh(neckGeo, woodMaterial);
    neckMesh.position.set(0, 1.5, 1.2);
    neckMesh.rotation.x = -0.3;
    horseGroup.add(neckMesh);

    const headGeo = new THREE.BoxGeometry(0.7, 0.8, 1.4);
    const headMesh = new THREE.Mesh(headGeo, woodMaterial);
    headMesh.position.set(0, 2.1, 1.6);
    horseGroup.add(headMesh);

    // Legs
    const legGeo = new THREE.BoxGeometry(0.4, 1.8, 0.4);
    const positions = [
      [-0.9, -0.6, 1.3],
      [0.9, -0.6, 1.3],
      [-0.9, -0.6, -1.3],
      [0.9, -0.6, -1.3]
    ];
    positions.forEach(pos => {
      const leg = new THREE.Mesh(legGeo, woodMaterial);
      leg.position.set(...pos);
      horseGroup.add(leg);
    });

    // Core inside the Horse
    const coreGeo = new THREE.SphereGeometry(0.65, 16, 16);
    const coreMesh = new THREE.Mesh(coreGeo, glowingCoreMaterial);
    coreMesh.position.set(0, 0.5, 0);
    horseGroup.add(coreMesh);

    scene.add(horseGroup);
    camera.position.set(0, 2, 6);
    camera.lookAt(0, 0, 0);

    // Animation & Transition Logic
    let localIsTransitioning = false;
    let animFrameId = null;
    const startCamPos = new THREE.Vector3(0, 2, 6);
    const targetCamPos = new THREE.Vector3(0, 0.5, 0);

    const triggerTransition = () => {
      if (localIsTransitioning) return;
      localIsTransitioning = true;
      setIsTransitioning(true);

      const startTime = performance.now();
      const duration = 1500; // 1.5s zoom

      const animateZoom = (currentTime) => {
        const elapsed = currentTime - startTime;
        const t = Math.min(elapsed / duration, 1);
        const easeT = 1 - Math.pow(1 - t, 3);

        camera.position.lerpVectors(startCamPos, targetCamPos, easeT);
        horseGroup.rotation.y += 0.025;

        if (t < 1) {
          requestAnimationFrame(animateZoom);
        } else {
          setIsInsideCore(true);
          setIsTransitioning(false);
        }
      };
      requestAnimationFrame(animateZoom);
    };

    const resetTransition = () => {
      setIsInsideCore(false);
      localIsTransitioning = true;
      setIsTransitioning(true);

      const startTime = performance.now();
      const duration = 1000;

      const animateReset = (currentTime) => {
        const elapsed = currentTime - startTime;
        const t = Math.min(elapsed / duration, 1);
        const easeT = 1 - Math.pow(1 - t, 3);

        camera.position.lerpVectors(targetCamPos, startCamPos, easeT);

        if (t < 1) {
          requestAnimationFrame(animateReset);
        } else {
          localIsTransitioning = false;
          setIsTransitioning(false);
        }
      };
      requestAnimationFrame(animateReset);
    };

    triggerTransitionRef.current = triggerTransition;
    resetTransitionRef.current = resetTransition;

    // Raycaster for clicking 3D model directly
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const handleCanvasClick = (event) => {
      const rect = renderer.domElement.getBoundingClientRect();
      if (
        event.clientX >= rect.left && 
        event.clientX <= rect.right && 
        event.clientY >= rect.top && 
        event.clientY <= rect.bottom
      ) {
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(horseGroup.children);
        if (intersects.length > 0 && !localIsTransitioning && !isInsideCore) {
          triggerTransition();
        }
      }
    };

    window.addEventListener('click', handleCanvasClick);

    // Render loop
    const animate = () => {
      animFrameId = requestAnimationFrame(animate);
      if (!localIsTransitioning && !isInsideCore) {
        horseGroup.rotation.y += 0.005;
      }
      renderer.render(scene, camera);
    };
    animate();

    // Resize
    const handleResize = () => {
      if (!container) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('click', handleCanvasClick);
      window.removeEventListener('resize', handleResize);
      if (animFrameId) cancelAnimationFrame(animFrameId);
      
      // Cleanup geometries & materials
      bodyGeo.dispose();
      neckGeo.dispose();
      headGeo.dispose();
      legGeo.dispose();
      coreGeo.dispose();
      woodMaterial.dispose();
      glowingCoreMaterial.dispose();
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div className="relative w-full min-h-screen bg-[#030712] overflow-x-hidden overflow-y-auto flex items-center justify-center text-white selection:bg-emerald-500/30 selection:text-emerald-400">
      
      {/* 1. Top Navbar / Back to Landing Control */}
      <div className="absolute top-0 left-0 right-0 z-30 p-4 sm:p-6 flex items-center justify-between pointer-events-auto">
        <button
          onClick={onBackToLanding}
          className="flex items-center space-x-2 text-xs font-bold text-slate-400 hover:text-white bg-slate-900/80 px-3.5 py-2 rounded-xl border border-slate-800 backdrop-blur-md transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Exit to Home Page</span>
        </button>

        <div className="flex items-center space-x-2">
          <Shield className="h-4 w-4 text-emerald-400" />
          <span className="text-xs font-mono font-bold tracking-wider text-slate-300 hidden sm:inline-block">
            ZERO TRUST PERIMETER DEFENSE
          </span>
        </div>
      </div>

      {/* 2. Three.js Canvas Container */}
      <div 
        ref={containerRef} 
        className="absolute inset-0 z-1 pointer-events-auto cursor-pointer"
        title="Click the 3D Trojan Horse to initialize transition"
      />

      {/* 3. Hero Overlay (Visible before entering the core) */}
      <div 
        className={`relative z-10 text-center px-4 max-w-xl mx-auto transition-all duration-700 ease-out pointer-events-auto ${
          isInsideCore ? 'opacity-0 pointer-events-none scale-95' : 'opacity-100 scale-100'
        }`}
      >
        <span className="inline-block bg-emerald-500/10 text-emerald-400 px-4 py-1.5 rounded-full text-xs font-bold border border-emerald-500/30 tracking-wider uppercase mb-5">
          ZERO TRUST BREACH SIMULATION
        </span>
        
        <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-white tracking-tight leading-tight mb-3">
          Bypass the Perimeter.<br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-200">
            Enter the Core.
          </span>
        </h1>
        
        <p className="text-slate-400 text-xs sm:text-sm max-w-md mx-auto mb-8 leading-relaxed">
          Click the interactive 3D Trojan Horse model or the button below to initiate the secure zero-trust tunnel transition into the SOC dashboard.
        </p>
        
        <button 
          onClick={() => triggerTransitionRef.current?.()}
          disabled={isTransitioning}
          className="bg-gradient-to-r from-emerald-500 to-emerald-700 hover:from-emerald-400 hover:to-emerald-600 text-white font-bold px-8 py-3.5 rounded-xl shadow-lg shadow-emerald-900/40 transform hover:-translate-y-0.5 active:translate-y-0 transition-all text-sm tracking-wide"
        >
          {isTransitioning ? 'Initializing Tunnel...' : 'Initialize Entry Transition'}
        </button>
      </div>

      {/* 4. Interior Dashboard View + Included Login Page (Fades in once inside the core) */}
      <div 
        className={`absolute inset-0 z-20 bg-[#030712]/95 backdrop-blur-xl transition-all duration-1000 ease-in-out flex flex-col p-4 sm:p-8 md:p-12 overflow-y-auto ${
          isInsideCore ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
      >
        <div className="max-w-5xl w-full mx-auto space-y-6 my-auto pt-12 pb-8">
          
          {/* Header Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800/80 gap-3">
            <div className="flex items-center space-x-3">
              <div className="h-10 w-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 text-emerald-400 flex items-center justify-center font-bold">
                🛡️
              </div>
              <div>
                <h2 className="text-lg sm:text-xl font-black text-white tracking-tight">
                  NIDS Executive SOC Core
                </h2>
                <p className="text-[11px] font-mono text-emerald-400">
                  TUNNEL ESTABLISHED // ZERO-TRUST VERIFIED
                </p>
              </div>
            </div>

            <button 
              onClick={() => resetTransitionRef.current?.()}
              className="self-start sm:self-auto bg-rose-500/10 text-rose-400 border border-rose-500/30 hover:bg-rose-500/20 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-colors"
            >
              Exit Core
            </button>
          </div>

          {/* Core Telemetry Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
            <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl">
              <p className="text-slate-400 text-xs font-medium mb-1">Active 5-Tuple Flows</p>
              <h3 className="text-white text-2xl font-black font-mono">1,429</h3>
            </div>
            <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl">
              <p className="text-slate-400 text-xs font-medium mb-1">Zero Trust Status</p>
              <h3 className="text-emerald-400 text-2xl font-black font-mono">VERIFIED</h3>
            </div>
            <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-2xl">
              <p className="text-slate-400 text-xs font-medium mb-1">Threat Confidence</p>
              <h3 className="text-blue-400 text-2xl font-black font-mono">99.4%</h3>
            </div>
          </div>

          {/* Included Login Page & Direct Access Hub */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch pt-2">
            
            {/* Left: Security Portal Authentication Card */}
            <div className="lg:col-span-7 bg-slate-900/90 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl space-y-5">
              <div className="flex items-center space-x-3">
                <div className="h-9 w-9 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-400 flex items-center justify-center">
                  <Lock className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">
                    Authenticate to Access Core
                  </h3>
                  <p className="text-xs text-slate-400">
                    Sign in with your role credentials to unlock full SOC capabilities.
                  </p>
                </div>
              </div>

              {/* Role Toggle Selector */}
              <div className="grid grid-cols-2 gap-1.5 bg-slate-950 p-1.5 rounded-xl border border-slate-800 text-xs font-semibold">
                {['Admin', 'Analyst'].map((r) => (
                  <button
                    key={r}
                    type="button"
                    onClick={() => handleRoleSelect(r)}
                    className={`py-2 rounded-lg transition-all text-center ${
                      selectedRole === r
                        ? 'bg-blue-600 text-white font-bold shadow-xs'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {r} Role
                  </button>
                ))}
              </div>

              {loginError && (
                <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center space-x-2">
                  <AlertCircle className="h-4 w-4 shrink-0" />
                  <span>{loginError}</span>
                </div>
              )}

              {/* Login Form */}
              <form onSubmit={handleLoginSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">
                    Username
                  </label>
                  <div className="relative">
                    <User className="h-4 w-4 text-slate-500 absolute left-3 top-2.5" />
                    <input
                      type="text"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      required
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1">
                    Password
                  </label>
                  <div className="relative">
                    <Key className="h-4 w-4 text-slate-500 absolute left-3 top-2.5" />
                    <input
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2.5 rounded-xl text-xs flex items-center justify-center space-x-2 shadow-lg shadow-blue-900/30 transition-all active:scale-[0.99]"
                >
                  <Lock className="h-3.5 w-3.5" />
                  <span>{loading ? 'Authenticating...' : 'Sign In & Enter Dashboard'}</span>
                </button>
              </form>
            </div>

            {/* Right: Instant Direct Exploration Hub */}
            <div className="lg:col-span-5 bg-gradient-to-br from-emerald-950/40 via-slate-900/90 to-slate-900/90 border border-emerald-500/20 rounded-3xl p-6 sm:p-8 flex flex-col justify-between space-y-5">
              <div className="space-y-3">
                <span className="text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-400 px-2.5 py-0.5 rounded border border-emerald-500/30">
                  INSTANT SOC ACCESS
                </span>
                <h4 className="text-base font-bold text-white">
                  Explore Live Dashboard Directly
                </h4>
                <p className="text-xs text-slate-400 leading-relaxed">
                  Bypass manual sign-in to inspect live traffic, neural network metrics, and the security operations center immediately.
                </p>
                <div className="space-y-1.5 text-[11px] text-slate-400 font-mono pt-2">
                  <div className="flex items-center space-x-2 text-emerald-400">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    <span>Real-time Live Packet Capture</span>
                  </div>
                  <div className="flex items-center space-x-2 text-emerald-400">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    <span>Zero Trust RBAC Enforcement</span>
                  </div>
                  <div className="flex items-center space-x-2 text-emerald-400">
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    <span>ML Threat Detection Models</span>
                  </div>
                </div>
              </div>

              <button
                onClick={onExploreDashboard}
                className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2.5 rounded-xl text-xs flex items-center justify-center space-x-2 shadow-lg shadow-emerald-900/40 transition-all active:scale-[0.99]"
              >
                <span>Enter SOC Dashboard Now</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </button>
            </div>

          </div>

        </div>
      </div>

    </div>
  );
};
