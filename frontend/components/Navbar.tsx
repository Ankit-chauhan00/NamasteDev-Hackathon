"use client";
import Image from "next/image";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import React from "react";

const links = [
  {
    name: "Home",
    href: "/",
  },
  {
    name: "Features",
    href: "/features",
  },
  {
    name: "Pricing",
    href: "/pricing",
  },
  {
    name: "About",
    href: "/about",
  },
];

interface NavbarProps {
  user: {
    id: string;
    name: string;
    email: string;
  } | null;
}

const Navbar = ({ user }: NavbarProps) => {
  const path = usePathname();
  const router = useRouter();

  const handleLogout = async () => {
    await fetch("/api/auth/logout", {
      method: "POST",
    });

    router.push("/");
  };

  return (
    <nav className="fixed top-0 left-0 z-50 w-full">
      <div className="mx-auto mt-5 w-[95%] p-1 items-center justify-between rounded-md flex  shadow-2xl">
        <Link href="/" className="flex  flex-row items-center">
          <Image
            src="/images/navlogo.png"
            alt="nav-logo"
            height={62}
            width={62}
          />
          <p className="-ml-3 font-3 text-2xl font-bold text-clinical-800">
            Namaste Dev
          </p>
        </Link>

        {/* Nav Links */}
        <div className="hidden md:flex items-center gap-5">
          {links.map((link) => {
            const active = path === link.href;

            return (
              <Link
                key={link.href}
                href={link.href}
                className="group relative text-[15px] font-medium text-neutral-700 transition hover:text-black"
              >
                {link.name}

                <span
                  className={`absolute -bottom-2 left-0 h-[2px] rounded-full bg-blue-600 transition-all duration-300 ${
                    active ? "w-full" : "w-0 group-hover:w-full"
                  }`}
                />
              </Link>
            );
          })}
        </div>

        {/* Buttons */}
        {user ? (
          <div className="flex items-center gap-4">
            <span className="text-xl font-extralight font-3">Hi, {user.name}</span>

            <button onClick={handleLogout} className="rounded-md bg-blue-600 px-5 py-2 text-sm font-medium text-white transition hover:bg-blue-700">
              Logout
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-4">
            <Link
              href="/sign-in"
              className="rounded-xl border border-clinical-600 px-5 py-2 text-sm font-medium transition hover:bg-neutral-100"
            >
              Sign In
            </Link>

            <Link
              href="/sign-up"
              className="rounded-xl bg-blue-600 px-5 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
