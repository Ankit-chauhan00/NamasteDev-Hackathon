// components/TransactionCard.tsx
"use client";

import { ArrowDownCircle, ArrowUpCircle, ArrowLeftRight } from "lucide-react";

export type Transaction = {
  id: string;
  amount: string;
  transaction_type: "EXPENSE" | "INCOME" | "TRANSFER";
  description: string;
  transaction_date: string;
  account_id: string;
};

function formatCurrency(amount: string) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(amount));
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

const TYPE_CONFIG = {
  EXPENSE: {
    icon: ArrowUpCircle,
    iconBg: "bg-red-50",
    iconColor: "text-red-500",
    amountColor: "text-red-600",
    sign: "-",
  },
  INCOME: {
    icon: ArrowDownCircle,
    iconBg: "bg-green-50",
    iconColor: "text-green-500",
    amountColor: "text-green-600",
    sign: "+",
  },
  TRANSFER: {
    icon: ArrowLeftRight,
    iconBg: "bg-blue-50",
    iconColor: "text-blue-500",
    amountColor: "text-blue-600",
    sign: "",
  },
} as const;

export function TransactionCard({ transaction }: { transaction: Transaction }) {
  const config = TYPE_CONFIG[transaction.transaction_type];
  const Icon = config.icon;

  return (
    <div className="flex items-center justify-between rounded-xl border border-gray-200 bg-white px-4 py-3 transition hover:border-gray-300">
      <div className="flex items-center gap-3">
        <div className={`flex h-10 w-10 items-center justify-center rounded-full ${config.iconBg}`}>
          <Icon className={`h-5 w-5 ${config.iconColor}`} />
        </div>

        <div>
          <p className="text-sm font-medium text-gray-900">
            {transaction.description}
          </p>
          <p className="text-xs text-gray-500">
            {formatDate(transaction.transaction_date)}
          </p>
        </div>
      </div>

      <p className={`text-sm font-semibold ${config.amountColor}`}>
        {config.sign} {formatCurrency(transaction.amount)}
      </p>
    </div>
  );
}