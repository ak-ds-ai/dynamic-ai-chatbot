/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      // You can add custom colors here if needed
      colors: {
        // Example: 'custom-blue': '#1fb6ff',
      }
    },
  },
  plugins: [],
}
export default {
  darkMode: "class", // ✅ IMPORTANT
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};

