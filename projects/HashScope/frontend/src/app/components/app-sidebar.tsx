import { Home, Flame, Search, Info, Activity, User, Key } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import Image from "next/image"

const mainItems = [
  {
    title: "Home",
    url: "/",
    icon: Home,
  },
  {
    title: "Hot",
    url: "/hot",
    icon: Flame,
  },
  {
    title: "Search APIs",
    url: "/search",
    icon: Search,
  },
  {
    title: "About Tier",
    url: "/about",
    icon: Info,
  },
]

const myItems = [
  {
    title: "Usage",
    url: "/my/usage",
    icon: Activity,
  },
  {
    title: "Profile",
    url: "/my/profile",
    icon: User,
  },
  {
    title: "Secret",
    url: "/secret",
    icon: Key,
  },
]

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="mb-4">
            <Image src="/logo-500.png" alt="logo" width={32} height={32} />
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {mainItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>My</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {myItems.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
