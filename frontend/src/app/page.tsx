import URLInput from "@/components/URLInput";
import Image from "next/image";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <h1 className="text-4xl font-bold">ProComp</h1>
        <p className="text-lg text-gray-600">
          Company profile generator
        </p>
        <Image
          src="/logo.png"
          alt="ProComp Logo"
          width={150}
          height={150}
          className="rounded-full"
        />
        <div className="w-full max-w-md">
          {/* URLInput component will be used here */}
          <URLInput />
        </div>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
        © Copyright 2025, Bruno Mariz
      </footer>
    </div>
  );
}
