// components/BotModel.tsx
"use client";

import {
  useGLTF,
  Environment,
  PresentationControls,
  useAnimations,
} from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import * as THREE from "three";
import { useEffect, useRef } from "react";

function Bot() {
  const group = useRef<THREE.Group>(null);
  const { scene, animations } = useGLTF("/model/michi_bot.glb");
  const { actions, names } = useAnimations(animations, group);

  useEffect(() => {
    console.log(names); // See available animation names

    actions["Take 001"]?.play();
  }, [actions, names]);

  return (
    <group ref={group}> 
    <primitive
      object={scene}
      scale={24.6}
      position={[0, -0.04, 0]}
      rotation={[0, -0.4, 0]}
    />
    </group>
  );
}

export default function BotModel() {
  return (
    <Canvas camera={{ position: [0, 0, 1], fov: 30 }}>
      {/* <directionalLight intensity={1} /> */}
      <pointLight position={[0.2,0.2,0]}/>
      <Environment preset="forest" resolution={2048}/>
      <PresentationControls
        global
        rotation={[0, 0, 0]}
        polar={[-0.2, 0.2]}
        azimuth={[-0.4, 0.4]}
      >
        <Bot />
      </PresentationControls>
    </Canvas>
  );
}

useGLTF.preload("/models/michi_bot.glb");
