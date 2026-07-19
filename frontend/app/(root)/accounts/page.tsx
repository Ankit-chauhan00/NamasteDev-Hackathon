"use client";

import { useUser } from "@/context/userProvider";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { Account } from "@/components/AccountCard";
import { AccountsList } from "@/components/AccountList";


const AccountDetails = () => {
  const user = useUser();
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!user) return;

    const loadAccounts = async () => {
      setLoading(true);
      setError("");

      try {
        const res = await fetch("/api/services/accounts");

        if (!res.ok) {
          throw new Error("Failed to load accounts");
        }

        const data = await res.json();
        setAccounts(data.accounts);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Something went wrong");
      } finally {
        setLoading(false);
      }
    };

    loadAccounts();
  }, [user]);

  if (!user) {
    redirect("/sign-in");
  }

  return (
    <div className="h-full w-full">
      <div className="w-full h-full p-10 mt-20">
        <h1 className="text-3xl text-clinical-600 font-semibold mb-4">Your Accounts</h1>

        {loading && (
          <p className="text-center text-sm text-gray-400 py-8">Loading...</p>
        )}

        {error && (
          <p className="text-center text-sm text-red-600 py-4" role="alert">
            {error}
          </p>
        )}

        {!loading && !error && <AccountsList accounts={accounts} />}
      </div>
    </div>
  );
};

export default AccountDetails;