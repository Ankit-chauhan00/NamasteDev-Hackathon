import Navbar from "@/components/Navbar";
import React, { ReactNode } from "react";

const RootLayout = ({ children }: { children: ReactNode }) => {
  return (
    <main className="min-h-screen w-full flex flex-col">
        <Navbar/>
      <section className="flex-1">
        {children}
      </section>
    </main>
  );
};

export default RootLayout;