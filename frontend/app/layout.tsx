import localFont from "next/font/local";
import "./globals.css";

const font_1 = localFont({
  src: "../public/fonts/font1.ttf",
  variable: "--font-font-1",
  weight: "100 200 300 400 500 600 700 800 800 900",
});

const font_2 = localFont({
  src: "../public/fonts/font2.ttf",
  variable: "--font-font-2",
  weight: "100 200 300 400 500 600 700 800 800 900",
});

const font_3 = localFont({
  src: "../public/fonts/font3.ttf",
  variable: "--font-font-3",
  weight: "100 200 300 400 500 600 700 800 800 900",
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${font_1.variable} ${font_2.variable} ${font_3.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
