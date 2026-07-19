import Navbar from "@/components/Navbar";
import { UserProvider } from "@/context/userProvider";
import { getCurrentUser } from "@/lib/auth";
import React, { ReactNode } from "react";

const RootLayout = async ({ children }: { children: ReactNode }) => {
  const user = await getCurrentUser();
  return (
    <main className="min-h-screen w-full flex flex-col">
      <UserProvider user={user}>
        <Navbar user={user} />
        <section className="flex-1">{children}</section>
      </UserProvider>
    </main>
  );
};

export default RootLayout;
