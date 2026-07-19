// components/TransactionList.tsx
"use client";

import { Transaction, TransactionCard } from "./TransactionCard";

export function TransactionList({ transactions }: { transactions: Transaction[] }) {
  if (transactions.length === 0) {
    return (
      <p className="text-center text-sm text-gray-400 py-8">
        No transactions yet.
      </p>
    );
  }

  return (
    <div className="space-y-2">
      {transactions.map((txn) => (
        <TransactionCard key={txn.id} transaction={txn} />
      ))}
    </div>
  );
}