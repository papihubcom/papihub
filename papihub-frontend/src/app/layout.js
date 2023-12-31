import './globals.css'
import {Inter} from 'next/font/google'
import AuthProvider from "@/auth/auth-provider";
import {QueryProvider} from "@/context/query-provider";

const inter = Inter({subsets: ['latin']})

export const metadata = {
  title: 'PapiHub',
  description: 'Generated by create next app',
}

export default function RootLayout({children}) {
  return (
      <html lang="en">
      <body className={inter.className}>
      <QueryProvider>
        <AuthProvider>
          {children}
        </AuthProvider>
      </QueryProvider>
      </body>
      </html>
  )
}
