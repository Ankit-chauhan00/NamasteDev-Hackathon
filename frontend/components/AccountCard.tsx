"use client";

import { Landmark, Wallet } from "lucide-react";

export type Account = {
  id: string;
  name: string;
  account_type: "SAVINGS" | "CURRENT";
  balance: string;
};

function formatCurrency(amount: string) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(amount));
}

const TYPE_CONFIG = {
  SAVINGS: {
    icon: Wallet,
    iconBg: "bg-blue-50",
    iconColor: "text-blue-500",
    badgeBg: "bg-blue-50",
    badgeText: "text-blue-600",
  },
  CURRENT: {
    icon: Landmark,
    iconBg: "bg-purple-50",
    iconColor: "text-purple-500",
    badgeBg: "bg-purple-50",
    badgeText: "text-purple-600",
  },
} as const;

export function AccountCard({ account }: { account: Account }) {
  const config = TYPE_CONFIG[account.account_type];
  const Icon = config.icon;

  return (
    <div className="flex items-center justify-between rounded-xl border border-gray-200 bg-white px-4 py-3 transition hover:border-gray-300">
      <div className="flex items-center gap-3">
        <div className={`flex h-10 w-10 items-center justify-center rounded-full ${config.iconBg}`}>
          <Icon className={`h-5 w-5 ${config.iconColor}`} />
        </div>

        <div>
          <p className="text-sm font-medium text-gray-900">{account.name}</p>
          <span
            className={`inline-block mt-0.5 rounded-full px-2 py-0.5 text-xs font-medium ${config.badgeBg} ${config.badgeText}`}
          >
            {account.account_type}
          </span>
        </div>
      </div>

      <p className="text-sm font-semibold text-gray-900">
        {formatCurrency(account.balance)}
      </p>
    </div>
  );
}