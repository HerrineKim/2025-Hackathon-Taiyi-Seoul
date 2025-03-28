import type { Metadata } from "next";
import { Archivo } from "next/font/google";
import "./globals.css";
import MetaMaskProviderWrapper from "@/components/providers/MetaMaskProviderWrapper";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/app/components/app-sidebar"

const archivo = Archivo({
  variable: "--font-archivo",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "HashScope",
  description: "HashScope",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${archivo.variable} antialiased`}>
        <MetaMaskProviderWrapper>
          <SidebarProvider>
            <AppSidebar />
            <main className="flex-1">
              <div className="fixed top-0 right-0 z-20 h-14 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 md:left-[var(--sidebar-width)] left-0">
                <div className="flex h-full items-center px-4">
                  <SidebarTrigger />
                </div>
              </div>
              <div className="pt-14">
                {children}
              </div>
            </main>
          </SidebarProvider>
        </MetaMaskProviderWrapper>
      </body>
    </html>
  );
}
