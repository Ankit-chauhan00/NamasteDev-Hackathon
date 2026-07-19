"use client";
import ChatWindow from '@/components/ChatWindow'
import { useUser } from '@/context/userProvider'
import { redirect } from 'next/navigation';

const ChatPAge = () => {
  const user = useUser(); 


  if(!user){
    redirect("/sign-in");
  }
  
  return (
    <div className='h-screen flex items-center justify-center w-full '>
        <ChatWindow/>
    </div>
  )
}

export default ChatPAge