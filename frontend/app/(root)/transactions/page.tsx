"use client";

import { useUser } from "@/context/userProvider";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { Transaction } from "@/components/TransactionCard";
import { TransactionList } from "@/components/TransactionsList";


const TransactionDetails = () => {
  const user = useUser();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!user) return;

    const loadTransactions = async () => {
      setLoading(true);
      setError("");

      try {
        const res = await fetch("/api/services/transactions");

        if (!res.ok) {
          throw new Error("Failed to load transactions");
        }

        const data = await res.json();
        setTransactions(data.transactions);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Something went wrong");
      } finally {
        setLoading(false);
      }
    };

    loadTransactions();
  }, [user]);

  if (!user) {
    redirect("/sign-in");
  }

  return (
    <div className="h-full w-full">
    <div className="w-full h-full p-10 mt-20">
      <h1 className="text-3xl text-clinical-600  font-semibold mb-4">Your Transactions</h1>

      {loading && (
        <p className="text-center text-sm text-gray-400 py-8">Loading...</p>
      )}

      {error && (
        <p className="text-center text-sm text-red-600 py-4" role="alert">
          {error}
        </p>
      )}

      {!loading && !error && <TransactionList  transactions={transactions} />}
    </div>
    </div>
  );
};

export default TransactionDetails;