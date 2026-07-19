import React, { ReactNode } from "react";
import Image from "next/image";

const AuthLayout = ({ children }: { children: ReactNode }) => {
  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-gradient-main-2 px-4 py-10">

      {/* Background Glow */}
      <div className="absolute left-1/2 top-1/2 h-[700px] w-[700px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-blue-500/10 blur-[180px]" />

      {/* Bottom Gradient */}
      <div className="absolute bottom-0 left-1/2 h-72 w-[700px] -translate-x-1/2 rounded-full bg-cyan-400/20 blur-[140px]" />

      {/* Auth Card */}
      <section className="relative z-10 w-full max-w-md rounded-3xl border border-white/20 bg-white/70 p-8 shadow-2xl backdrop-blur-xl">

        {/* Logo */}
        <div className="flex flex-col items-center text-center">

          {/* Replace with your logo */}
          <Image
            src="/images/navlogo.png"
            alt="AI Finance"
            width={100}
            height={100}
          />

          <h1 className="mt-1 text-3xl font-bold text-gray-900">
            Welcome
          </h1>

          <p className="mt-2 text-sm text-gray-600">
            Your AI-powered financial assistant.
          </p>
        </div>

        {/* Form */}
        <div className="mt-8">
          {children}
        </div>

        {/* Bottom Text */}
        <div className="mt-8 border-t border-gray-200 pt-5 text-center">
          <p className="text-sm text-gray-500">
            Secure • Private • AI Powered
          </p>
        </div>

      </section>
    </main>
  );
};

export default AuthLayout;