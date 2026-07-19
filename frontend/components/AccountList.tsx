"use client";

import { Account, AccountCard } from "./AccountCard";

export function AccountsList({ accounts }: { accounts: Account[] }) {
  if (accounts.length === 0) {
    return (
      <p className="text-center text-sm text-gray-400 py-8">
        No accounts yet.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {accounts.map((acc) => (
        <AccountCard key={acc.id} account={acc} />
      ))}
    </div>
  );
}