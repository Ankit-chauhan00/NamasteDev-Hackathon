"use client";
import { useUser } from '@/context/userProvider'
import { redirect } from 'next/navigation';
import React from 'react'

const TransactionDetails = () => {
  const user = useUser()
  if(!user){
    redirect("/sign-in");
  }
  return (
    <div>TransactionDetails</div>
  )
}

export default TransactionDetails