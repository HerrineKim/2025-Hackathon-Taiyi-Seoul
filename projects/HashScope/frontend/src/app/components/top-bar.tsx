import { SidebarTrigger } from "@/components/ui/sidebar"

export function TopBar() {
  return (
    <div className="sticky top-0 z-20 bg-gray-800 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-full items-center px-4 bg-gray-800">
        <SidebarTrigger className="bg-gray-800 text-white" />
      </div>
    </div>
  )
} 