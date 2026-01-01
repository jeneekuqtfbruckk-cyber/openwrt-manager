import OpenWrtManager from "@/components/openwrt-manager"

export default function Home() {
  return (
    <main className="min-h-screen bg-[#3a3a3c] p-4 md:p-8 flex items-start justify-center">
      <OpenWrtManager />
    </main>
  )
}
