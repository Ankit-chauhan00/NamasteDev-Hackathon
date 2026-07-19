import BotModel from "@/components/Model";
import { WiStars } from "react-icons/wi";


const HomePage = () => {
 


  return (
    <section className="bg-gradient-main-2 min-h-screen">
      <main className="h-full w-full flex items-center">
        <div className="mt-32 p-20 h-full w-full flex gap-2">
          <div className="flex flex-col w-[40%]">
            <span className="flex flex-row rounded-full w-[40%] bg-indigo-400 items-center pl-1">
              <WiStars size={32} className="text-mist-50 " />
              <p className="p-2 -ml-1 font-2 font-bold text-clinical-50">
                AI Powered Finance
              </p>
            </span>

            <div className="flex flex-col mt-3 font-medium font-2">
              <h1 className="text-6xl">
                Your Finance,
                <br></br>
                managed by AI
                <p>
                  {" "}
                  that{" "}
                  <span className="text-clinical-600">
                    actually <br /> Understands
                  </span>
                </p>
                them
              </h1>

              <div className="mt-3">
                <p className="text-sm text-ink-muted">
                  Track accounts, transactions, and goals through
                  <br></br>
                  natural conversation, No spreadsheets, no forms,
                  <br />
                  just smart financial clarity
                </p>
              </div>

              <div className="mt-5 flex flex-row gap-5">
                <button className="bg-blue-500 p-2 rounded-full text-surface-muted">
                  Get Started »
                </button>
                <button className="bg-blue-500 p-2 rounded-full text-surface-muted">
                  see how it works »
                </button>
              </div>
            </div>
          </div>

          <div className="w-[60%] -mt-36 h-[800px]">
            <BotModel/>
          </div>
        </div>
      </main>
    </section>
  );
};

export default HomePage;
